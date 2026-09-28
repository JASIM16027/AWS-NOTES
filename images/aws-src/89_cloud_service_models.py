from diagrams import Diagram, Cluster
from diagrams.aws.general import TraditionalServer, GenericOfficeBuilding
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Cloud Service Models: IaaS vs PaaS vs SaaS", filename="images/89-cloud-service-models", show=False, direction="LR", graph_attr=graph_attr):
    user = User("You")
    with Cluster("On-Premises\n(Traditional IT)"):
        srv = TraditionalServer("You manage\neverything")
    with Cluster("IaaS\nAWS: EC2, VPC"):
        iaas = EC2("You manage OS\n+ App, AWS manages\nhardware")
    with Cluster("PaaS\nAWS: Lambda, Beanstalk"):
        paas = Lambda("You manage code only,\nAWS manages\nruntime")
    with Cluster("SaaS\nready-to-use software"):
        saas = S3("Just use it,\nno management\n(e.g. Gmail, Dropbox)")

    user >> srv
    user >> iaas
    user >> paas
    user >> saas
