import os

if os.getenv("MAESTRO_CONFIG") is None:
    os.environ["MAESTRO_CONFIG"] = "configs.simple_light"

from orchestrator import Orchestrator

orch = Orchestrator()
orch.connect()
# orch.run()
orch.disconnect()
