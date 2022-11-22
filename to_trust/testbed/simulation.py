from ..agents import Witness, Provider, Consumer
from ..util import ToDoException
from .scenario import Scenario


class Simulation:
    witnesses: list[Witness]
    consumers: list[Consumer]
    providers: list[Provider]

    total_epochs: int

    def __init__(
        self,
        scenario: Scenario,
        ntcm: type[Consumer],
        total_epochs: int = 100,
    ):
        if scenario is None or ntcm is None:
            raise ToDoException()

        self.consumers = scenario.get_consumers(ntcm)
        self.providers = scenario.get_providers()
        self.witnesses = scenario.get_witnesses()
        self.total_epochs = total_epochs

    def run(self):

        true_values = {p: 0.0 for p in self.providers}
        last_value = {p: 0.0 for p in self.providers}

        scores = {consumer: 0.0 for consumer in self.consumers}
        for c in self.consumers:
            c.register_providers(self.providers)
            c.register_witnesses(self.witnesses)
        for w in self.witnesses:
            w.register_providers(self.providers)
        for _step in range(self.total_epochs):

            for p in self.providers:
                last_value[p] = p.get_service()
                true_values[p] += last_value[p]

            for consumer in self.consumers:
                chosen_provider = consumer.choose_provider()

                score = last_value[chosen_provider]

                scores[consumer] += score
                consumer.update_provider(chosen_provider, score)
            for consumer in self.consumers:
                consumer.update()
            for witness in self.witnesses:
                witness.update(_step)
            # for provider in self.providers:
            #     provider.update()

        return scores.values(), true_values.values()
