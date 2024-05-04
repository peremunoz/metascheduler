from ..classes.apache_hadoop import ApacheHadoop
from ..classes.sge import SGE


def get_scheduler(scheduler_name: str):
    '''
    Gets the scheduler class based on the scheduler name.

    '''
    if scheduler_name == 'Apache Hadoop':
        return ApacheHadoop()
    if scheduler_name == 'SGE':
        return SGE()
    raise ValueError('Scheduler not implemented')
