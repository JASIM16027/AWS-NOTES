from diagrams import Diagram, Edge
from diagrams.aws.devtools import Codepipeline, Codebuild, Codecommit, Codedeploy
from diagrams.aws.compute import EC2Instance
from diagrams.aws.general import User

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("CI/CD Automation", filename="images/98-cicd-pipeline", show=False, direction="LR", graph_attr=graph_attr):
    dev = User("You (git push)")
    repo = Codecommit("Source\n(GitHub/CodeCommit)")
    pipeline = Codepipeline("CodePipeline\n(orchestrator)")
    build = Codebuild("CodeBuild\n(test + build)")
    deploy = Codedeploy("CodeDeploy")
    prod = EC2Instance("Production\nServer")

    dev >> repo >> pipeline >> build >> deploy >> prod
