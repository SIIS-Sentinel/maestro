from hub import Hub
from node import Node

# General settings
username: str = "pi"
keyfile: str = "/Users/adrien/.ssh/iot_rsa"
framework: str = "hass"

# Hub settings
hub: Hub = Hub()
hub.addr = "hub.local"
hub.sched_path = "/home/pi/scheduler/"
hub.watch_path = "/home/pi/watchtower/"

# Nodes settings
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
