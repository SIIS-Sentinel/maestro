from paramiko import SSHClient

# General settings

username: str = "pi"
keyfile: str = "/Users/adrien/.ssh/iot_rsa"
framework: str = "hass"

# Hub settings


class Hub():
    def __init__(self):
        self.addr: str = "hub.local"
        self.port: int = 22
        self.sched_path: str
        self.watch_path: str
        self.sched_client: SSHClient
        self.watch_client: SSHClient


hub: Hub = Hub()
hub.addr = "hub.local"
hub.sched_path = "/home/pi/scheduler/"
hub.watch_path = "/home/pi/watchtower/"

# Nodes settings


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


node_light = Node()
node_light.name = "light"
node_light.addr = "node.local"
node_light.integ_path = "/home/pi/src/integrations/"
node_light.watch_path = "/home/pi/src/watchtower/"
node_light.device_file = "light.py"
node_light.sudo_needed = True

nodes: list = [
    node_light
]
