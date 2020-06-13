import os

if os.getenv("MAESTRO_CONFIG") is None:
    os.environ["MAESTRO_CONFIG"] = "configs.all_devices"

from orchestrator import Orchestrator

orch = Orchestrator()
orch.connect()
orch.run_nodes_watch()
# orch.run()
orch.disconnect()
