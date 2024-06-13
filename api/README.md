The metascheduler API, built with FastAPI, will be the responsible of keeping track the cluster status, including all of its running/pending jobs and queues. It uses a SQLite database to store the information, and it will be accessed by the metascheduler to make decisions about the cluster status, also ensuring the possible concurrent access to the database.
# Asumptions
## User creation
The API will be running in the frontend node of the cluster, with a user created for it, 'metascheduler' as the recommended name. This user will have the necessary permissions to access the other nodes of the cluster, via ssh, passwordless, using a public key, and it will be able to run the necessary commands to manage the cluster. Optionally, the user will have sudo permissions to enable certain commands that require it.

# Config information
## Config file definition
The file `config/test.config` is a configuration example file that contains all the possible options and configuration of the cluster.
### Define the cluster policy
To define the cluster policy, it is necessary to create a `policy` object with the following attributes:
- `name`: The name of the policy. It can be any string.
- `high_priority`: The scheduler with the highest priority. It has to be the index of the scheduler in the `schedulers` array.
### Define the nodes
To define the nodes, it is necessary to create a `nodes` array with the following attributes:
- `ip`: The IP of the node.
- `port`: The port of the node.
### Define the schedulers
To define the schedulers, it is necessary to create a `schedulers` array with the following attributes:
- `name`: The name of the scheduler. It can be any string.
- `master`: A number that indicates which node is the master node of the scheduler. It has to be the index of the node in the `nodes` array.
- `weight`: The weight of the scheduler. It has to be a number between 0 and 100. Used in the shared policy.
# Setup the project
## Install dependencies
To install the dependencies, it is necessary to have pipenv installed. Then, it is necessary to install the dependencies with the following command:
```bash
pipenv install
```
## Run the project
To run the project, it is necessary to activate the virtual environment with the following command:
```bash
pipenv shell
```
After that, you can run the project with the following command:
```bash
export PYTHONPATH=.. && python3 main.py <config-file> [OPTIONS]
```
### Possible options to run the project
- `--host`: The host of the API. Default: 0.0.0.0
- `--port`: The port of the API. Default: 8000
- `--database-file`: The database file. Default: /db/db.sqlite3
- `--ssh-key-file`: The ssh key file. Default: System default
- `--ssh-user`: The ssh user. Default: metascheduler

