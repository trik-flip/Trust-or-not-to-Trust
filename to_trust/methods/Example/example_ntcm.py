from to_trust.testbed.agents import NovelTrustComputingMethod, Witness


class ExampleNtcm(NovelTrustComputingMethod):
    def calc(self, score: float, testimonies: dict[Witness, float]) -> float:
        return score + sum(testimonies.values()) / len(testimonies)
