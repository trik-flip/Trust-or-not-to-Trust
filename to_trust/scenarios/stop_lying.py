# Rita
from to_trust.agents import Consumer, Provider, Witness, LyingMode
from to_trust.testbed import Scenario


class StopLying(Scenario):
    # There is an environment where agents start being honest,
    # but eventually start lying.
    def __init__(
        self,
        witness_amount: int = 0,
        witness_percentage_lying: float = 1,
        lying_epochs: int = 0,
        # ratio_honest_epochs: int = 1,
        consumers: list[Consumer] | None = None,
        consumer_amount: int = 0,
        consumer_options: dict[str, object] | None = None,
        providers: list[Provider] | None = None,
        provider_amount: int = 0,
        provider_options: dict[str, object] | None = None,
        consumer_as_witness=False,
        lying_mode: LyingMode = LyingMode.Bonus,
        bonus: float = 0.2,
    ):
        self.witness_percentage_lying = witness_percentage_lying
        witnesses: list[Witness] = []
        witnesses_to_lie = round(witness_amount * witness_percentage_lying)

        for _ in range(witnesses_to_lie):
            witnesses.append(
                Witness(
                    honesty=0,
                    change_honesty=True,
                    epochs_before_dishonest=lying_epochs,
                    lying_mode=lying_mode,
                    honesty_step=0.1,
                    bonus=bonus,
                )
            )
        for _ in range(witness_amount - witnesses_to_lie):
            witnesses.append(Witness())

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
