from . import Provider, Witness, Agent
from ..util import ToDoException


class Consumer(Agent):
    witnesses: dict[Witness, float | None]
    scores: dict[Provider, float]
    providers: dict[Provider, float | None]

    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.witnesses = {}
        self.providers = {}
        self.scores = {}

    def register_witnesses(self, witnesses: list[Witness]):
        for w in witnesses:
            self.witnesses[w] = None

    def register_providers(self, providers: list[Provider]):
        for p in providers:
            self.providers[p] = None

    def score_of(self, provider: Provider) -> float:
        if provider not in self.scores:
            self.scores[provider] = 0
        return self.scores[provider]

    def update_provider(self, p: Provider, score: float) -> None:
        raise ToDoException()

    def choose_provider(self) -> Provider:
        if len(self.providers) == 0:
            raise ToDoException()

        best_provider = list(self.providers.keys())[0]
        for provider in self.providers:
            testimonies: dict[Witness, float] = {}
            for witness in self.witnesses:
                testimonies[witness] = witness.score_of(provider)

        return best_provider

    def update(self, *_):
        return
