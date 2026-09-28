from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import InternetGateway, RouteTable, Nacl, PublicSubnet
from diagrams.aws.compute import EC2Instance
from diagrams.aws.general import InternetAlt1

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Security Group vs Network ACL", filename="images/09-sg-vs-nacl", show=False, direction="LR", graph_attr=graph_attr):
    net = InternetAlt1("Internet")
    igw = InternetGateway("IGW")
    rt = RouteTable("Route Table")

    with Cluster("Subnet"):
        nacl = Nacl("Network ACL\nSUBNET level - STATELESS\nAllow + Deny, rule order")
        with Cluster("EC2 Instance\n(Security Group: INSTANCE level, STATEFUL, allow-only)"):
            inst = EC2Instance("Application")

    net >> igw >> rt >> nacl >> inst
    inst >> Edge(label="response auto-allowed by SG,\nNACL needs outbound rule\n(ephemeral ports 1024-65535)", style="dashed", color="firebrick") >> nacl
