from typing import List

from hub import Hub
from node import Node


class ConfigInterface:
    """
    This class is used to define what configuration items are present in a maestro config file
    """

    def __init__(self):
        self.username: str
        self.keyfile: str
        self.framework: str
        self.hub: Hub
        self.nodes: List[Node]
