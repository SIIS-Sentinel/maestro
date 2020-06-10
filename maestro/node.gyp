class Node():
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
