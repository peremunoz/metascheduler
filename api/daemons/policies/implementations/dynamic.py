from api.daemons.policies.planification_policy import PlanificationPolicy


class DynamicPolicy(PlanificationPolicy):
    '''

    '''

    def __init__(self, policy: PlanificationPolicy):
        '''

        '''
        super().__init__(policy.schedulers, policy.highest_priority)

    def apply(self):
        '''

        '''
        pass
