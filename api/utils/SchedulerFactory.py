def get_scheduler(scheduler_name: str):
    """
    Gets the scheduler class based on the scheduler name.

    """
    if scheduler_name == "Apache Hadoop":
        from ..classes.ApacheHadoop import ApacheHadoop
        return ApacheHadoop()
    elif scheduler_name == "SGE":
        from ..classes.SGE import SGE
        return SGE()
    else:
        raise ValueError("Scheduler not implemented")
