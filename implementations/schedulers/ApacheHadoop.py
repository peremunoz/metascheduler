from interfaces.Scheduler import Scheduler


class ApacheHadoop(Scheduler):
    """
    Apache Hadoop scheduler.
    
    """
    def __str__(self):
        return "Apache Hadoop"