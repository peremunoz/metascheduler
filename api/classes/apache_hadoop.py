from api.interfaces.scheduler import Scheduler


class ApacheHadoop(Scheduler):
    '''
    Apache Hadoop Scheduler

    '''

    def __str__(self) -> str:
        return f'Apache Hadoop Scheduler: {self.hostname}:{self.port}'
