from typing import List
from api.config.config import AppConfig
from api.daemons.policies.planification_policy import PlanificationPolicy
from api.interfaces.job import Job
from api.interfaces.node import Node

MINIMUM_NICE_VALUE = 19


class BestEffortPolicy(PlanificationPolicy):
    ''' The Best Effort Policy is a planification policy that allows all schedulers
    to run jobs concurrently, but prioritizes the jobs of the scheduler with the
    highest priority. This policy is useful for running jobs that require the
    maximum amount of resources available., while still allowing other jobs to
    run concurrently.

    So, if a job from the highest priority scheduler is available, it will be
    queued. If no job from the highest priority scheduler is available, the
    jobs from the other schedulers will be queued, and monitored to reduce the
    priority of them.
    '''
    nodes: List[Node] = []

    def __init__(self, policy: PlanificationPolicy):
        '''

        '''
        super().__init__(policy.schedulers, policy.highest_priority)
        self.nodes = AppConfig().nodes

    def apply(self, to_be_queued_jobs: List[Job]):
        '''

        '''
        if not to_be_queued_jobs:
            print('No jobs to be queued, but adjusting priorities...')
            self._adjust_priorities()
            return

        next_job = to_be_queued_jobs[0]
        next_job_scheduler_index = next_job.queue - 1

        print(
            f'Queuing job {next_job.id_} from scheduler {next_job_scheduler_index}...')
        self.schedulers[next_job_scheduler_index].queue_job(next_job)

        self._adjust_priorities()

    def _adjust_priorities(self):
        '''
        Adjust the priorities of the jobs in the schedulers that are not the
        highest priority scheduler.

        '''
        for scheduler in self.schedulers:
            if scheduler == self.highest_priority:
                continue
            if len(scheduler.get_job_list()) > 0:
                scheduler.adjust_nice_of_all_jobs(MINIMUM_NICE_VALUE)
