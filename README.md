[![Pylint](https://github.com/peremunoz/metascheduler/actions/workflows/pylint.yml/badge.svg)](https://github.com/peremunoz/metascheduler/actions/workflows/pylint.yml) [![Pytest on API](https://github.com/peremunoz/metascheduler/actions/workflows/pytest.yml/badge.svg)](https://github.com/peremunoz/metascheduler/actions/workflows/pytest.yml)

# Metascheduler

A job-metascheduler developed in Python. Used to manage workflows in a hybrid cluster ecosystem, with Hadoop and SGE as cluster frameworks, but has been implemented the most generic way possible, to allow other cluster frameworks to work effortless.

This repository is mainly divided into two different parts:

- The API, which is the core of the metascheduler, and is responsible for managing the jobs and the cluster frameworks.
- The Client (CLI), which is a command-line interface that allows the user to interact with the API.

## Installation

Each of the components has its own installation process, so please refer to the README files in the corresponding directories. (Both are using pipfile for dependency management)

## Usage

The API is a RESTful API, so it can be used with any HTTP client. The client is a command-line interface that allows the user to interact with the API. To test it in a local environment, you have to set up the API with the master nodes of the cluster frameworks you want to use, using the configuration file.

In the folder `local_test_scenario` you can find two folders, one for each cluster framework, with the docker-compose files to set up a local environment to test the metascheduler. The SGE cluster framework is already set up with a master node and a worker node, and the Hadoop cluster framework is set up with all the necessary nodes, but you will face some issues related to the Hadoop users permissions. Inside the `local_test_scenario/hadoop` folder, you can find a init_command.txt file with the commands you have to run to set up the Hadoop users, to allow the API to interact with the Hadoop cluster.
