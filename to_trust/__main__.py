import matplotlib.pyplot as plt
import pandas as pd
from to_trust.util import profiler

from to_trust.methods import ITEA, MET, Act, Travos
from to_trust.metrics import MetricSystem
from to_trust.settings import (
    epochs,
    line_alpha,
    ntcm_type,
    plot_average,
    plot_run,
    runs,
    scenarios,
)
from to_trust.testbed.simulation import Simulation


def name_of(ntcm):
    if ntcm is Travos:
        return "Travos"
    elif ntcm is Act:
        return "ACT-RL"
    elif ntcm is ITEA:
        return "ITEA"
    elif ntcm is MET:
        return "MET"
    else:
        raise Exception("Method doesn't exist")


if __name__ == "__main__":
    sensor = MetricSystem()
    profiler.start()
    print(f"Running {name_of(ntcm_type)}")

    consumer_utility_data = pd.DataFrame(
        [],
        columns=[
            "overall_run_index",
            "simulation_run_index",
            "consumer_index",
            "utility",
        ],
    )
    provider_utility_data = pd.DataFrame(
        [],
        columns=[
            "overall_run_index",
            "simulation_run_index",
            "provider_index",
            "utility",
        ],
    )

    consumer_mae_data = pd.DataFrame(
        [],
        columns=["overall_run_index", "simulation_run_index", "consumer_index", "mae"],
    )
    for s in scenarios:
        simulation = Simulation(scenarios[s], ntcm_type, runs)

        for overall_run_index, (consumers, providers) in enumerate(
            simulation.runs(epochs, printing=True)
        ):
            sensor.measure(consumers, providers, runs)
            profiler.start("single run")

            # collect data for export
            consumer_utility_data_one_run = (
                pd.DataFrame(consumers.values())
                .stack()
                .reset_index()
                .rename(
                    columns={
                        "level_0": "consumer_index",
                        "level_1": "simulation_run_index",
                        0: "utility",
                    }
                )
            )
            consumer_utility_data_one_run["overall_run_index"] = overall_run_index
            consumer_utility_data = pd.concat(
                [consumer_utility_data, consumer_utility_data_one_run],
                ignore_index=True,
            )

            provider_utility_data_one_run = (
                pd.DataFrame(providers.values())
                .stack()
                .reset_index()
                .rename(
                    columns={
                        "level_0": "provider_index",
                        "level_1": "simulation_run_index",
                        0: "utility",
                    }
                )
            )
            provider_utility_data_one_run["overall_run_index"] = overall_run_index
            provider_utility_data = pd.concat(
                [provider_utility_data, provider_utility_data_one_run],
                ignore_index=True,
            )

            print()
            print(f"Consumer Average: {sensor.average(consumers):.2f}")
            print(f"Provider Average: {sensor.average(providers):.2f}")

            consumer_list = {
                _c: [sum(_v[:v]) for v in range(len(_v))]
                for _c, _v in consumers.items()
            }  # get the compounded list per consumer which contains the values
            best_consumer = max(
                consumer_list.keys(), key=lambda c: consumer_list[c][-1]
            )

            provider_list = {
                _p: [sum(_v[:v]) for v in range(len(_v))]
                for _p, _v in providers.items()
            }  # Same but then for the providers
            best_provider = max(
                provider_list.keys(), key=lambda p: provider_list[p][-1]
            )

            consumer_label_set = False
            provider_label_set = False

            average_provider = [
                sum(x) / len(provider_list.values())
                for x in zip(*provider_list.values())
            ]
            average_consumer = [
                sum(x) / len(consumer_list.values())
                for x in zip(*consumer_list.values())
            ]

            if plot_average:
                plt.plot(average_consumer, "-", lw=4, label="Average Consumer")
                plt.plot(average_provider, ":", lw=4, label="Average Provider")

            for consumer in consumers:
                if best_consumer == consumer:
                    plt.plot(consumer_list[consumer], "-b", label="Best Consumer")
                else:
                    if not consumer_label_set:
                        plt.plot(
                            consumer_list[consumer],
                            "-g",
                            label="Consumer",
                            alpha=line_alpha,
                        )
                        consumer_label_set = True
                    else:
                        plt.plot(consumer_list[consumer], "-g", alpha=line_alpha)

            for provider in providers:
                if best_provider == provider:
                    plt.plot(provider_list[provider], ":c", label="Best Provider")
                else:
                    if not provider_label_set:
                        plt.plot(
                            provider_list[provider],
                            ":r",
                            label="Provider",
                            alpha=line_alpha,
                        )
                        provider_label_set = True
                    else:
                        plt.plot(provider_list[provider], ":r", alpha=line_alpha)

            profiler.stop("single run")
            plt.title(f"Trust Simulation - {s} - {name_of(ntcm_type)}")
            plt.xlabel("Time step")
            plt.ylabel("Accumulated Utility")
            plt.legend()
            if plot_run:
                plt.show()

            consumer_mae_data_one_run = []
            for c in consumers:
                plt.plot(c.MAE)
                consumer_mae_data_one_run.append(c.MAE)
            if plot_run:
                plt.show()

            # collect data for export
            consumer_mae_data_one_run = (
                pd.DataFrame(consumer_mae_data_one_run)
                .stack()
                .reset_index()
                .rename(
                    columns={
                        "level_0": "consumer_index",
                        "level_1": "simulation_run_index",
                        0: "mae",
                    }
                )
            )
            consumer_mae_data_one_run["overall_run_index"] = overall_run_index
            consumer_mae_data = pd.concat(
                [consumer_mae_data, consumer_mae_data_one_run], ignore_index=True
            )
        name = name_of(ntcm_type)
        consumer_utility_data.to_csv(name + "_" + s + "_consumer_utility_data.csv")
        provider_utility_data.to_csv(name + "_" + s + "_provider_utility_data.csv")
        consumer_mae_data.to_csv(name + "_" + s + "_consumer_mae_data.csv")

    profiler.stop()
    profiler.show()
