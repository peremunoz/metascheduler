The metascheduler API, built with FastAPI, will be the responsible of keeping track the cluster status, including all of its running/pending jobs and queues. It uses a SQLite database to store the information, and it will be accessed by the metascheduler to make decisions about the cluster status, also ensuring the possible concurrent access to the database.
# Asumptions
## User creation
The API will be running in the frontend node of the cluster, with a user created for it, named 'metascheduler'. This user will have the necessary permissions to access the other nodes of the cluster, via ssh, without password, and it will be able to run the necessary commands to manage the cluster. Optionally, the user will have sudo permissions to enable certain commands that require it, but it is not necessary.

# Config information
## Config file definition
The file `config/test.config` is a configuration example file that contains all the possible options and configuration of the cluster.
### Define the master node
To correctly set the master node, it has to be defined the first node of the `nodes` array.
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
export PYTHONPATH=.. && python3 main.py
```

