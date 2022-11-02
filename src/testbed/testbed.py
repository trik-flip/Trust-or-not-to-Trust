class Simulation:
    witnesses: [Witness]
    consumer: NTCM 
    providers: [Provider]

    total_steps = 100

    def __init__(self,scenario:Scenario,ntcm:NTCM, total_steps = 100):
        if scenario is None or ntcm is None:
            raise Exception("scenario and ntcm must be implemented")

        self.consumer = ntcm
        self.witnesses = scenario.get_witnesses()
        self.providers = scenario.get_providers()
        self.total_steps = total_steps
    
    def run(self):
        total_score = 0
        for step in self.total_steps:

            chosen_provider = self.consumer.choose_provider(self.providers, self.witnesses) 

            score = chosen_provider.get_service()
            total_score += score



            for consumer in consumers:
                consumer.update()
            for witness in witnesses:
                witness.update()
            for provider in providers:
                provider.update()

        return total_score
