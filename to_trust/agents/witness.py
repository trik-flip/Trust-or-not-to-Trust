from random import random, choice

from ..util import profiler
from . import Provider
from .agent import Agent, LyingMode


class Witness(Agent):
    honesty: float
    honesty_step: float
    ballot_stuffing: bool
    lying_mode: LyingMode
    bad_mouthing: bool
    scores: dict[Provider, float]
    bonus: float

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
        epochs_before_dishonest: int = 0,
    ) -> None:
        super().__init__()
        self.epoch = 0
        self.scores = {}
        self.bonus = bonus
        self.ring = []
        self.honesty = honesty
        self.ballot_stuffing = ballot_stuffing
        self.lying_mode = lying_mode
        self.bad_mouthing = bad_mouthing
        self.honesty_step = honesty_step
        self.starts_lying = starts_lying
        self.epochs_before_dishonest = epochs_before_dishonest

    @profiler.profile
    def score_of(self, provider: Provider) -> float:
        if provider not in self.scores:
            self.scores[provider] = 0
        ret_val: float = self.scores[provider]

        if provider in self.ring:

            if self.lying_mode == LyingMode.Fixed:
                return self.bonus
            else:
                ret_val += self.bonus if self.ballot_stuffing else 0
        else:
            if self.lying_mode == LyingMode.Fixed:
                return 1 - self.bonus
            else:
                ret_val -= self.bonus if self.bad_mouthing else 0

        ret_val = min(1, max(0, ret_val))
        if self.honesty > random():
            return ret_val
        else:
            return 1 - ret_val

    @profiler.profile
    def becomes_dishonest(self):
        self.honesty = 0

    @profiler.profile
    def update(self) -> None:
        if self.starts_lying and self.epoch == self.epochs_before_dishonest:
            self.becomes_dishonest()
        self.epoch += 1

    @profiler.profile
    def register_providers(self, providers: list[Provider]):
        # TODO: what should the value be?
        self.scores = {p: (p.chance * p.quality) - p.cost for p in providers}

    def choose_provider(self):
        return choice(self.scores.keys())

    def update_provider(self, p, score):
        pass
