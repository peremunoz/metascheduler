from interfaces.Cluster import Cluster
from ui.ClusterList import ask_for_cluster
from utils.ClusterFactory import get_cluster
from utils.ConsoleHelper import print_color

def main():
    """
    Main function of the program.

    """
    cluster: Cluster = clusterSetup()

def clusterSetup() -> Cluster:
    """
    Initial setup of the cluster.

    """
    # Ask the user to select a cluster system
    cluster_system = ask_for_cluster()
    print("Selected cluster system: ", end='')
    print_color(cluster_system, "blue")

    # Get the cluster object
    cluster = get_cluster(cluster_system)

    # Setup the cluster
    cluster.setup()

    print(cluster)

    return cluster
    

if __name__ == '__main__':
    main()