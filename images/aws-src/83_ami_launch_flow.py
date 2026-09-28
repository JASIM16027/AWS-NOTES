from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Ami, EC2Instance
from diagrams.aws.storage import ElasticBlockStoreEBSSnapshot, EBS
from diagrams.aws.general import User

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("AMI to EC2 Launch Flow", filename="images/83-ami-launch-flow", show=False, direction="LR", graph_attr=graph_attr):
    you = User("You")
    ami = EC2Ami("AMI\n(OS + Software + Config)")
    snap = ElasticBlockStoreEBSSnapshot("Root Volume\nSnapshot")

    with Cluster("New EC2 Instance"):
        inst = EC2Instance("Running Instance")
        vol = EBS("Root EBS Volume")
        inst - vol

    you >> Edge(label="Launch") >> ami
    ami >> Edge(label="copy") >> snap
    snap >> Edge(label="attach at boot") >> vol
