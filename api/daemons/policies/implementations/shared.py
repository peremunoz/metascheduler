from typing import List
from api.daemons.policies.planification_policy import PlanificationPolicy
from api.interfaces.job import Job


class SharedPolicy(PlanificationPolicy):
    '''

    '''

    def __init__(self, policy: PlanificationPolicy):
        '''

        '''
        super().__init__(policy.schedulers, policy.highest_priority)

    def apply(self, to_be_queued_jobs: List[Job]):
        '''

        '''
