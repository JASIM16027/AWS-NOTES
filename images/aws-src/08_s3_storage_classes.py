from diagrams import Diagram, Edge
from diagrams.aws.storage import S3, S3Glacier

graph_attr = {"fontsize": "22", "bgcolor": "white"}

with Diagram("S3 Storage Classes and Lifecycle", filename="images/08-s3-storage-classes", show=False, direction="LR", graph_attr=graph_attr):
    std = S3("S3 Standard\nHot data, ms access")
    ia = S3("Standard-IA\nInfrequent, ms\n+retrieval fee")
    gir = S3Glacier("Glacier Instant\nRetrieval - ms")
    gfr = S3Glacier("Glacier Flexible\nRetrieval - min to 12h")
    da = S3Glacier("Glacier Deep\nArchive - 12-48h\nCheapest")
    exp = S3("Expire / Delete")

    std >> Edge(label="30 days") >> ia >> Edge(label="90 days") >> gir >> Edge(label="180 days") >> gfr >> Edge(label="365 days") >> da >> Edge(label="7 years") >> exp
