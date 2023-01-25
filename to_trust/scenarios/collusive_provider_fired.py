# Philip
from random import choice, random, sample

from to_trust.agents import Consumer, Provider, Witness
from to_trust.testbed import Scenario


class FireProvider(Scenario):
    """A Scenario where witness are fired from a collusive ring"""

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
        consumer_as_witness: bool = False,
        fire_member_chance: float = 0.2,
        ring_size: int = 10
    ) -> None:
        super().__init__(
            witnesses=witnesses,
            witness_amount=witness_amount,
            witness_options=witness_options,
            consumers=consumers,
            consumer_amount=consumer_amount,
            consumer_options=consumer_options,
            providers=providers,
            provider_amount=provider_amount,
            provider_options=provider_options,
            consumer_as_witness=consumer_as_witness,
        )
        self.ring_size = ring_size
        self.change = fire_member_chance

    def preprocess(self):
        self.ring = []
        collusive_members = sample(
            set(self.witnesses) ^ set(self.providers), self.ring_size
        )
        for member in collusive_members:
            member.add_to_ring(self.ring)

        return super().preprocess()

    def update(self, providers, _c, _w):
        if random() > self.change:
            return
        collusive_members = set()

        for w in providers:
            if len(w.ring) != 0:
                collusive_members.add(w)
        if len(collusive_members) > 0:
            choosen_one = self.__select_member(collusive_members)
            choosen_one.remove_from_ring()

    @staticmethod
    def __select_member(collusive_members):
        return choice(list(collusive_members))
        # TODO: implement other strategies to recruit a member
