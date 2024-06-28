from typing import List
from api.daemons.policies.planification_policy import PlanificationPolicy
from api.interfaces.job import Job
import time

MAX_NICE = 19
MIN_NICE_NO_ROOT = 0


class DynamicPolicy(PlanificationPolicy):
    ''' The Dynamic Policy is a planification policy that allows all schedulers
    to run jobs concurrently. This policy defines different initial weights
    for each scheduler, and the jobs' priority is defined by the scheduler's
    weight, behavior that is identical to the Shared Policy.

    The difference between the Dynamic Policy and the Shared Policy is that the
    Dynamic Policy adjusts the weights of the schedulers dynamically, based on
    the performance of the schedulers and the jobs.

    '''

    def __init__(self, policy: PlanificationPolicy):
        '''

        '''
        super().__init__(policy.schedulers, policy.highest_priority)

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

        '''
        for scheduler in self.schedulers:
            actual_jobs_info = scheduler.get_all_jobs_info()
            for job_info in actual_jobs_info:
                pid = job_info[0]
                nice = job_info[1]
                cpu = job_info[2]
                mem = job_info[3]
                user = job_info[4]
                self._write_log_in_csv(
                    f'{time.time()},{pid},{nice},{cpu},{mem},{user}'
                )
                if nice == 0:
                    scheduler.adjust_nice_of_job(
                        pid, self._calculate_nice_from_weight(scheduler.weight), user)
                    continue
                if cpu > float(scheduler.weight) or mem > float(scheduler.weight):
                    scheduler.adjust_nice_of_job(pid, nice+1, user)
                elif cpu < scheduler.weight or mem < scheduler.weight:
                    # HAS TO BE ROOT!!!
                    scheduler.adjust_nice_of_job(pid, nice-1, user)

    def _write_log_in_csv(self, log: str):
        '''

        '''
        with open('log.csv', 'a') as file:
            file.write(log + '\n')

    def _calculate_nice_from_weight(self, weight: int) -> int:
        '''
        Calculate the nice value of a job based on the scheduler's weight.
        Assumes that the scheduler's weight is a percentage value, from 0 to 100.
        Assumes that the nice value of a job is a value from 0 to 19.
        Assumes that the sum of all weights is 100.

        '''
        if weight == 0:
            return MAX_NICE
        proportional_cpu_usage = weight / 100
        nice_range = MAX_NICE - MIN_NICE_NO_ROOT
        nice = MIN_NICE_NO_ROOT + (1 - proportional_cpu_usage) * nice_range
        return round(nice)
