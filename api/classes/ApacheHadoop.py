from api.interfaces.Scheduler import Scheduler


class ApacheHadoop(Scheduler):
    '''
    Apache Hadoop Scheduler

    '''

    def __str__(self) -> str:
        return "Apache Hadoop"
