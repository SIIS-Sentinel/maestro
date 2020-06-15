from typing import IO

from paramiko import SSHClient
from paramiko.channel import ChannelFile


class Hub():
    def __init__(self):
        self.addr: str = "hub.local"
        self.port: int = 22
        self.sched_path: str
        self.watch_path: str
        self.sched_client: SSHClient
        self.sched_stdout: ChannelFile
        self.watch_client: SSHClient
        self.watch_stdout: ChannelFile
        self.experiment_name: str
