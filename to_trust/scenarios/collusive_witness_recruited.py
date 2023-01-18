# Philip
from random import choice, sample

from ..agents import Witness
from ..testbed import Scenario


class RecruitWitness(Scenario):
    """A Scenario where witness are recruited to a collusive ring"""
    def __init__(self,
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
                 consumer_as_witness=False,
                 ring_size:int = 0,
                 witness_precentage_of_ring:float = .8
                 ):
        ring = []
        collusive_members = sample(witnesses, ring_size * witness_precentage_of_ring)
        collusive_members.extend(sample(consumers, ring_size * (1-witness_precentage_of_ring)))
        for member in collusive_members:
            member.add_to_ring(ring)

        super.__init__(witnesses = witnesses, witness_options=witness_options, witness_amount=witness_amount,
                       consumers=consumers, consumer_options=consumer_options,consumer_amount=consumer_amount,
                       providers=providers, provider_options=provider_options, provider_amount=provider_amount,
                       consumer_as_witness = consumer_as_witness)
    def update(self, providers, consumers, witnesses):
        collusive_ring = None
        not_collusive_members = set()
        collusive_members = set()

        for w in witnesses:
            if len(w.ring) == 0:
                not_collusive_members.add(w)
            else:
                collusive_members.add(w)
                collusive_ring = w.ring

        for member in not_collusive_members:
            choosen_one = choice(list(collusive_ring))
            member.add_to_ring(choosen_one)
