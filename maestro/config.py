# General settings

username: str = "pi"
keyfile: str = "/Users/adrien/.ssh/iot_rsa"
framework: str = "hass/"

# Hub settings


class Hub():
    def __init__(self):
        self.addr: str
        self.port: int = 22
        self.sched_path: str
        self.watch_path: str


hub: Hub = Hub()
hub.addr = "hub.local"
hub.sched_path = "/home/pi/scheduler/"
hub.watch_path = "/home/pi/watchtower/"

# Nodes settings


class Node():
    def __init__(self):
        self.addr: str
        self.port: int = 22
        self.intruder_path: str
        self.watch_path: str
        self.device_file: str


node_light = Node()
node_light.addr = "node.local"
node_light.intruder_path = "/home/pi/src/intruder/"
node_light.watch_path = "/home/pi/src/watchtower/"
node_light.device_file = "light.py"

nodes: list = [
    node_light
]
