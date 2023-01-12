from abc import ABC

from ..agents import Consumer, Provider, Witness
from ..util import profiler


class Scenario(ABC):

    witnesses: list[Witness] | None
    consumers: list[Consumer] | None
    providers: list[Provider] | None

    witness_amount: int
    consumer_amount: int
    provider_amount: int

    witness_options: dict[str, object] | None
    consumer_options: dict[str, object] | None
    provider_options: dict[str, object] | None

    def __init__(
        self,
        *,
        witnesses: list[Witness] | None = None,
        witness_amount: int = 0,
        witness_options: dict[str, object] | None = None,
        consumers: list[Consumer] | None = None,
        consumer_amount: int = 0,
        consumer_options: dict[str, object] | None = None,
        providers: list[Provider] | None = None,
        provider_amount: int = 0,
        provider_options: dict[str, object] | None = None,
        consumer_as_witness=False
    ) -> None:
        super().__init__()
        self.witnesses = witnesses
        self.witness_amount = witness_amount
        self.witness_options = witness_options or {}

        self.consumers = consumers
        self.consumer_amount = consumer_amount
        self.consumer_options = consumer_options or {}

        self.providers = providers
        self.provider_amount = provider_amount
        self.provider_options = provider_options or {}

        self.consumer_as_witness = consumer_as_witness

    @profiler.profile
    def get_consumers(
        self,
        ntcm: type[Consumer],
    ) -> list[Consumer]:
        if self.consumers is None:
            self.consumers = [
                ntcm(**self.consumer_options) for _ in range(self.consumer_amount)
            ]
        return self.consumers

    @profiler.profile
    def get_witnesses(self) -> list[Witness]:
        if self.consumer_as_witness:
            return self.consumers

        if self.witnesses is None:
            self.witnesses = [
                Witness(**self.witness_options) for _ in range(self.witness_amount)
            ]
        return self.witnesses

    @profiler.profile
    def get_providers(self) -> list[Provider]:
        if self.providers is None:
            self.providers = [
                Provider(**self.provider_options) for _ in range(self.provider_amount)
            ]
        return self.providers

    def update(self, providers, consumers, witnesses):
        pass
