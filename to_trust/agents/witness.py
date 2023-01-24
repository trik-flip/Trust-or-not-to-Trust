from random import choice, random

from to_trust.util import profiler

from .agent import Agent, LyingMode
from .provider import Provider


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

        if not self.honest():
            match(provider in self.ring, self.lying_mode):
                case(True, LyingMode.Fixed):
                    ret_val = self.bonus
                case(True, LyingMode.Bonus):
                    ret_val += self.bonus if self.ballot_stuffing else 0
                case(True, LyingMode.Inverse):
                    pass
                case(False, LyingMode.Fixed):
                    ret_val = 1 - self.bonus
                case(False, LyingMode.Bonus):
                    if self.bad_mouthing:
                        ret_val -= self.bonus
                    elif self.ballot_stuffing and len(self.ring) == 0:
                        ret_val += self.bonus
                case(False, LyingMode.Inverse):
                    ret_val = 1 - ret_val

        return min(1., max(.0, ret_val))


    def honest(self):
        return self.honesty >= random()

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
