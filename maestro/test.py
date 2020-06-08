from orchestrator import Orchestrator
import time

orch = Orchestrator()
orch.connect()
orch.run(True)
orch.disconnect()
