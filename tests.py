import unittest
from random import seed


from to_trust.methods import ITEA, Act, Travos  # , MET
from to_trust.scenarios import HostileEnvironment, StartLying, RecruitWitness, Simple
from to_trust.testbed import Simulation, Scenario
from to_trust.agents import Consumer, Provider, Witness, RandomWitness


class TestingTravos(unittest.TestCase):
    def setUp(self) -> None:
        seed(42)
        return super().setUp()

    def test_Hostile_Env(self):
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


class TestingACT(unittest.TestCase):
    def setUp(self) -> None:
        seed(42)
        scenario_settings = {
            "witness_amount": 5,
            "consumer_amount": 5,
            "provider_amount": 5,
            "provider_options": {
                "chance": 0.7,
                "l_quality": 0.8,
                "l_cost": 0.3,
                "u_cost": 0.6,
            },
        }

        def sim_create(scenario: Scenario):
            return Simulation(scenario(**scenario_settings), Act, 200)  # type: ignore

        self.sim = sim_create
        return super().setUp()

    def test_Lying_Env(self):
        _con_scores, _pro_scores = self.sim(StartLying).run()  # type: ignore

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

    def test_Hostile_Env(self):
        _con_scores, _pro_scores = self.sim(HostileEnvironment).run()  # type: ignore

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

    def test_RecruitWitness(self):
        _con_scores, _pro_scores = self.sim(RecruitWitness).run()  # type: ignore
        result_con = [sum(_con_scores[c]) for c in _con_scores]
        expected_con = [
            52.977242743727224,
            52.977242743727224,
            74.11937230269591,
            75.37115951090811,
            60.362004465197344,
        ]
        result_pro = [sum(_pro_scores[p]) for p in _pro_scores]
        expected_pro = [
            61.90810752561976,
            45.4531707617321,
            33.91381323688335,
            75.67844159213465,
            55.8352872373441,
        ]

        self.assertEqual(result_con, expected_con)
        self.assertEqual(result_pro, expected_pro)

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
        assert False

    def test_ITEA_MAE(self):
        """
            - Interaction with a trustee: either positive or negative
            - Each provider has a constant trustworthiness value in [0, 1] = probability of a positive outcome when interacting with that trustee
            - TODO Trustworthiness value of each provider sampled uniformly at random from the values 0.1, 0.2, . . . , 0.9 -> not scenario?
            - 1 consumer, 10 providers, 100 witnesses
            - Result = average over 100 sampled provider combinations


        Mean actual difference between the real and estimated value
        Mean taken over all pairs of truster and trustee
        Need from ITEA as result -> the actual and estimated


        Number of witnesses = 100
        Percentages of unreliable advisers (40%, 70%, 90%)
        """

        # Calculate the squared error loss
        ntcm = ITEA
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
        witnesses = []
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

