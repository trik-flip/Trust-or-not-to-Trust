# Benedikt
from to_trust import Scenario, Witness


class HostileEnvironment(Scenario):
    # There is a hostile environment of 0% up to 80% (with intervals of 20%), where the percentage
    # of hostility is equal to the amount of agents lying. this is done for both BM as for BS
    def __int__(
            self,
            bm_pct: float = 0.5,
            bs_pct: float = 0.5,
            witness_amount: int = 0,
            consumer_amount: int = 0,
            provider_amount: int = 0,
            provider_options: dict[str, object] | None = None
    ):
        witnesses = []
        for _ in range(round(bm_pct * witness_amount)):
            witnesses.append(Witness(bad_mouthing=True))

        for _ in range(round(bs_pct * witness_amount)):
            witnesses.append(Witness(ballot_stuffing=True))

        if len(witnesses) < witness_amount:
            if bm_pct > bs_pct:
                witnesses.append(Witness(bad_mouthing=True))
            else:
                witnesses.append(Witness(ballot_stuffing=True))

        super().__init__(witnesses=witnesses, consumer_amount=consumer_amount, provider_amount=provider_amount, provider_options=provider_options)
