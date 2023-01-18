from .methods import ITEA, Act, Travos
from .scenarios import FireWitness, HostileEnvironment, RecruitWitness, StartLying
from .testbed import Simulation

Scenario_type = HostileEnvironment
epochs = 20
runs = 50
ntcm_type = Act

scenario = Scenario_type(
    consumer_amount=5,
    provider_amount=5,
    witness_amount=5,
    provider_options={"chance": 0.7, "l_quality": 0.8, "l_cost": 0.2, "u_cost": 0.5},
)
simulation = Simulation(scenario, ntcm_type, runs)
