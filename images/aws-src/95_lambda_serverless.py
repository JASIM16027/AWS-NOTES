from diagrams import Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.general import User

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Serverless with Lambda", filename="images/95-lambda-serverless", show=False, direction="LR", graph_attr=graph_attr):
    user = User("Client App")
    api = APIGateway("API Gateway")
    fn = Lambda("Lambda Function\n(runs your code,\nno server to manage)")

    user >> Edge(label="1. HTTPS request") >> api >> Edge(label="2. triggers") >> fn
