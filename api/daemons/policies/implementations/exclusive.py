from typing import List
from api.daemons.policies.planification_policy import PlanificationPolicy
from api.interfaces.job import Job


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
        super().__init__(policy.schedulers, policy.highest_priority)

    def apply(self, to_be_queued_jobs: List[Job]):
        ''' Apply the Exclusive Policy '''
        if not to_be_queued_jobs:
            print('No jobs to be queued.')
            return

        next_job = to_be_queued_jobs[0]
        next_job_scheduler_index = next_job.queue - 1

        for i, scheduler in enumerate(self.schedulers):
            if i != next_job_scheduler_index and len(scheduler.get_job_list()) > 0:
                print(
                    f'Scheduler {i} has running jobs. Cannot run job from scheduler {next_job_scheduler_index}.')
                return
        print(
            f'Queuing job {next_job.id_} from scheduler {next_job_scheduler_index}...')
        self.schedulers[next_job_scheduler_index].queue_job(next_job)
