from api.interfaces.scheduler import Scheduler


class SGE(Scheduler):
    '''
    SGE Scheduler

    '''

    def __str__(self) -> str:
        return f'SGE Scheduler: {self.hostname}:{self.port}'
