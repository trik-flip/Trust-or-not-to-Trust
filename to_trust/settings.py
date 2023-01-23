from .methods import ITEA, Act, Travos
from .scenarios import FireWitness, HostileEnvironment, RecruitWitness, StartLying
from .testbed import Simulation

Scenario_type = RecruitWitness
epochs = 1
runs = 50
ntcm_type = Act

# Plotting settings
plot_run = True
plot_average = True
line_alpha = 0.2

scenario = Scenario_type(
    consumer_amount=10,
    provider_amount=25,
    witness_amount=100,
    provider_options={"chance": 0.7, "l_quality": 0.8, "l_cost": 0.2, "u_cost": 0.5},
)
simulation = Simulation(scenario, ntcm_type, runs)
