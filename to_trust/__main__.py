from to_trust import Simulation, Scenario
from to_trust.methods.Example.example_ntcm import ExampleNtcm


scenario = Scenario(
    witness_amount=5,
    consumer_amount=5,
    provider_amount=5,
    provider_options={"change": 0.7, "quality": 0.9},
)

ntcm = ExampleNtcm()
sim = Simulation(scenario, ntcm, 20)
scores = sim.run()

print(scores)
