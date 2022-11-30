from random import random

from ..util import profiler
from .agent import Agent


class Provider(Agent):
    chance: float
    quality: float
    cost: float

    def __init__(
        self,
        *,
        chance: float | None = None,
        quality: float | None = None,
        cost: float | None = None,
        l_chance: float = 0,
        u_chance: float = 1,
        l_quality: float = 0,
        u_quality: float = 1,
        l_cost: float = 0,
        u_cost: float = 1,
    ) -> None:

        self.chance = chance or l_chance + (u_chance - l_chance) * random()
        self.quality = quality or l_quality + (u_quality - l_quality) * random()
        self.cost = cost or l_cost + (u_cost - l_cost) * random()

    @profiler.profile
    def get_service(self) -> float:
        if self.chance > random():
            return self.quality - self.cost
        return -self.cost
