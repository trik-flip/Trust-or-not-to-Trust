import matplotlib.pyplot as plt

from .metrics import MetricSystem
from .settings import epochs, line_alpha, plot_average, runs, simulation, plot_run
from .util import profiler

if __name__ == '__main__':
    sensor = MetricSystem()
    profiler.start()

    for consumers, providers in simulation.runs(epochs, printing=True):
        sensor.measure(consumers, providers, runs)
        profiler.start("single run")
        print()
        print(f"Consumer Average: {sensor.average(consumers):.2f}")
        print(f"Provider Average: {sensor.average(providers):.2f}")

        consumer_list = {
            _c: [sum(_v[:v]) for v in range(len(_v))] for _c, _v in consumers.items()
        }  # get the compounded list per consumer which contains the values
        best_consumer = max(consumer_list.keys(), key=lambda c: consumer_list[c][-1])

        producer_list = {
            _p: [sum(_v[:v]) for v in range(len(_v))] for _p, _v in providers.items()
        }  # Same but then for the providers
        best_provider = max(producer_list.keys(), key=lambda p: producer_list[p][-1])

        consumer_label_set = False
        provider_label_set = False

        average_producer = [
            sum(x) / len(producer_list.values()) for x in zip(*producer_list.values())
        ]
        average_consumer = [
            sum(x) / len(consumer_list.values()) for x in zip(*consumer_list.values())
        ]

        if plot_average:
            plt.plot(average_consumer, "-", lw=4, label="Average Consumer")
            plt.plot(average_producer, ":", lw=4, label="Average Provider")

        for consumer in consumers:
            if best_consumer == consumer:
                plt.plot(consumer_list[consumer], "-b", label="Best Consumer")
            else:
                if not consumer_label_set:
                    plt.plot(
                        consumer_list[consumer], "-g", label="Consumer", alpha=line_alpha
                    )
                    consumer_label_set = True
                else:
                    plt.plot(consumer_list[consumer], "-g", alpha=line_alpha)

        for provider in providers:
            if best_provider == provider:
                plt.plot(producer_list[provider], ":c", label="Best Provider")
            else:
                if not provider_label_set:
                    plt.plot(
                        producer_list[provider], ":r", label="Provider", alpha=line_alpha
                    )
                    provider_label_set = True
                else:
                    plt.plot(producer_list[provider], ":r", alpha=line_alpha)

        profiler.stop("single run")
        plt.title("Trust Simulation")
        plt.xlabel("Time step")
        plt.ylabel("Accumulated Utility")
        plt.legend()
        if plot_run:
            plt.show()

        for c in consumers:
            plt.plot(c.MAE)
        if plot_run:
            plt.show()

    profiler.stop()
    profiler.show()
