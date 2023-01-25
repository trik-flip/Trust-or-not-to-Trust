from to_trust import LyingMode
from to_trust.methods import ITEA, MET, Act, Travos
from to_trust.scenarios import (
    FireProvider,
    FireWitness,
    HostileEnvironment,
    MultiCollusiveRing,
    RecruitProvider,
    RecruitWitness,
    StartLying,
)
from to_trust.scenarios.stop_lying import StopLying

epochs = 1
runs = 50
ntcm_type = ITEA

# Plotting settings
plot_run = True
plot_average = True
line_alpha = 0.2

# general settings
general_parameters = {
    "witness_amount": 30,
    # "witness_options": {
    #     "bonus": None,
    #     "honesty": None,
    #     "honesty_step": None,
    #     "ballot_stuffing": None,
    #     "lying_mode": None,
    #     "bad_mouthing": None,
    #     "starts_lying": None,
    #     "epochs_before_dishonest": None,
    # },
    "consumer_amount": 1 if ntcm_type is Travos else 5,
    "provider_amount": 50,
    "provider_options": {
        "chance": None,
        "l_chance": 0.5,
        "u_chance": 0.85,
        "quality": None,
        "l_quality": 0.75,
        "u_quality": 0.99,
        "cost": None,
        "l_cost": 0.1,
        "u_cost": 0.3,
    },
}

# A witness is “recruited” into a collusive ring
recruit_witness_parameters = {
    # size of the ring
    "ring_size": 5,
    # witness/provider ratio in ring
    "witness_percentage_of_ring": 0.3,
    # chance for each iteration to add a member to the ring
    "add_member_chance": 0.2,
}
collusive_witness_recruited = RecruitWitness(
    **general_parameters, **recruit_witness_parameters
)

# A witness is “fired” from a collusive ring
fire_witness_parameters = {
    # size of the ring
    "ring_size": 10,
    # chance for each iteration to fire a member from the ring
    "fire_member_chance": 0.2,
}
collusive_witness_fired = FireWitness(**general_parameters, **fire_witness_parameters)

# A provider is “recruited” into a collusive ring
recruit_provider_parameters = {
    # size of the ring
    "ring_size": 5,
    # witness/provider ratio in ring
    "witness_percentage_of_ring": 0.3,
    # chance for each iteration to add a member to the ring
    "add_member_chance": 0.2,
}
collusive_provider_recruited = RecruitProvider(
    **general_parameters, **recruit_provider_parameters
)

# A provider is “fired” from a collusive ring
fire_provider_parameters = {
    # size of the ring
    "ring_size": 10,
    # chance for each iteration to fire a member from the ring
    "fire_member_chance": 0.2,
}
collusive_provider_fired = FireProvider(
    **general_parameters, **fire_provider_parameters
)

# Multiple collusive rings
multi_collusive_rings = {
    # size of the ring
    "ring_size": 5,
    # number of rings
    "nr_rings": 5,
}
multiple_collusive_rings = MultiCollusiveRing(
    **general_parameters, **multi_collusive_rings
)

# Witnesses become more dishonest over time
become_honest_parameters = {
    # Percentage of witnesses that will start from being honest to being completely dishonest
    "witness_percentage_lying": 0.5,
    # Number of epochs before the witnesses become dishonest
    "lying_epochs": 10,
    #
    "lying_mode": LyingMode.Bonus,
    "bonus": 0.2,
}
become_honest = StopLying(**general_parameters, **become_honest_parameters)

become_dishonest_parameters = {
    # Percentage of witnesses that will start from being honest to being completely dishonest
    "witness_percentage_lying": 0.5,
    # Number of epochs before the witnesses become dishonest
    "honest_epochs": 10,
    #
    "lying_mode": LyingMode.Bonus,
    "bonus": 0.2,
}
become_dishonest = StartLying(**general_parameters, **become_dishonest_parameters)

# Mixed world where 20% to 80% of the witnesses are lying either by ballot-stuffing or badmouthing
bs_bm_hostile_20_parameters = {
    # % of witnesses badmouthing
    "bm_pct": 0.1,
    # % of witnesses ballot-stuffing
    "bs_pct": 0.1,
    # Bonus: adds/subtract bonus to provider value
    # Fixed: gives a fixed value for the providers
    # Inverse: gives 1 - true value of the provider
    "lying_mode": LyingMode.Bonus,
    # Amount of bonus added/subtracted if lying mode is bonus
    # Amount given if lying mode is fixed
    "bonus": 0.4,
}
bs_bm_hostile_20 = HostileEnvironment(
    **general_parameters, **bs_bm_hostile_20_parameters
)

bs_bm_hostile_40_parameters = {
    "bm_pct": 0.2,
    "bs_pct": 0.2,
    "lying_mode": LyingMode.Bonus,
    "bonus": 0.4,
}
bs_bm_hostile_40 = HostileEnvironment(
    **general_parameters, **bs_bm_hostile_40_parameters
)

bs_bm_hostile_80_parameters = {
    "bm_pct": 0.4,
    "bs_pct": 0.4,
    "lying_mode": LyingMode.Bonus,
    "bonus": 0.4,
}
bs_bm_hostile_80 = HostileEnvironment(
    **general_parameters, **bs_bm_hostile_80_parameters
)

scenarios = {
    # "stop_lying": become_honest,
    # "start_lying": become_dishonest,
    # "collusive_witness_recruited": collusive_witness_recruited,
    # "collusive_witness_fired": collusive_witness_fired,
    # "collusive_provider_recruited": collusive_provider_recruited,
    # "collusive_provider_fired": collusive_provider_fired,
    # "bs_bm_hostile_20": bs_bm_hostile_20,
    # "bs_bm_hostile_40": bs_bm_hostile_40,
    # "bs_bm_hostile_80": bs_bm_hostile_80,
    "multiple_collusive_rings": multiple_collusive_rings,
}
