from api.interfaces.scheduler import Scheduler


class Queue:
    '''
    Interface for a Queue

    '''

    id_: int
    scheduler_name: Scheduler

    def __init__(self, id_: int = None, scheduler_name: str = None) -> None:
        self.id_ = id_
        self.scheduler_name = scheduler_name
