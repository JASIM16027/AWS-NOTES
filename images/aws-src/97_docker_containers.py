from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.container import Docker
from diagrams.aws.compute import ECR, ECS, EKS, Fargate

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Docker + Containers on AWS", filename="images/97-docker-containers", show=False, direction="LR", graph_attr=graph_attr):
    docker = Docker("Dockerfile\n(build image)")
    ecr = ECR("ECR\n(image registry)")

    with Cluster("Run it - choose one"):
        ecs = ECS("ECS\n(AWS-native, simple)")
        eks = EKS("EKS\n(Kubernetes)")
        fg = Fargate("Fargate\n(serverless containers,\nno EC2 to manage)")

    docker >> Edge(label="push image") >> ecr
    ecr >> ecs
    ecr >> eks
    ecs >> fg
