from api.interfaces.scheduler import Scheduler


class Queue:
    """
    Interface for a Queue

    """

    id: int
    scheduler_name: Scheduler

    def __init__(self, id: int = None, scheduler_name: str = None) -> None:
        self.id = id
        self.scheduler_name = scheduler_name
