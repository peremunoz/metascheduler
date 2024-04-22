from interfaces.Scheduler import Scheduler


class SGE(Scheduler):
    """
    SGE scheduler.

    """

    def __str__(self):
        return "SGE"
