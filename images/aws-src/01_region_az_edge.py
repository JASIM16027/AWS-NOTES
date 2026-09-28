from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Instance
from diagrams.aws.network import CloudFrontEdgeLocation
from diagrams.aws.general import User

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("AWS Global Infrastructure: Region, AZ and Edge Location", filename="images/01-region-az-edge", show=False, direction="TB", graph_attr=graph_attr):
    user = User("User (Bangladesh)")

    with Cluster("Edge Locations"):
        edge_dhaka = CloudFrontEdgeLocation("Dhaka Edge")
        edge_sg = CloudFrontEdgeLocation("Singapore Edge")

    with Cluster("Region: ap-south-1 (Mumbai)"):
        with Cluster("AZ ap-south-1a"):
            a1 = EC2Instance("Data center(s)")
        with Cluster("AZ ap-south-1b"):
            a2 = EC2Instance("Data center(s)")
        with Cluster("AZ ap-south-1c"):
            a3 = EC2Instance("Data center(s)")
        a1 - Edge(label="low-latency\nprivate fiber") - a2 - Edge() - a3

    with Cluster("Region: us-east-1 (N. Virginia)"):
        b1 = EC2Instance("AZ us-east-1a")
        b2 = EC2Instance("AZ us-east-1b")
        b3 = EC2Instance("AZ us-east-1c ...")

    user >> edge_dhaka
    edge_dhaka >> Edge(label="AWS backbone") >> a1
    edge_sg >> b1
