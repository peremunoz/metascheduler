class Scheduler():
    """
    Interface for a scheduler.

    """
    master: str

    def set_master(self, master: str):
        """
        Sets the master of the scheduler.

        """
        self.master = master