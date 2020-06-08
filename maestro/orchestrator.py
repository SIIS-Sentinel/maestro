from typing import List
import time

import paramiko

import config as cfg


class Orchestrator():
    def __init__(self, username: str = cfg.username, keyfile: str = cfg.keyfile, hub: cfg.Hub = cfg.hub, nodes: List[cfg.Node] = cfg.nodes):
        # self.hub_client: paramiko.SSHClient
        # self.nodes_clients: List[paramiko.SSHClient]

        self.username: str = username
        self.keyfile: str = keyfile
        self.framework: str = cfg.framework

        self.hub: cfg.Hub = hub
        self.nodes: List[cfg.Node] = nodes

    def connect_nodes(self):
        for node in self.nodes:
            client = self.make_client()
            client.connect(
                hostname=node.addr,
                port=node.port,
                username=self.username,
                key_filename=self.keyfile
            )
            node.watch_client = client
            client = self.make_client()
            client.connect(
                hostname=node.addr,
                port=node.port,
                username=self.username,
                key_filename=self.keyfile
            )
            node.integ_client = client

    def disconnect_nodes(self):
        for node in self.nodes:
            node.watch_client.close()
            node.integ_client.close()

    def disconnect_hub(self):
        self.hub.watch_client.close()
        self.hub.sched_client.close()

    def connect_hub(self):
        client = self.make_client()
        client.connect(
            hostname=self.hub.addr,
            port=self.hub.port,
            username=self.username,
            key_filename=self.keyfile
        )
        self.hub.watch_client = client
        client = self.make_client()
        client.connect(
            hostname=self.hub.addr,
            port=self.hub.port,
            username=self.username,
            key_filename=self.keyfile
        )
        self.hub.sched_client = client

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

    def run_hub_sched(self, blocking: bool = True):
        print("Starting Scheduler for the hub")
        command: str = f"cd {self.hub.sched_path} && \
            source venv/bin/activate && \
            python main_test.py "
        print(command)
        _, stdout, _ = self.hub.sched_client.exec_command(command, get_pty=True)
        if blocking:
            line: str
            for line in stdout:
                print(line.strip("\n"))

    def reset_db(self):
        print("Resetting the Watchtower database")
        command: str = f'cd {self.hub.watch_path} && \
            ./reset_db.sh'
        _, stdout, _ = self.hub.watch_client.exec_command(command, get_pty=True)
        stdout.channel.recv_exit_status()

    def run_hub_watchtower(self):
        self.reset_db()
        print("Starting Watchtower for the hub")
        command: str = f"cd {self.hub.watch_path} && \
            source venv/bin/activate && \
            python main_hub.py "
        print(command)
        self.hub.watch_client.exec_command(command, get_pty=True)
        time.sleep(2)

    def run_nodes_integration(self, debug: bool = False):
        for node in self.nodes:
            print(f"Starting Integrations for {node.name}")
            command: str
            if node.sudo_needed:
                command = f'cd {node.integ_path} && \
                    sudo bash -c \
                    "source venv/bin/activate && \
                    python {self.framework}/{node.device_file}"'

            else:
                command = f"cd {node.integ_path} && \
                    source venv/bin/activate && \
                    python {self.framework}/{node.device_file} "
            print(command)
            _, stdout, _ = node.integ_client.exec_command(command, get_pty=True)

    def run_nodes_watch(self, debug: bool = False):
        for node in self.nodes:
            print(f"Starting Watchtower for {node.name}")
            command: str = f"cd {node.watch_path} && \
                source venv/bin/activate && \
                python main_node.py"
            print(command)
            node.watch_client.exec_command(command, get_pty=True)

    def run_hub(self, blocking: bool = True):
        self.run_hub_watchtower()
        self.run_hub_sched(blocking)

    def run_nodes(self):
        self.run_nodes_integration()
        self.run_nodes_watch()

    def run(self, blocking: bool = True):
        self.run_nodes()
        self.run_hub()

    def test_connect(self):
        print("Starting the connection test")
        print("Connecting to the hub")
        self.connect_hub()
        print("OK")
        print("Connecting to the nodes")
        self.connect_nodes()
        print("OK")
        print("All connections successful, closing all")
        self.disconnect()
