class Node:
    """
    Interface for a node.

    """
    ip: str
    port: int
    ssh_user: str
    ssh_password: str

    def __init__(self, ip: str, port: int, ssh_user: str, ssh_password: str) -> None:
        """
        Constructor.

        """
        self.ip = ip
        self.port = port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password

    def __str__(self) -> str:
        """
        String representation of the node.

        """
        return f"IP: {self.ssh_ip}, Port: {self.ssh_port}, User: {self.ssh_user}, Password: {self.ssh_password}"
