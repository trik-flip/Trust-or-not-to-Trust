from __future__ import annotations

import numpy as np
import math
from to_trust import Provider, Consumer, Witness


# Predictions: each row is an advisor's prediction for one provider
# The columns are the predictions for a specific provider
def current_prediction(recommendations, weights):
    weight = np.array(recommendations) * np.array(weights)
    sum_recommendations = sum(weight)
    sum_weights = sum(weights)
    predictions = sum_recommendations / sum_weights
    return predictions


def loss_function(real, predicted):
    return (predicted - real) ** 2


class ITEA(Consumer):

    def __init__(
        self,
        # witnesses: int=0,
        T: float= 100,
        # prov: list[Provider] | None = None,
        learning_rate: float=0.5
    ) -> None:
        super().__init__()
        self.T = T
        self.weights = []

        # self.K = len(witnesses)

    def register_witnesses(self, witnesses: list[Witness]):
        super().register_witnesses(witnesses)
        self.K = len(witnesses)
        self.learning_rate = math.sqrt((8 * math.log(self.K)) / self.T)
        self.weights = np.ones(self.K) / self.K  # first weight = 1/K
        self.weights = [[self.weights[i] for i in range(len(self.weights))] for j in range(len(self.providers))]



    def update_provider(self, p: Provider, score: float) -> None:
        self.prov = []

    def register_providers(self, providers: list[Provider]):
        super().register_providers(providers)
        self.providerss = providers
        self._alphas_p = {p: 1 for p in providers}
        self._betas_p = {p: 1 for p in providers}

    def update(self):
        """    Update the weights etc
                Make the choice
                Must be called after each timestep
        """
        prediction_for_provider = []
        witnesses_recommendations = []
        for provider_index in range(len(self.providerss)):
            witness_recommendations = []
            for witness in self.witnesses:
                witness_recommendations.append(witness.score_of(self.providerss[provider_index]))

            own_prediction = current_prediction(witness_recommendations, self.weights[provider_index])
            witnesses_recommendations.append(witness_recommendations)
            prediction_for_provider.append(own_prediction)

        # Pick the provider with the highest prediction
        highest_provider = np.argmax(prediction_for_provider)

        # Observe the outcome
        provider_outcome = self.providerss[highest_provider].get_service()

        ## Consumer suffers loss - loss from consumers preditions and the real prediciton
        consumer_loss= loss_function(provider_outcome, prediction_for_provider[highest_provider])

        ## Witness suffers loss - loss from value from witness and the real
        # update weight of advisers
        for witness_index in range(len(self.witnesses)):
            witness_loss = loss_function(provider_outcome, witnesses_recommendations[highest_provider][witness_index])
            self.weights[highest_provider][witness_index] = self.weights[witness_index][highest_provider]*math.exp(-self.learning_rate*witness_loss)
