The metascheduler API, built with FastAPI, will be the responsible of keeping track the cluster status, including all of its running/pending jobs and queues. It uses a SQLite database to store the information, and it will be accessed by the metascheduler to make decisions about the cluster status, also ensuring the possible concurrent access to the database.

## Config file definition
The file `config/test.config` is a configuration example file that contains all the possible options and configuration of the cluster.
### Define the master node
To correctly set the master node, it has to be defined the first node of the `nodes` array.