class Node:
    """
    Interface for a node.

    """
    ssh_ip: str
    ssh_port: int
    ssh_user: str
    ssh_password: str

    def __init__(self, ssh_ip: str, ssh_port: int, ssh_user: str, ssh_password: str) -> None:
        """
        Constructor.

        """
        self.ssh_ip = ssh_ip
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password

    def __str__(self) -> str:
        """
        String representation of the node.

        """
        return f"IP: {self.ssh_ip}, Port: {self.ssh_port}, User: {self.ssh_user}, Password: {self.ssh_password}"

    def connect(self):
        """
        Connects to the node.

        """
        raise NotImplementedError("Method not implemented")
    
    def disconnect(self):
        """
        Disconnects from the node.

        """
        raise NotImplementedError("Method not implemented")
    
    def is_active(self) -> bool:
        """
        Checks if the node is active.

        """
        raise NotImplementedError("Method not implemented")
    