def get_scheduler(scheduler_name: str):
    """
    Gets the scheduler object based on the selected scheduler name.

    """
    if scheduler_name == "Apache Hadoop":
        from implementations.schedulers.ApacheHadoop import ApacheHadoop
        return ApacheHadoop()
    elif scheduler_name == "SGE":
        from implementations.schedulers.SGE import SGE
        return SGE()
    else:
        raise ValueError("Scheduler not implemented")
