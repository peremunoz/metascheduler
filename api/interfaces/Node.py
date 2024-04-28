from icmplib import ping


class Node:
    """
    Interface for a node.

    """
    id: int
    ip: str
    port: int
    ssh_user: str
    ssh_password: str

    def __init__(self, id: int, ip: str, port: int, ssh_user: str, ssh_password: str) -> None:
        """
        Constructor.

        """
        self.id = id
        self.ip = ip
        self.port = port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password

    def __str__(self) -> str:
        """
        String representation of the node.

        """
        return f"IP: {self.ip}, Port: {self.port}, User: {self.ssh_user}, Password: {self.ssh_password}"

    def is_alive(self) -> bool | None:
        """
        [ROOT REQUIRED]
        Check if the node is alive.

        Returns:
            bool: True if the node is alive, False otherwise.
            None: If the api is not running as root.

        """
        try:
            return ping(self.ip, count=1).is_alive
        except Exception as e:
            return None
