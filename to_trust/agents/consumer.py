from ..util import ToDoException, profiler
from . import Provider, Witness


class Consumer(Witness):
    witnesses: dict[Witness, float | None]
    scores: dict[Provider, float]
    providers: dict[Provider, float | None]

    @staticmethod
    def preprocess(witnesses, providers):
        pass
    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.witnesses = {}
        self.providers = {}
        self.scores = {}

    @profiler.profile
    def register_witnesses(self, witnesses: list[Witness]):
        for w in witnesses:
            self.witnesses[w] = None

    @profiler.profile
    def register_providers(self, providers: list[Provider]):
        for p in providers:
            self.providers[p] = None

    @profiler.profile
    def update_provider(self, p: Provider, score: float) -> None:
        raise ToDoException()

    @profiler.profile
    def choose_provider(self) -> Provider:
        if len(self.providers) == 0:
            raise ToDoException()

        best_provider = list(self.providers.keys())[0]
        for provider in self.providers:
            testimonies: dict[Witness, float] = {}
            for witness in self.witnesses:
                testimonies[witness] = witness.score_of(provider)

        return best_provider

    @profiler.profile
    def update(self, *_):
        pass
