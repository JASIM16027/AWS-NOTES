from diagrams import Diagram, Cluster, Edge
from diagrams.aws.security import IAM, IAMRole, IAMPermissions
from diagrams.aws.general import User, Users

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("IAM Setup: Users, Roles and Policies", filename="images/90-iam-setup", show=False, direction="LR", graph_attr=graph_attr):
    root = User("Root User\n(never use daily)")
    with Cluster("IAM"):
        admin = IAM("IAM Admin User\n(MFA enabled)")
        role = IAMRole("IAM Role\n(for EC2/Lambda)")
        policy = IAMPermissions("IAM Policy\n(least privilege)")

    root >> Edge(label="create, then lock away", color="firebrick") >> admin
    admin >> Edge(label="attach") >> policy
    role >> Edge(label="attach") >> policy
