import pulumi
from pulumi_gcp import compute

class VPC:
    def __init__(self, name: str, subnet_cidr: str, secondary_ranges: dict, network_tags: list[str]):
        
        # create a new VPC network
        self.vpc_network = compute.Network(
            name,
            auto_create_subnetworks=False,
            description=f"{name} VPC Network"
        )
        
        # create a new subnet in the VPC network
        self.subnet = compute.Subnetwork(
            f"{name}-subnet",
            ip_cidr_range=subnet_cidr,
            region="us-central1",
            network=self.vpc_network.self_link,
            secondary_ip_ranges=[
                {"rangeName": k, "ipCidrRange": v} for k, v in secondary_ranges.items()]
        )
        
        # create a firewall rule to allow incoming traffic to specific ports
        self.firewall_rule = compute.Firewall(
            f"{name}-firewall-rule",
            network=self.vpc_network.self_link,
            allows=[
                {
                    "protocol": "tcp",
                    "ports": ["10250", "443", "15017","8080", "15000",],
                },
            ],
            
            # allow traffic only from a specific IP range
            source_ranges=["10.2.0.0/16"],
            
            # apply the firewall rule to instances with specific network tags
            target_tags=network_tags,
        )
