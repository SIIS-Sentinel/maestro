import os
import time

if os.getenv("MAESTRO_CONFIG") is None:
    os.environ["MAESTRO_CONFIG"] = "configs.all_devices_hass"

from orchestrator import Orchestrator

orch = Orchestrator()
orch.connect()
orch.run()
orch.disconnect()
