import numpy as np
import math
import random as rand
from to_trust.agents import Witness, Consumer, Provider

class MET(Consumer):
    """
    Some assumptions because paper doesn't cover everything:
    - witnesses keep the same opinion of providers
    - witnesses trust networks remain the same (never update)
    - use mean rating from witnesses and omit discounting factor (not enough information on this)
    """
    def __init__(self,
                num_generations = 10,
                size_network = 5,
                p_local = 0.8,
                cr = 0.6,
                pm = 0.05,
                delta = 0.1,
                eta = 20,
                F = 0.3) -> None:
        super(MET, self).__init__()                                           # according to paper:
        self._num_generations = num_generations                  # 10
        self._size_network = size_network                                # 25
        self._p_local = p_local                                                  # 0.8
        self._eta = eta                                                               #20
        self._F = F                                                                     #3
        self._cr = cr                                                                  # 0.6
        self._pm = pm                                                             #0.05
        self._days = 0
        self._threshold = 0.5
        self._trust_values = {}
        self._consumer_trust_network = {}
        self._rating_history = {}                                                   # { Consumer : { provider : {"mean" : float, "history" : []}}}
        self._avg_absolute_errors = []
        self._trust_network_dict = {}                                            # { Consumer/witness : {witness : trust_val, witness : trust_val, ...}}


    def update(self):
        """
        FIXME: CHECK FOR CONSISTENCY OF DATASTRUCTURES
        """
        super().update()
        self.best_trust_network = self._consumer_trust_network
        self.fitness_score = self.calculate_fitness(self.best_trust_network)

        if rand.uniform(0,1) < self._p_local:
            candidate_witnesses = self.select_advisors(self.best_trust_network)
        else:
            candidate_witnesses = rand.sample(list(self.witnesses), k=3)
        new_trust_network = self.crossover(candidate_witnesses)
        new_trust_network = self.mutation()
        new_fitness_score = self.calculate_fitness(new_trust_network)
        if new_fitness_score < self.fitness_score:
            self._consumer_trust_network = new_trust_network 
            self.fitness_score = new_fitness_score
        
        # calculate mean absolute error per time step
        mae = 0
        for provider in self.providers.keys():
            temp_prov_score = 0
            for witness in self._consumer_trust_network.keys():
                temp_prov_score += witness.score_of(provider)
            absolute_error = abs(provider.get_service() - (temp_prov_score/len(self._consumer_trust_network)))      #TODO: fill in correct stuff (12) ; ask what actual provider reputation is
            mae += absolute_error/ (len(self.witnesses)* self._days)
        self.MAE.append(mae)
        #print(self._avg_absolute_errors)
        

    def register_witnesses(self, witnesses: list[Witness]): #25 witnesses
        super().register_witnesses(witnesses)
        self._trust_values = {w: rand.uniform(0,1) for w in witnesses}
        witness_list1 = rand.sample(witnesses, k=self._size_network)
        for w in witness_list1:
            self._consumer_trust_network[w] = self._trust_values[w]
        leftover1 = list(set(witnesses) - set(witness_list1))
        for w in leftover1:
            self._consumer_trust_network[w] = 0.5
        for witness in witnesses:
            witness_list2 = rand.sample([w for w in witnesses if w != witness], k=self._size_network)
            self._trust_network_dict[witness] = {}
            for w in witness_list2:
                self._trust_network_dict[witness][w] = self._trust_values[w]
            leftover2 = list(set(witnesses) - set(witness_list2))
            for w in leftover2:
                self._trust_network_dict[witness][w] = 0.5
            

    def register_providers(self, providers: list[Provider]):
        super().register_providers(providers)

    def register_rating_history(self):
        for provider in self.providers:
            rand_ratings = [rand.uniform(0,1,5)]
            self._rating_history[provider]["mean"] = np.average(rand_ratings)   # [mean, rating history]
            self._rating_history[provider]["history"] = rand_ratings

    def update_provider(self, p: Provider, score: float) -> None:
        """
        
        """
        for witness in self._consumer_trust_network.keys():
            temp_score = witness.score_of(p) - ((p.get_service() + 1) / 2)
            if temp_score > 0:
                self._consumer_trust_network[witness] = (self._consumer_trust_network[witness] + abs(temp_score)) / 2
            else:
                self._consumer_trust_network[witness] = (self._consumer_trust_network[witness] - abs(temp_score)) / 2
        if p in self._rating_history.keys():
            self._rating_history[p]["history"].append((p.get_service() + 1) / 2)
        else:
            self._rating_history[p] = {}
            self._rating_history[p]["history"] = [(p.get_service() + 1) / 2]
        self._rating_history[p]["mean"] = np.average(self._rating_history[p]["history"])


    def choose_provider(self) -> Provider:
        self._days += 1
        return rand.choice(list(self.providers))

    def select_advisors(self,trust_network):
        """

        """
        diff_trustworthiness = 0
        satisfy_6 = []
        for witness in trust_network.keys():
            union = trust_network.keys() & self._trust_network_dict[witness].keys()
            for w in union:
                diff_trustworthiness += trust_network[w] - self._trust_network_dict[witness][w]
            total_diff_trustworthiness = (1/len(union)) * diff_trustworthiness

            diff_fitness_score = self.calculate_fitness(trust_network) - self.calculate_fitness(self._trust_network_dict[witness])
            if np.dot( (total_diff_trustworthiness - 0.5), (diff_fitness_score-0.5) ) > 0:
                satisfy_6.append(witness)

        return rand.sample(satisfy_6, k=3)

    def calculate_rating_diff(self, trust_network):
        rating_diff = 0
        for provider in self.providers:
            if provider in self._rating_history.keys():
                consumer_rating = self._rating_history[provider]["mean"]
            else:
                consumer_rating = 0.5
            if consumer_rating != 0.5:
                sum_witness_rating = 0
                num_w = 0
                for witness in trust_network:
                    if witness.score_of(provider) != 0.5:
                        num_w += 1
                        sum_witness_rating += witness.score_of(provider)        # supposedly vector multiplication but used for loop over all witnesses
                witness_rating = sum_witness_rating / num_w     #TODO: add discounting operator (3), see above comment
            else:
                witness_rating = 0.5
            rating_diff += consumer_rating - witness_rating
        return num_w, abs(rating_diff)

    def calculate_fitness(self, trust_network):
        m, diff = self.calculate_rating_diff(trust_network)
        return (1/m) * diff

    def crossover(self, selection):
        """

        """
        temp_network_dict = self._consumer_trust_network.copy()
        for witness in self._consumer_trust_network.keys():
            rand_k = rand.uniform(0,1)
            if rand_k <= self._cr:
                temp_network_dict[witness] = self._trust_network_dict[selection[0]][witness] + (self._F * self._trust_network_dict[selection[1]][witness]) - (self._F * self._trust_network_dict[selection[2]][witness])
            else:
                temp_network_dict[witness] = self._consumer_trust_network[witness]
        return temp_network_dict

    def mutation(self):
        """

        """
        r = rand.uniform(0,1)
        rand_k = rand.uniform(0,1)
        temp_network_dict = {}
        if r < 0.5:
            delta = (2 * r) ** (1/ (self._eta + 1) )
        else:
            delta = 1 - (abs(2* ( 1 - r ) ) ** (1 / (self._eta + 1)))

        for witness in self._consumer_trust_network.keys():    
            if rand_k <= self._pm:
                temp_network_dict[witness] = self._consumer_trust_network[witness] + delta
            else:
                temp_network_dict[witness] = self._consumer_trust_network[witness]
        
        return temp_network_dict