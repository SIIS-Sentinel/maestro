import os
import time

if os.getenv("MAESTRO_CONFIG") is None:
    raise EnvironmentError("MAESTRO_CONFIG is not set")

from orchestrator import Orchestrator

orch = Orchestrator()
orch.connect()
orch.run()
orch.disconnect()
