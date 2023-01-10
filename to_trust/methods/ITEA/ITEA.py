from __future__ import annotations

import numpy as np
import math
from to_trust import Provider, Consumer


# Predictions: each row is an advisor's prediction for one provider
# The columns are the predictions for a specific provider
def current_prediction(recommendations, weights):
    weight = round(np.dot(recommendations, weights), 4)
    sum_weights = round(sum(weights), 4)
    predictions = weight / sum_weights
    return predictions


def loss_function(real, predicted):
    return (predicted - real) ** 2


class ITEA(Consumer):
    def __init__(
        self,
        recommendations,
        T,
        prov: list[Provider] | None = None,
    ):
        K = len(recommendations)
        learning_rate = math.sqrt((8 * math.log(K)) / T)
        weights = np.ones_like(recommendations) / K  # first weight = 1/K

        for t in range(1, T + 1):
            # Iterate over each provider
            predictions = np.zeros(recommendations.shape[1])
            for j in range(0, recommendations.shape[1]):
                # Get recommendation for each provider from advisors
                f = recommendations[:, j]
                predictions[j] = current_prediction(f, weights[:, j])

            # Consumer picks provider with the highest prediction
            index = np.argmax(predictions)
            prov[index]

            real_outcome = prov[index].get_service()
            loss_prediction = loss_function(real_outcome, predictions[index])
            loss_advisors = []
            for advisor in range(0, recommendations.shape[0]):
                loss_advisors.append(
                    loss_function(real_outcome, recommendations[advisor])
                )
            # Update weights
            for advisor_i in range(0, recommendations.shape[0]):
                for provider_i in range(0, recommendations.shape[1]):
                    update_weight = weights[advisor_i][provider_i] * math.exp(
                        -learning_rate * loss_advisors[advisor_i][provider_i]
                    )
                    weights[advisor_i][provider_i] = update_weight
