from api.interfaces.scheduler import Scheduler


class ApacheHadoop(Scheduler):
    '''
    Apache Hadoop Scheduler

    '''

    def __init__(self) -> None:
        super().__init__()
        self.name = 'Apache Hadoop'

    def __str__(self) -> str:
        return f'Apache Hadoop Scheduler: {self.hostname}:{self.port}'
