from random import seed
import unittest

import matplotlib.pyplot as plt

from .scenarios.start_lying import StartLying

from .scenarios import HostileEnvironment
from .methods import Act, Travos
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
            witness_amount=20,
            consumer_amount=1,
            provider_amount=101,
            provider_options={
                "chance": 1,
                "cost": 0,
            },
            simple_lying=True
        )
        ntcm = Travos
        sim = Simulation(scenario, ntcm, 200)

        try:
            _con_scores, _pro_scores = sim.run(True)
        except KeyboardInterrupt:
            plt.plot(sim.consumers[0].avg_estimation_errors)
            plt.ylabel("mean estimation error")
            plt.xlabel("num. interactions")
            plt.savefig("hostile_travos.png")
