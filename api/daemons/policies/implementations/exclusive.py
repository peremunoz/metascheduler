from typing import List
from api.daemons.policies.planification_policy import PlanificationPolicy
from api.interfaces.scheduler import Scheduler


class ExclusivePolicy(PlanificationPolicy):
    ''' The Exclusive Policy is a planification policy that allows only one scheduler
    to run at a time. This policy is useful for running jobs that require exclusive
    access to the resources. This way, the jobs of a specific scheduler will not be
    affected by the jobs of other schedulers.

    The Exclusive Policy is a subclass of the PlaniicationPolicy class and implements
    the apply method. The apply method is responsible for applying the policy to the
    schedulers queue.
    '''

    def __init__(self, policy: PlanificationPolicy):
        ''' Initialize the Exclusive Policy '''
        super().__init__(policy.schedulers)

    def apply(self, metascheduler_queue: List[Scheduler]):
        ''' Apply the Exclusive Policy '''
        pass
