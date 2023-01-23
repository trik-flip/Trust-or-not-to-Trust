from .methods import ITEA, Act, Travos, MET
from .scenarios import FireWitness, HostileEnvironment, RecruitWitness, StartLying
from .testbed import Simulation

Scenario_type = StartLying
epochs = 20
runs = 100
ntcm_type = MET

# Plotting settings
plot_run = True
plot_average = True
line_alpha = 0.2

scenario = Scenario_type(
    consumer_amount=5,
    provider_amount=5,
    witness_amount=50,
    provider_options={"chance": 0.7, "l_quality": 0.8, "l_cost": 0.2, "u_cost": 0.5},
)
simulation = Simulation(scenario, ntcm_type, runs)
