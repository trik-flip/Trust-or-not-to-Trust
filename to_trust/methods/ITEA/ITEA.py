from __future__ import annotations

import math
import random
from random import choice

import numpy as np

from to_trust.util import profiler
from random import choice

def current_prediction(recommendations, weights):
    recommendations = [r for r in recommendations]
    weights = [weight for weight in weights]
    weighted_sum = sum(np.array(recommendations) * np.array(weights))
    sum_weights = sum(weights)
    predictions = weighted_sum / sum_weights
    return predictions


def loss_function(real, predicted):
    """
    Squared error loss for 2 values
    """
    return (real - predicted) ** 2


def mean_absolute_error(real, predicted):
    """
    For experiments
    """
    return np.mean(np.abs(real - predicted))


def beta_reputation_system():
    """
    for a provider: b(p, n) = (p+1)/(p+n+2)
    """


class ITEA(Consumer):
    @staticmethod
    def preprocess(witnesses, providers, epochs=30000, threshold=0.5):
        for w in witnesses:
            w.good_interactions = {p: 0 for p in providers}
            w.bad_interactions = {p: 0 for p in providers}

        for i in range(epochs):
            w = choice(witnesses)
            p = choice(providers)
            if p.get_service() >= threshold:
                w.good_interactions[p] += 1
            else:
                w.bad_interactions[p] += 1
        for w in witnesses:
            for p in providers:

                w.scores[p] = (w.good_interactions[p] + 1) / (
                    w.good_interactions[p] + w.bad_interactions[p] + 2
                )

    def __init__(
        self,
        T: float = 100,
    ) -> None:
        super().__init__()
        self.learning_rate = None
        self.interactions = None
        self.K = None
        self.T = T
        self.weights = []
        self.loss = []

    def register_witnesses(self, witnesses: list[Witness]):
        super().register_witnesses(witnesses)

        self.K = len(witnesses)
        self.learning_rate = math.sqrt((8 * math.log(self.K)) / self.T)
        self.weights = {}
        for provider in self.providers:
            self.weights[provider] = {w: 1 / self.K for w in self.witnesses}

    def update_provider(self, p: Provider, score: float) -> None:
        self.interactions[p] = score

    def register_providers(self, providers: list[Provider]):
        super().register_providers(providers)
        self.interactions = {p: 0 for p in providers}

    @profiler.profile
    def choose_provider(self):
        predictions_for_providers = dict()
        witnesses_recommendations = dict()

        for p in self.providers.keys():
            witness_recommendations = dict()
            for witness in self.witnesses:
                witness_recommendations[witness] = witness.score_of(p)
            own_prediction = current_prediction(
                witness_recommendations.values(), self.weights[p].values()
            )
            witnesses_recommendations[p] = witness_recommendations
            predictions_for_providers[p] = own_prediction

        # Get the value of the highest prediction
        max_prediction = max(predictions_for_providers.values())

        # If more than 1 candidate -> choose 1 at random
        max_providers = [
            k for k, v in predictions_for_providers.items() if v == max_prediction
        ]
        highest_provider = random.choice(max_providers)

        return highest_provider

    def update(self):
        """
        Update the weights etc
        Make the choice
        Must be called after each timestep
        """
        super().update()
        predictions_for_providers = dict()
        witnesses_recommendations = dict()

        for p in self.providers.keys():
            witness_recommendations = dict()
            for witness in self.witnesses:
                witness_recommendations[witness] = witness.score_of(p)
            own_prediction = current_prediction(
                witness_recommendations.values(), self.weights[p].values()
            )
            witnesses_recommendations[p] = witness_recommendations
            predictions_for_providers[p] = own_prediction

        # Get the value of the highest prediction
        max_prediction = max(predictions_for_providers.values())

        # If more than 1 candidate -> choose 1 at random
        max_providers = [
            k for k, v in predictions_for_providers.items() if v == max_prediction
        ]
        highest_provider = random.choice(max_providers)

        # Observe the outcome
        highest_provider_actual = self.interactions[highest_provider]
        self.loss.append(loss_function(highest_provider_actual, max_prediction))

        for witness in self.witnesses:
            witness_loss = loss_function(
                highest_provider_actual,
                witnesses_recommendations[highest_provider][witness],
            )
            # Update weights for the witness
            exp = -self.learning_rate * witness_loss
            self.weights[highest_provider][witness] = self.weights[highest_provider][
                witness
            ] * math.exp(exp)
