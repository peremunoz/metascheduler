from typing import List
from interfaces.Scheduler import Scheduler


class Cluster:
    """
    Interface for a cluster.

    """
    schedulers: List[Scheduler]
    master: str

    def setup():
        """
        Sets up the cluster.

        """
        raise NotImplementedError("Method not implemented")
    
    def setup_schedulers():
        """
        Sets up the schedulers of the cluster.
        
        """
        raise NotImplementedError("Method not implemented")

    def connect(self):
        """
        Connects to the cluster.
        
        """
        raise NotImplementedError("Method not implemented")
    
    def disconnect(self):
        """
        Disconnects from the cluster.
        
        """
        raise NotImplementedError("Method not implemented")
    
    def is_active(self) -> bool:
        """
        Checks if the cluster is active.
        
        """
        raise NotImplementedError("Method not implemented")
    
    def __str__(self):
        """
        String representation of the cluster.

        """
        raise NotImplementedError("Method not implemented")
    
    def get_schedulers(self):
        """
        Gets the schedulers of the cluster.
        
        """
        return self.schedulers
    
    def set_schedulers(self, schedulers: List[Scheduler]):
        """
        Sets the schedulers of the cluster.
        
        """
        self.schedulers = schedulers
    
    def remove_scheduler(self, scheduler: Scheduler):
        """
        Removes a scheduler from the cluster.
        
        """
        self.schedulers.remove(scheduler)
    
    def get_master(self) -> str:
        """
        Gets the master of the cluster.
        
        """
        return self.master
    
    def set_master(self, master: str):
        """
        Sets the master of the cluster.
        
        """
        self.master = master
