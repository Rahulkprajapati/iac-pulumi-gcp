import pulumi
from network import VPC
from gke import GKECluster

if __name__ == '__main__':

    # Define secondary IP ranges for the subnetwork
    secondary_ranges = {
        "pod-range-1": "10.21.0.0/16",
        "svc-range-1": "10.22.0.0/16"
    }

    # Define node pools for the GKE cluster
    node_pools = [
        {
            "name": "frontend-pool",
            "node_count": 1,
            "node_config": {
                "preemptible":True,
                "machine_type": "n1-standard-1",
                "oauth_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
                "tags": ["frontend"],

            }
        },
        {
            "name": "backend-pool",
            "node_count": 1,
            "node_config": {
                "preemptible":True,
                "machine_type": "n1-standard-1",
                "oauth_scopes": ["https://www.googleapis.com/auth/cloud-platform"],
                "tags": ["backend"],
            }
        }
    ]
    
    # Define authorized networks for the GKE cluster's master
    master_authorized_networks = [
        {
        "cidr_block": "14.142.42.202/32", 
         "display_name": "levi ip"
         },
        {
        "cidr_block": "106.132.43.208/32", 
        "display_name": "office system ip"
         }
        ]
    
    # Define network tags for the VPC firewall rule
    network_tags = ["bastion-host"]

    # Create a VPC
    my_vpc = VPC("<network-name>", "10.20.0.0/16", secondary_ranges, network_tags)

    # Create a GKE cluster
    my_gke_cluster = GKECluster("<gke-cluster-name>", node_pools, master_authorized_networks, my_vpc.subnet)

    # Export some values for future reference
    pulumi.export("vpc_network_name", my_vpc.vpc_network.name)
    pulumi.export("subnet_name", my_vpc.subnet.name)
    pulumi.export("ip_cidr_range", my_vpc.subnet.ip_cidr_range)
    pulumi.export("gke_cluster_name", my_gke_cluster.cluster.name)
