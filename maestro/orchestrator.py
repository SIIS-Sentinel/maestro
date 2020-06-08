from typing import List

import paramiko

import config as cfg


class Orchestrator():
    def __init__(self, username: str = cfg.username, keyfile: str = cfg.keyfile, hub: cfg.Hub = cfg.hub, nodes: List[cfg.Node] = cfg.nodes):
        self.hub_client: paramiko.SSHClient
        self.node_clients: List[paramiko.SSHClient]

        self.username: str = username
        self.keyfile: str = keyfile

        self.hub_cfg: cfg.Hub = hub
        self.nodes_cfg: List[cfg.Node] = nodes

    def connect_hub(self):
        self.node_clients = []
        for node in self.nodes_cfg:
            client = self.make_client()
            client.connect(
                hostname=node.addr,
                port=node.port,
                username=self.username,
                key_filename=self.keyfile
            )
            self.node_clients.append(client)

    def disconnect_nodes(self):
        for client in self.node_clients:
            client.close()

    def disconnect_hub(self):
        self.hub_client.close()

    def connect_nodes(self):
        self.hub_client = self.make_client()
        self.hub_client.connect(
            hostname=self.hub_cfg.addr,
            port=self.hub_cfg.port,
            username=self.username,
            key_filename=self.keyfile
        )

    def connect(self):
        self.connect_hub()
        self.connect_nodes()

    def disconnect(self):
        self.disconnect_hub()
        self.disconnect_nodes()

    @staticmethod
    def make_client() -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        return client
