from icmplib import ping


class Node:
    """
    Interface for a node.

    """
    id: int
    ip: str
    port: int
    is_alive: bool | None

    def __init__(self, id: int, ip: str, port: int) -> None:
        """
        Constructor.

        """
        self.id = id
        self.ip = ip
        self.port = port
        self.is_alive = self._is_alive()

    def __str__(self) -> str:
        """
        String representation of the node.

        """
        return f"IP: {self.ip}, Port: {self.port}"

    def _is_alive(self) -> bool | None:
        """
        [ROOT REQUIRED]
        Check if the node is alive.

        Returns:
            bool: True if the node is alive, False otherwise.
            None: If the api is not running as root.

        """
        try:
            return ping(self.ip, count=1).is_alive
        except Exception:
            return None
