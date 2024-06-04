import os
import threading
from icmplib import ping
from fabric import Connection


class Node:
    '''
    Interface for a node.

    '''
    id_: int
    ip: str
    port: int
    is_alive: bool | None

    def __init__(self, id_: int, ip: str, port: int) -> None:
        '''
        Constructor.

        '''
        self.id_ = id_
        self.ip = ip
        self.port = port
        self.is_alive = self._is_alive()

    def __str__(self) -> str:
        '''
        String representation of the node.

        '''
        return f'ID: {self.id_}, IP: {self.ip}, Port: {self.port}'

    def send_command(self, command: str) -> str:
        '''
        Send a command to the node.

        Args:
            command (str): The command to send.

        Returns:
            str: The response from the node.

        '''
        ssh_key_file = os.getenv('SSH_KEY_FILE')
        try:
            with Connection(
                self.ip,
                port=self.port,
                user=os.getenv('SSH_USER'),
                connect_kwargs={'key_filename': ssh_key_file}
            ) as conn:
                result = conn.run(command, hide=True)
                return result.stdout
        except Exception as e:
            raise e

    def send_command_async(self, command: str) -> None:
        '''
        Send a command to the node asynchronously.

        Args:
            command (str): The command to send.

        '''
        ssh_key_file = os.getenv('SSH_KEY_FILE')

        def run_command():
            try:
                with Connection(
                    self.ip,
                    port=self.port,
                    user=os.getenv('SSH_USER'),
                    connect_kwargs={'key_filename': ssh_key_file}
                ) as conn:
                    conn.run(command, hide=True)
            except Exception as e:
                raise e

        thread = threading.Thread(target=run_command)
        thread.start()

    def _is_alive(self) -> bool | None:
        '''
        [ROOT REQUIRED]
        Check if the node is alive.

        Returns:
            bool: True if the node is alive, False otherwise.
            None: If the api is not running as root.

        '''
        try:
            return ping(self.ip, count=1).is_alive
        except Exception:
            return None
