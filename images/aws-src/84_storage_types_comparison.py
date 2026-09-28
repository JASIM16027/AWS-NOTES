from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2Instance
from diagrams.aws.storage import EBS, EFS
from diagrams.aws.general import Disk

graph_attr = {"fontsize": "22", "bgcolor": "white", "splines": "ortho"}

with Diagram("EBS vs Instance Store vs EFS", filename="images/84-storage-types-comparison", show=False, direction="TB", graph_attr=graph_attr):
    with Cluster("EBS - Block Storage\ngp3 / io2 / st1 / sc1\nNetwork-attached - survives stop - snapshot to S3"):
        e1 = EC2Instance("EC2")
        e1v = EBS("EBS Volume")
        e1 >> e1v

    with Cluster("Instance Store - Ephemeral\nHost-attached - fastest I/O\nLOST on stop/terminate"):
        e2 = EC2Instance("EC2")
        e2v = Disk("Local Disk")
        e2 >> e2v

    with Cluster("EFS - Shared File Storage\nNFS - auto-scaling - Multi-AZ by default"):
        e3a = EC2Instance("EC2 A")
        e3b = EC2Instance("EC2 B")
        e3v = EFS("EFS File System")
        e3a >> e3v
        e3b >> e3v
