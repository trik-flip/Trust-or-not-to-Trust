import unittest
from random import seed

import matplotlib.pyplot as plt
import numpy as np

from to_trust.methods import ITEA, Act, Travos  # , MET
from to_trust.scenarios import HostileEnvironment, StartLying
from to_trust.testbed import Simulation


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
        sim = Simulation(scenario, Act, 200)
        _con_scores, _pro_scores = sim.run()

        result_con = [sum(_con_scores[c]) for c in _con_scores]
        expected_con = [
            67.00252496554533,
            63.9234021760778,
            66.97055283491797,
            63.41475978623277,
            63.2963817690425,
        ]
        result_pro = [sum(_pro_scores[p]) for p in _pro_scores]
        expected_pro = [
            66.5475343240777,
            48.87319421642739,
            31.07193050838494,
            64.9156465431839,
            69.98543706033685,
        ]

        self.assertEqual(result_con, expected_con)
        self.assertEqual(result_pro, expected_pro)

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
        sim = Simulation(scenario, Act, 200)
        _con_scores, _pro_scores = sim.run()

        result_con = [sum(_con_scores[c]) for c in _con_scores]
        expected_con = [
            67.00252496554533,
            63.9234021760778,
            66.97055283491797,
            63.41475978623277,
            63.2963817690425,
        ]

        result_pro = [sum(_pro_scores[p]) for p in _pro_scores]
        expected_pro = [
            66.5475343240777,
            48.87319421642739,
            31.07193050838494,
            64.9156465431839,
            69.98543706033685,
        ]
        self.assertEqual(result_con, expected_con)
        self.assertEqual(result_pro, expected_pro)

    def test_Hostile_with_Travos(self):
        scenario = HostileEnvironment(
            witness_amount=5,
            consumer_amount=1,
            provider_amount=20,
            provider_options={
                "chance": 1,
                "cost": 0,
            },
            simple_lying=True,
        )
        sim = Simulation(scenario, Travos, 50)
        _con_scores, _pro_scores = sim.run()
        result_con = [sum(_con_scores[c]) for c in _con_scores]
        expected_con = [15.285075700775115]

        result_pro = [sum(_pro_scores[p]) for p in _pro_scores]
        expected_pro = [
            31.97133992289417,
            1.250537761133348,
            13.751465918455972,
            11.160536907441129,
            36.823560708200624,
            33.83497437114558,
            44.60897838524222,
            4.346941631470804,
            21.09609098426351,
            1.4898609719035156,
            10.931898740180156,
            25.267764405168144,
            1.3267984841931812,
            9.941882534332432,
            32.494221888976156,
            27.247074030160853,
            11.022031102034822,
            29.463284193795413,
            40.47152283389131,
            0.32493798390305084,
        ]
        self.assertEqual(result_con, expected_con)
        self.assertEqual(result_pro, expected_pro)

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


if __name__ == "__main__":
    unittest.main()
