from math import e, exp, log
from random import choice, random

from ..agents import Consumer, Provider, Witness
from ..util import profiler


class Act(Consumer):
    """
    - [x] [1]: Gamma = Nij / Nmin if Nij < Nmin else 1
    - [x] [2]: Nmin = - (1/(2epsilon**2))*ln((1 - theta)/ 2)
    - [x] [3]: direct_trust[p] = (alpha[p] + 1)/(alpha[p] + beta[p] + 2)
        - [] [3.1]: alpha = successful interactions between p and self,
        - [] [3.2]: beta = unsuccessful interactions between p and self,
    - [x] [4]: r[p] = u[p]*(G-C[p]) - (1-u[p]) * C[p]
    - [x] [5]: u[p] = 0 if O[p]==0 or D[p] == 1 elif O[p]==0 or D[p] == 1 then 1
    - [x] [6]: theta[w] [p] =1 /T[w] sum
    - [x] [7]: d[w] [p] =0 if witnesses[p] < Th else 1
        - [x] [7.1]: Th = [0,1]
    - [x] [8]: p[w] [p] = p[w] [p] + rho * (r[p]-r_tilde[p]-delta*theta[w] [p])* (1-pi[w] [p])
    - [x] [9]: pi[w] [p] = e**(p[w] [p])/sum(p[w] [p] for w in witnesses)
    - [x] [10]:r_tilde[p] = phi * r_tilde[p] + (1 - phi)*r[p]
        - [x] [10.1]: phi = (0, 1]
    - [x] [11]: indirect_trust[p] = sum(pi[w] [p] * test[w] [p] for w in top_witnesses)/sum(pi[w] [p] for w in top_witnesses)
    - [x] [12]: direct_reward = u_tilde * R + (1-u_tilde)*P
    - [x] [13]: u_tilde = 1 if O[p] == D[p] else 0
    - [x] [14]: D[p] =1 if direct_trust[p]>= Th else 0
    - [x] [15]: direct_p = direct_p + rho*(direct_r - r_tilde)*(1-direct_pi)
    - [x] [16]: direct_r_tilde = phi* direct_r_tilde + (1- phi)*direct_r
    - [x] [17]: direct_pi = (e**direct_p)/(e**direct_p + e**indirect_p)
    - [x] [18]: indirect_pi = e**indirect_p/(e**direct_p + e**indirect_p)
    - [x] [19]: rep[p] = gamma * direct_trust[p] + (1 - gamma) * indirect_trust[p]
    - [] [20]: sigma = 1/(T*N) * (sum)/(g_max - g_min) # TODO: (complete)
        - [] [20.1]: N is the number of service consumers adopting the same approach as c i does in the test-bed
    - [] [21]: cp =sum(try(c) for c in non_colluding_consumers)/(non_colluding_consumers * Nm)
    """

    def __init__(
        self,
        delta=0.5,
        epsilon=0.5,
        G=0.5,
        M=3,
        p_direct=0.5,
        p_indirect=0.5,
        P=0.5,
        phi=0.5,
        pr_min=0.3,
        Th=0.5,
        R=0.5,
        r_tilde_direct=0.5,
        rho=0.5,
        small_theta=0.5,
    ) -> None:
        super().__init__()
        self._alpha = {}
        self._beta = {}
        self._D = {}
        self._delta = delta
        self._epsilon = epsilon
        self._G = G
        self._M = M
        self._O = {}
        self._p = {}
        self._p_direct = p_direct
        self._p_indirect = p_indirect
        self._P = P
        self._phi = phi
        self._r_tilde = {}
        self._R = R
        self._r_tilde_direct = r_tilde_direct
        self._rho = rho
        self._small_theta = small_theta
        self._test = {}
        self._Th = Th
        self._pr_min = pr_min
        self._pr = 1

    @profiler.profile
    def update(self):
        super().update()
        self._pr = max(self._pr_min, self._pr - 0.2)

    @profiler.profile
    def _gamma(self, p: Provider):
        if self._N(p) < self._N_min:
            return self._N(p) / self._N_min
        return 1

    @profiler.profile
    def _N(self, p: Provider):
        return self._alpha[p] + self._beta[p]

    """number of interactions"""
    _M: int
    """Magnitude"""

    @property
    @profiler.profile
    def _N_min(self):
        return 1 / (2 * self._epsilon**2) * log((1 - self._small_theta) / 2, e)

    _epsilon: float
    """acceptable level of error rate"""
    _small_theta: float
    """confidence level"""

    @profiler.profile
    def _direct_trust(self, p: Provider, _t: int):
        return (self._alpha[p] + 1) / (self._alpha[p] + self._beta[p] + 2)

    _alpha: dict[Provider, int]
    _beta: dict[Provider, int]

    @profiler.profile
    def _r(self, p: Provider):
        return (
            self._u(p, self.epoch) * (self._G - p.cost)
            - (1 - self._u(p, self.epoch)) * p.cost
        )

    _G: float
    """utility derived from a successful interaction"""

    @profiler.profile
    def _u(self, p: Provider, t: int):
        if not self._O[p][t] and self._D[p][t] == 1:
            return 0
        if self._O[p][t] and self._D[p][t] == 1:
            return 1
        return 0

    _O: dict[Provider, list[bool]]
    """The outcome of an interaction between ci and sj at time t."""
    _D: dict[Provider, list[int]]
    """The overall decision by ci on whether to interact sj with at time t based on both direct and indirect trust evidence"""

    @profiler.profile
    def _theta(self, w: Witness, p: Provider):
        return (1 / len(self._test[w][p])) * sum(
            self._d(w, p, t) * (1 - self._O[p][t])
            for t, _ in enumerate(self._test[w][p])
        )

    @profiler.profile
    def _d(self, w: Witness, p: Provider, t: int):
        return self._test[w][p][t] >= self._Th

    _test: dict[Witness, dict[Provider, list[float]]]
    """testimony"""
    _Th: float
    """predefined threshold"""
    _p: dict[Witness, dict[Provider, float]]

    @profiler.profile
    def _update_p(self, w: Witness, p: Provider):
        self._p[w][p] = self._p[w][p] + self._rho * (
            self._r(p) - self._r_tilde[p] - self._delta * self._theta(w, p)
        ) * (1 - self._pi(w, p))

    _rho: float
    """learning rate"""
    _delta: float
    """bias towards penalizing collusion"""

    @profiler.profile
    def _pi(self, w: Witness, p: Provider):
        return (e ** self._p[w][p]) / sum(e ** self._p[_w][p] for _w in self.witnesses)

    _r_tilde: dict[Provider, float]
    """total accumulated reward """

    @profiler.profile
    def _update_r_tilde(self, p: Provider):
        self._r_tilde[p] = self._phi * \
            self._r_tilde[p] + (1 - self._phi) * self._r(p)

    _phi: float
    """determines the influence of the latest rewards in the smoothed baseline reward"""

    @profiler.profile
    def _indirect_trust(self, p: Provider, t: int):
        profiler.start("ACT-1")
        top = sum(self._pi(w, p) * w.score_of(p) for w in self.witnesses)
        profiler.switch("ACT-1", "ACT-2")
        bottom = sum(self._pi(w, p) for w in self.witnesses)
        profiler.stop("ACT-2")
        return top / bottom

    @profiler.profile
    def _r_direct(self):
        return self._u_tilde(self.epoch) * self._R + (1 - self._u_tilde(self.epoch)) * self._P

    _R: float
    """reward"""
    _P: float
    """penalty"""

    @profiler.profile
    def _u_tilde(self, t: int):
        for p in self.providers:
            if self._O[p][t] != self._Dd(p, t):
                return 0
        return 1

    @profiler.profile
    def _Dd(self, p: Provider, t: int):
        if self._direct_trust(p, t) >= self._Th:
            return True
        return False

    # 15, called 0x
    @profiler.profile
    def _update_p_direct(self):
        self._p_direct = self._p_direct + self._rho * (
            self._r_direct() - self._r_tilde_direct
        ) * (1 - self._pi_direct())

    _p_direct: float
    """learning parameter"""

    # 16, called 0x
    @profiler.profile
    def _update_r_tilde_direct(self):
        self._r_tilde_direct = (
            self._phi * self._r_tilde_direct +
            (1 - self._phi) * self._r_direct()
        )

    _r_tilde_direct: float
    """can be treated as a basis for comparing whether c i is better off or
worse off by aggregating the direct trust evidence into the estimation
for the trustworthiness of sj using the latest γij value"""

    # called 0x
    @profiler.profile
    def _pi_direct(self):
        return exp(self._p_direct) / (exp(self._p_direct) + exp(self._p_indirect))

    _p_indirect: float
    """learning parameter"""

    # called 0x
    @profiler.profile
    def _pi_indirect(self):
        return exp(self._p_indirect) / (exp(self._p_direct) + exp(self._p_indirect))

    @profiler.profile
    def _rep(self, p: Provider, t: int):
        return self._gamma(p) * self._direct_trust(p, t) + (
            1 - self._gamma(p)
        ) * self._indirect_trust(p, t)

    _pr: float
    _pr_min: float

    @profiler.profile
    def register_providers(self, providers: list[Provider]):
        super().register_providers(providers)
        self._alpha = {p: 0 for p in providers}
        self._beta = {p: 0 for p in providers}
        self._r_tilde = {p: 0 for p in providers}
        self._O = {p: [] for p in providers}
        self._D = {p: [] for p in providers}

    @profiler.profile
    def register_witnesses(self, witnesses: list[Witness]):
        super().register_witnesses(witnesses)
        self._p = {w: {p: 0 for p in self.providers} for w in witnesses}
        self._test = {w: {p: [] for p in self.providers} for w in witnesses}

    @profiler.profile
    def choose_provider(self):
        return self._testimony_aggregation()

    @profiler.profile
    def _testimony_aggregation(self):
        exploration_probability = random()  # 2
        # 3
        if exploration_probability <= self._pr and len(self._unknown_providers()):
            return choice(self._unknown_providers())  # 4
        known_sp = sorted(self._known_providers(), key=lambda p: self._direct_trust(
            p, self.epoch), reverse=True)  # 5, 6
        for p in known_sp:  # 7
            for w in self._top_witnesses:
                self._test[w][p] += [w.score_of(p)]  # 8
        # self.providers = {p: self._rep(p, self._t) for p in self.providers}
        for p in self.providers:
            self.scores[p] = self._rep(p, self.epoch)
        # 10, 11, 12
        return sorted(self.scores, key=lambda p: self.scores[p], reverse=True)[0]

    @profiler.profile
    def update_provider(self, p: Provider, score: float):
        self._O[p].append(score >= self._Th)
        self._D[p].append(True)
        for _p in self.providers:
            if _p != p:
                self._O[_p].append(False)
                self._D[_p].append(False)

        # 14
        if score >= self._Th:
            self._alpha[p] += 1
        else:
            self._beta[p] += 1
        # 15
        if self._N(p) > 1:
            for w in self._top_witnesses:
                self._update_p(w, p)  # TODO(Philip): check if this works
        # 17
        for w in self.witnesses:
            self.witnesses[w] = self._pi(w, p)

    @property
    @profiler.profile
    def _top_witnesses(self):
        witnesses = sorted(self.witnesses.items(),
                           key=lambda w: w[1], reverse=True)
        return [w[0] for w in witnesses[: self._M]]

    def _unknown_providers(self):
        return [p for p in self.providers if self._N(p) == 0]

    @profiler.profile
    def _known_providers(self):
        return [p for p in self.providers if self._N(p) != 0]
