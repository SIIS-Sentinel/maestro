import os

if os.getenv("MAESTRO_CONFIG") is None:
    os.environ["MAESTRO_CONFIG"] = "configs.no_sensor_hass"

from orchestrator import Orchestrator

orch = Orchestrator()
# orch.connect()
# orch.run_nodes_watch()
orch.connect_hub()
orch.run_hub()
# orch.run_hub_sched()
orch.disconnect_hub()
