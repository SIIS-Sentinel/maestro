from typing import List
import time
import importlib
import os
import sys

import paramiko

from hub import Hub
from node import Node
from config_interface import ConfigInterface

# The configuration option is passed as an environment variable at start time
config_path: str = os.environ["MAESTRO_CONFIG"]
try:
    cfg: ConfigInterface = importlib.import_module(config_path)  # type:ignore
except ImportError:
    print(f"Invalid config file: {config_path}")
    sys.exit(-1)


# Shell control characters used to change the color of the displayed text
# The colors may vary depending on your terminal color scheme
class bcolors:
    BROWN = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Orchestrator():
    """
    This class is in charge of handling the connection to and orchestration of the nodes and hub.
    """

    def __init__(self, username: str = cfg.username, keyfile: str = cfg.keyfile, hub: Hub = cfg.hub, nodes: List[Node] = cfg.nodes):
        """
        username: username to use to connect to the devices
        keyfile: path to the SSH key used to connect
        hub: Hub object that contains all the useful data about the hub
        node: list of Node objects that contain all the useful data about the nodes
        """
        self.username: str = username
        self.keyfile: str = keyfile
        self.framework: str = cfg.framework

        self.hub: Hub = hub
        self.nodes: List[Node] = nodes

    def connect_nodes(self):
        """
        Create a two new SSH connection to each node, one for the Sentinel commands, the other for the IoT handler commands
        """
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
        """
        Closes both SSH connection to each node
        """
        for node in self.nodes:
            node.watch_client.close()
            node.integ_client.close()

    def disconnect_hub(self):
        """
        Closes the two SSH connection to the hub
        """
        self.hub.watch_client.close()
        self.hub.sched_client.close()

    def connect_hub(self):
        """
        Creates two SSH connection to the hub, one for the Sentinel commands, the other for the Scheduler commands
        """
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
        """
        Creates all the SSH connections to the hub and the nodes
        """
        self.connect_hub()
        self.connect_nodes()
        print("Connected to the nodes and the hub")

    def disconnect(self):
        """
        Closes all the SSH connections to the hub and the nodes
        """
        self.disconnect_hub()
        self.disconnect_nodes()

    @staticmethod
    def make_client() -> paramiko.SSHClient:
        """
        Helper function to create a new SSH client with the SSH key
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        return client

    def run_hub_sched(self, blocking: bool = True):
        """
        Runs the Scheduler commands at the hub, and stores the stdout stream
        """
        print("Starting Scheduler for the hub")
        command: str = f"cd {self.hub.sched_path} && \
            source venv/bin/activate && \
            cd experiments/{self.hub.experiment_name} && \
            python {self.hub.experiment_name}.py"
        print(" ".join(command.split()))
        stdout: paramiko.channel.ChannelFile
        _, stdout, _ = self.hub.sched_client.exec_command(command, get_pty=True)
        self.hub.sched_stdout = stdout

    def reset_db(self):
        """
        Dumps and recreates the Sentinel database
        CAUTION: causes the loss of all previously recorded experimental, make sure you saved it if needed
        """
        self.print_color(bcolors.BOLD, "Resetting the Watchtower database")
        command: str = f'cd {self.hub.watch_path} && \
            ./reset_db.sh'
        stdout: paramiko.channel.ChannelFile
        _, stdout, _ = self.hub.watch_client.exec_command(command, get_pty=True)
        stdout.channel.recv_exit_status()

    def run_hub_watchtower(self):
        """
        Resets the Sentinel database and runs the Sentinel commands at the hub, and store the stdout stream
        CAUTION: causes the loss of all previouslyrecorded experimental, make sure you saved it if needed
        """
        self.reset_db()
        self.print_color(bcolors.BOLD, "Starting Watchtower for the hub")
        command: str = f"cd {self.hub.watch_path} && \
            source venv/bin/activate && \
            python watchtower_hub.py "
        print(" ".join(command.split()))
        stdout: paramiko.channel.ChannelFile
        _, stdout, _ = self.hub.watch_client.exec_command(command, get_pty=True)
        self.hub.watch_stdout = stdout
        time.sleep(2)

    def run_nodes_integration(self, debug: bool = False):
        """
        Runs the IoT handler commands for each node
        """
        self.print_color(bcolors.BOLD, "Staring integrations...")
        for node in self.nodes:
            self.print_color(bcolors.BOLD, f"Starting Integrations for {node.name}")
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
            print(" ".join(command.split()))
            node.integ_client.exec_command(command, get_pty=True)

    def run_nodes_watch(self, debug: bool = False):
        """
        Runs the Sentinel commands for each node
        """
        for node in self.nodes:
            self.print_color(bcolors.BOLD, f"Starting Watchtower for {node.name}")
            command: str = f'sudo bash -c \
                "pgrep python > /sys/kernel/sentinel/tracked_pid" && \
                cd {node.watch_path} && \
                source venv/bin/activate && \
                python main_node.py'
            print(" ".join(command.split()))
            node.watch_client.exec_command(command, get_pty=True)

    def run_hub(self, blocking: bool = True):
        """
        Runs the Scheduler and Sentinel commands at the hub, and displays their outputs.
        Keeps running until Scheduler is finished
        """
        self.run_hub_watchtower()
        self.run_hub_sched(blocking)
        if blocking is True:
            while not self.hub.sched_stdout.channel.exit_status_ready():
                if self.hub.sched_stdout.channel.recv_ready():
                    line = self.hub.sched_stdout.readline()
                    self.print_color(bcolors.GREEN, line.strip("\n"))
                if self.hub.watch_stdout.channel.recv_ready():
                    line = self.hub.watch_stdout.readline()
                    self.print_color(bcolors.BLUE, line.strip("\n"))
            # Print the last Scheduler lines
            for line in self.hub.sched_stdout:
                self.print_color(bcolors.GREEN, line.strip("\n"))
            return

    def run_node_command(self, cmd: str) -> None:
        """
        Runs the given shell command at every node
        """
        for node in self.nodes:
            client = self.make_client()
            client.connect(
                hostname=node.addr,
                port=node.port,
                username=self.username,
                key_filename=self.keyfile
            )
            self.print_color(bcolors.BOLD, f"{node.name}: {cmd}")
            _, stdout, _ = client.exec_command(cmd)
            for line in stdout:
                print(line.strip("\n"))

    @ staticmethod
    def print_color(color: str, line: str):
        "Helper function to add color to a print statement"
        print(color + line + bcolors.ENDC)

    def run_nodes(self):
        """
        Runs the IoT handler and Sentinel commands for each node
        """
        self.run_nodes_integration()
        # Sleep needed to prevent obscure crashing
        time.sleep(5)
        self.run_nodes_watch()

    def run(self, blocking: bool = True):
        """
        Starts the commands at the nodes and the hub.
        Returns when the Scheduler is done.
        """
        self.run_nodes()
        self.run_hub()

    def test_connect(self):
        """
        Helper method that checks if it can connect to each device
        """
        print("Starting the connection test")
        print("Connecting to the hub")
        self.connect_hub()
        print("OK")
        print("Connecting to the nodes")
        self.connect_nodes()
        print("OK")
        print("All connections successful, closing all")
        self.disconnect()
