from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2Instance, EC2AutoScaling
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.aws.management import Cloudwatch, CloudwatchAlarm
from diagrams.aws.general import Users

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Auto Scaling Group in Action", filename="images/04-asg-scaling", show=False, direction="LR", graph_attr=graph_attr):
    users = Users("Users")
    alb = ElbApplicationLoadBalancer("ALB")

    with Cluster("Auto Scaling Group\nmin 2 / desired 3 / max 10"):
        i1 = EC2Instance("EC2 (AZ-a)")
        i2 = EC2Instance("EC2 (AZ-b)")
        i3 = EC2Instance("EC2 (AZ-c)")
        i4 = EC2AutoScaling("New EC2\n(from Launch Template)")

    cw = Cloudwatch("CloudWatch\nCPU metrics")
    alarm = CloudwatchAlarm("Target Tracking\nCPU > 50%")

    users >> alb
    alb >> i1
    alb >> i2
    alb >> i3
    [i1, i2, i3] >> cw
    cw >> alarm
    alarm >> Edge(label="scale out +1", color="firebrick") >> i4
    i4 >> Edge(label="auto register", style="dashed") >> alb
