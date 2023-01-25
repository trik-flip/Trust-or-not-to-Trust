import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from to_trust.settings import scenarios

scenario_name_mapping = {
    "collusive_witness_recruited": "Collusive ring\nRecruiting witnesses",
    "collusive_witness_fired": "Collusive ring\nFiring witnesses",
    "collusive_provider_recruited": "Collusive ring\nRecruiting providers",
    "collusive_provider_fired": "Collusive ring\nFiring providers",
    "bs_bm_hostile_20": "Hostile environment\n20% Lying",
    "bs_bm_hostile_40": "Hostile environment\n40% Lying",
    "bs_bm_hostile_80": "Hostile environment\n80% Lying",
    "stop_lying": "Witnesses stop lying after 10 epochs",
    "start_lying": "Witnesses start lying after 10 epochs"
}

if __name__ == '__main__':
    consumer_utility_files = {}
    provider_utility_files = {}
    consumer_mae_files = {}

    for scenario_name in scenarios.keys():
        consumer_utility_files[scenario_name] = []
        consumer_mae_files[scenario_name] = []
        provider_utility_files[scenario_name] = []

    for file_name in os.listdir('.'):
        for scenario_name in scenarios.keys():
            if file_name.endswith(scenario_name + "_consumer_utility_data.csv"):
                consumer_utility_files[scenario_name].append(file_name)
            elif file_name.endswith(scenario_name + "_provider_utility_data.csv"):
                provider_utility_files[scenario_name].append(file_name)
            elif file_name.endswith(scenario_name + "_consumer_mae_data.csv"):
                consumer_mae_files[scenario_name].append(file_name)

    consumer_utility_data = {}
    for scenario_name, consumer_utility_file_names in consumer_utility_files.items():
        consumer_utility_data[scenario_name] = []
        for file_name in consumer_utility_file_names:
            consumer_utility_dataframe = pd.read_csv(file_name, index_col=0)
            consumer_utility_dataframe = consumer_utility_dataframe.groupby('simulation_run_index').mean().cumsum()
            consumer_utility_dataframe.drop(['overall_run_index', 'consumer_index'], axis=1, inplace=True)
            consumer_utility_dataframe['Method'] = file_name.split('_')[0]
            consumer_utility_dataframe['num. interactions'] = consumer_utility_dataframe.index
            consumer_utility_data[scenario_name].append(consumer_utility_dataframe)
        consumer_utility_data[scenario_name] = pd.concat(consumer_utility_data[scenario_name], ignore_index=True)

    consumer_mae_data = {}
    for scenario_name, consumer_mae_file_names in consumer_mae_files.items():
        consumer_mae_data[scenario_name] = []
        for file_name in consumer_mae_file_names:
            consumer_mae_dataframe = pd.read_csv(file_name, index_col=0)
            consumer_mae_dataframe = consumer_mae_dataframe.groupby('simulation_run_index').mean()
            consumer_mae_dataframe.drop(['overall_run_index', 'consumer_index'], axis=1, inplace=True)
            consumer_mae_dataframe['Method'] = file_name.split('_')[0]
            consumer_mae_dataframe['num. interactions'] = consumer_mae_dataframe.index
            consumer_mae_data[scenario_name].append(consumer_mae_dataframe)
        consumer_mae_data[scenario_name] = pd.concat(consumer_mae_data[scenario_name], ignore_index=True)

    hue_order = list(consumer_utility_data.values())[0]['Method'].unique().tolist()
    for scenario_name in scenarios:
        plt.xlim((0, consumer_utility_data[scenario_name]['num. interactions'].max()))
        plt.title(scenario_name_mapping[scenario_name])
        sns.lineplot(data=consumer_utility_data[scenario_name], x='num. interactions', y='utility',
                             hue='Method', hue_order=hue_order)
        plt.savefig("average_utility_" + scenario_name + ".png")
        plt.clf()

        plt.xlim((0, consumer_utility_data[scenario_name]['num. interactions'].max()))
        plt.title(scenario_name_mapping[scenario_name])
        sns.lineplot(data=consumer_mae_data[scenario_name], x='num. interactions', y='mae',
                             hue='Method', hue_order=hue_order)
        plt.ylabel("mean estimation error")
        plt.savefig("mae_" + scenario_name + ".png")
        plt.clf()
