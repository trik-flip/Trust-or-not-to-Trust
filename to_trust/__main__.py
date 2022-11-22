from .testbed import Simulation
from .methods import Act
from .scenarios import HostileEnvironment, StartLying

scenario = StartLying(
    witness_amount=5,
    consumer_amount=5,
    provider_amount=5,
    provider_options={"chance": 0.7, "l_quality": 0.8, "l_cost": 0.3, "u_cost": 0.6},
)
ntcm = Act
sim = Simulation(scenario, ntcm, 1000)
scores, max_scores = sim.run()

print(f"Consumer Average: {sum(scores)/len(scores):.2f}")
print(f"Provider Average: {sum(max_scores)/len(max_scores):.2f}")
