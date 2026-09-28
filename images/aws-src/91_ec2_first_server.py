from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Instance
from diagrams.aws.general import User
from diagrams.onprem.client import Client

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Launch Your First Server (EC2)", filename="images/91-ec2-first-server", show=False, direction="LR", graph_attr=graph_attr):
    you = User("You")
    with Cluster("EC2 Instance (Ubuntu, t2.micro)"):
        inst = EC2Instance("Node.js App\nrunning")

    you >> Edge(label="1. Launch with Key Pair") >> inst
    you >> Edge(label="2. SSH connect") >> inst
    you >> Edge(label="3. Install Node.js\n+ run app") >> inst
    client = Client("Internet User")
    client >> Edge(label="4. Access via Public IP") >> inst
