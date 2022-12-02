import numpy as np
from scipy import stats, integrate
from to_trust import Provider, Witness, Consumer


class Travos(Consumer):
    def __init__(self,
                 epsilon_confidence: float = 0.1,
                 num_steps_integration: int = 100,
                 confidence_threshold: float = 0.8,
                 num_intervals: int = 5):
        super(Travos, self).__init__()
        self._alphas_p = {}
        self._betas_p = {}

        self._H = {}

        self._epsilon_confidence = epsilon_confidence
        self._num_steps_integration = num_steps_integration
        self._confidence_threshold = confidence_threshold

        self._intervals = np.linspace(0, 1, num_intervals + 1)

        # is used to estimate alpha and beta values for the witnesses
        self._num_runs = 0
        self.avg_estimation_errors = []

    def register_witnesses(self, witnesses: list[Witness]):
        super(Travos, self).register_witnesses(witnesses)
        for w in witnesses:
            if w not in self._H.keys():
                self._H[w] = {}
            for p in self.providers:
                self._H[w][p] = np.array([], dtype=[('outcome', int), ('expected_value', float)])

    def register_providers(self, providers: list[Provider]):
        super(Travos, self).register_providers(providers)
        self._alphas_p = {p: 1 for p in providers}
        self._betas_p = {p: 1 for p in providers}

    def update(self):
        # update avg estimation error
        avg_estimation_error = 0
        for p in self.providers.keys():
            avg_estimation_error += abs(self.providers[p] - p.chance)
        self.avg_estimation_errors.append(avg_estimation_error / len(self.providers))

    def update_provider(self, p: Provider, score: float) -> None:
        outcome = score > -p.cost
        for w in self._H.keys():
            # bin_idx = np.argwhere(self._intervals <= score)
            # if bin_idx.size == 0:
            #     bin_idx = 0
            # elif bin_idx.size == self._intervals.size:
            #     bin_idx = self._intervals.size - 2
            # else:
            #     bin_idx = bin_idx[-1][0]

            # self._H[w][p][-1]['outcome'] = (self._intervals[bin_idx]
            #                                 <= self._H[w][p][-1]['expected_value']
            #                                 <= self._intervals[bin_idx + 1])

            self._H[w][p][-1]['outcome'] = outcome

        if outcome:
            self._alphas_p[p] += 1
        else:
            self._betas_p[p] += 1

    def choose_provider(self) -> Provider:
        # calculate confidence values based on own experience
        confidence_values = self._calc_confidence_values()

        uniform_std_dev = stats.beta.std(1, 1)
        uniform_e_value = stats.beta.mean(1, 1)
        for provider, (confidence_value, expected_value) in confidence_values.items():
            # if the confidence value is lower than the threshold take opinions of witnesses into account
            if confidence_value > self._confidence_threshold:
                self.providers[provider] = expected_value
            else:
                alpha = 1
                beta = 1
                for witness in self.witnesses:
                    # estimate alpha and beta values based on number of runs
                    # α = μν, β = (1−μ)ν
                    # ν = α + β
                    e_value = witness.score_of(provider)
                    # +2 (because alpha = ... + 1 and beta = ... + 1)
                    w_alpha = e_value * (self._num_runs + 2)
                    w_beta = (1 - e_value) * (self._num_runs + 2)
                    std = stats.beta.std(w_alpha, w_beta)

                    # update expected value and std according to accuracy
                    acc = self._accuracy_of_witness(provider, witness)
                    e_value = uniform_e_value + acc * (e_value - uniform_e_value)
                    std = uniform_std_dev + acc * (std - uniform_std_dev)

                    # update alpha and beta values according to new expected value and std
                    alpha += (e_value ** 2 - e_value ** 3) / std ** 2 - e_value - 1
                    beta += ((1 - e_value) ** 2 - (1 - e_value) ** 3) / std ** 2 - (1 - e_value) - 1
                self.providers[provider] = stats.beta.mean(alpha, beta)

        self._num_runs += 1
        return max(self.providers, key=self.providers.get)

    def _calc_confidence_values(self) -> dict[Provider, (float, float)]:
        res = {}
        for p in self.providers:
            e_value = stats.beta.mean(self._alphas_p[p], self._betas_p[p])

            def beta_func(x):
                return stats.beta.pdf(x, self._alphas_p[p], self._betas_p[p])
            v1, _ = integrate.quad(beta_func, e_value - self._epsilon_confidence, e_value + self._epsilon_confidence)
            v2, _ = integrate.quad(beta_func, 0, 1)
            res[p] = (v1 / v2, e_value)
        return res

    def _accuracy_of_witness(self, p: Provider, w: Witness) -> float:
        score = w.score_of(p)
        alpha = np.sum(self._H[w][p]['outcome'] == 1) + 1
        beta = np.sum(self._H[w][p]['outcome'] == 0) + 1

        self._H[w][p] = np.append(np.array([(-1, score)], dtype=[('outcome', int), ('expected_value', float)]),
                                  self._H[w][p])

        # suggestion: use an epsilon environment around score rather than working with static intervals
        # then also update update_provider function

        bin_idx = np.argwhere(self._intervals <= score)
        if bin_idx.size == 0:
            bin_idx = 0
        elif bin_idx.size == self._intervals.size:
            bin_idx = bin_idx[-2][0]
        else:
            bin_idx = bin_idx[-1][0]

        def beta_func(x):
            return stats.beta.pdf(x, alpha, beta)
        t1, _ = integrate.quad(beta_func, self._intervals[bin_idx], self._intervals[bin_idx + 1])
        t2, _ = integrate.quad(beta_func, 0, 1)

        return t1 / t2
