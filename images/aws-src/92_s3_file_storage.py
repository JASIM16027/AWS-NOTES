from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.general import User
from diagrams.onprem.client import Client

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("Store Files with S3", filename="images/92-s3-file-storage", show=False, direction="LR", graph_attr=graph_attr):
    you = User("You")
    with Cluster("S3 Bucket\n(public read policy)"):
        bucket = S3("your-app-bucket")

    viewer = Client("Anyone with the URL")

    you >> Edge(label="1. Create bucket") >> bucket
    you >> Edge(label="2. Upload image/file") >> bucket
    you >> Edge(label="3. Make public") >> bucket
    bucket >> Edge(label="4. Access via https:// URL") >> viewer
