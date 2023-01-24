from __future__ import annotations

import random

import numpy as np
import math
from to_trust import Provider, Consumer, Witness

from util import profiler
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

    # TODO: The trustworthiness value of each individual provider is sampled uniformly at
    #  random from the values 0.1, 0.2, . . . , 0.9; each reported result is the average
    #  over 100 such sampled trustee combinations.

    @staticmethod
    def preprocess(witnesses, providers, epochs=30000, threshold=.5):
        for w in witnesses:
            w.good_interactions = {p: 0 for p in providers}
            w.bad_interactions = {p: 0 for p in providers}

        for i in range(epochs):
            w = choice(list(witnesses))
            p = choice(list(providers))
            if p.get_service() >= threshold:
                w.good_interactions[p] += 1
            else:
                w.bad_interactions[p] += 1
        for w in witnesses:
            for p in providers:
                w.scores[p] = (w.good_interactions[p] + 1) / (w.good_interactions[p] + w.bad_interactions[p] + 2)

    def __init__(
            self,
            T: float = 100,
            threshold=0
    ) -> None:
        super().__init__()
        self.bad_interactions = None
        self.good_interactions = None
        self.learning_rate = None
        self.interactions = None
        self.K = None
        self.T = T
        self.weights = []
        self.loss = []
        self.threshold = threshold

    def register_witnesses(self, witnesses: list[Witness]):
        super().register_witnesses(witnesses)

        self.K = len(witnesses)
        self.learning_rate = math.sqrt((8 * math.log(self.K)) / self.T)
        self.weights = {}
        for provider in self.providers:
            self.weights[provider] = {w: 1 / self.K for w in self.witnesses}

    def update_provider(self, p: Provider, score: float) -> None:
        self.interactions[p] = score
        if score > self.threshold:
            self.good_interactions[p] += 1
        else:
            self.bad_interactions[p] += 1

    def register_providers(self, providers: list[Provider]):
        super().register_providers(providers)
        self.interactions = {p: 0 for p in providers}
        self.good_interactions = {p: 0 for p in providers}
        self.bad_interactions = {p: 0 for p in providers}
        self.absolute_difference = {p: 0 for p in providers}

    @profiler.profile
    def choose_provider(self):
        """
            Make the choice
            Update the weights
        """
        predictions_for_providers = dict()
        witnesses_recommendations = dict()

        for p in self.providers.keys():
            witness_recommendations = dict()
            for witness in self.witnesses:
                witness_recommendations[witness] = witness.score_of(p)
            own_prediction = current_prediction(witness_recommendations.values(), self.weights[p].values())
            witnesses_recommendations[p] = witness_recommendations
            predictions_for_providers[p] = own_prediction

        # Get the value of the highest prediction
        max_prediction = max(predictions_for_providers.values())

        # If more than 1 candidate -> choose 1 at random
        max_providers = [k for k, v in predictions_for_providers.items() if v == max_prediction]
        highest_provider = random.choice(max_providers)

        # Observe the outcome
        highest_provider_actual = self.interactions[highest_provider]
        self.loss.append(loss_function(highest_provider_actual, max_prediction))

        # Store the absolute difference between the actual and the estimated values
        self.absolute_difference[p] = self.absolute_difference[p] + abs(max_prediction-highest_provider_actual)

        for witness in self.witnesses:
            witness_loss = loss_function(highest_provider_actual, witnesses_recommendations[highest_provider][witness])
            # Update weights for the witness
            exp = -self.learning_rate * witness_loss
            self.weights[highest_provider][witness] = self.weights[highest_provider][witness] * math.exp(exp)

        return highest_provider

    def update(self):
        super().update()

