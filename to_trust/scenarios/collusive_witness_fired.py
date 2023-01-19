# Philip
from random import choice

from ..agents import Witness
from ..testbed import Scenario


class FireWitness(Scenario):
    """A Scenario where witness are fired from a collusive ring"""

    def update(self, providers, consumers, witnesses):
        collusive_members = set()

        for w in witnesses:
            if len(w.ring) != 0:
                collusive_members.add(w)

        choosen_one = self.__select_member(collusive_members)
        choosen_one.remove_from_ring()

    @staticmethod
    def __select_member(collusive_members):
        return choice(list(collusive_members))
        # TODO: implement other strategies to recruit a member
