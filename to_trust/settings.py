from methods import ITEA, Act, Travos, MET
from scenarios import FireWitness, HostileEnvironment, RecruitWitness, StartLying, MultiCollusiveRing
from testbed import Simulation
from to_trust import LyingMode

Scenario_type = StartLying
epochs = 2
runs = 3
ntcm_type = Travos

# Plotting settings
plot_run = True
plot_average = True
line_alpha = 0.2

# general settings
general_parameters = {
    "witness_amount": 30,
    "consumer_amount": 1 if ntcm_type is Travos else 5,
    "provider_amount": 50,
}

# A witness is “recruited” into a collusive ring
recruit_witness_parameters = {
    # size of the ring
    "ring_size": 5,
    # witness/provider ratio in ring
    "witness_percentage_of_ring": 0.3,
    # chance for each iteration to add a member to the ring
    "add_member_chance": 0.2
}
collusive_witness_recruited = RecruitWitness(**general_parameters, **recruit_witness_parameters)

# A witness is “fired” from a collusive ring
fire_witness_parameters = {
    # size of the ring
    "ring_size": 10,
    # chance for each iteration to fire a member from the ring
    "fire_member_chance": 0.2
}
collusive_witness_fired = FireWitness(**general_parameters, **fire_witness_parameters)

# A provider is “recruited” into a collusive ring
recruit_provider_parameters = {
    # size of the ring
    "ring_size": 5,
    # provider/provider ratio in ring
    "provider_percentage_of_ring": 0.3,
    # chance for each iteration to add a member to the ring
    "add_member_chance": 0.2
}
collusive_provider_recruited = RecruitWitness(**general_parameters, **recruit_provider_parameters)

# A provider is “fired” from a collusive ring
fire_provider_parameters = {
    # size of the ring
    "ring_size": 10,
    # chance for each iteration to fire a member from the ring
    "fire_member_chance": 0.2
}
collusive_provider_fired = FireWitness(**general_parameters, **fire_provider_parameters)

# Multiple collusive rings
multi_collusive_rings = {
    # size of the ring
    "ring_size": 5,
    # provider/provider ratio in ring
    "nr_rings": 5,
}
multiple_collusive_rings = MultiCollusiveRing(**general_parameters, **multi_collusive_rings)

# Witnesses become more dishonest over time
become_dishonest_parameters = {
    # Percentage of witnesses that will start from being honest to being completely dishonest
    "witness_percentage_lying": 0.5,
    # Number of epochs before the witnesses become dishonest
    "honest_epochs": 50,
    #
    "lying_mode": LyingMode.Bonus,
    "bonus": .2
}
become_dishonest = StartLying(**general_parameters, ** become_dishonest_parameters)

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
    "bonus": .4,
}
bs_bm_hostile_20 = HostileEnvironment(**general_parameters, ** bs_bm_hostile_20_parameters)

bs_bm_hostile_40_parameters = {
    "bm_pct": 0.2,
    "bs_pct": 0.2,
    "lying_mode": LyingMode.Bonus,
    "bonus": .4,
}
bs_bm_hostile_40 = HostileEnvironment(**general_parameters, ** bs_bm_hostile_40_parameters)

bs_bm_hostile_80_parameters = {
    "bm_pct": 0.4,
    "bs_pct": 0.4,
    "lying_mode": LyingMode.Bonus,
    "bonus": .4,
}
bs_bm_hostile_80 = HostileEnvironment(**general_parameters, ** bs_bm_hostile_80_parameters)

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
