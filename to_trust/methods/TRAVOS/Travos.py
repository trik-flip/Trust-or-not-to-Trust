import numpy as np
from scipy import stats, integrate
from to_trust import Provider, Witness, Consumer

UNIFORM_STD_DEV = stats.beta.std(1, 1)
UNIFORM_EXPECTED_VALUE = 0.5


class Travos(Consumer):
    def __init__(
            self,
            epsilon_confidence: float = 0.2,
            num_steps_integration: int = 100,
            confidence_threshold: float = 0.8,
            num_intervals: int = 5,
            outcome_threshold: float = 0.5,
    ):
        super(Travos, self).__init__()
        self._alphas_p = {}
        self._betas_p = {}

        self._outcome_history = {}

        self._epsilon_confidence = epsilon_confidence
        self._num_steps_integration = num_steps_integration
        self._confidence_threshold = confidence_threshold
        self._outcome_threshold = outcome_threshold

        self._intervals = np.linspace(0, 1, num_intervals + 1)

        self.avg_estimation_errors = []
        self.run_index = 0

    def register_witnesses(self, witnesses: list[Witness]):
        super(Travos, self).register_witnesses(witnesses)
        for witness in witnesses:
            if witness not in self._outcome_history.keys():
                self._outcome_history[witness] = {}
            for provider in self.providers:
                self._outcome_history[witness][provider] = np.array([], dtype=[("run_index", int),
                                                                               ("outcome", bool),
                                                                               ("expected_value", float),
                                                                               ("bin_index", int)])

    def register_providers(self, providers: list[Provider]):
        super(Travos, self).register_providers(providers)
        self._alphas_p = {provider: 1 for provider in providers}
        self._betas_p = {provider: 1 for provider in providers}

    def update(self):
        # update avg estimation error
        avg_estimation_error = 0
        for provider in self.providers.keys():
            avg_estimation_error += abs(self.providers[provider] - provider.quality)
        self.avg_estimation_errors.append(avg_estimation_error / len(self.providers))
        print(self.avg_estimation_errors[-1])

    def update_provider(self, provider: Provider, score: float) -> None:
        outcome = score > self._outcome_threshold

        for witness in self.witnesses:
            relevant_entry = np.argwhere(self._outcome_history[witness][provider]["run_index"] == self.run_index)
            expected_outcome = self._outcome_history[witness][provider][relevant_entry]["expected_value"] > self._outcome_threshold
            self._outcome_history[witness][provider][relevant_entry]["outcome"] = expected_outcome == outcome

        if outcome:
            self._alphas_p[provider] += 1
        else:
            self._betas_p[provider] += 1

    def choose_provider(self) -> Provider:
        self.run_index += 1
        # calculate confidence values based on own experience
        confidence_values = self._confidence_values_of_providers()

        for provider, (confidence_value, expected_value) in confidence_values.items():
            # if the confidence value is lower than the threshold take opinions of witnesses into account
            if confidence_value < self._confidence_threshold:
                expected_value = self._estimate_value_with_witnesses_opinions(provider, expected_value)
            self.providers[provider] = expected_value
        return max(self.providers, key=self.providers.get)

    def _confidence_values_of_providers(self) -> dict[Provider, (float, float)]:
        res = {}
        for p in self.providers:
            expected_value = stats.beta.expect(args=(self._alphas_p[p], self._betas_p[p]))

            def beta_func(x):
                return stats.beta.pdf(x, self._alphas_p[p], self._betas_p[p])

            expected_area, _ = integrate.quad(beta_func,
                                              expected_value - self._epsilon_confidence,
                                              expected_value + self._epsilon_confidence)
            full_area, _ = integrate.quad(beta_func, 0, 1)
            res[p] = (expected_area / full_area, expected_value)
        return res

    def _estimate_value_with_witnesses_opinions(self, provider: Provider, original_expected_value: float):
        bin_index = np.argwhere(self._intervals < original_expected_value)
        if bin_index.size == 0:
            bin_index = 0
        elif bin_index.size == self._intervals.size:
            bin_index = bin_index[-2][0]
        else:
            bin_index = bin_index[-1][0]

        alpha = 0
        beta = 0
        for witness in self.witnesses:
            witness_accuracy, witness_expected_value = self._accuracy_of_witness(provider, witness, bin_index)

            # update expected value and standard deviation according to accuracy
            witness_standard_deviation = 0.15

            adjusted_expected_value = UNIFORM_EXPECTED_VALUE + witness_accuracy * (witness_expected_value - UNIFORM_EXPECTED_VALUE)
            adjusted_standard_deviation = UNIFORM_STD_DEV + witness_accuracy * (witness_standard_deviation - UNIFORM_STD_DEV)

            # update alpha and beta values according to adjusted expected value and standard deviation
            adjusted_alpha, adjusted_beta = self._calculate_alpha_beta(adjusted_expected_value,
                                                                       adjusted_standard_deviation)

            alpha += adjusted_alpha
            beta += adjusted_beta

        return stats.beta.expect(args=(alpha, beta))

    def _accuracy_of_witness(self, provider: Provider, witness: Witness, bin_idx: int) -> (float, float):
        # calculate accuracy of witness
        alpha = 1
        beta = 1

        relevant_entries = np.argwhere(self._outcome_history[witness][provider]["bin_index"] == bin_idx)
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
                                          self._intervals[bin_idx],
                                          self._intervals[bin_idx + 1])
        full_area, _ = integrate.quad(beta_func, 0, 1)

        # store the provided value of the witness
        expected_value = witness.score_of(provider)
        self._outcome_history[witness][provider] = np.append(
            np.array([(self.run_index, False, expected_value, bin_idx)],
                     dtype=[("run_index", int),
                            ("outcome", bool),
                            ("expected_value", float),
                            ("bin_index", int)]),
            self._outcome_history[witness][provider],
        )

        return expected_area / full_area, expected_value

    @staticmethod
    def _calculate_alpha_beta(expected_value: float, standard_deviation: float) -> (float, float):
        alpha = (expected_value ** 2 - expected_value ** 3) / standard_deviation ** 2 - expected_value
        beta = (((1 - expected_value) ** 2 - (1 - expected_value) ** 3) /
                standard_deviation ** 2 - (1 - expected_value))
        return alpha, beta
