from hub import Hub
from node import Node

# General settings
username: str = "pi"
keyfile: str = "/home/pi/.ssh/iot_rsa"
framework: str = "hass"

# Hub settings
hub: Hub = Hub()
hub.addr = "hub.local"
hub.sched_path = "/home/pi/scheduler/"
hub.watch_path = "/home/pi/watchtower/"
hub.experiment_name = "all_devices"

# Nodes settings
# HVAC
node_hvac = Node()
node_hvac.name = "hvac"
node_hvac.addr = "hvac.local"
node_hvac.integ_path = "/home/pi/src/integrations/"
node_hvac.watch_path = "/home/pi/src/watchtower/"
node_hvac.device_file = "hvac.py"
node_hvac.sudo_needed = False

# Light
node_light = Node()
node_light.name = "light"
node_light.addr = "light.local"
node_light.integ_path = "/home/pi/src/integrations/"
node_light.watch_path = "/home/pi/src/watchtower/"
node_light.device_file = "light.py"
node_light.sudo_needed = True

# Lock
node_lock = Node()
node_lock.name = "lock"
node_lock.addr = "lock.local"
node_lock.integ_path = "/home/pi/src/integrations/"
node_lock.watch_path = "/home/pi/src/watchtower/"
node_lock.device_file = "lock.py"
node_lock.sudo_needed = False

# Outlet
node_outlet = Node()
node_outlet.name = "outlet"
node_outlet.addr = "outlet.local"
node_outlet.integ_path = "/home/pi/src/integrations/"
node_outlet.watch_path = "/home/pi/src/watchtower/"
node_outlet.device_file = "outlet.py"
node_outlet.sudo_needed = False

# Presence
node_presence = Node()
node_presence.name = "presence"
node_presence.addr = "presence.local"
node_presence.integ_path = "/home/pi/src/integrations/"
node_presence.watch_path = "/home/pi/src/watchtower/"
node_presence.device_file = "presence.py"
node_presence.sudo_needed = False

# Sensor(weather station)
node_sensor = Node()
node_sensor.name = "sensor"
node_sensor.addr = "sensor.local"
node_sensor.integ_path = "/home/pi/src/integrations/"
node_sensor.watch_path = "/home/pi/src/watchtower/"
node_sensor.device_file = "sensor.py"
node_sensor.sudo_needed = False

# Smoke
node_smoke = Node()
node_smoke.name = "smoke"
node_smoke.addr = "smoke.local"
node_smoke.integ_path = "/home/pi/src/integrations/"
node_smoke.watch_path = "/home/pi/src/watchtower/"
node_smoke.device_file = "smoke.py"
node_smoke.sudo_needed = False

# Switch
node_switch = Node()
node_switch.name = "switch"
node_switch.addr = "switch.local"
node_switch.integ_path = "/home/pi/src/integrations/"
node_switch.watch_path = "/home/pi/src/watchtower/"
node_switch.device_file = "switch.py"
node_switch.sudo_needed = False

# TV
node_tv = Node()
node_tv.name = "tv"
node_tv.addr = "tv.local"
node_tv.integ_path = "/home/pi/src/integrations/"
node_tv.watch_path = "/home/pi/src/watchtower/"
node_tv.device_file = "tv.py"
node_tv.sudo_needed = False

nodes: list = [
    node_hvac,
    node_light,
    node_lock,
    node_outlet,
    node_presence,
    node_sensor,
    node_smoke,
    node_switch,
    node_tv
]
