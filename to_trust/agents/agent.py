from abc import ABC
from enum import Enum
from typing import Any

from ..util import ToDoException


class Agent(ABC):
    ring: list[object]

    def remove_from_ring(self):
        self.ring.remove(self)
        self.ring = []

    def update(self, *_: Any) -> None:
        raise ToDoException()


class LyingMode(Enum):
    Fixed = 1
    Bonus = 2
