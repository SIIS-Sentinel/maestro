# Maestro

Maestro is a tool that uses [paramiko](http://www.paramiko.org/) to control all the nodes and hub of the Sentinel network at the same time.

## Installing

* Create a new virtual environment: `virtualenv venv`
* Activate it: `source venv/bin/activate`
* Install the dependencies: `pip install -r requirements.txt`

## Usage

To run `maestro`, you need to give it a configuration file that contains the list of all the devices it should connect to, as well as where to find the needed application folders on eadch of them. Premade config files are stored in the `maestro/configs` folder. 

* Make sure the hub and each node are accessible over SSH from this machine, using a single SSH key.

* `cd` into the `maestro` folder.

* Run `MAESTRO_CONFIG=configs.$CONFIG_NAME python run.py`, where `$CONFIG_NAME` is the name of the Python config file, without its `.py` extention

The `run.py` performs the following tasks: 
1. Connect to the nodes and hub
2. Start the nodes Sentinel application
3. Start the nodes IoT device handlers
4. Start the hub Sentinel application
5. Start the hub Scheduler application
6. Wait until the Scheduler process is done
7. Kill all started processes and terminate

## Running a single command

If you want to run a single shell command on a set of devices (e.g. to upgrade packages), you can use the `command.py` file. This file connects to the nodes, and executes the shell command that is written in the Python file.