from paramiko import SSHClient


class Node():
    """
    This class holds all the data related to a node, for use by the config file
    """

    def __init__(self):
        self.name: str
        self.addr: str
        self.port: int = 22
        self.device_file: str
        self.sudo_needed: bool = False
        self.client: SSHClient
        self.integ_path: str
        self.watch_path: str
        self.integ_client: SSHClient
        self.watch_client: SSHClient
