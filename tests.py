from random import seed
import unittest

import matplotlib.pyplot as plt

from to_trust.scenarios import HostileEnvironment, StartLying
from to_trust.methods import Act, Travos
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
                63.2963817690425
                ]
        result_pro = [sum(_pro_scores[p]) for p in _pro_scores]
        expected_pro = [
                66.5475343240777,
                48.87319421642739,
                31.07193050838494,
                64.9156465431839,
                69.98543706033685
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
        expected_con=[
                67.00252496554533,
                63.9234021760778,
                66.97055283491797,
                63.41475978623277,
                63.2963817690425
                ]

        result_pro = [sum(_pro_scores[p]) for p in _pro_scores]
        expected_pro=[
                66.5475343240777,
                48.87319421642739,
                31.07193050838494,
                64.9156465431839,
                69.98543706033685
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
                simple_lying=True
                )
        sim = Simulation(scenario, Travos, 50)
        _con_scores, _pro_scores = sim.run()
        result_con = [sum(_con_scores[c]) for c in _con_scores]
        expected_con=[
                15.285075700775115
                ]

        result_pro = [sum(_pro_scores[p]) for p in _pro_scores]
        expected_pro=[
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
                0.32493798390305084
                ]
        self.assertEqual(result_con, expected_con)
        self.assertEqual(result_pro, expected_pro)



if __name__ == "__main__":
    unittest.main()

