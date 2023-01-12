import matplotlib.pyplot as plt

from .methods import Act, Travos, ITEA
from .scenarios import HostileEnvironment, StartLying, RecruitWitness, FireWitness
from .testbed import Simulation, Scenario
from .util import profiler

Scenario_type = RecruitWitness
epochs = 1
ntcm_type = Act

scenario = Scenario_type(
    consumer_amount=5,
    provider_amount=5,
    provider_options={"chance": 0.7, "l_quality": 0.8, "l_cost": 0.2, "u_cost": 0.5},
    consumer_as_witness=True,
)

simulation = Simulation(scenario, ntcm_type, 50)


profiler.start()
for consumers, providers in simulation.runs(epochs, printing=True):

    profiler.start("single run")
    print()
    print(
        f"Consumer Average: {sum(sum(consumers[_c]) for _c in consumers )/len(consumers):.2f}"
    )
    print(
        f"Provider Average: {sum(sum(providers[_p]) for _p in providers)/len(providers):.2f}"
    )

    profiler.start("main-1")
    consumer_list = {
        _c: [sum(_v[:v]) for v in range(len(_v))] for _c, _v in consumers.items()
    }
    best_consumer = max(consumer_list.keys(), key=lambda c: consumer_list[c][-1])
    profiler.switch("main-1", "main-2")

    producer_list = {
        _p: [sum(_v[:v]) for v in range(len(_v))] for _p, _v in providers.items()
    }
    best_provider = max(producer_list.keys(), key=lambda p: producer_list[p][-1])
    profiler.stop("main-2")

    consumer_label_set = False
    provider_label_set = False

    average_producer = [
        sum(x) / len(producer_list.values()) for x in zip(*producer_list.values())
    ]
    average_consumer = [
        sum(x) / len(consumer_list.values()) for x in zip(*consumer_list.values())
    ]

    plt.plot(average_consumer, "-", lw=4, label="Average Consumer")
    plt.plot(average_producer, ":", lw=4, label="Average Provider")

    for consumer in consumers:
        if best_consumer == consumer:
            plt.plot(consumer_list[consumer], "-b", label="Best Consumer")
        else:
            if not consumer_label_set:
                plt.plot(consumer_list[consumer], "-g", label="Consumer")
                consumer_label_set = True
            else:
                plt.plot(consumer_list[consumer], "-g")

    for provider in providers:
        if best_provider == provider:
            plt.plot(producer_list[provider], ":c", label="Best Provider")
        else:
            if not provider_label_set:
                plt.plot(producer_list[provider], ":r", label="Provider")
                provider_label_set = True
            else:
                plt.plot(producer_list[provider], ":r")

    profiler.stop("single run")
    plt.title("Trust Simulation")
    plt.xlabel("Time step")
    plt.ylabel("Utility")
    plt.legend()
    plt.show()

profiler.stop()

profiler.show()
