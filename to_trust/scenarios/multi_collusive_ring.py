# Chloe
from random import sample

from to_trust.agents import Consumer, Provider, Witness, Agent
from to_trust.testbed import Scenario


class MultiCollusiveRing(Scenario):
    """
    There are multiple groups working together (collusive rings), they ballot-stuff each other.
    """

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
        nr_rings: int = 5,
    ):
        self.ring_size = ring_size
        self.nr_rings = nr_rings
        self.rings = {}
        collusive_witnesses: list[Agent] = []
        independent_witnesses = []

        for _ in range(ring_size * nr_rings):
            collusive_witnesses.append(Witness(honesty=1, ballot_stuffing=True))

        for _ in range(witness_amount - (ring_size * nr_rings)):
            independent_witnesses.append(Witness(honesty=1, bad_mouthing=True))

        for ring in range(nr_rings):
            selection = sample(collusive_witnesses, k=ring_size)
            self.rings[ring] = []
            for agent in selection:
                agent.add_to_ring(self.rings[ring])
                collusive_witnesses.remove(agent)

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
