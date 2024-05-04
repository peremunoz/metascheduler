def get_scheduler(scheduler_name: str):
    """
    Gets the scheduler class based on the scheduler name.

    """
    if scheduler_name == "Apache Hadoop":
        from ..classes.apache_hadoop import ApacheHadoop
        return ApacheHadoop()
    elif scheduler_name == "SGE":
        from ..classes.sge import SGE
        return SGE()
    else:
        raise ValueError("Scheduler not implemented")
