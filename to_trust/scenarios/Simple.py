# Rita
from ..testbed import Scenario
from ..agents import Witness, Consumer, Provider


class Simple(Scenario):

    def __init__(
            self,
            witnesses: list[Witness] | None = None,
            consumers: list[Consumer] | None = None,
            consumer_amount: int = 0,
            consumer_options: dict[str, object] | None = None,
            providers: list[Provider] | None = None,
            provider_amount: int = 0,
            provider_options: dict[str, object] | None = None,
            consumer_as_witness=False,
    ):
        super().__init__(
            witnesses=witnesses,
            consumers=consumers,
            consumer_amount=consumer_amount,
            consumer_options=consumer_options,
            providers=providers,
            provider_amount=provider_amount,
            provider_options=provider_options,
            consumer_as_witness=consumer_as_witness,
        )
