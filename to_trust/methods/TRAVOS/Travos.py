import numpy as np
from scipy import integrate, stats

from to_trust import Consumer, Provider, Witness

UNIFORM_STD_DEV = stats.beta.std(1, 1)
UNIFORM_EXPECTED_VALUE = 0.5


class Travos(Consumer):
    def __init__(
            self,
            epsilon_confidence: float = 0.2,
            num_steps_integration: int = 100,
            confidence_threshold: float = 0.95,
            num_intervals: int = 5,
            outcome_threshold: float = 0.5,
    ):
        super(Travos, self).__init__()
        self._positive_outcomes = {}
        self._negative_outcomes = {}

        self._outcome_history = {}
        self._last_outcome_history = {}

        self._epsilon_confidence = epsilon_confidence
        self._num_steps_integration = num_steps_integration
        self._confidence_threshold = confidence_threshold
        self._outcome_threshold = outcome_threshold

        self._intervals = np.linspace(0, 1, num_intervals + 1)

    def register_witnesses(self, witnesses: list[Witness]):
        super(Travos, self).register_witnesses(witnesses)
        for witness in witnesses:
            if witness not in self._outcome_history.keys():
                self._outcome_history[witness] = {}
                self._last_outcome_history[witness] = {}
            for provider in self.providers:
                self._outcome_history[witness][provider] = np.array([], dtype=[("outcome", bool),
                                                                               ("bin_index", int)])

    def register_providers(self, providers: list[Provider]):
        super(Travos, self).register_providers(providers)
        self._positive_outcomes = {provider: 0 for provider in providers}
        self._negative_outcomes = {provider: 0 for provider in providers}

    def update(self):
        # update avg estimation error
        avg_estimation_error = 0
        for provider in self.providers.keys():
            avg_estimation_error += abs(self.providers[provider] - provider.get_average_value())
        self.MAE.append(avg_estimation_error / len(self.providers))

    def update_provider(self, provider: Provider, score: float) -> None:
        outcome = score > self._outcome_threshold

        for witness in self.witnesses:
            if provider not in self._last_outcome_history[witness]:
                continue

            expected_outcome = self._last_outcome_history[witness][provider]["expected_value"] > self._outcome_threshold
            self._outcome_history[witness][provider] = np.append(
                np.array((expected_outcome == outcome,
                          self._last_outcome_history[witness][provider]["bin_index"]),
                         dtype=[("outcome", bool),
                                ("bin_index", int)]),
                self._outcome_history[witness][provider]
            )

        if outcome:
            self._positive_outcomes[provider] += 1
        else:
            self._negative_outcomes[provider] += 1

    def choose_provider(self) -> Provider:
        # clean last_outcome_history
        for witness, _ in self._last_outcome_history.items():
            self._last_outcome_history[witness] = {}

        # calculate confidence values based on own experience
        confidence_values = self._confidence_values_of_providers()

        for provider, (confidence_value, expected_value) in confidence_values.items():
            # if the confidence value is lower than the threshold take opinions of witnesses into account
            if confidence_value < self._confidence_threshold:
                expected_value = self._estimate_value_with_witnesses_opinions(provider)
            self.providers[provider] = expected_value
        return max(self.providers, key=self.providers.get)

    def _confidence_values_of_providers(self) -> dict[Provider, (float, float)]:
        res = {}
        for p in self.providers:
            expected_value = stats.beta.expect(args=(self._positive_outcomes[p] + 1, self._negative_outcomes[p] + 1))

            def beta_func(x):
                return stats.beta.pdf(x, self._positive_outcomes[p] + 1, self._negative_outcomes[p] + 1)

            expected_area, _ = integrate.quad(
                beta_func,
                expected_value - self._epsilon_confidence,
                expected_value + self._epsilon_confidence,
            )
            full_area, _ = integrate.quad(beta_func, 0, 1)
            res[p] = (expected_area / full_area, expected_value)
        return res

    def _estimate_value_with_witnesses_opinions(self, provider: Provider):
        alpha = self._positive_outcomes[provider] + 1
        beta = self._negative_outcomes[provider] + 1
        for witness in self.witnesses:
            witness_accuracy, witness_expected_value = self._accuracy_of_witness(provider, witness)

            # update expected value and standard deviation according to accuracy
            witness_standard_deviation = 0.1

            adjusted_expected_value = UNIFORM_EXPECTED_VALUE + witness_accuracy * (
                    witness_expected_value - UNIFORM_EXPECTED_VALUE
            )
            adjusted_standard_deviation = UNIFORM_STD_DEV + witness_accuracy * (
                    witness_standard_deviation - UNIFORM_STD_DEV
            )

            # update alpha and beta values according to adjusted expected value and standard deviation
            adjusted_alpha, adjusted_beta = self._calculate_alpha_beta(
                adjusted_expected_value, adjusted_standard_deviation
            )

            # used because of the standard deviation being set to a constant, which causes beta and alpha < 1
            # and then the calculation of alpha and beta does not work this way
            adjusted_alpha = max(adjusted_alpha, 1.0)
            adjusted_beta = max(adjusted_beta, 1.0)

            alpha += adjusted_alpha - 1
            beta += adjusted_beta - 1

        return stats.beta.expect(args=(alpha, beta))

    def _accuracy_of_witness(self, provider: Provider, witness: Witness) -> (float, float):
        expected_value = witness.score_of(provider)
        bin_index = np.argwhere(self._intervals < expected_value)
        if bin_index.size == 0:
            bin_index = 0
        elif bin_index.size == self._intervals.size:
            bin_index = bin_index[-2][0]
        else:
            bin_index = bin_index[-1][0]

        # calculate accuracy of witness
        alpha = 1
        beta = 1

        relevant_entries = np.argwhere(self._outcome_history[witness][provider]["bin_index"] == bin_index)
        alpha += np.sum(self._outcome_history[witness][provider][relevant_entries]["outcome"])
        beta += np.sum(np.invert(self._outcome_history[witness][provider][relevant_entries]["outcome"]))

        # for (outcome, _, witness_bin_index) in self._outcome_history[witness][provider]:
        #     # calculate alpha and beta based on previously given values
        #     # suggestion: use an epsilon environment around score rather than working with static intervals
        #     if bin_idx == witness_bin_index:
        #         if outcome:
        #             alpha += 1
        #         else:
        #             beta += 1

        # alpha = max(1, alpha)
        # beta = max(1, beta)

        def beta_func(x):
            return stats.beta.pdf(x, alpha, beta)

        expected_area, _ = integrate.quad(beta_func,
                                          self._intervals[bin_index],
                                          self._intervals[bin_index + 1])
        full_area, _ = integrate.quad(beta_func, 0, 1)

        # store the provided value of the witness
        self._last_outcome_history[witness][provider] = {
            "expected_value": expected_value,
            "bin_index": bin_index
        }

        return expected_area / full_area, expected_value

    @staticmethod
    def _calculate_alpha_beta(
            expected_value: float, standard_deviation: float
    ) -> (float, float):
        alpha = (
                        expected_value ** 2 - expected_value ** 3
                ) / standard_deviation ** 2 - expected_value
        beta = (
                       (1 - expected_value) ** 2 - (1 - expected_value) ** 3
               ) / standard_deviation ** 2 - (1 - expected_value)
        return alpha, beta
