from abc import ABC
from math import exp
from random import random
from typing_extensions import Self


class ToDoException(Exception):
    def __str__(self):
        return f"This method is not implemented!"


class Agent(ABC):
    ring: list[Self]

    def update(self):
        pass


class Provider(Agent):
    change: float
    quality: float

    def __init__(self, *, change: float, quality: float) -> None:
        self.change = change
        self.quality = quality

    def get_service(self) -> float:
        if self.change > random():
            return self.quality
        # TODO(Philip): Determine lowest score possible
        # Default cost of service?
        return 0


class Witness(Agent):
    scores: dict[Provider, float]
    bonus: float

    def __init__(self, *, bonus: float = 1) -> None:
        super().__init__()
        self.scores = {}
        self.bonus = bonus
        self.ring = []

    def score_of(self, provider: Provider) -> float:
        if provider not in self.scores:
            self.scores[provider] = 0

        if provider in self.ring:
            return self.scores[provider] + self.bonus
        else:
            return self.scores[provider]  # - self.bonus?


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

    def update(self):
        return

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


def updater(
    testimonies: dict[Witness, float],
    witness: Witness,
    provider: Provider,
):
    testimonies[witness] = witness.score_of(provider)
