from typing import Callable

from to_trust.agents import Agent
from to_trust.agents.consumer import Consumer
from to_trust.agents.provider import Provider
from to_trust.util import Singleton

MetricFunction = Callable[
    [dict[Consumer, list[float]], dict[Provider, list[float]], int], float
]


class MetricSystem(metaclass=Singleton):
    _metric_methods: dict[str, MetricFunction] = {}

    @staticmethod
    def register(name: str):
        def outer_func(func: MetricFunction):
            def inner_func(*args, **kwargs):
                return func(*args, **kwargs)

            instance = MetricSystem()
            instance._metric_methods[name] = inner_func
            return inner_func

        return outer_func

    def measure(self, *args):
        for metrics in self._metric_methods:
            print(f"{metrics}: {self._metric_methods[metrics](*args)}")

    @staticmethod
    def average(agents: dict[Agent, list[float]]):
        return sum(sum(agents[_a]) for _a in agents) / len(agents)
