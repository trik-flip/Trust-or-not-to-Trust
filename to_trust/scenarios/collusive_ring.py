# Chloe
from random import choice, sample, random

from to_trust.agents import Consumer, Provider, Witness
from to_trust.testbed import Scenario

class CollusiveRing(Scenario):
    #There is a group working together (a collusive ring), they ballot-stuff each other.
     def __init__(
        self,
        *,
        witnesses: list[Witness] | None = None,
        witness_amount: int = 0,
        witness_options: dict[str, object] | None = {},
        consumers: list[Consumer] | None = None,
        consumer_amount: int = 0,
        consumer_options: dict[str, object] | None = {},
        providers: list[Provider] | None = None,
        provider_amount: int = 0,
        provider_options: dict[str, object] | None = {},
        consumer_as_witness=False,
        ring_size: int = 5,
        ):
        self.ring_size = ring_size
        self.ring = []
        self.independent = []

        for _ in range(self.ring_size):
            self.ring.append(Witness(honesty=1, ballot_stuffing=True))
        
        remaining_witnesses = witness_amount - ring_size
        for _ in range(remaining_witnesses):
            self.independent.append(Witness(honesty=1, bad_mouthing=True))

        super().__init__(
            witnesses=witnesses,
            witness_options=witness_options,
            witness_amount=witness_amount,
            consumers=consumers,
            consumer_options=consumer_options,
            consumer_amount=consumer_amount,
            providers=providers,
            provider_options=provider_options,
            provider_amount=provider_amount,
            consumer_as_witness=consumer_as_witness,
        )
            


