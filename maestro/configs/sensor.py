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
hub.experiment_name = "sensor"

# Nodes settings
# Sensor(weather station)
node_sensor = Node()
node_sensor.name = "sensor"
node_sensor.addr = "sensor.local"
node_sensor.integ_path = "/home/pi/src/integrations/"
node_sensor.watch_path = "/home/pi/src/watchtower/"
node_sensor.device_file = "sensor.py"
node_sensor.sudo_needed = False


nodes: list = [
    node_sensor
]
