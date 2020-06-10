from typing import List

from hub import Hub
from node import Node


class ConfigInterface:
    def __init__(self):
        self.username: str
        self.keyfile: str
        self.framework: str
        self.hub: Hub
        self.nodes: List[Node]
