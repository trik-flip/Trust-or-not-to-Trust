import logging

from ..agents import Consumer, Provider, Witness
from ..util import ToDoException, profiler
from .scenario import Scenario


class Simulation:
    witnesses: list[Witness]
    consumers: list[Consumer]
    providers: list[Provider]
    total_epochs: int
    runs_data: list[tuple[dict[Consumer, list[float]],
                          dict[Provider, list[float]]]]
    ntcm: type[Consumer]
    scenario: Scenario

    def __init__(
        self,
        scenario: Scenario,
        ntcm: type[Consumer],
        total_epochs: int = 100,
    ):
        # logging.basicConfig(level=logging.INFO)
        if scenario is None or ntcm is None:
            raise ToDoException()
        logging.info(f"[Init] Creating simulation with ntcm:{ntcm.__name__}")
        self.ntcm = ntcm
        logging.info(
            f"[Init] Creating simulation with scenario:{type(scenario).__name__}"
        )
        self.scenario = scenario
        logging.info(f"[Init] Creating simulation with {total_epochs} epochs")
        self.total_epochs = total_epochs
        self.runs_data = []

    @property
    @profiler.profile
    def last_run(self):
        return self.runs_data[-1]

    @profiler.profile
    def clean(self):
        logging.info("[Clean] Creating sim from scenario")
        self.consumers = self.scenario.get_consumers(self.ntcm)
        self.providers = self.scenario.get_providers()
        self.witnesses = self.scenario.get_witnesses()
        logging.info("[Clean] sim created from scenario")

    @profiler.profile
    def runs(self, n: int = 5):
        for _ in range(n):
            logging.info(f"[Run {_+1}/{n}] Starting")
            yield self.run()
            logging.info(f"[Run {_+1}/{n}] Done")

    @profiler.profile
    def run(self):
        self.clean()
        true_values: dict[Provider, list[float]] = {
            p: [] for p in self.providers}
        last_value = {p: 0.0 for p in self.providers}
        scores: dict[Consumer, list[float]] = {
            consumer: [] for consumer in self.consumers
        }
        self.setup()
        for _step in range(self.total_epochs):
            profiler.start("Simulation: epoch")
            logging.info(f"[Epoch: {_step}] Get services from all providers")
            for p in self.providers:
                last_value[p] = p.get_service()
                true_values[p] += [last_value[p]]
            logging.info(f"[Epoch: {_step}] consumer pick service providers")
            for consumer in self.consumers:
                chosen_provider = consumer.choose_provider()
                score = last_value[chosen_provider]
                scores[consumer] += [score]
                consumer.update_provider(chosen_provider, score)
            logging.info(f"[Epoch: {_step}] Updating consumers")
            for consumer in self.consumers:
                consumer.update()
            logging.info(f"[Epoch: {_step}] Updating witnesses")
            for witness in self.witnesses:
                witness.update(_step)
            # logging.info(f"[Epoch: {_step}] Updating providers")
            # for provider in self.providers:
            #     provider.update()
            profiler.stop("Simulation: epoch")
        self.runs_data.append((scores, true_values))
        return self.last_run

    @profiler.profile
    def setup(self):
        logging.info("[Setup] Registering at all consumers")
        for c in self.consumers:
            c.register_providers(self.providers)
            c.register_witnesses(self.witnesses)
        logging.info("[Setup] Registering at all witnesses")
        for w in self.witnesses:
            w.register_providers(self.providers)
