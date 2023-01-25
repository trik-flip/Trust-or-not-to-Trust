# Philip
from random import choice, sample, random

from to_trust.agents import Consumer, Provider, Witness
from to_trust.testbed import Scenario


class RecruitProvider(Scenario):
    """A Scenario where witness are recruited to a collusive ring"""

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
        witness_percentage_of_ring: float = 0.0,
        add_member_chance: float = 0.5
):
        self.ring_size = ring_size
        self.witness_percentage_of_ring = witness_percentage_of_ring
        self.add_member_chance = add_member_chance
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

    def preprocess(self):
        self.ring = []
        collusive_members = sample(
            self.witnesses, int(self.ring_size * self.witness_percentage_of_ring)
        )
        collusive_members.extend(
            sample(
                self.providers,
                int(self.ring_size * (1 - self.witness_percentage_of_ring)),
            )
        )
        for member in collusive_members:
            member.add_to_ring(self.ring)

    def update(self, providers, _c, witnesses):
        not_collusive_members = set()
        if self.witness_percentage_of_ring > random():
            for a in witnesses:
                if len(a.ring) == 0:
                    not_collusive_members.add(a)
        else:
            for a in providers:
                if len(a.ring) == 0:
                    not_collusive_members.add(a)
        if len(not_collusive_members) > 0 and self.add_member_chance > random():
            chosen_one = self.__select_new_member(not_collusive_members)
            chosen_one.add_to_ring(self.ring)

    @staticmethod
    def __select_new_member(collusive_ring):
        return choice(list(collusive_ring))
        # TODO: implement other strategies to recruit a member
