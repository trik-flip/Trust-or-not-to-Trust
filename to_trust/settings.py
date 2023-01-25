from to_trust import LyingMode
from to_trust.methods import ITEA, MET, Act, Travos
from to_trust.scenarios import (
    FireProvider,
    FireWitness,
    HostileEnvironment,
    RecruitProvider,
    RecruitWitness,
    StartLying,
)
from to_trust.testbed import Simulation

Scenario_type = StartLying
epochs = 1
runs = 50
ntcm_type = Act

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
        "quality": None,
        "cost": None,
        "l_chance": 0.5,
        "u_chance": 0.85,
        "l_quality": 0.75,
        "u_quality": 0.99,
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
# TODO: Chloe

# Witnesses become more honest over time
# TODO: Rita

# Mixed world where 20% to 80% of the witnesses are lying either by ballot-stuffing or badmouthing
bs_bm_hostile_20_parameters = {
    # % of wtnesses badmouthing
    "bm_pct": 0.1,
    # % of wtnesses ballot-stuffing
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
    "collusive_witness_recruited": collusive_witness_recruited,
    "collusive_witness_fired": collusive_witness_fired,
    "collusive_provider_recruited": collusive_provider_recruited,
    "collusive_provider_fired": collusive_provider_fired,
    "bs_bm_hostile_20": bs_bm_hostile_20,
    "bs_bm_hostile_40": bs_bm_hostile_40,
    "bs_bm_hostile_80": bs_bm_hostile_80,
}

scenario = Scenario_type(
    consumer_amount=5,
    provider_amount=5,
    witness_amount=50,
    provider_options={"chance": 0.7, "l_quality": 0.8, "l_cost": 0.2, "u_cost": 0.5},
)
simulation = Simulation(scenario, ntcm_type, runs)
