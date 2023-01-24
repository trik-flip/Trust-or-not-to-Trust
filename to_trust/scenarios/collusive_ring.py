# Chloe
from to_trust import Scenario, Witness

class CollusiveRing(Scenario):
    #There is a group working together (a collusive ring), at which they ballot-stuff each other.
    def __init__(
            self,
            ring_size: int = 0,
            witness_amount: int = 0,
            consumer_amount: int = 0,
            provider_amount: int = 0,
            provider_options: dict[str, object] | None = None
    )
        collusive_ring: list[Witness] = []

        # create a collusive ring as list
        for _ in range(ring_size):    
            witnesses.append(Witness(ballot_stuffing=True, honesty=1))

        witnesses = [collusive_ring]    # add the collusive ring to the list of witnesses as a list at position 0

        # add the other witnesses to the situation creating something like: collusive_ring = [ [collusive ring: witness1, witness2, ... ], witness, witness, ... ]
        for _ in range(witness_amount - ring_size):
            collusive_ring.append(Witness())  


        super().__init__(
            witnesses=witnesses, 
            consumer_amount=consumer_amount, 
            provider_amount=provider_amount, 
            provider_options=provider_options
         )




