# Benedikt
from to_trust.agents import Witness, LyingMode
from to_trust.testbed import Scenario


class HostileEnvironment(Scenario):
    # There is a hostile environment of 0% up to 80% (with intervals of 20%), where the percentage
    # of hostility is equal to the amount of agents lying. this is done for both BM as for BS
    def __init__(
        self,
        bm_pct: float = 0.5,
        bs_pct: float = 0.5,
        witness_amount: int = 0,
        witness_options: dict[str, object] = {},
        consumer_amount: int = 0,
        consumer_options: dict[str, object] = {},
        provider_amount: int = 0,
        provider_options: dict[str, object] | None = None,
        consumer_as_witness=False,
        lying_mode: LyingMode = LyingMode.Bonus,
        bonus: float = 0.2,
    ):
        witnesses: list[Witness] = []

        if lying_mode == LyingMode.Inverse:
            for _ in range(witness_amount):
                witnesses.append(
                    Witness(honesty=0, lying_mode=LyingMode.Inverse, **witness_options)
                )
        else:
            for _ in range(round(bm_pct * witness_amount)):
                witnesses.append(
                    Witness(
                        honesty=0,
                        bad_mouthing=True,
                        lying_mode=lying_mode,
                        bonus=bonus,
                        **witness_options
                    )
                )

            for _ in range(round(bs_pct * witness_amount)):
                witnesses.append(
                    Witness(
                        honesty=0,
                        ballot_stuffing=True,
                        lying_mode=lying_mode,
                        bonus=bonus,
                        **witness_options
                    )
                )

            if len(witnesses) < witness_amount:
                if bm_pct > bs_pct:
                    witnesses.append(
                        Witness(
                            honesty=0,
                            bad_mouthing=True,
                            lying_mode=lying_mode,
                            bonus=bonus,
                            **witness_options
                        )
                    )
                else:
                    witnesses.append(
                        Witness(
                            honesty=0,
                            ballot_stuffing=True,
                            lying_mode=lying_mode,
                            bonus=bonus,
                            **witness_options
                        )
                    )

        super().__init__(
            witnesses=witnesses,
            consumer_amount=consumer_amount,
            consumer_options=consumer_options,
            provider_amount=provider_amount,
            provider_options=provider_options,
            consumer_as_witness=consumer_as_witness,
        )
