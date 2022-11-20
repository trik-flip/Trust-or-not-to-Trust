from to_trust.util import ToDoException
from .agents import Consumer, NovelTrustComputingMethod, Provider, Witness
from .scenario import Scenario


class Simulation:
    witnesses: list[Witness]
    consumers: list[Consumer]
    providers: list[Provider]

    total_epochs: int

    def __init__(
        self,
        scenario: Scenario,
        ntcm: NovelTrustComputingMethod,
        total_epochs: int = 100,
    ):
        if scenario is None or ntcm is None:
            raise ToDoException()

        self.consumers = scenario.get_consumers(ntcm)
        self.witnesses = scenario.get_witnesses()
        self.providers = scenario.get_providers()
        self.total_epochs = total_epochs

    def run(self):

        scores: list[float] = [0 for _consumer in self.consumers]

        true_scores: dict[Provider, float] = {}
        for prov in self.providers:
            true_scores[prov] = 0
        for _step in range(self.total_epochs):
            print(f"epoch:{_step+1}")
            for prov in self.providers:
                b_score = prov.get_service()
                true_scores[prov] += b_score
            for index, consumer in enumerate(self.consumers):
                chosen_provider = consumer.choose_provider(
                    self.providers, self.witnesses
                )
                score = chosen_provider.get_service()
                scores[index] += score
                consumer.update_provider(chosen_provider, score)

            for consumer in self.consumers:
                consumer.update()
            for witness in self.witnesses:
                witness.update(_step)
            for provider in self.providers:
                provider.update()

        return scores, [v for v in true_scores.values()]
