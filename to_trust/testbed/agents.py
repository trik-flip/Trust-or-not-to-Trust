from abc import ABC
from enum import Enum
from math import exp
from random import random


class ToDoException(Exception):
    def __str__(self):
        return f"This method is not implemented!"


class Agent(ABC):
    ring: list[object]

    def remove_from_ring(self):
        self.ring.remove(self)
        self.ring = []

    def update(self):
        pass


class Provider(Agent):
    chance: float
    quality: float

    def __init__(self, *, chance: float, quality: float) -> None:
        self.chance = chance
        self.quality = quality

    def get_service(self) -> float:
        if self.chance > random():
            return self.quality
        # TODO(Philip): Determine lowest score possible
        # Default cost of service?
        return 0


class LyingMode(Enum):
    Fixed = 1
    Bonus = 2


class Witness(Agent):
    honesty: float
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
        ballot_stuffing: bool = False,
        lying_mode: LyingMode = LyingMode.Bonus,
        bad_mouthing: bool = False,
        starts_lying: bool = False,
        epochs_before_dishonest: int = 0,
    ) -> None:
        super().__init__()
        self.scores = {}
        self.bonus = bonus
        self.ring = []
        self.honesty = honesty
        self.ballot_stuffing = ballot_stuffing
        self.lying_mode = lying_mode
        self.bad_mouthing = bad_mouthing
        self.starts_lying = starts_lying
        self.epochs_before_dishonest = epochs_before_dishonest

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

        ret_val = max(1, ret_val)
        if self.honesty > random():
            return ret_val
        else:
            return 1 - ret_val

    def becomes_dishonest(self):
        self.honesty = 0

    def update(self, epoch):
        if self.starts_lying and epoch == self.epochs_before_dishonest:
            self.becomes_dishonest()


class NovelTrustComputingMethod(ABC):
    def calc(self, score: float, testimonies: dict[Witness, float]) -> float:
        raise ToDoException()


class Consumer(Agent):
    ntcm: NovelTrustComputingMethod
    scores: dict[Provider, float]

    def __init__(
        self,
        ntcm: NovelTrustComputingMethod,
    ) -> None:
        super().__init__()
        self.ntcm = ntcm
        self.scores = {}

    @staticmethod
    def calc_delta(old_score: float, score: float) -> float:
        # TODO(Philip): depends on ntcm
        return (score - old_score) ** 2

    def update_provider(self, provider: Provider, score: float):
        stored_score = self.scores[provider]
        delta = self.calc_delta(stored_score, score)

        self.scores[provider] += delta
        self.scores[provider] = self.scores[provider] / 1 + exp(-self.scores[provider])

    def score_of(self, provider: Provider) -> float:
        if provider not in self.scores:
            self.scores[provider] = 0
        return self.scores[provider]

    def choose_provider(
        self, providers: list[Provider], witnesses: list[Witness]
    ) -> Provider:
        if len(providers) == 0:
            raise ToDoException()

        best_provider = providers[0]
        best_score = float("-Inf")
        for provider in providers:
            score = self.score_of(provider)
            testimonies: dict[Witness, float] = {}
            for witness in witnesses:
                testimonies[witness] = witness.score_of(provider)

            ntcm_score = self.ntcm.calc(score, testimonies)

            if ntcm_score > best_score:
                best_provider = provider
                best_score = ntcm_score

        return best_provider
