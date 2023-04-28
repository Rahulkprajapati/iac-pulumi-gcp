import pulumi
from pulumi_gcp import container

class GKECluster:
    def __init__(self, name: str, node_pools: list[dict], master_authorized_networks: list[dict],  subnet: pulumi.Resource):
        
        # create a new GKE cluster
        self.cluster = container.Cluster(
            name,
            location="us-central1-a",
            # use the same VPC network and subnet as the one passed in
            network=subnet.network,
            subnetwork=subnet.self_link,

            # configure the cluster to use private nodes and a private endpoint
            private_cluster_config={
                "enablePrivateEndpoint": False,
                "enablePrivateNodes": True,
                "masterIpv4CidrBlock": "10.0.0.32/28",
            },

            # allow access to the cluster only from specific IP ranges
            master_authorized_networks_config={
                "cidr_blocks": master_authorized_networks
            },

            # configure the node pools for the cluster
            node_pools=node_pools,
            
            # enable shielded nodes for improved security
            enable_shielded_nodes=True,

            # configure IP allocation policy for the cluster
            ip_allocation_policy=container.ClusterIpAllocationPolicyArgs(
                cluster_secondary_range_name=subnet.secondary_ip_ranges[0].range_name,
                services_secondary_range_name=subnet.secondary_ip_ranges[1].range_name,
            ),
        )
