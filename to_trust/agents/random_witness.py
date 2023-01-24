# from random import random, choice
import random
from ..util import profiler
from . import Provider, Witness
from .agent import Agent, LyingMode
from collections import defaultdict


def get_pn_pairs(z, total_number_interactions=300000):
    """
        Given a z value - which is in [0, 1]
        Get all possible pairs (p, n) that can solve brs(p,n)=z=(p+1)/(p+n+2)
        Set p to: 0, 0.1, 0.2, ..., 0.9, 1
        Rewrite formula to isolate n: n = ((p+1)/z) -p - 2
    """
    pn_pairs = []
    for p in range(total_number_interactions):
        n = ((p + 1) / z) - p - 2
        pn_pairs.append([p, n])
    return pn_pairs


def get_random_pn_pair(z, total_number_interactions: float = 100):
    pairs = get_pn_pairs(z, total_number_interactions)
    return random.choice(pairs)


def brs(p, n):
    return (p + 1) / (p + n + 2)


class RandomWitness(Witness):

    def __init__(
            self,
            *,
            bonus: float = 1,
            honesty: float = 1,
            honesty_step: float = 0,
            ballot_stuffing: bool = False,
            lying_mode: LyingMode = LyingMode.Bonus,
            bad_mouthing: bool = False,
            starts_lying: bool = False,
            all_positive: bool = False,
            all_negative: bool = False,
            partially_random: bool = False,
            threshold_score: float = 0.5
    ) -> None:
        super().__init__(
            bonus=bonus,
            honesty=honesty,
            honesty_step=honesty_step,
            ballot_stuffing=ballot_stuffing,
            lying_mode=lying_mode,
            bad_mouthing=bad_mouthing,
            starts_lying=starts_lying
        )
        self.all_positive = all_positive
        self.all_negative = all_negative
        self.partially_random = partially_random

        # Dictionary to store for partially random
        self.providers = {}

        self.interactions = defaultdict(dict)

        self.threshold_score = threshold_score

    def score_of(self, provider: Provider) -> float:
        super().score_of(provider)
        if self.partially_random:
            if self.providers[provider]:
                rand_z = random.uniform(0, 1)
                p, n = get_random_pn_pair(rand_z)
                return brs(p, n)
            else:
                return self.scores[provider]
        elif self.all_positive:
            return brs(self.interactions[provider]['positive'] + self.interactions[provider]['negative'], 0)
        elif self.all_negative:
            return brs(0, self.interactions[provider]['positive'] + self.interactions[provider]['negative'])

    def update(self) -> None:
        self.epoch += 1

    def register_providers(self, providers: list[Provider]):
        for p in providers:
            if self.partially_random:
                if random.random() > 0.5:
                    # Provider picked for randomly distorted recommendations
                    self.providers[p] = True
                else:
                    # Provider NOT picked for randomly distorted recommendations -> always honest
                    self.providers[p] = False
            else:
                self.providers[p] = True
            self.interactions[p]['positive'] = 0
            self.interactions[p]['negative'] = 0

    def update_provider(self, p, score):
        super().update_provider(p=p, score=score)
        if score < self.threshold_score:
            self.interactions[p]['negative'] += 1
        else:
            self.interactions[p]['positive'] += 1
