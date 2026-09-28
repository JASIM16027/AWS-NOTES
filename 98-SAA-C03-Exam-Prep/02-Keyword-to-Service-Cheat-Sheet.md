# 🔑 Keyword → Service Cheat Sheet (SAA-C03)

> প্রশ্নে কোন কথা থাকলে কোন service উত্তর হওয়ার সম্ভাবনা বেশি, তার তালিকা। Exam-এর আগের দিন এটাই বারবার পড়ুন।

---

## 🖥 Compute

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| Event-driven, ১৫ মিনিটের কম চলে, সার্ভার manage করতে চায় না | **Lambda** |
| Container চালাবে, server manage করতে চায় না | **ECS/EKS on Fargate** |
| Kubernetes লাগবে / অন্য cloud-এ portable | **EKS** |
| Long-running batch job, Spot দিয়ে সস্তায় | **AWS Batch** |
| Code upload করলেই deploy, infra নিয়ে মাথাব্যথা নেই | **Elastic Beanstalk** |
| Interrupt হলেও চলবে (batch, CI, rendering), সবচেয়ে সস্তা | **Spot Instances** |
| 24/7 steady workload, ১–৩ বছর | **Savings Plans / Reserved Instances** |
| BYOL license (per-socket/core), compliance | **Dedicated Host** |
| HPC, node-এর মধ্যে সবচেয়ে কম latency | **Cluster placement group** |
| অল্প সংখ্যক critical instance, একসাথে fail যেন না হয় | **Spread placement group** |
| Kafka/Cassandra/HDFS, rack-aware | **Partition placement group** |
| RAM-এর state রেখে দ্রুত আবার চালু করা | **EC2 Hibernate** |

## 💾 Storage

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| অনেক EC2 (Linux) একসাথে একই file share করবে | **EFS** |
| Windows file share, SMB, Active Directory | **FSx for Windows File Server** |
| HPC, ML training, খুব দ্রুত parallel file system, S3-এর সাথে | **FSx for Lustre** |
| NetApp ONTAP / multi-protocol (NFS+SMB+iSCSI) | **FSx for NetApp ONTAP** |
| Boot volume / single EC2-এর block storage | **EBS** |
| সর্বোচ্চ IOPS, mission-critical DB | **EBS io2 Block Express** |
| Big data, sequential read, সস্তা HDD | **EBS st1** |
| Temporary cache/buffer, সর্বোচ্চ local IOPS, data হারালে সমস্যা নেই | **Instance Store** |
| Access pattern অজানা/বদলায় | **S3 Intelligent-Tiering** |
| মাসে কম access, কিন্তু দরকারে সাথে সাথে লাগবে | **S3 Standard-IA** |
| পুনরায় তৈরি করা যায় এমন data, সস্তা | **S3 One Zone-IA** |
| Archive, মিলিসেকেন্ডে লাগবে (quarterly) | **S3 Glacier Instant Retrieval** |
| Archive, কয়েক ঘণ্টায় পেলেই হবে | **S3 Glacier Flexible Retrieval** |
| ৭–১০ বছর compliance archive, ১২–৪৮ ঘণ্টা OK, সবচেয়ে সস্তা | **S3 Glacier Deep Archive** |
| WORM, কেউ delete করতে পারবে না (root-ও না) | **S3 Object Lock – Compliance mode** |
| Accidental delete থেকে রক্ষা | **S3 Versioning + MFA Delete** |
| দূরের user থেকে বড় file upload দ্রুত | **S3 Transfer Acceleration** (+ multipart upload) |
| User-কে সাময়িক private file access | **S3 pre-signed URL** |
| On-prem app → cloud storage (NFS/SMB/iSCSI/tape) hybrid | **Storage Gateway** (File / Volume / Tape) |
| On-prem NFS/SMB → S3/EFS online migration/sync | **DataSync** |
| TB–PB data, network ধীর/নেই | **Snowball Edge** |
| অন্য region-এ S3 copy (DR/latency) | **S3 Cross-Region Replication** |

## 💽 Database

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| Relational, SQL, JOIN, managed | **RDS** |
| High performance MySQL/PostgreSQL, ১৫ replica, ৬ copy | **Aurora** |
| Unpredictable/intermittent SQL workload, auto scale | **Aurora Serverless v2** |
| Global SQL DB, <1s cross-region, DR | **Aurora Global Database** |
| Key-value, millisecond, massive scale, serverless | **DynamoDB** |
| DynamoDB-তে microsecond read cache | **DAX** |
| Multi-region active-active NoSQL | **DynamoDB Global Tables** |
| DynamoDB item change-এ trigger | **DynamoDB Streams + Lambda** |
| Session store / DB query cache / leaderboard | **ElastiCache (Redis/Valkey)** |
| MongoDB compatible | **DocumentDB** |
| Graph, relationship, social network, fraud | **Neptune** |
| Data warehouse, OLAP, BI analytics, petabyte | **Redshift** |
| S3-এর data সরাসরি SQL-এ query, serverless | **Athena** |
| Time-series (IoT) | **Timestream** |
| Immutable ledger | **QLDB** *(২০২৫-এ বন্ধ হয়ে গেছে; পুরনো প্রশ্নে এখনো আসতে পারে। বিকল্প: Aurora PostgreSQL)* |
| Cassandra compatible | **Keyspaces** |
| Lambda থেকে RDS-এ অনেক connection / failover দ্রুত | **RDS Proxy** |
| DB-র high availability, automatic failover | **RDS Multi-AZ** |
| Read-heavy load কমানো | **Read Replica** (বা ElastiCache) |

## 🌐 Networking & Content Delivery

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| Private subnet থেকে internet-এ outbound (update) | **NAT Gateway** (public subnet-এ) |
| Private subnet থেকে S3/DynamoDB, internet ছাড়া, free | **Gateway VPC Endpoint** |
| Private subnet থেকে অন্য AWS service (SQS, KMS...) privately | **Interface VPC Endpoint (PrivateLink)** |
| নিজের service অন্য VPC/account-কে privately expose | **PrivateLink (NLB + Endpoint Service)** |
| ২–৩টা VPC connect | **VPC Peering** |
| অনেক VPC + on-prem, transitive routing | **Transit Gateway** |
| On-prem ↔ AWS দ্রুত setup, encrypted, internet দিয়ে | **Site-to-Site VPN** |
| On-prem ↔ AWS dedicated, consistent, high bandwidth | **Direct Connect** (backup হিসেবে VPN) |
| Static/dynamic content cache, global low latency | **CloudFront** |
| Non-HTTP (TCP/UDP), static IP, দ্রুত regional failover | **Global Accelerator** |
| Path/host-based routing, HTTP | **ALB** |
| Millions req/s, TCP/UDP, static IP | **NLB** |
| 3rd-party firewall/IDS appliance | **Gateway Load Balancer** |
| DR: primary fail হলে secondary | **Route 53 Failover routing** |
| User-কে সবচেয়ে কম latency-র region-এ | **Route 53 Latency routing** |
| দেশ অনুযায়ী আলাদা content/restriction | **Route 53 Geolocation** / CloudFront geo restriction |
| Traffic % ভাগ (A/B, canary) | **Route 53 Weighted** |
| Zone apex (example.com) → ALB/CloudFront | **Route 53 Alias record** |
| Private subnet-এ SSH ছাড়া access | **SSM Session Manager** |

## 🔐 Security & Identity

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| EC2/Lambda-কে AWS access দিতে | **IAM Role** (access key না!) |
| অন্য account-কে access | **Cross-account IAM Role (AssumeRole)** |
| সব account-এ guardrail (যেমন region restrict) | **SCP (AWS Organizations)** |
| Workforce SSO, একাধিক account | **IAM Identity Center** |
| Mobile/web app-এর user sign-up/sign-in | **Cognito User Pool** |
| App user-কে temporary AWS credential | **Cognito Identity Pool** |
| Encryption key manage, audit, rotation | **KMS** |
| Dedicated single-tenant HSM, FIPS 140-3 Level 3 নিজের control | **CloudHSM** |
| DB password auto-rotation | **Secrets Manager** |
| Config/parameter, সস্তা | **SSM Parameter Store** |
| SQL injection, XSS, rate limiting, IP block (Layer 7) | **AWS WAF** |
| DDoS protection (free) | **Shield Standard** |
| DDoS + 24/7 response team + cost protection | **Shield Advanced** |
| Threat detection (malicious IP, crypto-mining, compromised credential) | **GuardDuty** |
| EC2/ECR/Lambda vulnerability (CVE) scan | **Inspector** |
| S3-এ PII/sensitive data খোঁজা | **Macie** |
| Resource config history + compliance rule | **AWS Config** |
| কে কোন API call করেছে (audit) | **CloudTrail** |
| সব security finding এক জায়গায় | **Security Hub** |
| Public/cross-account access খুঁজে বের করা | **IAM Access Analyzer** |
| Free SSL/TLS certificate (ALB/CloudFront) | **ACM** (CloudFront-এর জন্য **us-east-1**) |
| Multi-account WAF/SG policy centrally | **Firewall Manager** |
| VPC-level stateful firewall, domain filtering | **AWS Network Firewall** |
| S3 bucket শুধু CloudFront দিয়ে access | **Origin Access Control (OAC)** |

## ⚡ Application Integration & Serverless

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| Decouple, buffer, async processing | **SQS** |
| Strict order + exactly-once | **SQS FIFO** |
| একটা message অনেক subscriber-কে (fan-out) | **SNS** (→ multiple SQS) |
| Event routing, SaaS event, rule/filter, schedule | **EventBridge** |
| Multi-step workflow, retry, human approval | **Step Functions** |
| REST/HTTP/WebSocket API, Lambda-র সামনে | **API Gateway** |
| GraphQL, real-time subscription | **AppSync** |
| Real-time streaming data (clickstream, log), multiple consumer, replay | **Kinesis Data Streams** |
| Streaming data S3/Redshift/OpenSearch-এ load, কোনো code ছাড়া | **Amazon Data Firehose** |
| Managed Kafka | **Amazon MSK** |
| ActiveMQ/RabbitMQ migrate (JMS, AMQP, MQTT) | **Amazon MQ** |
| ETL, data catalog | **AWS Glue** |
| Hadoop/Spark big data cluster | **EMR** |
| Dashboard / BI | **QuickSight** |
| Log search, full-text search | **OpenSearch Service** |

## 📊 Monitoring & Management

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| Metric, log, alarm | **CloudWatch** |
| EC2-এর memory/disk metric | **CloudWatch Agent** |
| Distributed tracing | **X-Ray** |
| Infrastructure as Code (AWS) | **CloudFormation** (multi-account/region: **StackSets**) |
| Patch, run command, inventory | **Systems Manager** |
| Cost/security/limit recommendation | **Trusted Advisor** |
| Cost alert | **AWS Budgets** |
| Right-size recommendation | **Compute Optimizer** |
| Centralized backup, cross-region/account | **AWS Backup** |
| Multi-account landing zone setup | **Control Tower** |
| Resource অন্য account-এর সাথে share (subnet, TGW) | **AWS RAM** |

## 🚚 Migration

| প্রশ্নে যা থাকে | উত্তর |
|---|---|
| Server rehost (lift & shift), minimal downtime | **Application Migration Service (MGN)** |
| DB migrate, source চালু রেখে (CDC) | **DMS** |
| ভিন্ন DB engine (Oracle → PostgreSQL) schema convert | **SCT / DMS Schema Conversion** |
| On-prem server discovery ও planning | **Application Discovery Service / Migration Hub** |
| Server-level DR, RPO seconds | **Elastic Disaster Recovery (DRS)** |

---

## 🔢 যে সংখ্যাগুলো মুখস্থ রাখবেন

| বিষয় | সংখ্যা |
|---|---|
| Lambda max timeout | **15 মিনিট** |
| Lambda memory | 128 MB – **10 GB** |
| API Gateway integration timeout | **29 সেকেন্ড** (default) |
| SQS message retention | default 4 দিন, max **14 দিন** |
| SQS visibility timeout | default 30 সেকেন্ড, max **12 ঘণ্টা** |
| SQS message size | **1 MiB** (২০২৫-এর আগে 256 KB ছিল, অনেক practice প্রশ্নে এখনো তাই লেখা থাকে); আরও বড় হলে S3 + Extended Client Library |
| S3 object max size | **5 TB** (single PUT 5 GB; >100 MB হলে multipart) |
| S3 durability | **11 nines** |
| DynamoDB item max | **400 KB** |
| RDS automated backup retention | **1–35 দিন** |
| Aurora replicas | **15** |
| Spot interruption notice | **2 মিনিট** |
| Spread placement group | AZ প্রতি **7 instance** |
| Glacier Deep Archive min duration | **180 দিন** |
| Standard-IA / One Zone-IA min duration | **30 দিন** |
| Glacier Instant / Flexible min duration | **90 দিন** |
| CloudTrail event history | **90 দিন** |
| STS temporary credential | 15 মিনিট – 12 ঘণ্টা |
| VPC-তে subnet প্রতি reserved IP | **5টা** |
