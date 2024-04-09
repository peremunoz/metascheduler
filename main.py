from interfaces.Cluster import Cluster
from ui.ClusterList import ask_for_cluster
from utils.ClusterFactory import get_cluster
from utils.ConsoleHelper import print_cluster_selection

def main():
    """
    Main function of the program.

    """
    cluster: Cluster = cluster_setup()
    cluster.setup_schedulers()

def cluster_setup() -> Cluster:
    """
    Initial setup of the cluster.

    """
    # Ask the user to select a cluster system
    cluster_system: str = ask_for_cluster()

    # Get the cluster object
    cluster: Cluster = get_cluster(cluster_system)
    print_cluster_selection(cluster)

    # Setup the cluster
    cluster.setup()

    return cluster
    

if __name__ == '__main__':
    main()