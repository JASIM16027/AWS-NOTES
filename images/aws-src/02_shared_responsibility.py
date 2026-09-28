from diagrams import Diagram, Cluster
from diagrams.aws.security import IAM, IAMPermissions
from diagrams.aws.general import SslPadlock, GenericFirewall
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.network import VPCRouter
from diagrams.aws.general import GenericOfficeBuilding

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("AWS Shared Responsibility Model", filename="images/02-shared-responsibility", show=False, direction="TB", graph_attr=graph_attr):
    with Cluster("CUSTOMER: Security IN the Cloud"):
        c1 = IAM("Customer Data\nand IAM users/roles")
        c2 = IAMPermissions("Platform, Applications\nIAM policies")
        c3 = GenericFirewall("Guest OS patching\nSecurity Group / NACL")
        c4 = SslPadlock("Encryption:\nclient-side, server-side, in-transit")
        c1 - c2 - c3 - c4

    with Cluster("AWS: Security OF the Cloud"):
        a1 = [EC2("Compute"), RDS("Database"), S3("Storage"), VPCRouter("Networking")]
        a2 = GenericOfficeBuilding("Regions, AZs, Edge Locations\nPhysical security")
        a1 >> a2

    c4 >> a1[0]
