from api.daemons.policies.planification_policy import PlanificationPolicy


class SharedPolicy(PlanificationPolicy):
    '''

    '''

    def __init__(self, policy: PlanificationPolicy):
        '''

        '''
        super().__init__(policy.schedulers)

    def apply(self):
        '''

        '''
        pass
