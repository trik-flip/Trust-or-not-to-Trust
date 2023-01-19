from random import seed
import unittest
import numpy as np

import matplotlib.pyplot as plt

from .scenarios.start_lying import StartLying

from .scenarios import HostileEnvironment
from .methods import Act, Travos, ITEA
from .testbed import Simulation


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        seed(42)
        return super().setUp()

    def test_Hostile_with_Act(self):
        scenario = HostileEnvironment(
            witness_amount=5,
            consumer_amount=5,
            provider_amount=5,
            provider_options={
                "chance": 0.7,
                "l_quality": 0.8,
                "l_cost": 0.3,
                "u_cost": 0.6,
            },
        )
        ntcm = Act
        sim = Simulation(scenario, ntcm, 1000)
        _con_scores, _pro_scores = sim.run()
        expected_con = [
            341.8534185781679,
            348.2561506412619,
            337.9225564913868,
            317.01997935373436,
            316.8465968723288,
        ]
        expected_pro = [
            350.36749345452847,
            224.70083621763737,
            172.410948912913,
            344.1469509867396,
            318.08934819994727,
        ]
        self.assertEqual(list(_con_scores), expected_con)
        self.assertEqual(list(_pro_scores), expected_pro)

    def test_Lying_with_Act(self):
        scenario = StartLying(
            witness_amount=5,
            consumer_amount=5,
            provider_amount=5,
            provider_options={
                "chance": 0.7,
                "l_quality": 0.8,
                "l_cost": 0.3,
                "u_cost": 0.6,
            },
        )
        ntcm = Act
        sim = Simulation(scenario, ntcm, 1000)
        _con_scores, _pro_scores = sim.run()
        expected_con = [
            341.8534185781679,
            348.2561506412619,
            337.9225564913868,
            317.01997935373436,
            316.8465968723288,
        ]
        expected_pro = [
            350.36749345452847,
            224.70083621763737,
            172.410948912913,
            344.1469509867396,
            318.08934819994727,
        ]
        self.assertEqual(list(_con_scores), expected_con)
        self.assertEqual(list(_pro_scores), expected_pro)

    def test_Hostile_with_Travos(self):
        scenario = HostileEnvironment(
            witness_amount=5,
            consumer_amount=1,
            provider_amount=5,
            provider_options={
                "chance": 0.7,
                "l_quality": 0.8,
                "l_cost": 0.3,
                "u_cost": 0.6,
            },
        )
        ntcm = Travos
        sim = Simulation(scenario, ntcm, 200)
        _con_scores, _pro_scores = sim.run()

        plt.plot(sim.consumers[0].avg_estimation_errors)
        plt.show()

    def test_startLyingITEA(self):
        scenario = StartLying(
            witness_amount=5,
            honest_epochs=5,
            consumer_amount=1,
            provider_amount=7,
            provider_options={
                "chance": 0.7,
                "l_quality": 0.8,
                "l_cost": 0.3,
                "u_cost": 0.6,
            },
        )
        ntcm = ITEA
        sim = Simulation(scenario, ntcm, 10)
        # ntcm.preprocessing(self)
        _con_scores, _pro_score = sim.run()
        l = []

    def test_ITEA_RFU(self):
        """
            Interaction with a trustee: either positive or negative
            Fraction of the number of negative interactions over the total number of interactions
            Number of witnesses = 100
            Percentages of unreliable advisers (40%, 70%, 90%)
        """
        test = []

    def test_ITEA_MAE(self):
        """
            - Interaction with a trustee: either positive or negative
            - Each provider has a constant trustworthiness value in [0, 1] = probability of a positive outcome when interacting with that trustee
            - Trustworthiness value of each provider sampled uniformly at random from the values 0.1, 0.2, . . . , 0.9
            - 1 consumer, 10 providers, 100 witnesses
            - Result = average over 100 sampled provider combinations

            - Pre-processing??? witnesses interact with the trustees to establish direct trust information
                                300 000 interactions -  1 witness randomly chosen from the 100
                                                        1 provider randomly chosen from the 10
                                each witness records for each provider the number of + and - interactions
                                witnesses compute direct trust using Beta Reputation System

                                for a provider: b(p, n) = (p+1)/(p+n+2)
                                Honest advisor: provides b(p, n) for the provider
            -

            Mean actual difference between the real and estimated value
            Mean taken over all pairs of truster and trustee

            Need from ITEA as result -> the actual and estimated


            Number of witnesses = 100
            Percentages of unreliable advisers (40%, 70%, 90%)
        """

        # Calculate the squared error loss
        ntcm = ITEA()
        scenario = StartLying(
            witness_amount=5,
            honest_epochs=5,
            consumer_amount=1,
            provider_amount=7,
            provider_options={
                "chance": 0.7,
                "l_quality": 0.8,
                "l_cost": 0.3,
                "u_cost": 0.6,
            },
        )
        sim = Simulation(scenario, ntcm, 10)
        _con_scores, _pro_score = sim.run()
        ntcm.preprocessing()

