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
hub.experiment_name = "hvac"

# Nodes settings
# HVAC
node_hvac = Node()
node_hvac.name = "hvac"
node_hvac.addr = "hvac.local"
node_hvac.integ_path = "/home/pi/src/integrations/"
node_hvac.watch_path = "/home/pi/src/watchtower/"
node_hvac.device_file = "hvac.py"
node_hvac.sudo_needed = False


nodes: list = [
    node_hvac
]
