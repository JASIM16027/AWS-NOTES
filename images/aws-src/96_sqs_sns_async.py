from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Instance, Lambda
from diagrams.aws.integration import SQS, SNS

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Async Systems: SQS + SNS", filename="images/96-sqs-sns-async", show=False, direction="LR", graph_attr=graph_attr):
    with Cluster("Queue (SQS) - decoupling"):
        producer = EC2Instance("Booking API\n(producer)")
        queue = SQS("SQS Queue")
        worker = Lambda("Worker\n(consumer)")
        producer >> Edge(label="send message") >> queue >> Edge(label="poll") >> worker

    with Cluster("Fan-out (SNS) - notify many"):
        topic = SNS("SNS Topic\n(booking confirmed)")
        email = Lambda("Email Service")
        sms = Lambda("SMS Service")
        topic >> email
        topic >> sms

    worker >> Edge(label="publish event") >> topic
