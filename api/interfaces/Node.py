from icmplib import ping


class Node:
    """
    Interface for a node.

    """
    id: int
    ip: str
    port: int

    def __init__(self, id: int, ip: str, port: int) -> None:
        """
        Constructor.

        """
        self.id = id
        self.ip = ip
        self.port = port

    def __str__(self) -> str:
        """
        String representation of the node.

        """
        return f"IP: {self.ip}, Port: {self.port}"

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
