from api.interfaces.Scheduler import Scheduler


class SGE(Scheduler):
    '''
    SGE Scheduler

    '''

    def __str__(self) -> str:
        return "SGE"
