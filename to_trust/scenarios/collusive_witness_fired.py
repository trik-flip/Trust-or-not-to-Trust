# Philip
from random import choice

from ..agents import Witness
from ..testbed import Scenario

class FireWitness(Scenario):
    """A Scenario where witness are fired from a collusive ring"""
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

        for member in collusive_members:
            choosen_one = choice(list(collusive_ring))
            member.remove_from_ring()
