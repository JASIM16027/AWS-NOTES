from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Instance
from diagrams.aws.database import RDS
from diagrams.aws.general import User

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Database Setup with RDS", filename="images/93-rds-database", show=False, direction="LR", graph_attr=graph_attr):
    you = User("You")
    ec2 = EC2Instance("EC2\n(Node.js app)")
    rds = RDS("RDS MySQL\n(Multi-AZ optional)")

    you >> Edge(label="1. Create MySQL RDS") >> rds
    ec2 >> Edge(label="2. Connect (private,\nsecurity-group restricted)") >> rds
    ec2 >> Edge(label="3. Store / query data") >> rds
