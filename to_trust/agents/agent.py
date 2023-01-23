from abc import ABC
from enum import Enum
from typing import Any

from to_trust.util import ToDoException, profiler


class Agent(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.ring = []

    @profiler.profile
    def add_to_ring(self, ring):
        self.ring = ring
        self.ring.append(self)

    @profiler.profile
    def remove_from_ring(self):
        self.ring.remove(self)
        self.ring = []

    @profiler.profile
    def update(self, *_: Any) -> None:
        raise ToDoException()


class LyingMode(Enum):
    Fixed = 1
    Bonus = 2
