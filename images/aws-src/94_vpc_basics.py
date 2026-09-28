from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import InternetGateway, NATGateway
from diagrams.aws.compute import EC2Instance
from diagrams.aws.database import RDS
from diagrams.aws.general import InternetAlt1

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Networking: VPC Basics", filename="images/94-vpc-basics", show=False, direction="TB", graph_attr=graph_attr):
    net = InternetAlt1("Internet")
    igw = InternetGateway("Internet Gateway")

    with Cluster("VPC (10.0.0.0/16)"):
        with Cluster("Public Subnet"):
            web = EC2Instance("Web Server\n(has public IP)")
            nat = NATGateway("NAT Gateway\n(private subnet's\noutbound-only path)")
        with Cluster("Private Subnet"):
            db = RDS("Database\n(no public IP,\nno inbound from internet)")

    net >> Edge(label="inbound web traffic") >> igw >> web
    web >> Edge(label="app queries DB\n(private traffic)") >> db
    db >> Edge(label="outbound updates only", style="dashed") >> nat
