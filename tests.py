from random import seed
import unittest
import numpy as np

import matplotlib.pyplot as plt

from to_trust.scenarios import HostileEnvironment, StartLying, RecruitWitness, Simple
from to_trust.methods import Act, Travos, ITEA
from to_trust.testbed import Simulation
from to_trust.agents import Consumer, Provider, Witness, RandomWitness


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
        sim = Simulation(scenario, Act, 1000)
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
        sim = Simulation(scenario, Act, 1000)
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
        sim = Simulation(scenario, Travos, 200)

        try:
            _con_scores, _pro_scores = sim.run(True)
        except KeyboardInterrupt:
            plt.plot(sim.consumers[0].avg_estimation_errors)
            plt.ylabel("mean estimation error")
            plt.xlabel("num. interactions")
            plt.savefig("hostile_travos.png")
            plt.plot(sim.consumers[0].avg_estimation_errors)
            plt.show()

    # if __name__ == "__main__":
    #     unittest.main()

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
        _con_scores, _pro_score = sim.run()

    def test_ITEA_RFU(self):
        """
            Interaction with a trustee: either positive or negative
            Fraction of the number of negative interactions over the total number of interactions
            Number of witnesses = 100
            Percentages of unreliable advisers (40%, 70%, 90%)

            T = target number of positive interactions
        """
        test = []

    def test_ITEA_MAE(self):
        """
            - Interaction with a trustee: either positive or negative
            - Each provider has a constant trustworthiness value in [0, 1] = probability of a positive outcome when interacting with that trustee
            - TODO Trustworthiness value of each provider sampled uniformly at random from the values 0.1, 0.2, . . . , 0.9 -> not scenario?
            - 1 consumer, 10 providers, 100 witnesses
            - Result = average over 100 sampled provider combinations


            Mean actual difference between the real and estimated value
            Mean taken over all pairs of truster and trustee

            Number of witnesses = 100
            Percentages of unreliable advisers (40%, 70%, 90%)

            Ignore direct trust
            Each round:     1. Interrogates a witness ->  compute indirect trust for each trustee
                            2. Highest indirect trust provider is chosen
                            3. Get the real outcome of interaction -> update direct trust information
                                p increments if positive, n increments if negative interaction

            For MAE: T=number of rounds=number of interactions so far(?)

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

    def test_ITEA_partly_random_advisors(self):
        """
            Partly random advisor:  picks provider for which provide random recommendations for all interactions
                                    randomly selects z, computes  a pair for which brs(p, n)=z
            Each provider has 0.5 chance of being picked
            For other not chosen providers - the advisor will be honest
            Percentage of unreliable advisors: 40%, 70%, 90%
            Chosen at random
        """
        ntcm = ITEA
        witness_amount = 100
        witnesses: list[Witness] = []
        percentage_unreliable_witnesses = [0.4, 0.7, 0.9]
        for unreliable_witnesses in percentage_unreliable_witnesses:
            witnesses_to_lie = round(witness_amount * unreliable_witnesses)

            for _ in range(witnesses_to_lie):
                witnesses.append(RandomWitness(partially_random=True))
            for _ in range(witness_amount - witnesses_to_lie):
                witnesses.append(Witness(honesty=1))

            providers = []
            for i in range(10):
                providers.append(Provider(
                    chance=0.5,
                    l_quality=0,
                    u_quality=1))

            scenario = Simple(
                witnesses=witnesses,
                providers=providers,
                consumer_amount=1,
            )
            sim = Simulation(scenario, ntcm, 50)
            _con_scores, _pro_scores = sim.run()
            print("Con")
            print(_con_scores)
            print("Pro")
            print(_pro_scores)

    def test_ITEA_BM(self):
        """
            - Picks providers for which will always provide distorted recommendations
            - Each provider has 50% chance of being picked - The trustworthiness value of each individual provider is sampled uniformly at random from the values 0.1, 0.2, . . . , 0.9;
            - Those not picked - witness will be honest
            - Distorted recommendation: (p, n) from pre-processing -> always returns lowest (BM) or highest (BS)

            Percentage of unreliable advisors: 40%, 70%, 90%
            Chosen at random
        """
        ntcm = ITEA()

        witness_amount = 100
        witnesses: list[Witness] = []
        percentage_unreliable_witnesses = [0.4, 0.7, 0.9]
        for unreliable_witnesses in percentage_unreliable_witnesses:
            witnesses_to_lie = round(witness_amount * unreliable_witnesses)

            for _ in range(witnesses_to_lie):
                witnesses.append(Witness(bad_mouthing=True))
            for _ in range(witness_amount - witnesses_to_lie):
                witnesses.append(Witness(honesty=1))

            providers = []
            for i in range(10):
                providers.append(Provider(
                    chance=0.5,
                    l_quality=0,
                    u_quality=1))

            scenario = RecruitWitness(
                witnesses=witnesses,
                witness_amount=witness_amount,
                witness_options={
                    'bad_mouthing': True
                },
                providers=providers,
                consumer_amount=1,
                ring_size=100,
                witness_percentage_of_ring=unreliable_witnesses
            )
            sim = Simulation(scenario, ntcm, 50)
            _con_scores, _pro_scores = sim.run()

    def test_ITEA_BS(self):
        """
            - Picks providers for which will always provide distorted recommendations
            - Each provider has 50% chance of being picked - The trustworthiness value of each individual provider is sampled uniformly at random from the values 0.1, 0.2, . . . , 0.9;
            - Those not picked - witness will be honest
            - Distorted recommendation: (p, n) from pre-processing -> always returns lowest (BM) or highest (BS)

            Percentage of unreliable advisors: 40%, 70%, 90%
            Chosen at random
        """
        ntcm = ITEA()

        witness_amount = 100
        witnesses: list[Witness] = []
        percentage_unreliable_witnesses = [0.4, 0.7, 0.9]
        for unreliable_witnesses in percentage_unreliable_witnesses:
            witnesses_to_lie = round(witness_amount * unreliable_witnesses)

            for _ in range(witnesses_to_lie):
                witnesses.append(Witness(ballot_stuffing=True))
            for _ in range(witness_amount - witnesses_to_lie):
                witnesses.append(Witness(honesty=1))

            providers = []
            for i in range(10):
                providers.append(Provider(
                    chance=0.5,
                    l_quality=0,
                    u_quality=1))

            scenario = RecruitWitness(
                witnesses=witnesses,
                witness_amount=witness_amount,
                witness_options={
                    'ballot_stuffing': True
                },
                providers=providers,
                consumer_amount=1,
                ring_size=100,
                witness_percentage_of_ring=unreliable_witnesses
            )
            sim = Simulation(scenario, ntcm, 50)
            _con_scores, _pro_scores = sim.run()

    def test_ITEA_additive_BM(self):
        """
            Independently for each provider p An additive BM adviser :
            1) Samples a random number z in [0.8, 1]
            2) Subtracts z from its own direct trust in p to obtain z_star
            3) z_star = brs(p, n) - z
            4) If z_star>0  :   return (p, n) where brs(p, n)=z_star
                  else      :   return (0, p+n) so all interaction with provider are negative
        """

    def test_ITEA_additive_BS(self):
        """
            Independently for each provider p An additive BM adviser :
            1) Samples a random number z in [0.8, 1]
            2) Subtracts z from its own direct trust in p to obtain z_star
            3) z_star = brs(p, n) - z
            4) If z_star<1  :   return (p, n) where brs(p, n)=z_star
                  else      :   return (p+n, 0) so all interaction with provider are positive
        """

    def test_ITEA_all_positive(self):
        """
            Report  p = number of interactions
                    n = 0
            Doesn't take into account actual interactions
        """

    def test_ITEA_all_negative(self):
        """
            Report  p = 0
                    n = number of interactions
            Doesn't take into account actual interactions
        """

    def test_ITEA_fully_random(self):
        """
            Randomly distort the recommendations for all providers
            Randomly selects z in [0, 1], computes  a pair for which brs(p, n)=z
        """
        ntcm = ITEA()
        witness_amount = 100
        percentage_unreliable_witnesses = [0.4, 0.7, 0.9]
        for n_unreliable_witnesses in percentage_unreliable_witnesses:
            unreliable_witnesses = round(witness_amount * n_unreliable_witnesses)
            witnesses = []
            for _ in range(unreliable_witnesses):
                # Create the fully random advisors

                witnesses.append(Witness())
            for _ in range(witness_amount - unreliable_witnesses):
                witnesses.append(Witness(honesty=1))

            scenario = RecruitWitness(
                witnesses=witnesses,
                provider_amount=1,
                consumer_amount=1,
            )
            sim = Simulation(scenario, ntcm, 50)
            _con_scores, _pro_scores = sim.run()

    def test_ITEA_selective_BM(self):
        """
            Selective BM advisor is honest for each trustee with direct trust < 0.5
                Returns (p, n)
            For other
                Returns (0, p+n) as if each interaction was negative

        """

    def test_ITEA_selective_BS(self):
        """
            Selective BS advisor is honest for each trustee with direct trust > 0.5
                Returns (p, n)
            For other
                Returns (p+n, 0) as if each interaction was positive

        """