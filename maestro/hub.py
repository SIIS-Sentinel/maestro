from paramiko import SSHClient


class Hub():
    def __init__(self):
        self.addr: str = "hub.local"
        self.port: int = 22
        self.sched_path: str
        self.watch_path: str
        self.sched_client: SSHClient
        self.watch_client: SSHClient
