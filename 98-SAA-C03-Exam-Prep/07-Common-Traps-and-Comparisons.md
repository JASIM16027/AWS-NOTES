# ⚠️ Common Traps ও Confusing Comparisons (SAA-C03)

> Exam-এ দুটো কাছাকাছি option দিয়ে বিভ্রান্ত করা হয়। এই তালিকাটা "কোনটা আর কোনটা না" মনে রাখার জন্য।

---

## 🪤 ১০টা সবচেয়ে common ফাঁদ

| # | ফাঁদ | আসলে সঠিক কী |
|---|---|---|
| 1 | "Security Group-এ deny rule দিয়ে IP block" | SG-তে **deny নেই**। Block করতে **NACL** বা **WAF** লাগবে |
| 2 | "Read Replica দিয়ে HA / auto failover" | Auto failover হয় **Multi-AZ**-এ; Read Replica = read scaling (manual promote) |
| 3 | "IAM policy দিয়ে root user-কে আটকানো" | Root user-কে আটকায় শুধু **SCP** (member account-এ) |
| 4 | "NAT Gateway private subnet-এ রাখা" | NAT GW থাকে **public subnet-এ**, private subnet-এর route table থেকে NAT-এ route যায় |
| 5 | "CloudFront-এর certificate যেকোনো region-এ" | CloudFront-এর ACM certificate **শুধু `us-east-1`-এ** বানাতে হয় |
| 6 | "Lambda দিয়ে ১ ঘণ্টার job" | Lambda-র সীমা **১৫ মিনিট**। লম্বা কাজ → **ECS/Fargate, Batch, Step Functions** |
| 7 | "CNAME দিয়ে zone apex (example.com)" | Zone apex-এ CNAME দেওয়া যায় না, দিতে হবে **Alias record** |
| 8 | "Instance Store-এ database রাখা" | Instance store **ephemeral**, stop/terminate হলে data চলে যায়। Persistent data → **EBS** |
| 9 | "S3 Transfer Acceleration দিয়ে download দ্রুত করা" | Download/serve দ্রুত করতে **CloudFront**; TA মূলত **upload**-এর জন্য |
| 10 | "SQS Standard-এ exactly-once/order" | Order আর exactly-once লাগলে **SQS FIFO** |

---

## 🔄 কাছাকাছি service — পার্থক্য এক লাইনে

### Storage
- **EBS vs EFS vs S3** → Block (একটা EC2) / Shared file (অনেক EC2) / Object (API দিয়ে)
- **EFS vs FSx for Windows** → Linux NFS / Windows SMB + AD
- **FSx Lustre vs EFS** → HPC/ML-এর জন্য বিশাল speed / সাধারণ shared file
- **Storage Gateway vs DataSync** → চলমান hybrid access / data move বা sync
- **DataSync vs Snowball** → network যথেষ্ট / network ধীর বা নেই (TB–PB)
- **Glacier Instant vs Flexible vs Deep Archive** → ms / minutes–hours / 12–48 hours

### Database
- **RDS vs Aurora** → standard managed DB / বেশি performance, ১৫ replica, ৬ copy
- **Aurora Global DB vs RDS cross-region replica** → <1s lag, দ্রুত failover / async, manual
- **DynamoDB vs RDS** → key-value, অসীম scale / SQL, JOIN
- **DAX vs ElastiCache** → শুধু DynamoDB-র cache / যেকোনো DB বা app-এর cache
- **Redshift vs Athena** → data warehouse (cluster/serverless) / S3-এর data-তে serverless query
- **Multi-AZ instance vs Multi-AZ DB cluster** → standby-তে read করা যায় না / ২টা readable standby

### Networking
- **VPC Peering vs Transit Gateway** → অল্প VPC, non-transitive / অনেক VPC, transitive
- **VPN vs Direct Connect** → দ্রুত setup, internet দিয়ে encrypted / private link, consistent speed, সপ্তাহ লাগে
- **Gateway vs Interface Endpoint** → S3/DynamoDB, free, route table-এ / বেশিরভাগ service, ENI, paid
- **CloudFront vs Global Accelerator** → HTTP cache / TCP-UDP, static IP, cache করে না
- **ALB vs NLB vs GWLB** → L7 HTTP / L4 TCP-UDP, static IP / L3 firewall appliance
- **Latency vs Geolocation routing** → সবচেয়ে দ্রুত region / user কোথা থেকে আসছে
- **NAT Gateway vs NAT Instance** → managed, HA per AZ / নিজে manage, সস্তা, পুরনো পদ্ধতি

### Security
- **KMS vs CloudHSM** → multi-tenant managed / single-tenant, পুরো control আপনার
- **Secrets Manager vs Parameter Store** → auto rotation, দামি / config রাখার জন্য, free tier আছে
- **GuardDuty vs Inspector vs Macie** → threat / vulnerability / S3-এর PII
- **CloudTrail vs Config vs CloudWatch** → কে কী করেছে / resource কেমন আছে ও compliant কিনা / performance metric, log
- **WAF vs Shield vs Network Firewall** → L7 web attack / DDoS / VPC-level firewall
- **Cognito User Pool vs Identity Pool** → login (authentication) / AWS credential দেওয়া (authorization)
- **SCP vs IAM policy vs Permissions boundary** → account-এর সর্বোচ্চ সীমা / permission দেওয়া / user বা role-এর সর্বোচ্চ সীমা

### Integration
- **SQS vs SNS vs EventBridge** → queue (pull) / pub-sub (push) / event bus + rules
- **Kinesis Data Streams vs Firehose** → real-time, custom consumer, replay / code ছাড়া S3 বা Redshift-এ load
- **Kinesis vs SQS** → একাধিক consumer, ordering per shard, replay / একটা consumer, message delete হয়ে যায়
- **Step Functions vs SQS** → workflow orchestration / decoupling buffer
- **Amazon MQ vs SQS** → পুরনো protocol (JMS/AMQP/MQTT) migrate / নতুন cloud-native app

### Compute
- **ECS vs EKS** → AWS-native সহজ / Kubernetes
- **Fargate vs EC2 launch type** → serverless / নিজে instance manage
- **Spot vs Savings Plan vs RI** → interruptible সস্তা / flexible commitment / নির্দিষ্ট commitment (zonal RI capacity reserve করে)
- **Dedicated Host vs Dedicated Instance** → পুরো physical server-এর control, BYOL / শুধু hardware isolation
- **Stop vs Hibernate** → RAM হারায় / RAM EBS-এ save থাকে
- **Beanstalk vs CloudFormation** → PaaS, code upload করলেই হলো / IaC, সব resource template-এ লিখে define

---

## 🧮 Qualifier দেখে উত্তর বাছাইয়ের উদাহরণ

একই scenario-র ৪টা ভিন্ন qualifier দিলে উত্তরও বদলে যায়:

> *"A company needs to process uploaded files..."*

| Qualifier | উত্তর |
|---|---|
| ... **with the LEAST operational overhead** | S3 event → **Lambda** |
| ... **that can take up to 2 hours each** | S3 event → SQS → **ECS Fargate / AWS Batch** |
| ... **at the LOWEST cost, interruptions acceptable** | SQS → **Spot** fleet / Fargate Spot |
| ... **in strict order, exactly once** | **SQS FIFO** → consumer |

---

## ✅ Exam-এর আগের রাতের ১০টা লাইন

1. HA = Multi-AZ, DR = Multi-Region
2. Decouple = SQS
3. EC2-কে access = Role
4. সব account-এ guardrail = SCP
5. Private S3 access, free = Gateway Endpoint
6. Serverless, least overhead = Lambda / Fargate / DynamoDB / Aurora Serverless
7. Interruptible, সস্তা = Spot
8. Unknown S3 access pattern = Intelligent-Tiering
9. Global HTTP = CloudFront; TCP/UDP + static IP = Global Accelerator
10. DB password rotation = Secrets Manager
