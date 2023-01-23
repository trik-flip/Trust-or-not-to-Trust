from to_trust.agents import Consumer, Provider, Witness
from to_trust.util import ToDoException, profiler
from .scenario import Scenario


class Simulation:
    witnesses: list[Witness]
    consumers: list[Consumer]
    providers: list[Provider]
    total_epochs: int
    runs_data: list[tuple[dict[Consumer, list[float]], dict[Provider, list[float]]]]
    ntcm: type[Consumer]
    scenario: Scenario

    def __init__(
        self,
        scenario: Scenario,
        ntcm: type[Consumer],
        total_epochs: int = 100,
    ):
        if scenario is None or ntcm is None:
            raise ToDoException()
        self.ntcm = ntcm
        self.scenario = scenario
        self.total_epochs = total_epochs
        self.runs_data = []

    @property
    @profiler.profile
    def last_run(self):
        return self.runs_data[-1]

    @profiler.profile
    def clean(self):
        self.consumers = self.scenario.get_consumers(self.ntcm)
        self.providers = self.scenario.get_providers()
        self.witnesses = self.scenario.get_witnesses()

    @profiler.profile
    def runs(self, n: int = 5, printing=False):
        for i in range(n):
            if printing:
                print(f"Epoch: {i}")
            yield self.run(printing)

    @profiler.profile
    def run(self, printing=False):
        self.clean()
        true_values: dict[Provider, list[float]] = {p: [] for p in self.providers}
        last_value = {p: 0.0 for p in self.providers}
        scores: dict[Consumer, list[float]] = {
            consumer: [] for consumer in self.consumers
        }
        self.setup()
        self.ntcm.preprocess(self.witnesses, self.providers)
        for _step in range(self.total_epochs):
            profiler.start("Simulation: epoch")
            if printing:
                print(f"[Epoch: {_step:2}]")
            for p in self.providers:
                last_value[p] = p.get_service()
                true_values[p] += [last_value[p]]
            for consumer in self.consumers:
                chosen_provider = consumer.choose_provider()
                score = last_value[chosen_provider]
                scores[consumer] += [score]
                consumer.update_provider(chosen_provider, score)
            for consumer in self.consumers:
                consumer.update()
            for witness in self.witnesses:
                witness.update()
            # for provider in self.providers:
            #     provider.update()
            self.scenario.update(self.providers, self.consumers, self.witnesses)
            profiler.stop("Simulation: epoch")
        self.runs_data.append((scores, true_values))
        return self.last_run

    @profiler.profile
    def setup(self):
        for c in self.consumers:
            c.register_providers(self.providers)
            c.register_witnesses(self.witnesses)
        for w in self.witnesses:
            w.register_providers(self.providers)
