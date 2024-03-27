from interfaces.Cluster import Cluster


def get_cluster(cluster_name: str) -> Cluster:
    """
    Gets the cluster object based on the selected cluster name.

    """
    if cluster_name == "Kubernetes":
        from implementations.clusters.Kubernetes import KubernetesCluster
        return KubernetesCluster()
    else:
        raise ValueError("Cluster not implemented")