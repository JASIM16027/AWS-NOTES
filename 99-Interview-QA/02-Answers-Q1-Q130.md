# 🎯 AWS Interview Questions — উত্তরসহ Notes (Q1–Q130)

> [প্রশ্ন তালিকা (01-Questions.md)](./01-Questions.md)-র সব প্রশ্নের উত্তর note আকারে। প্রতিটা উত্তরে: মূল ধারণা → key points → কখন কী ব্যবহার → 💡 Interview tip।
> ভাষা: বাংলা + technical term ইংরেজিতে (interview-এ যেভাবে বলবেন)।

## 📑 সূচিপত্র
- [Core / Foundational (Q1–6)](#-core--foundational)
- [EC2 & Compute (Q7–14)](#-ec2--compute)
- [Storage (Q15–21)](#-storage)
- [Networking — VPC (Q22–28)](#-networking-vpc)
- [Databases (Q29–34)](#-databases)
- [Security & IAM (Q35–43)](#-security--iam)
- [Serverless & Application Integration (Q44–49)](#-serverless--application-integration)
- [Monitoring, DevOps & Architecture (Q50–57)](#-monitoring-devops--architecture)
- [Scenario-Based (Q58–62)](#-scenario-based)
- [Core / Foundational — additional (Q63–67)](#-core--foundational-additional)
- [EC2 & Compute — additional (Q68–75)](#-ec2--compute-additional)
- [Storage — additional (Q76–82)](#-storage-additional)
- [Networking — additional (Q83–89)](#-networking-vpc-additional)
- [Databases — additional (Q90–96)](#-databases-additional)
- [Security & IAM — additional (Q97–104)](#-security--iam-additional)
- [Serverless — additional (Q105–109)](#-serverless--application-integration-additional)
- [Monitoring, DevOps — additional (Q110–117)](#-monitoring-devops--architecture-additional)
- [Migration & Hybrid Cloud (Q118–123)](#-migration--hybrid-cloud)
- [Scenario-Based — additional (Q124–130)](#-scenario-based-additional)

---

## 🔰 Core / Foundational

### Q1. AWS কী, এবং এর main service category গুলো কী কী?

**AWS (Amazon Web Services)** = Amazon-এর public cloud platform। Internet-এর মাধ্যমে on-demand, pay-as-you-go ভিত্তিতে compute, storage, database, networking ইত্যাদি IT resource ভাড়া দেয়। নিজের data center কিনতে/চালাতে হয় না।

**Main categories:**

| Category | Example Services |
|---|---|
| Compute | EC2, Lambda, ECS, EKS, Fargate, Elastic Beanstalk, Batch |
| Storage | S3, EBS, EFS, FSx, Glacier, Storage Gateway |
| Database | RDS, Aurora, DynamoDB, ElastiCache, Redshift, DocumentDB, Neptune |
| Networking & CDN | VPC, Route 53, CloudFront, ELB, Direct Connect, Global Accelerator, Transit Gateway |
| Security & Identity | IAM, KMS, Secrets Manager, WAF, Shield, GuardDuty, Inspector, Cognito |
| Management & Monitoring | CloudWatch, CloudTrail, Config, Systems Manager, Trusted Advisor, Organizations |
| DevOps / IaC | CloudFormation, CodePipeline, CodeBuild, CodeDeploy, CDK |
| Application Integration | SQS, SNS, EventBridge, Step Functions, API Gateway |
| Analytics | Athena, EMR, Kinesis, Glue, QuickSight |
| AI/ML | SageMaker, Bedrock, Rekognition, Comprehend |
| Migration | DMS, SCT, MGN, Snow Family, DataSync |

💡 **Tip:** "AWS = 200+ fully featured service, global infrastructure (Region/AZ/Edge), pay-as-you-go model" — এক লাইনে এভাবে শুরু করুন।

---

### Q2. Availability Zone, Region, এবং Edge Location-এর পার্থক্য

- **Region** — একটা geographic area (যেমন `ap-south-1` Mumbai, `us-east-1` N. Virginia)। প্রতিটা Region সম্পূর্ণ **isolated**। সাধারণত ৩+ AZ থাকে।
  - Region বাছাই করার factor: **Compliance/data residency, Latency (user-এর কাছাকাছি), Service availability, Pricing**।
- **Availability Zone (AZ)** — Region-এর ভেতরে এক বা একাধিক discrete data center, আলাদা power, cooling, networking সহ। AZ গুলো নিজেদের মধ্যে **low-latency, high-bandwidth private fiber** দিয়ে যুক্ত। একটা AZ down হলে অন্যটা চলে → **High Availability**-র ভিত্তি।
  - নাম: `ap-south-1a`, `ap-south-1b` ...
- **Edge Location** — Region/AZ-এর বাইরে, বড় শহরগুলোতে থাকা **Point of Presence (PoP)**। CloudFront (CDN cache), Route 53 (DNS), Global Accelerator, WAF, Lambda@Edge এখানে চলে। Region-এর চেয়ে অনেক বেশি সংখ্যক (৪০০+)।

| | Region | AZ | Edge Location |
|---|---|---|---|
| কী | Geographic area | Isolated data center(s) | Cache/PoP |
| উদ্দেশ্য | Data residency, latency | HA / fault tolerance | Content delivery, low latency |
| সংখ্যা | ~৩০+ | ~১০০+ | ৪০০+ |

(এছাড়াও: **Local Zones**, **Wavelength Zones**, **Outposts** — edge-এ compute আনার জন্য।)

---

### Q3. AWS Shared Responsibility Model কী?

Security দায়িত্ব AWS আর customer-এর মধ্যে ভাগ করা।

- **AWS → "Security OF the Cloud"**: physical data center, hardware, network infrastructure, hypervisor, managed service-এর underlying software।
- **Customer → "Security IN the Cloud"**: নিজের data, IAM (user/permission), OS patching (EC2-তে), application, Security Group/NACL config, encryption, client-side & server-side data protection।

**Service type অনুযায়ী দায়িত্ব shift হয়:**

| Service | Customer-এর দায়িত্ব |
|---|---|
| EC2 (IaaS) | Guest OS patch, app, firewall (SG), data, IAM — অনেক বেশি |
| RDS (managed) | DB user, SG, parameter, data; OS/patch AWS করে |
| Lambda / S3 (serverless) | শুধু code, data, IAM, bucket policy |

**Shared controls:** Patch management, Configuration management, Awareness & training — দুই পক্ষই নিজ নিজ layer-এ।

💡 **Tip:** "Unencrypted public S3 bucket → customer-এর দোষ, AWS-এর না" — এমন উদাহরণ দিন।

---

### Q4. Public subnet vs Private subnet

পার্থক্যটা subnet-এর নিজের কোনো property না — **route table**-এ নির্ভর করে।

- **Public subnet**: associated route table-এ `0.0.0.0/0 → Internet Gateway (igw-xxx)` route আছে। Instance-এর public IP/EIP থাকলে internet থেকে সরাসরি reachable।
  - রাখা হয়: ALB, NAT Gateway, Bastion host।
- **Private subnet**: IGW-তে route নেই। Outbound internet লাগলে `0.0.0.0/0 → NAT Gateway` (যেটা public subnet-এ থাকে)। Inbound internet থেকে সরাসরি আসা যায় না।
  - রাখা হয়: App server, Database, cache।

💡 **Tip:** "Public IP থাকলেই public subnet না — IGW route না থাকলে traffic যাবে না।"

---

### Q5. Scalability vs Elasticity

- **Scalability** — বাড়তি load সামলানোর জন্য system-এর resource **বাড়ানোর ক্ষমতা** (long-term growth, planned)। Vertical বা horizontal।
- **Elasticity** — demand অনুযায়ী resource **automatically বাড়া এবং কমা** (short-term, real-time)। Load কমলে resource ছেড়ে দিয়ে খরচ বাঁচায়।

| | Scalability | Elasticity |
|---|---|---|
| দিক | মূলত বাড়ানো | বাড়ানো + কমানো |
| সময় | Long-term, planned | Real-time, automatic |
| AWS উদাহরণ | বড় instance type, আরও node যোগ | Auto Scaling Group, Lambda, DynamoDB on-demand |

উদাহরণ: E-commerce সাইট Black Friday-তে ১০টা থেকে ৫০টা instance-এ গেল, পরদিন আবার ১০টায় নামল → elasticity।

---

### Q6. Vertical vs Horizontal scaling — AWS কীভাবে support করে?

- **Vertical scaling (Scale Up/Down)** — একই machine-কে বড়/ছোট করা (CPU, RAM বাড়ানো)।
  - AWS: EC2 instance type change (`t3.medium → m5.xlarge`, stop→change→start), RDS instance class modify, EBS volume size/IOPS বাড়ানো (Elastic Volumes)।
  - ✅ সহজ, app change লাগে না। ❌ Hardware limit আছে, সাধারণত downtime, single point of failure।
- **Horizontal scaling (Scale Out/In)** — আরও machine যোগ/বাদ দেওয়া।
  - AWS: Auto Scaling Group + ELB, RDS Read Replicas, DynamoDB partitions, ECS/EKS task/pod scaling, Aurora replicas, Lambda concurrency।
  - ✅ প্রায় unlimited, HA, fault-tolerant। ❌ App-কে **stateless** হতে হয় (session → ElastiCache/DynamoDB)।

💡 **Tip:** Cloud-native design-এ horizontal scaling preferred।

---

## 💻 EC2 & Compute

### Q7. EC2 pricing models — কখন কোনটা?

| Model | Discount | Commitment | কখন ব্যবহার |
|---|---|---|---|
| **On-Demand** | 0% | নেই | Short-term, unpredictable workload, dev/test, নতুন app |
| **Reserved Instances (RI)** | ~৭২% পর্যন্ত | ১ বা ৩ বছর, specific instance family/region | Steady-state 24/7 workload (DB server) |
| **Savings Plans** | ~৭২% পর্যন্ত | ১/৩ বছর, $/hour commit | Steady usage কিন্তু flexibility লাগবে (Compute SP: EC2+Fargate+Lambda, যেকোনো region/family) |
| **Spot** | ~৯০% পর্যন্ত | নেই, কিন্তু **২ মিনিট notice-এ interrupt** হতে পারে | Fault-tolerant, stateless: batch, CI/CD, big data, rendering |
| **Dedicated Host** | — | On-demand/reserved | BYOL license (per-socket/core), compliance |
| **Dedicated Instance** | — | — | Hardware isolation লাগবে কিন্তু host control লাগবে না |
| **Capacity Reservation** | — | — | নির্দিষ্ট AZ-এ capacity guarantee (discount নেই, RI/SP-এর সাথে combine করা যায়) |

- RI payment: All Upfront > Partial > No Upfront (discount ক্রমানুসারে কম)। Standard RI (বেশি discount, কম flexible) vs Convertible RI (family change করা যায়)।

💡 **Best practice mix:** Baseline → Savings Plan/RI, spikes → On-Demand, batch → Spot।

---

### Q8. EC2 instance vs Lambda function — কখন কোনটা?

| | EC2 | Lambda |
|---|---|---|
| Model | Virtual server (IaaS) | Serverless function (FaaS) |
| Management | OS, patch, scaling আপনার | সব AWS-এর |
| Runtime limit | Unlimited | Max **15 মিনিট** |
| Memory | TB পর্যন্ত | 128 MB – 10 GB |
| Scaling | ASG দিয়ে configure করতে হয় | Automatic, per request |
| Billing | Running থাকলেই (per second) | Request সংখ্যা + duration (ms) × memory |
| State | Stateful হতে পারে | Stateless |
| Cold start | নেই | আছে |

- **Lambda বাছুন:** Event-driven (S3 upload, SQS, API Gateway), short task, অনিয়মিত traffic, দ্রুত ship করতে চান।
- **EC2 বাছুন:** Long-running process, full OS control, special software/GPU, steady high traffic (তখন EC2 সস্তা হয়), persistent connection (WebSocket server, game server)।

---

### Q9. AMI (Amazon Machine Image) কী?

EC2 instance launch করার **template/blueprint**। এতে থাকে:
- Root volume-এর template (OS + pre-installed software + config)
- Launch permission (কে ব্যবহার করতে পারবে: private, shared, public)
- Block device mapping (কোন EBS volume attach হবে)

**Types:** AWS-provided (Amazon Linux, Ubuntu), AWS Marketplace AMI, Community AMI, **Custom AMI** (নিজে বানানো)।

**Key points:**
- AMI **region-specific** — অন্য region-এ ব্যবহার করতে **copy** করতে হয়।
- Custom AMI = "Golden AMI" → দ্রুত boot, consistent config (Auto Scaling-এ কাজে লাগে)।
- EBS-backed AMI তৈরি হলে পেছনে EBS snapshot থাকে।
- Tool: EC2 Image Builder দিয়ে AMI pipeline automate।

---

### Q10. Auto Scaling Group (ASG) — কীভাবে কাজ করে, কী trigger করে?

ASG = একদল EC2 instance যাদের সংখ্যা automatically manage হয়।

**Config:**
- **Launch Template** (AMI, instance type, SG, user data)
- **Min / Desired / Max** capacity
- **Subnets (multi-AZ)** — AZ জুড়ে balance করে
- ELB target group attach → নতুন instance auto register

**Scaling triggers/policies:**
1. **Target Tracking** — "CPU গড়ে ৫০% রাখো" (সবচেয়ে সহজ, recommended)।
2. **Step Scaling** — CloudWatch alarm-এর মাত্রা অনুযায়ী ধাপে ধাপে (CPU>70% → +2, >90% → +4)।
3. **Simple Scaling** — একটা alarm → একটা action, তারপর cooldown।
4. **Scheduled Scaling** — নির্দিষ্ট সময়ে (প্রতি সোমবার ৯টায় desired=10)।
5. **Predictive Scaling** — ML দিয়ে history দেখে আগেই scale।

**Health check:** EC2 status check বা ELB health check fail → instance terminate করে নতুন launch (self-healing)।

**অন্যান্য:** Cooldown/warm-up period, Lifecycle hooks (launch/terminate-এর আগে custom action), Termination policy (default: সবচেয়ে বেশি instance যে AZ-এ, সেখানে পুরনো launch template-এর instance আগে)।

---

### Q11. ALB vs NLB

| | Application Load Balancer | Network Load Balancer |
|---|---|---|
| OSI Layer | **Layer 7** (HTTP/HTTPS, gRPC, WebSocket) | **Layer 4** (TCP, UDP, TLS) |
| Routing | Path (`/api`), host (`api.x.com`), header, query string, method | শুধু port/protocol |
| Performance | ভালো, কিন্তু একটু বেশি latency | **Millions req/sec, ultra-low latency** |
| Static IP | না (DNS name) | **হ্যাঁ, প্রতি AZ-এ একটা static/Elastic IP** |
| Target | Instance, IP, **Lambda**, container | Instance, IP, ALB |
| Features | WAF integration, auth (Cognito/OIDC), redirect, fixed response | Client source IP preserve, PrivateLink-এর জন্য দরকার |

- **ALB**: Microservices, container, web app, content-based routing।
- **NLB**: Gaming, IoT, financial trading, non-HTTP protocol, static IP whitelisting লাগলে, PrivateLink service।
- (আরও: **Gateway Load Balancer** — Layer 3, 3rd-party firewall/IDS appliance-এর জন্য; Classic LB — legacy।)

---

### Q12. Lambda pricing ও cold start

**Pricing:**
1. **Requests**: প্রতি ১০ লাখ request ≈ $0.20
2. **Duration**: GB-second হিসাবে (memory × execution time, 1ms granularity)
3. Extra: Provisioned Concurrency, ephemeral storage > 512MB, data transfer
- Free tier: প্রতি মাসে ১M request + 400,000 GB-seconds।
- Memory বাড়ালে CPU-ও proportionally বাড়ে → অনেক সময় বেশি memory দিয়ে কম সময়ে শেষ হয়ে খরচ কমে (AWS Lambda Power Tuning দিয়ে বের করুন)।

**Cold start:**
- নতুন execution environment তৈরি হতে যে delay: container/microVM (Firecracker) চালু → runtime load → code download → init code (handler-এর বাইরের code) চালানো।
- কখন হয়: প্রথম invocation, idle থাকার পর, concurrency হঠাৎ বাড়লে।
- Warm start: আগের environment reuse → দ্রুত।

**Cold start কমানোর উপায়:**
- **Provisioned Concurrency** (environment আগে থেকে ready)
- **SnapStart** (Java, Python, .NET — snapshot থেকে resume)
- Package ছোট রাখা, কম dependency
- Lightweight runtime (Node/Python/Go vs Java)
- Heavy init (DB connection) handler-এর বাইরে রেখে reuse
- VPC-attached Lambda-তে এখন আর বড় penalty নেই (Hyperplane ENI)

---

### Q13. EC2 instance type — কীসের জন্য optimized, কীভাবে বাছবেন?

Naming: `m5.xlarge` → **m** = family, **5** = generation, **xlarge** = size। Extra letter: `g` = Graviton (ARM), `a` = AMD, `n` = network enhanced, `d` = local NVMe।

| Family | Optimized | Use case |
|---|---|---|
| **T, M** (General Purpose) | Balanced CPU/RAM; T = burstable (CPU credit) | Web server, small DB, dev/test |
| **C** (Compute) | High CPU ratio | Batch, gaming server, HPC, ML inference, video encoding |
| **R, X, z** (Memory) | High RAM | In-memory DB (Redis), SAP HANA, big data analytics |
| **I, D, H** (Storage) | High local IOPS/throughput (NVMe) | NoSQL DB, data warehouse, Elasticsearch, Kafka |
| **P, G, Trn, Inf** (Accelerated) | GPU / custom ML chip | ML training/inference, graphics rendering |
| **Hpc** | HPC | Scientific simulation |

**কীভাবে বাছবেন:**
1. Workload profile করুন (CPU-bound? memory-bound? I/O-bound?)
2. ছোট থেকে শুরু, CloudWatch metrics দেখে **right-size**
3. **AWS Compute Optimizer** recommendation নিন
4. Price-performance-এর জন্য **Graviton** বিবেচনা (~৪০% better)
5. Latest generation বেছে নিন (সস্তা + দ্রুত)

---

### Q14. ECS vs EKS vs Fargate

- **ECS (Elastic Container Service)** — AWS-এর নিজস্ব container **orchestrator**। সহজ, AWS-native (IAM, ALB, CloudWatch integration), control plane free। Concept: Cluster → Service → Task (Task Definition)।
- **EKS (Elastic Kubernetes Service)** — Managed **Kubernetes** control plane। Standard K8s API, portable (multi-cloud/hybrid), বড় ecosystem (Helm, operators)। Control plane-এর জন্য ~$0.10/hour charge। Learning curve বেশি।
- **Fargate** — Orchestrator না, এটা **serverless compute engine** (launch type) — ECS বা EKS দুটোর নিচেই চলে। EC2 server manage করতে হয় না; per task/pod vCPU+memory অনুযায়ী bill।

| প্রশ্ন | উত্তর |
|---|---|
| কে container schedule করবে? | ECS বা EKS |
| Container কোথায় চলবে? | EC2 (নিজে manage) বা Fargate (serverless) |

- **বাছাই:** AWS-only, simple → ECS + Fargate। K8s expertise/portability দরকার → EKS। Server manage করতে চান না → Fargate। GPU/special instance, খরচ optimize (Spot/RI) → EC2 launch type।

---

## 💾 Storage

### Q15. S3 storage classes

| Class | Availability | AZ | Min duration | Retrieval | Use case |
|---|---|---|---|---|---|
| **S3 Standard** | 99.99% | ≥3 | নেই | ms, free | Frequently accessed data, website, analytics |
| **Intelligent-Tiering** | 99.9% | ≥3 | নেই | ms | Unknown/changing access pattern — auto tier move (small monitoring fee, retrieval fee নেই) |
| **Standard-IA** | 99.9% | ≥3 | 30 দিন | ms, per-GB fee | কম access কিন্তু দরকারে দ্রুত (backup, DR) |
| **One Zone-IA** | 99.5% | **1** | 30 দিন | ms, fee | Re-creatable data, secondary backup (AZ গেলে data যাবে) |
| **Glacier Instant Retrieval** | 99.9% | ≥3 | 90 দিন | ms | Quarterly access archive (medical image) |
| **Glacier Flexible Retrieval** | 99.99% | ≥3 | 90 দিন | minutes–12 h (Expedited 1–5 min, Standard 3–5 h, Bulk 5–12 h) | Backup archive |
| **Glacier Deep Archive** | 99.99% | ≥3 | 180 দিন | 12–48 h | Compliance, ৭-১০ বছর retention — সবচেয়ে সস্তা |
| **S3 Express One Zone** | — | 1 | — | single-digit ms | Ultra-low latency, ML/analytics |

- Durability সবগুলোর **11 nines** (One Zone-এ single AZ-এর মধ্যে)।
- Lifecycle policy দিয়ে class-এর মধ্যে automatically transition।

---

### Q16. S3 durability (11 nines) — কীভাবে, এবং মানে কী?

**99.999999999% durability** মানে: ১ কোটি (10M) object রাখলে গড়ে **প্রতি ১০,০০০ বছরে ১টা object হারাতে পারে**।

**কীভাবে অর্জন করে:**
- Data automatically **কমপক্ষে ৩টা AZ-এ** একাধিক device-এ redundantly store (erasure coding)
- **Checksum** দিয়ে নিয়মিত data integrity যাচাই, corruption পেলে auto repair
- Lost redundancy দ্রুত detect করে re-replicate
- Write-এ success return করার আগেই multi-AZ-এ store নিশ্চিত

**Durability ≠ Availability:**
- Durability = data **হারাবে না**
- Availability = data **এখনই access করা যাবে** (Standard: 99.99% = বছরে ~৫৩ মিনিট unavailable হতে পারে)

⚠️ 11 nines **accidental delete বা overwrite থেকে রক্ষা করে না** → Versioning, MFA Delete, Object Lock, Replication লাগবে।

---

### Q17. EBS vs Instance Store

| | EBS | Instance Store |
|---|---|---|
| Type | Network-attached block storage | Host-এর physically attached disk (NVMe/SSD) |
| Persistence | Stop/terminate-এর পরও থাকে (DeleteOnTermination config) | **Ephemeral** — stop, terminate, hardware fail-এ data হারায় (reboot-এ থাকে) |
| Performance | ভালো (io2 Block Express: 256K IOPS) | **অত্যন্ত বেশি IOPS, lowest latency** |
| Snapshot | হ্যাঁ (S3-এ) | না |
| Detach/attach | হ্যাঁ (same AZ) | না |
| Resize | হ্যাঁ | না (instance type-এ fixed) |
| Cost | আলাদা charge | Instance price-এ included |

- **Instance store use:** Cache, buffer, scratch data, temp file, replicated data (Cassandra/Kafka cluster যেখানে replication আছে)।
- **EBS use:** Root volume, database, persistent যেকোনো data।

---

### Q18. EBS vs EFS vs S3 — কখন কোনটা?

| | EBS | EFS | S3 |
|---|---|---|---|
| Type | **Block** storage | **File** storage (NFS) | **Object** storage |
| Access | সাধারণত ১টা EC2 (একই AZ) — io1/io2 Multi-Attach ব্যতিক্রম | **হাজারো EC2/container/Lambda একসাথে, multi-AZ** | HTTP API দিয়ে যেকোনো জায়গা থেকে |
| Scope | AZ | Region | Region (global namespace) |
| Scaling | Size আগে provision | Auto grow/shrink, petabyte | Unlimited |
| Protocol | Disk mount | NFSv4 (Linux only; Windows → FSx) | REST/HTTPS |
| Cost | মাঝারি (provisioned GB) | বেশি (used GB) | সবচেয়ে সস্তা |
| Use case | OS boot volume, database, low-latency app | Shared content, CMS (WordPress), home directory, ML shared data | Backup, static website, data lake, media, log |

💡 মনে রাখার উপায়: **EBS = hard disk, EFS = shared network drive, S3 = Dropbox/Google Drive (API দিয়ে)।**

---

### Q19. S3 bucket policy vs IAM policy

| | IAM Policy | S3 Bucket Policy |
|---|---|---|
| Type | **Identity-based** | **Resource-based** |
| কোথায় attach | User, Group, Role | Bucket |
| `Principal` element | নেই (যার সাথে attach সে-ই principal) | **আবশ্যক** — কাকে access দেওয়া হচ্ছে |
| Cross-account | সরাসরি না (role assume লাগে) | হ্যাঁ, অন্য account-কে সরাসরি access দিতে পারে |
| Anonymous/public | না | হ্যাঁ (`"Principal": "*"`) |
| Size limit | 6,144 chars (managed) | 20 KB |

**কখন কোনটা:**
- IAM policy → "এই user/role কোন কোন AWS resource-এ কী করতে পারবে" (user-কেন্দ্রিক)।
- Bucket policy → "এই bucket-এ কে কে access পাবে" (resource-কেন্দ্রিক), cross-account, VPC endpoint/IP restrict, HTTPS enforce (`aws:SecureTransport`)।

**Evaluation:** Same account-এ দুটোর যেকোনো একটায় Allow থাকলেই যথেষ্ট (explicit Deny না থাকলে)। Cross-account-এ **দুই দিকেই** Allow লাগবে।

---

### Q20. S3 Versioning ও Lifecycle policy-র সাথে সম্পর্ক

**Versioning:**
- Bucket-level setting: Unversioned → Enabled → Suspended (একবার enable করলে আর disable করা যায় না, শুধু suspend)।
- প্রতিটা overwrite নতুন **version ID** তৈরি করে; পুরনো version থাকে।
- Delete করলে আসলে **delete marker** বসে — object লুকায়, মুছে না। Marker মুছলে object ফিরে আসে।
- নির্দিষ্ট version ID দিয়ে delete করলে সেটা permanently মুছে যায়।
- প্রতিটা version-এর জন্য storage cost লাগে।

**Lifecycle-এর সাথে interaction:**
- **Current version**-এর জন্য rule: `Transition` (৩০ দিন পর Standard-IA, ৯০ দিন পর Glacier), `Expiration` (current-কে noncurrent বানিয়ে delete marker বসায়)।
- **Noncurrent version**-এর জন্য rule: `NoncurrentVersionTransition`, `NoncurrentVersionExpiration` (যেমন: noncurrent হওয়ার ৩০ দিন পর permanently delete, শেষ ৩টা version রাখো)।
- **Expired object delete marker** cleanup ও **incomplete multipart upload abort** করার rule।

💡 Versioning + lifecycle ছাড়া versioned bucket-এর cost অনিয়ন্ত্রিতভাবে বাড়ে।

---

### Q21. S3 pre-signed URL ও use case

**Pre-signed URL** = এমন একটা URL যেটা কোনো IAM principal-এর credential দিয়ে **sign করা** এবং নির্দিষ্ট সময়ের জন্য (**expiry**) valid। যার কাছে URL আছে সে AWS credential ছাড়াই ঐ object **GET (download) বা PUT (upload)** করতে পারে।

- Permission = যে sign করেছে তার permission-এর সমান।
- Expiry: SDK/CLI দিয়ে max 7 দিন (IAM user); role credential হলে session শেষে expire।
- Bucket private থাকে।

```bash
aws s3 presign s3://my-bucket/report.pdf --expires-in 3600
```

**Use cases:**
- User-কে private file download করতে দেওয়া (paid content, invoice, video)
- **Browser থেকে সরাসরি S3-এ upload** — backend শুধু URL generate করে, বড় file app server দিয়ে যায় না → server load ও cost কমে
- Temporary share link

(CloudFront-এর সাথে একই কাজে: **CloudFront signed URL/cookies**।)

---

## 🌐 Networking (VPC)

### Q22. VPC কী, এবং এর core components

**VPC (Virtual Private Cloud)** = AWS-এর ভেতরে আপনার নিজস্ব **logically isolated virtual network**। নিজের IP range (CIDR, যেমন `10.0.0.0/16`), subnet, routing, firewall সব আপনার control-এ। VPC **region-scoped**, subnet **AZ-scoped**।

**Core components:**
- **Subnet** — VPC CIDR-এর একটা অংশ, একটা AZ-এ থাকে (public/private)। প্রতি subnet-এ AWS ৫টা IP reserve করে।
- **Route Table** — subnet থেকে traffic কোথায় যাবে তা নির্ধারণ করে। প্রতিটা subnet একটা route table-এর সাথে associated; `local` route সবসময় থাকে (VPC-র ভেতরে যোগাযোগ)।
- **Internet Gateway (IGW)** — VPC ↔ internet two-way যোগাযোগ; horizontally scaled, HA, free। VPC প্রতি ১টা।
- **NAT Gateway** — private subnet-এর instance outbound internet (update, API call) করতে পারে, কিন্তু বাইরে থেকে inbound connection আসতে পারে না।
- আরও: **Security Group, NACL, Elastic IP, VPC Endpoint, VPC Peering, Transit Gateway, VPN/Direct Connect, Flow Logs, DHCP option set**।

```
Internet ⇄ IGW ⇄ [Public Subnet: ALB, NAT GW] ⇄ [Private Subnet: App] ⇄ [Private Subnet: DB]
```

---

### Q23. NAT Gateway vs Internet Gateway

| | Internet Gateway | NAT Gateway |
|---|---|---|
| Direction | **Inbound + Outbound** (two-way) | **শুধু Outbound** (private → internet) |
| কে ব্যবহার করে | Public subnet-এর resource (public IP সহ) | Private subnet-এর resource |
| কোথায় থাকে | VPC-তে attach | **Public subnet-এ** (EIP সহ), AZ-scoped |
| Route | `0.0.0.0/0 → igw` (public RT) | `0.0.0.0/0 → nat` (private RT) |
| Cost | Free | Hourly + per-GB processing charge |
| HA | Built-in | AZ-level — HA-র জন্য **প্রতি AZ-এ একটা** |

- NAT Gateway নিজেও internet-এ যেতে IGW ব্যবহার করে।
- বিকল্প: **NAT Instance** (নিজে manage, সস্তা কিন্তু HA নেই, source/dest check disable করতে হয়)।
- IPv6-এর জন্য: **Egress-only Internet Gateway**।

---

### Q24. Security Group vs Network ACL

| | Security Group | Network ACL |
|---|---|---|
| Level | **Instance/ENI level** | **Subnet level** |
| State | **Stateful** — inbound allow করলে response auto allow | **Stateless** — inbound ও outbound দুটোই আলাদা rule লাগে (ephemeral ports 1024–65535) |
| Rules | **শুধু Allow** | **Allow + Deny** |
| Evaluation | সব rule একসাথে evaluate | **Rule number ক্রমে** (ছোট আগে), প্রথম match-এ থামে |
| Default | Inbound সব deny, outbound সব allow | Default NACL: সব allow; Custom NACL: সব deny |
| Reference | অন্য SG-কে source হিসেবে reference করা যায় | শুধু CIDR |

- **Use:** SG → primary firewall (app tier শুধু ALB-এর SG থেকে traffic নেবে)। NACL → subnet-wide guardrail, নির্দিষ্ট IP **block** করা।

💡 "নির্দিষ্ট malicious IP block করতে হবে" → **NACL** (SG-তে deny rule নেই)।

---

### Q25. VPC Peering ও এর limitations

**VPC Peering** = দুটো VPC-কে private IP দিয়ে connect করা, যেন একই network। AWS backbone দিয়ে traffic যায়, internet দিয়ে না। Same/cross-account, same/cross-region (inter-region peering) হতে পারে।

**Setup:** Request → Accept → **দুই দিকের route table update** → SG/NACL-এ allow।

**Limitations:**
- ❌ **No transitive peering**: A↔B, B↔C থাকলে A→C যাবে না। A↔C আলাদা peering লাগবে।
- ❌ **CIDR overlap** করা যাবে না।
- ❌ Edge-to-edge routing নেই — peered VPC-র IGW, NAT GW, VPN, Direct Connect ব্যবহার করা যায় না।
- Full mesh-এ connection সংখ্যা = **n(n-1)/2** → ১০টা VPC = ৪৫টা peering → manage করা কঠিন।
- VPC প্রতি peering limit (default 50, max 125)।
- ✅ Data transfer cost কম, কোনো bandwidth bottleneck/single point of failure নেই।

---

### Q26. Transit Gateway — কেন VPC peering-এর বদলে?

**Transit Gateway (TGW)** = regional **hub-and-spoke** network router। সব VPC, VPN, Direct Connect একটা central hub-এ connect হয়।

**Peering-এর চেয়ে কেন ভালো (at scale):**
- **Transitive routing** support করে — সব VPC একে অপরের সাথে কথা বলতে পারে TGW হয়ে।
- n টা VPC → **n টা attachment** (peering-এ n(n-1)/2)।
- Centralized routing: **TGW route table** দিয়ে segmentation (prod ↔ dev isolate)।
- Hybrid: on-prem VPN/Direct Connect একবার TGW-তে connect করলেই সব VPC access পায়।
- Inter-region TGW peering, RAM দিয়ে multi-account share।
- Centralized egress (একটা shared NAT VPC), centralized inspection (firewall VPC)।
- হাজারো VPC scale করে।

**Trade-off:** Per-attachment hourly + per-GB data processing charge; peering-এ processing charge নেই। ২-৩টা VPC হলে peering যথেষ্ট ও সস্তা।

---

### Q27. Route 53 routing policies

| Policy | কীভাবে কাজ করে | Use case |
|---|---|---|
| **Simple** | একটা record → এক বা একাধিক value (random), health check নেই | Single server |
| **Weighted** | Weight অনুযায়ী traffic ভাগ (70/30) | A/B test, canary, gradual migration |
| **Latency-based** | User-এর জন্য সবচেয়ে কম latency-র **region**-এ পাঠায় | Global multi-region app |
| **Failover** | Primary healthy → primary; না হলে secondary (health check দরকার) | Active-passive DR |
| **Geolocation** | User-এর **location** (country/continent) অনুযায়ী | Localized content, compliance, licensing restriction |
| **Geoproximity** | Resource-এর location + **bias** দিয়ে traffic shift (Traffic Flow) | Region-এর মধ্যে traffic ভার ঠেলা |
| **Multivalue Answer** | Healthy record থেকে ৮টা পর্যন্ত return | Simple client-side load balancing + health check |
| **IP-based** | Client-এর CIDR অনুযায়ী | ISP-specific routing |

- **Health checks** দিয়ে unhealthy endpoint বাদ দেয় (failover, weighted, latency সবখানে ব্যবহারযোগ্য)।
- Latency ≠ Geolocation: latency = দ্রুততম, geolocation = কোথা থেকে আসছে।

---

### Q28. Public IP vs Elastic IP

| | Public IP (auto-assigned) | Elastic IP |
|---|---|---|
| Nature | **Dynamic** | **Static** |
| Stop/Start | Stop করলে **হারায়**, start করলে নতুন IP | থেকে যায় |
| Owner | AWS pool থেকে ধার | আপনার account-এ allocate করা |
| Remap | না | হ্যাঁ — এক instance থেকে আরেকটায় দ্রুত সরানো যায় (failover) |
| Cost | ২০২৪ থেকে সব public IPv4-এর জন্য ~$0.005/hr | একই charge (attach থাকুক বা না থাকুক) |
| Limit | — | Region প্রতি default ৫টা |

💡 Best practice: EIP কম ব্যবহার করুন — ALB/NLB + Route 53 DNS ব্যবহার করুন।

---

## 💽 Databases

### Q29. RDS vs DynamoDB — কখন কোনটা?

| | RDS | DynamoDB |
|---|---|---|
| Type | **Relational (SQL)** — MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora | **NoSQL** key-value + document |
| Schema | Fixed schema | Schema-less (শুধু key define) |
| Query | Complex SQL, **JOIN**, aggregation | Key দিয়ে access; JOIN নেই; limited query (index দিয়ে) |
| Transactions | Full ACID | ACID transaction support আছে (TransactWriteItems) কিন্তু limited |
| Scaling | Vertical + read replica | **Horizontal, প্রায় unlimited, auto** |
| Performance | ভালো, load বাড়লে কমে | **Single-digit ms** যেকোনো scale-এ |
| Management | Managed কিন্তু instance আছে | Fully **serverless** |
| Cost model | Instance hours + storage | Read/write capacity বা per request + storage |

- **RDS:** Complex relationship, reporting, existing SQL app, ERP/CRM, financial transaction।
- **DynamoDB:** Massive scale, known access pattern, session store, gaming leaderboard, IoT, shopping cart, serverless app।

---

### Q30. RDS Multi-AZ vs Read Replicas

| | Multi-AZ | Read Replica |
|---|---|---|
| উদ্দেশ্য | **High Availability / DR** | **Read scalability / performance** |
| Replication | **Synchronous** | **Asynchronous** (replication lag থাকতে পারে) |
| Standby readable? | না (classic Multi-AZ instance); Multi-AZ **DB Cluster** (২ readable standby) হলে হ্যাঁ | হ্যাঁ, read query চালানো যায় |
| Failover | **Automatic** (~60–120s), একই DNS endpoint | Manual **promote** (তখন standalone DB হয়ে যায়) |
| Location | Same region, ভিন্ন AZ | Same AZ, cross-AZ, বা **cross-region** |
| সংখ্যা | ১ standby (বা ২ cluster-এ) | ১৫টা পর্যন্ত (engine অনুযায়ী) |
| Backup | Standby থেকে নেওয়া হয় → primary-তে I/O impact কম | — |

💡 দুটো একসাথে ব্যবহার করা যায়: Multi-AZ (HA) + Read Replica (scale), এবং Read Replica নিজেও Multi-AZ হতে পারে। Cross-region read replica = DR strategy।

---

### Q31. DynamoDB Partition key ও Sort key — performance-এ প্রভাব

- **Partition Key (PK / hash key)** — এর **hash value** দিয়ে ঠিক হয় item কোন physical **partition**-এ যাবে।
- **Sort Key (SK / range key)** — optional। একই PK-এর মধ্যে item গুলো SK অনুযায়ী sorted থাকে।
- **Primary key** = শুধু PK (simple) বা **PK + SK (composite)**। Composite হলে PK+SK মিলে unique।

**Performance-এ প্রভাব:**
- প্রতিটা partition-এর limit: ~**3,000 RCU / 1,000 WCU / 10 GB**।
- **High-cardinality PK** (userId, orderId) → data সমানভাবে ছড়ায় → ভালো performance।
- **Low-cardinality PK** (status = "active", date) → **hot partition** → throttling।
- Hot partition সমাধান: **write sharding** (PK-তে random suffix যোগ), better key design; DynamoDB **adaptive capacity** কিছুটা সাহায্য করে।
- Sort key দিয়ে efficient **range query**: `begins_with`, `between`, `>`, `<` (যেমন `PK=user#123, SK begins_with "order#2024"`)।
- **Query** (PK দিয়ে) দ্রুত ও সস্তা; **Scan** (পুরো টেবিল) ধীর ও ব্যয়বহুল — এড়িয়ে চলুন।
- অন্য attribute দিয়ে query → **GSI** (ভিন্ন PK/SK, যেকোনো সময় বানানো যায়) বা **LSI** (same PK, ভিন্ন SK, table তৈরির সময়ই)।

💡 DynamoDB design = **access pattern আগে, table পরে** (single-table design)।

---

### Q32. DynamoDB read/write capacity — Provisioned vs On-Demand

**Capacity unit:**
- **1 RCU** = প্রতি সেকেন্ডে ১টা **strongly consistent** read (৪ KB পর্যন্ত) **অথবা** ২টা **eventually consistent** read। Transactional read = 2 RCU।
- **1 WCU** = প্রতি সেকেন্ডে ১টা write (১ KB পর্যন্ত)। Transactional write = 2 WCU।
- উদাহরণ: ১০টা item/sec, প্রতিটা ৬ KB, strongly consistent → ceil(6/4)=2 × 10 = **20 RCU**।

| | Provisioned | On-Demand |
|---|---|---|
| কীভাবে | RCU/WCU আগে set করেন; **Auto Scaling** দিয়ে target utilization অনুযায়ী বাড়ে-কমে | কিছু set করতে হয় না, request অনুযায়ী instant scale |
| Billing | Provisioned capacity per hour (use করুন বা না করুন) | Per read/write **request unit** |
| Cost | Predictable traffic-এ **সস্তা**; Reserved capacity দিয়ে আরও কম | Per request দামি (কিন্তু 2024-এ দাম ~৫০% কমেছে) |
| Throttling | Limit পার হলে `ProvisionedThroughputExceededException` (burst capacity কিছুটা বাঁচায়) | প্রায় নেই (আগের peak-এর 2x পর্যন্ত instant) |
| Use case | Steady, predictable traffic | নতুন app, unpredictable/spiky, dev/test |

- দুটোর মধ্যে ২৪ ঘণ্টায় একবার switch করা যায়।

---

### Q33. Aurora vs standard RDS (MySQL/PostgreSQL)

**Aurora** = AWS-এর নিজস্ব cloud-native relational DB engine, **MySQL ও PostgreSQL compatible**।

| | Standard RDS MySQL/PostgreSQL | Aurora |
|---|---|---|
| Performance | Baseline | MySQL-এর **~5x**, PostgreSQL-এর **~3x** throughput |
| Storage | EBS volume, আগে provision | **Shared distributed cluster volume**, auto grow 10GB → 128 TB |
| Durability | EBS (single AZ; Multi-AZ-এ standby) | **৩ AZ-এ ৬টা copy** — ২টা copy হারালেও write চলে, ৩টা হারালেও read চলে; self-healing |
| Replicas | ৫–১৫টা, async (replication lag seconds) | **১৫টা replica**, shared storage → lag **ms-এ** |
| Failover | ~1–2 মিনিট | **<30 seconds** (replica promote) |
| Extra | — | **Aurora Serverless v2** (auto scale ACU), **Global Database** (<1s cross-region lag), Backtrack, Fast clone, Reader endpoint auto load balance |
| Cost | কম | ~২০% বেশি instance cost, কিন্তু I/O-optimized option |

- **Aurora:** High performance, HA, বড় scale, global app।
- **Standard RDS:** ছোট workload, খরচ কম রাখতে, specific engine version/feature দরকার।

---

### Q34. ElastiCache — Redis vs Memcached

**ElastiCache** = Managed **in-memory cache** service → DB-র সামনে বসিয়ে read latency microsecond-এ নামানো ও DB load কমানো।

**Use case:** DB query cache, **session store**, leaderboard, rate limiting, pub/sub, real-time analytics।

**Caching patterns:** **Lazy loading (cache-aside)** — miss হলে DB থেকে এনে cache-এ রাখা; **Write-through** — DB-তে write-এর সাথে cache update; **TTL** দিয়ে stale data এড়ানো।

| | Redis (বা Valkey) | Memcached |
|---|---|---|
| Data types | String, Hash, List, Set, Sorted Set, Stream, Geo | শুধু simple key-value (string) |
| Persistence | হ্যাঁ (snapshot/AOF, backup/restore) | না |
| Replication / HA | হ্যাঁ — Multi-AZ, auto failover, read replica | না |
| Threading | মূলত single-threaded (I/O multi-threaded) | **Multi-threaded** |
| Advanced | Pub/Sub, Lua script, transaction, Sorted Set (leaderboard), Global Datastore | — |
| Scaling | Cluster mode (sharding) | Node যোগ করে horizontal |

- **Redis বাছুন:** প্রায় সব ক্ষেত্রে — HA, persistence, complex data type লাগলে।
- **Memcached বাছুন:** Simplest cache, multi-threaded, data হারালে সমস্যা নেই।

---

## 🔐 Security & IAM

### Q35. IAM Role vs IAM User

| | IAM User | IAM Role |
|---|---|---|
| কী | একজন ব্যক্তি/application-এর **permanent identity** | **Assume** করা যায় এমন identity, কারো সাথে স্থায়ীভাবে বাঁধা নয় |
| Credential | **Long-term**: password (console) + access key (CLI/API) | **Temporary** credential (STS), auto-rotate, ১৫ মিনিট–১২ ঘণ্টা |
| কে ব্যবহার করে | নির্দিষ্ট মানুষ | AWS service (EC2, Lambda), অন্য account, federated user (SSO), web identity |
| Trust policy | নেই | **আছে** — কে assume করতে পারবে |

**Best practice:**
- Application-এর জন্য access key hardcode না করে **role** (EC2 instance profile, Lambda execution role)।
- মানুষের জন্য **IAM Identity Center (SSO)** + role; IAM user কম ব্যবহার।
- Cross-account access → role।

---

### Q36. IAM policy evaluation logic

মূল নিয়ম:
1. **Default = Implicit Deny** — কিছু allow না থাকলে সব deny।
2. **Explicit Deny সবসময় জেতে** — কোথাও Deny থাকলে, অন্য যত Allow-ই থাকুক, deny।
3. **Explicit Allow** implicit deny-কে override করে।

**Evaluation flow (একই account):**
```
Request
 → কোনো policy-তে explicit Deny? ── হ্যাঁ → DENY
 → Organizations SCP / RCP allow করে? ── না → DENY
 → Resource-based policy allow করে? ── হ্যাঁ → ALLOW (কিছু ক্ষেত্রে)
 → Identity-based policy allow করে? ── না → DENY
 → Permissions boundary allow করে? ── না → DENY
 → Session policy (assume role-এ) allow করে? ── না → DENY
 → ALLOW
```
- Effective permission = **SCP ∩ Permissions Boundary ∩ Identity policy** (এবং session policy)।
- **Cross-account:** Caller-এর identity policy **এবং** target-এর resource policy — দুটোতেই Allow লাগবে।
- Debug tool: **IAM Policy Simulator**, CloudTrail-এ `AccessDenied`।

---

### Q37. Principle of Least Privilege — AWS-এ কীভাবে implement?

**সংজ্ঞা:** প্রত্যেক identity শুধু **কাজের জন্য যতটুকু দরকার ঠিক ততটুকু permission**, ততক্ষণের জন্য পাবে।

**Implementation:**
- `*` action/resource এড়িয়ে নির্দিষ্ট **action + resource ARN + condition** দিয়ে policy লেখা।
- AWS managed policy দিয়ে শুরু, তারপর **customer managed** policy দিয়ে narrow।
- **IAM Access Analyzer** — CloudTrail থেকে actual usage দেখে least-privilege policy **generate** করে; unused access ও public/cross-account access খুঁজে দেয়।
- **Last accessed information** দেখে unused permission/role সরানো।
- **Role + temporary credential**, long-term access key নয়।
- **Permissions boundary** (delegated admin-এর জন্য max limit), **SCP** (account-level guardrail)।
- **Condition keys**: `aws:SourceIp`, `aws:MultiFactorAuthPresent`, `aws:RequestedRegion`, tag-based (ABAC)।
- Group-based permission, নিয়মিত review/audit।
- Break-glass/JIT access (Identity Center temporary elevated access)।

---

### Q38. IAM (identity-based) policy vs Resource-based policy

| | Identity-based | Resource-based |
|---|---|---|
| Attach | User/Group/Role-এ | Resource-এ (S3 bucket, SQS queue, SNS topic, KMS key, Lambda, ECR, Secrets Manager) |
| Principal | Implicit (যার সাথে attach) | **Explicitly** `Principal` দিতে হয় |
| প্রশ্নের উত্তর দেয় | "এই identity কী করতে পারবে?" | "এই resource-এ কে কী করতে পারবে?" |
| Cross-account | Role assume করতে হয় (নিজের permission ছেড়ে দেয়) | সরাসরি access দেওয়া যায় (caller নিজের permission রাখে) |
| Managed/Inline | Both | শুধু inline |

- **Trust policy** (role-এ) নিজেও এক ধরনের resource-based policy।
- KMS key policy বিশেষ: key policy-তে allow না থাকলে IAM policy দিয়েও access পাবেন না।

---

### Q39. AWS KMS কী, S3 ও EBS-এর সাথে কীভাবে integrate?

**KMS (Key Management Service)** = Managed service যেটা encryption key তৈরি, store, rotate ও control করে। Key গুলো **FIPS 140-3 validated HSM**-এ থাকে, কখনো plaintext হিসেবে বের হয় না। প্রতিটা key usage **CloudTrail**-এ log হয়।

**Envelope encryption (মূল ধারণা):**
1. Service KMS-কে `GenerateDataKey` call করে → পায় plaintext data key + encrypted data key।
2. Plaintext data key দিয়ে data encrypt করে, তারপর plaintext key memory থেকে মুছে ফেলে।
3. Encrypted data key data-র সাথে store হয়।
4. Decrypt-এর সময় encrypted data key KMS-এ পাঠিয়ে plaintext ফেরত নেয়।
- কারণ: KMS সরাসরি শুধু ৪ KB পর্যন্ত encrypt করে; বড় data local-এ দ্রুত encrypt হয়।

**S3:**
- **SSE-S3** (S3-managed key, default এখন), **SSE-KMS** (KMS key, audit + key policy control), **DSSE-KMS** (dual-layer), **SSE-C** (customer-provided key)।
- SSE-KMS-এ **S3 Bucket Key** ব্যবহার করলে KMS request cost ~৯৯% কমে।
- Bucket policy দিয়ে encryption enforce করা যায়।

**EBS:**
- Volume create-এর সময় KMS key দিয়ে encrypt → data at rest, instance ↔ volume data in transit, **snapshot**, এবং snapshot থেকে বানানো volume সব encrypted।
- Account-level **"EBS encryption by default"** চালু করা যায়।
- Unencrypted volume encrypt করতে: snapshot → encrypted copy → নতুন volume।

---

### Q40. Secrets Manager vs Systems Manager Parameter Store

| | Secrets Manager | SSM Parameter Store |
|---|---|---|
| উদ্দেশ্য | **Secrets** (DB password, API key) | Config data + secrets (SecureString) |
| **Automatic rotation** | ✅ Built-in (RDS, Redshift, DocumentDB) + Lambda দিয়ে custom | ❌ Native নেই (নিজে EventBridge + Lambda বানাতে হবে) |
| Cost | ~$0.40/secret/month + API call | **Standard tier free**; Advanced tier $0.05/param/month |
| Size | 64 KB | 4 KB (standard) / 8 KB (advanced) |
| Cross-account | ✅ Resource policy দিয়ে | Advanced tier-এ শেয়ার (RAM) |
| Cross-region replication | ✅ | ❌ |
| Hierarchy | — | ✅ `/prod/app/db_url` path, version, TTL policy (advanced) |
| Encryption | সবসময় KMS | SecureString-এ KMS |

- **Secrets Manager:** DB credential যেগুলো rotate করতে হবে, compliance।
- **Parameter Store:** App config, feature flag, সস্তা simple secret।
- Parameter Store থেকে Secrets Manager-এর secret reference করা যায়।

---

### Q41. IAM-এ MFA কীভাবে কাজ করে, কীভাবে enforce করবেন?

**MFA (Multi-Factor Authentication)** = password (যা জানেন) + device-generated code (যা আছে)।

**Supported device:** Virtual MFA app (Google Authenticator, Authy), **FIDO2 passkey/security key** (YubiKey), Hardware TOTP token। প্রতি user-এ ৮টা পর্যন্ত MFA device।

**Enforce করার উপায়:**
1. **Root account-এ MFA** অবশ্যই (এখন AWS বাধ্যতামূলক করছে)।
2. **IAM policy condition** — MFA না থাকলে সব deny:
```json
{
  "Effect": "Deny",
  "NotAction": ["iam:CreateVirtualMFADevice","iam:EnableMFADevice","iam:ListMFADevices","sts:GetSessionToken","iam:ChangePassword"],
  "Resource": "*",
  "Condition": { "BoolIfExists": { "aws:MultiFactorAuthPresent": "false" } }
}
```
3. Sensitive action-এ `aws:MultiFactorAuthAge` দিয়ে সাম্প্রতিক MFA চাওয়া।
4. **Role trust policy**-তে MFA condition → assume করতে MFA লাগবে।
5. CLI-তে MFA: `aws sts get-session-token --serial-number arn:... --token-code 123456`।
6. **S3 MFA Delete** — version permanently delete করতে MFA।
7. **IAM Identity Center**-এ MFA বাধ্যতামূলক setting।
8. **AWS Config rule** (`iam-user-mfa-enabled`, `root-account-mfa-enabled`) দিয়ে compliance monitor।

---

### Q42. AWS Organizations ও Service Control Policies (SCP)

**AWS Organizations** = একাধিক AWS account centrally manage করার service।
- Structure: **Management account** (root) → **Organizational Units (OU)** → Member accounts।
- Features: **Consolidated billing** (এক bill, volume discount, RI/SP sharing), programmatic account creation, policy-based control, service integration (CloudTrail org trail, GuardDuty, Security Hub delegated admin)।

**SCP (Service Control Policy):**
- Account/OU-র জন্য **maximum permission guardrail**। নিজে কিছু **grant করে না**, শুধু সীমা ঠিক করে।
- Effective permission = **SCP ∩ IAM policy**।
- Member account-এর **root user সহ সবার** উপর প্রযোজ্য; **Management account-এ প্রযোজ্য নয়**; service-linked role-এ নয়।
- Inheritance: Root → OU → Account — উপরের SCP নিচে ফিল্টার করে।
- Strategy: **Deny list** (default `FullAWSAccess` রেখে নির্দিষ্ট Deny) বা **Allow list**।

**উদাহরণ SCP:** নির্দিষ্ট region বাদে সব deny, CloudTrail বন্ধ করা নিষেধ, root user ব্যবহার নিষেধ, organization ছেড়ে যাওয়া নিষেধ।

(এছাড়াও: **RCP** — Resource Control Policies, **Tag policies**, **Backup policies**; **Control Tower** দিয়ে landing zone automate।)

---

### Q43. AWS WAF কী, কীভাবে application রক্ষা করে?

**WAF (Web Application Firewall)** = **Layer 7** firewall যেটা HTTP/HTTPS request inspect করে filter করে।

**Deploy করা যায়:** CloudFront, ALB, API Gateway, AppSync, Cognito User Pool, App Runner, Verified Access।

**Components:**
- **Web ACL** → এর মধ্যে **Rules / Rule groups** → Action: **Allow, Block, Count, CAPTCHA, Challenge**।
- Rule condition: IP set, geo match, header/body/query/URI string match, regex, size constraint, **SQL injection**, **XSS** detection।
- **Rate-based rule** — একটা IP থেকে ৫ মিনিটে N-এর বেশি request → block (brute force, Layer-7 DDoS)।
- **AWS Managed Rules** — OWASP Top 10 (Core rule set), Known bad inputs, IP reputation list, Bot Control, Account Takeover Prevention (ATP), Fraud Control।
- Marketplace rule groups।

**কী থেকে রক্ষা:** SQLi, XSS, bad bot, scraper, credential stuffing, HTTP flood, নির্দিষ্ট দেশ/IP থেকে traffic।

- Logging: CloudWatch Logs, S3, Kinesis Firehose।
- Multi-account management: **Firewall Manager**।
- Layer 3/4 DDoS-এর জন্য **Shield** (WAF-এর পরিপূরক)।

---

## ⚡ Serverless & Application Integration

### Q44. SQS vs SNS

| | SQS | SNS |
|---|---|---|
| Model | **Queue (Pull)** — consumer poll করে | **Pub/Sub (Push)** — subscriber-দের push করে |
| Delivery | একটা message **একজন consumer** process করে | একটা message **সব subscriber** পায় (fan-out) |
| Persistence | Message queue-তে থাকে (1 min – **14 দিন**, default 4 দিন) | Persist করে না — deliver করতে না পারলে (retry শেষে) হারায় (DLQ দেওয়া যায়) |
| Subscribers/Consumers | Worker (EC2, Lambda, ECS) | SQS, Lambda, HTTP/S, Email, SMS, mobile push, Firehose |
| Use case | **Decoupling**, buffering, load leveling, background job | Notification, alert, একই event বহু system-এ পাঠানো |

💡 একসাথে: **SNS → multiple SQS (fan-out pattern)** — Q109 দেখুন।

---

### Q45. SQS Standard vs FIFO

| | Standard | FIFO |
|---|---|---|
| Throughput | **প্রায় unlimited** | 300 msg/s (batching-এ 3,000); **high-throughput mode**-এ অনেক বেশি (৭০,০০০+) |
| Ordering | **Best-effort** (ক্রম বদলাতে পারে) | **Strict ordering** (প্রতি **Message Group ID**-এর মধ্যে) |
| Delivery | **At-least-once** (duplicate হতে পারে) | **Exactly-once processing** (5 মিনিটের deduplication window, Deduplication ID বা content-based) |
| নাম | যেকোনো | অবশ্যই `.fifo` দিয়ে শেষ |
| Use case | High volume, order জরুরি না (image processing, log) | Order জরুরি: bank transaction, order status update, inventory |

- Standard ব্যবহার করলে consumer-কে **idempotent** বানান।

---

### Q46. API Gateway কীভাবে Lambda-র সাথে integrate হয়?

API Gateway = Managed service যেটা REST/HTTP/WebSocket API তৈরি, publish, secure করে। Client request → API Gateway → Lambda invoke → response ফেরত।

**Integration types:**
- **Lambda Proxy integration** (সবচেয়ে common) — পুরো HTTP request (headers, path, query, body) event হিসেবে Lambda-তে যায়; Lambda-কে `{statusCode, headers, body}` format-এ response দিতে হয়।
- **Lambda custom (non-proxy) integration** — Mapping template (VTL) দিয়ে request/response transform (শুধু REST API)।

**API types:**
- **REST API** — feature-rich (usage plan, API key, request validation, caching, WAF, private endpoint)।
- **HTTP API** — সস্তা (~৭০% কম), দ্রুত, simpler (JWT authorizer)।
- **WebSocket API** — real-time two-way (chat)।

**অন্যান্য features:**
- Auth: **IAM**, **Cognito User Pool**, **Lambda authorizer**, JWT
- **Throttling** (default 10,000 rps, 5,000 burst), usage plan
- Caching, CORS, stage (dev/prod), stage variables, canary release
- **Timeout: 29 seconds** (default; REST API-তে quota বাড়ানো যায়) — লম্বা কাজ হলে async pattern
- Permission: API Gateway-কে Lambda invoke করার **resource-based permission** লাগে (`lambda:InvokeFunction`)

```
Client → API Gateway (auth, throttle, validate) → Lambda → DynamoDB
```

---

### Q47. Step Functions কীসের জন্য?

**AWS Step Functions** = Serverless **workflow orchestration** service। একাধিক AWS service/Lambda-কে **state machine** (Amazon States Language — JSON) দিয়ে ধাপে ধাপে চালায়। Visual workflow।

**State types:** Task, Choice (if/else), Parallel, **Map** (loop/array-র প্রতিটা item parallel), Wait, Pass, Succeed, Fail।

**Built-in:** Retry (backoff সহ), Catch (error handling), timeout, state/data passing, execution history (debugging), 200+ service-এর **direct SDK integration** (Lambda ছাড়াই DynamoDB, SQS, ECS, Glue, Bedrock call)।

**Workflow types:**
- **Standard** — ১ বছর পর্যন্ত চলতে পারে, exactly-once, per state transition bill। Long-running, human approval (callback task token)।
- **Express** — ৫ মিনিট পর্যন্ত, high volume (১ লাখ+/sec), at-least-once, সস্তা। IoT ingestion, streaming।

**Use cases:** Order processing (payment → inventory → shipping), ETL pipeline, ML pipeline, **Saga pattern** (distributed transaction rollback), human approval flow, Lambda chaining (Lambda-র ভেতর থেকে Lambda call করার বদলে)।

---

### Q48. EventBridge vs SNS

| | EventBridge | SNS |
|---|---|---|
| Model | **Event bus** + rule-based routing | Pub/Sub topic |
| Filtering | **Advanced content-based filtering** — event-এর যেকোনো field (prefix, numeric range, exists, anything-but) | Message attribute/body-তে filter policy (তুলনামূলক সীমিত) |
| Sources | AWS services (native), **SaaS partners** (Shopify, Zendesk, Datadog), custom app | Publisher app/AWS services |
| Targets | 20+ AWS target (Lambda, Step Functions, SQS, Kinesis, API destinations — যেকোনো HTTP API) | SQS, Lambda, HTTP, Email, SMS, mobile push |
| Extra | **Schema registry**, **archive & replay**, **Scheduler** (cron), **Pipes** (point-to-point + transform), input transformer | খুব high throughput, **low latency**, SMS/email/mobile push |
| Throughput | High (region অনুযায়ী soft limit) | প্রায় unlimited |

- **EventBridge:** Event-driven microservices, AWS service event-এ react (EC2 state change, CodePipeline), SaaS integration, complex routing, scheduled job।
- **SNS:** Simple high-throughput fan-out, মানুষকে notification (SMS/email), খুব কম latency।

---

### Q49. Serverless-এ retry ও Dead-Letter Queue (DLQ) handle করা

**Invocation type অনুযায়ী retry behavior:**
- **Synchronous** (API Gateway → Lambda): Lambda retry করে না — caller/client retry করবে (exponential backoff + jitter)।
- **Asynchronous** (S3, SNS, EventBridge → Lambda): Lambda নিজে **২ বার retry** (মোট ৩ চেষ্টা), event ৬ ঘণ্টা পর্যন্ত রাখে। Configure: max retry 0–2, max event age।
  - ব্যর্থ event → **DLQ** (SQS/SNS) বা আরও ভালো **Lambda Destinations** (on-failure → SQS/SNS/EventBridge/Lambda; বেশি context দেয়)।
- **Poll-based / Event source mapping** (SQS, Kinesis, DynamoDB Streams):
  - **SQS**: fail হলে message **visibility timeout** শেষে আবার দেখা দেয়; `maxReceiveCount` পার হলে SQS-এর **redrive policy** অনুযায়ী **DLQ**-তে যায়। **Partial batch response** (`ReportBatchItemFailures`) দিয়ে শুধু failed message retry।
  - **Kinesis/DynamoDB Streams**: record expire না হওয়া পর্যন্ত retry করে shard **block** করে → `MaximumRetryAttempts`, `MaximumRecordAge`, **bisect batch on error**, on-failure destination set করুন।

**Best practices:**
- Consumer **idempotent** রাখুন (duplicate safe) — idempotency key, Powertools for Lambda।
- **Exponential backoff + jitter**।
- DLQ-তে **CloudWatch alarm** (`ApproximateNumberOfMessagesVisible > 0`)।
- DLQ inspect করে fix → **DLQ redrive** (source queue-এ ফেরত পাঠানো)।
- SQS visibility timeout ≥ **6 × Lambda timeout**।
- Step Functions-এ `Retry`/`Catch` block।
- Poison message আলাদা করে রাখুন।

---

## 📊 Monitoring, DevOps & Architecture

### Q50. CloudWatch — metrics, logs, alarms-এর পার্থক্য

**CloudWatch** = AWS-এর monitoring & observability service।

- **Metrics** — সময়ের সাথে **numeric data point** (time-series)। যেমন CPUUtilization, RequestCount।
  - Namespace + dimension দিয়ে organize। Default EC2 metric ৫ মিনিট (detailed = ১ মিনিট), custom high-resolution ১ সেকেন্ড।
  - ⚠️ EC2 **memory ও disk usage** default metric না → **CloudWatch Agent** লাগে।
  - Custom metric: `PutMetricData` বা Embedded Metric Format।
- **Logs** — Application/system-এর **text log event**। Structure: **Log Group → Log Stream → Log Event**।
  - Retention set করা যায়; **Logs Insights** দিয়ে query; **Metric filter** দিয়ে log থেকে metric বানানো (যেমন "ERROR" গণনা); Subscription filter → Lambda/Kinesis/OpenSearch; S3-এ export।
- **Alarms** — Metric-এর উপর **threshold** watch করে state পরিবর্তন: `OK`, `ALARM`, `INSUFFICIENT_DATA`।
  - Action: **SNS notification**, **Auto Scaling**, **EC2 action** (stop/reboot/recover), Systems Manager।
  - **Composite alarm** (একাধিক alarm AND/OR)।

**সম্পর্ক:** Logs → (metric filter) → Metrics → (threshold) → Alarm → Action।

**অন্যান্য:** Dashboards, **EventBridge** (আগে CloudWatch Events), Synthetics (canary), RUM, Container/Lambda Insights, Application Signals, Anomaly detection।

---

### Q51. CloudTrail কী, CloudWatch থেকে পার্থক্য

**CloudTrail** = AWS account-এর **API activity audit log** — "**কে, কখন, কোথা থেকে, কোন API call করেছে, result কী**"। Console, CLI, SDK সব action record হয়।

- **Event types:** Management events (default on — CreateBucket, RunInstances), Data events (S3 GetObject, Lambda Invoke — extra cost), Insights events (অস্বাভাবিক API activity)।
- **Event history**: ৯০ দিন free, console-এ দেখা যায়।
- দীর্ঘমেয়াদি রাখতে **Trail** → S3 (+ CloudWatch Logs); **Organization trail** সব account-এর জন্য; **log file integrity validation**।
- **CloudTrail Lake** — SQL দিয়ে query।

| | CloudWatch | CloudTrail |
|---|---|---|
| প্রশ্ন | "**কী হচ্ছে?**" (performance, health) | "**কে কী করেছে?**" (audit, governance) |
| Data | Metrics, logs, alarms | API call record |
| Use | Monitoring, alerting, troubleshooting, auto scaling | Security investigation, compliance, change tracking |
| উদাহরণ | CPU ৯০% হয়েছে | User X রাত ২টায় SG-তে port 22 খুলেছে |

💡 একসাথে ব্যবহার: CloudTrail → CloudWatch Logs → metric filter → alarm (যেমন root login হলে alert)।

---

### Q52. Infrastructure as Code (IaC) — CloudFormation vs Terraform

**IaC** = Infrastructure (server, network, DB) **code/template দিয়ে define ও provision** করা, হাতে console-এ click না করে।
- ✅ Repeatable, consistent environment (dev = prod), version control (Git), code review, automation, দ্রুত DR, drift detection, documentation।

| | CloudFormation | Terraform |
|---|---|---|
| Vendor | AWS native | HashiCorp (BSL license; open-source fork: **OpenTofu**) |
| Cloud | শুধু AWS | **Multi-cloud** (AWS, Azure, GCP, K8s, GitHub, Datadog... ৩০০০+ provider) |
| Language | JSON/YAML (বা **CDK** দিয়ে TypeScript/Python) | **HCL** |
| State | AWS **manage করে** (কোনো state file নেই) | **State file** নিজে manage (S3 + DynamoDB/S3 lock দিয়ে remote backend) |
| Preview | Change Sets | `terraform plan` |
| Rollback | **Automatic rollback** on failure | Auto rollback নেই (partial apply থাকে) |
| New AWS feature | সাধারণত দ্রুত (কখনো দেরি) | Provider update-এর উপর নির্ভর |
| Modularity | Nested stacks, modules | **Modules** (Terraform Registry), খুব শক্তিশালী |
| Cost | Free | Free (CLI); Terraform Cloud paid |

- **CloudFormation:** শুধু AWS, AWS support চান, state file ঝামেলা চান না, StackSets দিয়ে multi-account।
- **Terraform:** Multi-cloud/hybrid, বড় ecosystem, team ইতিমধ্যে জানে।

---

### Q53. AWS-এ CI/CD pipeline (CodePipeline, CodeBuild, CodeDeploy)

**CI (Continuous Integration)** = প্রতি commit-এ code automatically build + test।
**CD (Continuous Delivery/Deployment)** = test pass হলে automatically staging/production-এ deploy (Delivery-তে manual approval থাকে)।

**AWS Developer Tools:**
- **Source**: GitHub/GitLab/Bitbucket (CodeConnections), S3, ECR (CodeCommit নতুন customer-দের জন্য আর available না)।
- **CodeBuild** — Managed build server: compile, unit test, docker image build, artifact তৈরি। `buildspec.yml` দিয়ে configure। Per-minute billing।
- **CodeDeploy** — EC2/on-prem, **Lambda**, **ECS**-এ deploy automate। `appspec.yml`। Strategy: in-place, **blue/green**, canary, linear; auto rollback।
- **CodePipeline** — পুরো workflow **orchestrate** করে: Source → Build → Test → Approval → Deploy stage।
- **CodeArtifact** — package repository (npm, pip, maven)।

```
GitHub push → CodePipeline
   ├─ Source stage
   ├─ Build stage (CodeBuild: test + docker build → ECR)
   ├─ Manual approval (SNS email)
   └─ Deploy stage (CodeDeploy / ECS / CloudFormation)
```

(বিকল্প: GitHub Actions + OIDC role দিয়ে AWS-এ deploy — এখন খুব common।)

---

### Q54. Well-Architected Framework ও এর pillars

**AWS Well-Architected Framework** = Cloud-এ secure, high-performing, resilient, efficient architecture তৈরির জন্য AWS-এর best practice ও design principle-এর সংকলন। **Well-Architected Tool** দিয়ে workload review করা যায়; industry-specific **Lens** আছে (Serverless, SaaS, ML)।

**৬টা Pillar:**
1. **Operational Excellence** — IaC, ছোট ও reversible change, observability, runbook, failure থেকে শেখা (post-mortem)।
2. **Security** — Strong identity (least privilege), সব layer-এ security, traceability (logging), data protection (encryption), incident response-এর প্রস্তুতি।
3. **Reliability** — Failure থেকে auto recovery, horizontal scaling, multi-AZ, backup ও DR test, capacity guess না করা।
4. **Performance Efficiency** — ঠিক resource type, serverless, global deployment (কয়েক মিনিটে), experiment, data-driven selection।
5. **Cost Optimization** — Consumption model (pay for what you use), right-sizing, RI/SP/Spot, cost attribution (tag), managed service।
6. **Sustainability** — Energy/carbon impact কমানো: utilization maximize, Graviton, efficient code, data lifecycle।

💡 মনে রাখার উপায়: **"OS-R-P-C-S"** বা "**Oh Some Rabbits Prefer Carrots Sweetly**"।

---

### Q55. Highly available, fault-tolerant 3-tier web application design

```
                  Route 53 (DNS, health check)
                          │
                 CloudFront + WAF + Shield (static content: S3)
                          │
    ┌─────────────────────┴─── VPC (multi-AZ) ───────────────────┐
    │  Public subnets (AZ-a, AZ-b, AZ-c): ALB, NAT Gateway ×3     │
    │                          │                                  │
    │  Private App subnets: Auto Scaling Group (EC2/ECS)          │
    │        across 3 AZ, stateless, session → ElastiCache        │
    │                          │                                  │
    │  Private DB subnets: RDS/Aurora Multi-AZ + Read Replicas    │
    │                     ElastiCache Redis (Multi-AZ)            │
    └─────────────────────────────────────────────────────────────┘
```

**Tier অনুযায়ী:**
1. **Presentation (Web) tier:** CloudFront (CDN + cache), S3 (static asset), WAF, internet-facing **ALB** (multi-AZ)।
2. **Application tier:** **ASG** (min ২+, কমপক্ষে ২-৩ AZ), **stateless** app, session ElastiCache/DynamoDB-তে, ALB health check → unhealthy instance replace। অথবা ECS Fargate।
3. **Data tier:** **Aurora/RDS Multi-AZ** (auto failover), Read Replica (read scale), automated backup + PITR, ElastiCache।

**Cross-cutting:**
- Security: SG chaining (ALB SG → App SG → DB SG), private subnet, KMS encryption, Secrets Manager, IAM role।
- NAT Gateway প্রতি AZ-এ (AZ-independent)।
- Monitoring: CloudWatch alarms, X-Ray, CloudTrail।
- IaC (CloudFormation/Terraform), CI/CD।
- Decoupling: SQS দিয়ে async কাজ।
- DR: AWS Backup, cross-region snapshot/replica, Route 53 failover।

💡 মূল মন্ত্র: **"No single point of failure — সব layer-এ multi-AZ + auto healing।"**

---

### Q56. Blue/Green deployment — AWS-এ কীভাবে?

**Blue/Green** = দুটো identical environment: **Blue** (current production) ও **Green** (নতুন version)। Green-এ deploy ও test করে traffic **এক ধাক্কায় (বা ধীরে) Green-এ switch**। সমস্যা হলে সঙ্গে সঙ্গে Blue-তে ফেরত (**instant rollback**)।

✅ Zero/near-zero downtime, দ্রুত rollback, production-like test। ❌ সাময়িক দ্বিগুণ resource cost, DB schema change জটিল (backward compatible রাখতে হয়)।

**AWS-এ implement:**
- **Route 53** — DNS weighted record/switch (DNS TTL caching-এর কারণে ধীর)।
- **ALB** — দুটো target group, listener rule-এ **weighted target group** দিয়ে traffic shift (দ্রুত, DNS সমস্যা নেই)।
- **Auto Scaling** — নতুন ASG/launch template, ALB-তে swap।
- **CodeDeploy** — EC2, **ECS** (দুটো target group + test listener), **Lambda** (alias traffic shifting) — built-in blue/green + auto rollback on CloudWatch alarm।
- **Elastic Beanstalk** — "Swap environment URLs" (CNAME swap)।
- **API Gateway** — stage/canary release।
- **RDS Blue/Green Deployments** — DB upgrade-এর জন্য managed staging environment, ১ মিনিটের কম switchover।

---

### Q57. RDS vs DynamoDB-তে horizontal ও vertical scaling

**RDS (relational):**
- **Vertical (মূল উপায়)** — instance class বড় করা (`db.r6g.large → db.r6g.4xlarge`)। Multi-AZ-এ standby আগে upgrade হয়ে failover → downtime কম, তবু সামান্য।
- Storage: **Storage auto scaling**, IOPS বাড়ানো।
- **Horizontal (শুধু read-এর জন্য)** — **Read Replica** (১৫ পর্যন্ত)। Write horizontal scale করা যায় না — একটাই primary writer; write scale লাগলে **application-level sharding** (জটিল)।
- Aurora: Serverless v2 (auto vertical), ১৫ replica + reader endpoint auto scaling, **Aurora Limitless Database** (PostgreSQL write sharding)।

**DynamoDB (NoSQL):**
- **Horizontal by design** — data automatically **partition**-এ ভাগ হয়; throughput বা data বাড়লে DynamoDB নিজেই partition split করে। Read ও write দুটোই scale করে, প্রায় unlimited।
- কোনো instance নেই → **vertical scaling concept নেই**; আপনি শুধু capacity (RCU/WCU) বা on-demand mode বাছেন।
- শর্ত: **ভালো partition key** (hot partition এড়াতে)।
- Read-heavy হলে **DAX** (in-memory cache, microsecond latency)।
- Global scale: **Global Tables**।

| | RDS | DynamoDB |
|---|---|---|
| Write scaling | Vertical (single writer) | Horizontal (auto partition) |
| Read scaling | Read replica + vertical | Auto + DAX |
| Downtime | Vertical-এ সামান্য | নেই |

---

## 🧩 Scenario-Based

### Q58. 24/7 predictable EC2 workload-এর cost কমাবেন কীভাবে?

1. **Right-size আগে** — CloudWatch + **Compute Optimizer** দেখে over-provisioned instance ছোট করুন (commit করার আগেই!)।
2. **Commitment discount:**
   - **Compute Savings Plan** (৬৬% পর্যন্ত, flexible — family/region/OS/Fargate/Lambda) বা **EC2 Instance Savings Plan** (৭২% পর্যন্ত, নির্দিষ্ট family+region)।
   - বা **Standard Reserved Instance** (৩ বছর, All Upfront = সর্বোচ্চ ছাড়)।
3. **Graviton (ARM)** instance-এ migrate → ~২০-৪০% better price-performance।
4. **Latest generation** (m5 → m7g/m7i)।
5. EBS: **gp2 → gp3** (~২০% সস্তা), অব্যবহৃত volume/snapshot মুছুন।
6. Non-prod environment রাতে/weekend-এ **বন্ধ** রাখুন (Instance Scheduler)।
7. Data transfer optimize (একই AZ, VPC endpoint দিয়ে NAT cost কমানো)।
8. Managed/serverless বিকল্প বিবেচনা (যদি fit করে)।
9. **Cost Explorer**, **Budgets**, tag দিয়ে monitor; RI/SP **utilization & coverage** report।

---

### Q59. Global user-দের latency — architecture fix

1. **Amazon CloudFront (CDN)** — Static ও dynamic content edge location থেকে serve; cache করুন; TLS termination edge-এ; AWS backbone দিয়ে origin-এ যায়।
2. **S3 Transfer Acceleration** — global upload-এর জন্য।
3. **AWS Global Accelerator** — Non-HTTP বা dynamic API-র জন্য; anycast static IP, AWS backbone দিয়ে nearest healthy region।
4. **Multi-region deployment** — প্রধান market-এর কাছে region-এ app deploy + **Route 53 latency-based routing** (বা geolocation)।
5. **Data layer global:**
   - **DynamoDB Global Tables** (multi-region, multi-active)
   - **Aurora Global Database** (<1s replication, local read)
   - **ElastiCache Global Datastore**
6. **Edge compute** — CloudFront Functions / Lambda@Edge (auth, redirect, personalization edge-এ)।
7. App optimization — compression (gzip/brotli), HTTP/2/3, caching header, query optimization।
8. Measure — CloudWatch RUM, Synthetics, Internet Monitor।

---

### Q60. S3 bucket শুধু application access করবে, public না — কীভাবে secure?

1. **Block Public Access** — account ও bucket দুই level-এ ON (এখন default)।
2. **Object Ownership = Bucket owner enforced** → **ACL disable**।
3. **IAM Role** — App (EC2 instance profile / ECS task role / Lambda execution role)-কে least-privilege policy (শুধু `s3:GetObject`/`PutObject` ঐ bucket/prefix-এ)। Access key hardcode নয়।
4. **Bucket policy:**
   - শুধু app-এর role ARN-কে Allow, অথবা অন্য সবাইকে **Deny** (`aws:PrincipalArn` condition)।
   - **`aws:SourceVpce`** — শুধু নির্দিষ্ট **VPC Gateway Endpoint** থেকে access (traffic internet দিয়ে যায় না)।
   - **`aws:SecureTransport = false` → Deny** (HTTPS বাধ্যতামূলক)।
5. **Encryption** — SSE-KMS (customer managed key, key policy-তেও app role সীমিত) + Bucket Key।
6. User-কে file দিতে হলে **pre-signed URL** বা **CloudFront + Origin Access Control (OAC)** — bucket কখনো public নয়।
7. **Versioning + MFA Delete / Object Lock** — accidental/malicious delete থেকে রক্ষা।
8. **Monitoring:** CloudTrail data events, S3 server access logs, **IAM Access Analyzer for S3** (public/cross-account access alert), **Macie** (sensitive data), GuardDuty S3 protection, AWS Config rule (`s3-bucket-public-read-prohibited`)।

---

### Q61. Critical application-এর Disaster Recovery strategy (RTO/RPO)

- **RPO (Recovery Point Objective)** — সর্বোচ্চ কতটা **data loss** সহ্য করা যাবে (সময়ে)। যেমন RPO = 1 ঘণ্টা → শেষ ১ ঘণ্টার data হারালে চলবে।
- **RTO (Recovery Time Objective)** — disaster-এর পর কত **সময়ের মধ্যে service চালু** করতে হবে।

**৪টা DR strategy (সস্তা → দামি, ধীর → দ্রুত):**

| Strategy | কীভাবে | RPO / RTO | Cost |
|---|---|---|---|
| **Backup & Restore** | Backup (AWS Backup, snapshot) অন্য region-এ copy; disaster হলে IaC দিয়ে সব নতুন করে তৈরি | ঘণ্টা / ২৪ ঘণ্টা পর্যন্ত | $ |
| **Pilot Light** | Core (DB replica) অন্য region-এ সবসময় চালু; app server বন্ধ/AMI ready — দরকারে চালু | মিনিট / দশ মিনিট–ঘণ্টা | $$ |
| **Warm Standby** | পুরো system ছোট আকারে DR region-এ চলছে; failover-এ scale up | সেকেন্ড / মিনিট | $$$ |
| **Multi-Site Active/Active** | দুই+ region-এ full production, দুটোই traffic নেয় | ~০ / ~০ (near-zero) | $$$$ |

**Design ধাপ:**
1. Business impact analysis → প্রতিটা workload-এর RTO/RPO ঠিক করা।
2. Data replication: Aurora Global DB, DynamoDB Global Tables, S3 CRR, AWS Backup cross-region/cross-account (ransomware থেকে বাঁচতে **backup vault lock**)।
3. Infra: **IaC** দিয়ে DR region reproducible।
4. Traffic: **Route 53 failover** + health checks, বা Application Recovery Controller।
5. **AWS Elastic Disaster Recovery (DRS)** — server-level block replication, RPO seconds।
6. **নিয়মিত DR drill/test** (game day), runbook, **Fault Injection Service** দিয়ে chaos test।

---

### Q62. On-prem database → AWS, minimal downtime-এ migrate

**Approach: AWS DMS + CDC (Change Data Capture)**

1. **Assess & plan:** DB size, engine, dependency; target বাছাই (RDS/Aurora)। Engine ভিন্ন হলে (Oracle → Aurora PostgreSQL) → **Schema Conversion Tool (SCT)** / DMS Schema Conversion।
2. **Network:** Site-to-Site **VPN** বা **Direct Connect**।
3. **Target DB তৈরি** (Multi-AZ), schema load।
4. **Initial full load:**
   - ছোট/মাঝারি → **DMS full load**।
   - খুব বড় (TB–PB) → native backup (mysqldump/pg_dump/RMAN) বা **Snowball** দিয়ে ship, তারপর CDC।
5. **Ongoing replication (CDC)** — DMS source-এর transaction log পড়ে চলমান পরিবর্তন target-এ apply করে; source সচল থাকে।
6. **Validate** — DMS data validation, row count, app testing (target-এ read-only test)।
7. **Cutover (কয়েক মিনিট downtime):** App write বন্ধ → replication lag শূন্য হওয়া পর্যন্ত অপেক্ষা → app connection string (DNS/Route 53 CNAME) নতুন DB-তে → চালু।
8. **Rollback plan:** Reverse replication (target → source) কিছুদিন রাখা।

বিকল্প: Native replication (MySQL binlog replica থেকে RDS-এ promote, Oracle Data Guard), Homogeneous migration-এ DMS homogeneous data migration।

---

## 🔰 Core / Foundational (additional)

### Q63. AWS Account vs AWS Organization

- **AWS Account** — AWS resource-এর মৌলিক **container + security & billing boundary**। প্রতিটার আলাদা root user, IAM, resource, bill, service quota। একটা account-এর resource ডিফল্টভাবে অন্য account থেকে isolated।
- **AWS Organization** — একাধিক account-কে একসাথে **group ও centrally govern** করার service।
  - Management account + member accounts, OU hierarchy
  - **Consolidated billing** (volume discount, RI/SP sharing)
  - **SCP/RCP** দিয়ে guardrail, tag/backup policies
  - Central security service (CloudTrail org trail, GuardDuty, Config)
  - API দিয়ে নতুন account তৈরি

💡 Multi-account কেন: blast radius কমানো, environment isolation (dev/prod), billing আলাদা, quota আলাদা।

---

### Q64. AWS Free Tier ও এর limitations

**তিন ধরনের free offer (ঐতিহ্যগতভাবে):**
1. **Always Free** — কখনো expire হয় না: Lambda (১M request/মাস), DynamoDB (২৫ GB), SNS, CloudWatch-এর কিছু অংশ।
2. **12 months free** — নতুন account-এর প্রথম ১২ মাস: EC2 t2/t3.micro **৭৫০ ঘণ্টা/মাস**, S3 ৫ GB, RDS micro ৭৫০ ঘণ্টা, ৩০ GB EBS।
3. **Trials** — short-term (SageMaker, Redshift ইত্যাদি)।

⚠️ **জুলাই ২০২৫ থেকে নতুন account-এর জন্য model বদলেছে:** নতুন account **$100 credit** পায় (নির্দিষ্ট activity করলে আরও $100 পর্যন্ত) এবং **Free plan** (৬ মাস বা credit শেষ পর্যন্ত) বা **Paid plan** বেছে নিতে হয়। Always-free service গুলো আছে।

**Limitations:**
- Limit ছাড়ালে **সাধারণ দামে charge** হয়।
- সব region/instance type/service cover করে না (NAT Gateway, Elastic IP (idle), public IPv4, data transfer-এর বড় অংশ free না)।
- Limit সব resource মিলিয়ে (২টা micro instance একসাথে চালালে ৭৫০ ঘণ্টা দ্রুত শেষ)।
- Organization-এ শুধু একটা account free tier পায় (legacy নিয়ম)।
- ✅ অবশ্যই **AWS Budgets + billing alert** set করুন।

---

### Q65. Management Console vs CLI vs SDK

| | Console | CLI | SDK |
|---|---|---|---|
| কী | Web-based **GUI** | **Command-line** tool (`aws ...`) | Programming language **library** (boto3, AWS SDK for JS/Java/Go) |
| Auth | Username/password + MFA (বা SSO) | Access key / SSO profile / role | Access key / role (credential provider chain) |
| Best for | শেখা, exploration, একবারের কাজ, dashboard দেখা | **Scripting**, automation, দ্রুত admin কাজ, CI/CD | Application-এর ভেতরে AWS integrate করা |
| Repeatable | ❌ | ✅ | ✅ |

- তিনটাই পেছনে **একই AWS API** call করে (HTTPS, SigV4 signed)।
- এছাড়া: **CloudShell** (browser-এ pre-authenticated CLI), **IaC** (CloudFormation/CDK/Terraform)।

---

### Q66. Service quota (limit) কী, কীভাবে increase করবেন?

**Service Quotas** = প্রতি account, প্রতি region-এ resource বা API-র **maximum সংখ্যা** — accidental overspend ও abuse রোধ এবং AWS capacity রক্ষার জন্য।
- **Soft limit** (adjustable) — যেমন: region প্রতি ৫টা VPC, ৫টা Elastic IP, On-Demand vCPU limit, Lambda concurrency ১০০০।
- **Hard limit** (বাড়ানো যায় না) — যেমন S3 object max ৫ TB, Lambda timeout ১৫ মিনিট।
- API **rate limit** (throttling) ও quota।

**Increase করার উপায়:**
1. **Service Quotas console** → service → quota → "**Request increase at account level**"।
2. CLI: `aws service-quotas request-service-quota-increase --service-code ec2 --quota-code L-1216C47A --desired-value 256`
3. পুরনো পদ্ধতি: Support Center case।
4. Organization-এ **quota request template** — নতুন account তৈরি হলেই auto request।

**Monitor:** Service Quotas + **CloudWatch alarm** (usage metric), **Trusted Advisor** service limit check।

---

### Q67. Managed service vs Unmanaged/self-hosted

- **Unmanaged/self-hosted** — আপনি EC2-তে নিজে software install করে চালান (যেমন EC2-তে MySQL, Kafka, Redis)।
  - আপনার দায়িত্ব: OS patch, install, backup, replication, HA, scaling, monitoring, security।
  - ✅ Full control, যেকোনো version/config, কখনো সস্তা। ❌ Operational overhead অনেক।
- **Managed service** — AWS operation-এর বড় অংশ নেয় (RDS, ElastiCache, MSK, OpenSearch, EKS)।
  - AWS করে: provisioning, patching, backup, failover, monitoring integration।
  - ✅ কম ops কাজ, built-in HA, দ্রুত। ❌ কম control (OS access নেই), কিছু feature সীমিত, একটু দামি।
- **Serverless / fully managed** — সার্ভার ধারণাই নেই (Lambda, DynamoDB, S3, Fargate) → auto scaling, pay-per-use।

💡 Shared responsibility model-এ managed service = আপনার দায়িত্ব কম। Rule of thumb: **"Undifferentiated heavy lifting" AWS-কে দিন, আপনার business logic-এ মনোযোগ দিন।**

---

## 💻 EC2 & Compute (additional)

### Q68. Spot Instances vs Spot Fleet

- **Spot Instance** — একটা **single instance** request, AWS-এর অব্যবহৃত capacity-তে ~৯০% পর্যন্ত ছাড়। AWS দরকার হলে **২ মিনিটের notice** দিয়ে reclaim করে (interruption: terminate/stop/hibernate)। Rebalance recommendation signal আগে আসতে পারে।
- **Spot Fleet** — **একাধিক Spot (এবং optionally On-Demand) instance-এর সমষ্টি**, নির্দিষ্ট **target capacity** (instance সংখ্যা বা vCPU/weight) পূরণ করতে একাধিক **instance type, AZ (launch pool)** থেকে instance নেয়।
  - **Allocation strategy:** `price-capacity-optimized` (recommended), `capacity-optimized`, `lowest-price`, `diversified`।
  - Interrupt হলে fleet automatically replacement খোঁজে (maintain mode)।

💡 আজকাল Spot Fleet-এর বদলে **EC2 Fleet** বা **Auto Scaling Group with mixed instances policy** (On-Demand base + Spot, multiple instance types) recommended।

---

### Q69. Launch Template vs Launch Configuration

| | Launch Configuration (legacy) | Launch Template (recommended) |
|---|---|---|
| Versioning | ❌ নেই — বদলাতে নতুন বানাতে হয় (immutable) | ✅ **Multiple versions**, default/latest version |
| ব্যবহার | শুধু Auto Scaling | ASG, EC2 **RunInstances**, EC2 Fleet, Spot Fleet |
| Mixed instances / Spot + On-Demand | ❌ | ✅ |
| Newer features | ❌ (নতুন instance type-ও support করে না) | ✅ T2/T3 unlimited, placement group, capacity reservation, dedicated host, multiple network interface, IMDSv2 setting |
| Inheritance | ❌ | ✅ অন্য template থেকে parameter inherit |
| Status | **Deprecated** — নতুন account-এ তৈরি করা যায় না | Current |

---

### Q70. EC2 Placement Groups (Cluster, Spread, Partition)

| Type | কীভাবে রাখে | সুবিধা | অসুবিধা | Use case |
|---|---|---|---|---|
| **Cluster** | একই AZ-এ, একই rack/কাছাকাছি hardware-এ | **Lowest latency, 10–100+ Gbps** network | Rack fail → সব instance প্রভাবিত (low HA) | HPC, tightly coupled workload, big data job |
| **Spread** | প্রতিটা instance **আলাদা rack**-এ (আলাদা power/network) | Max isolation — একসাথে fail-এর ঝুঁকি কম; multi-AZ সম্ভব | **প্রতি AZ-এ max 7 instance** | ছোট সংখ্যক critical instance (primary/secondary DB, Zookeeper node) |
| **Partition** | Instance গুলো **partition**-এ ভাগ, প্রতি partition আলাদা rack set-এ; **প্রতি AZ-এ ৭টা partition**, partition-এ শত শত instance | বড় distributed system-এ rack failure isolate; partition info metadata-তে পাওয়া যায় (topology aware) | Cluster-এর মতো low latency না | **HDFS, HBase, Cassandra, Kafka** |

---

### Q71. EBS-backed vs Instance-store-backed AMI

| | EBS-backed | Instance store-backed |
|---|---|---|
| Root volume | EBS volume (snapshot থেকে) | Instance store (S3-এর template থেকে copy) |
| Boot time | **দ্রুত** (< ১ মিনিট; lazy load) | ধীর (S3 থেকে পুরো image copy, < ৫ মিনিট) |
| **Stop** | ✅ Stop/start করা যায় (data থাকে) | ❌ Stop করা যায় না — শুধু reboot/terminate |
| Data persistence | Root volume টিকে থাকে (DeleteOnTermination false হলে terminate-এর পরও) | Terminate বা failure-এ root data হারায় |
| Root size | ৬৪ TiB পর্যন্ত | ১০ GiB |
| Instance type change | ✅ (stop → change → start) | ❌ |
| AMI তৈরি | এক command/click-এ (`CreateImage`) | AMI tools দিয়ে bundle করে S3-এ upload |
| Charge | Instance + EBS storage + snapshot | Instance + S3 storage (AMI) |

💡 আজকাল প্রায় সব AMI **EBS-backed** — instance store-backed legacy।

---

### Q72. Elastic Beanstalk vs manually EC2 + ALB + ASG

**Elastic Beanstalk** = **PaaS**। Code upload করুন (Java, .NET, Node.js, Python, PHP, Ruby, Go, Docker) → Beanstalk automatically EC2, ASG, ELB, security group, CloudWatch monitoring, (optional) RDS provision করে।

| | Elastic Beanstalk | Manual EC2 + ALB + ASG |
|---|---|---|
| Setup | মিনিটে, খুব কম config | নিজে প্রতিটা component design ও configure |
| Control | সীমিত (`.ebextensions`, platform hooks দিয়ে customize) | **পূর্ণ control** |
| Deployment | Built-in: All at once, Rolling, Rolling with batch, **Immutable**, Traffic splitting, Blue/Green (URL swap) | নিজে বানাতে হবে (CodeDeploy ইত্যাদি) |
| Platform update | Managed platform update | নিজে |
| Cost | Beanstalk-এর নিজস্ব charge নেই — শুধু underlying resource | একই |
| Best for | ছোট টিম, দ্রুত web app deploy, prototype, standard stack | Complex/custom architecture, fine-grained tuning, IaC-driven বড় platform |

💡 Beanstalk-ও পেছনে CloudFormation ব্যবহার করে; resource গুলো আপনার account-এ দেখা যায়।

---

### Q73. AWS Batch — কখন Lambda বা সরাসরি EC2-এর বদলে?

**AWS Batch** = Fully managed **batch computing** — হাজারো batch job queue করে, প্রয়োজনমতো compute (EC2, **Spot**, Fargate, EKS) provision করে চালায় ও কাজ শেষে scale down করে। Batch-এর নিজস্ব charge নেই।

**Components:** Job Definition (container image, vCPU, memory) → Job Queue (priority) → Compute Environment (managed/unmanaged)। Array job, job dependency, multi-node parallel job (MPI/HPC)।

**Lambda-র বদলে কখন:**
- Job **১৫ মিনিটের বেশি** চলে
- **>10 GB memory, GPU**, বড় disk দরকার
- Heavy compute (genomics, video transcoding, financial risk simulation, ML training)

**সরাসরি EC2-র বদলে কখন:**
- নিজে scheduler/queue/scaling/retry বানাতে চান না
- Job সংখ্যা ওঠানামা করে — idle সময়ে ০ instance
- Spot ব্যবহার করে সস্তায় চালাতে চান (interruption-এ auto retry)

💡 Short event-driven কাজ → Lambda; long-running service → EC2/ECS; **বড় পরিমাণ, queue-based, finite job → Batch।**

---

### Q74. Lightsail vs EC2

| | Lightsail | EC2 |
|---|---|---|
| লক্ষ্য | Beginner, ছোট project, simple website | সব ধরনের workload, enterprise |
| Pricing | **Fixed monthly bundle** (~$5/মাস থেকে: VM + SSD + data transfer + static IP) | Per-second, component অনুযায়ী আলাদা (instance, EBS, data transfer) — জটিল |
| Setup | One-click blueprint (WordPress, LAMP, Node.js) | অনেক option configure |
| Features | Simple firewall, snapshot, load balancer, managed DB, container, CDN (সীমিত) | ৭৫০+ instance type, ASG, placement group, full VPC control, সব AWS integration |
| Scaling | সীমিত | প্রায় unlimited |
| Networking | Managed VPC (peering দিয়ে AWS VPC-র সাথে যোগ) | Full VPC control |

- **Lightsail:** Blog, ছোট business website, dev/test, predictable খরচ।
- **EC2:** Auto scaling, complex architecture, production at scale। Lightsail snapshot → EC2-এ export করা যায়।

---

### Q75. Hibernation vs Stop

| | Stop | Hibernate |
|---|---|---|
| RAM | হারায় | **RAM content root EBS volume-এ save** হয় (suspend-to-disk) |
| Start হলে | OS নতুন করে **boot** — app নতুন করে শুরু, cache warm-up লাগে | **আগের অবস্থা থেকে resume** — process, memory, app state অক্ষত |
| Startup time | ধীর (boot + app init) | দ্রুত (বিশেষত বড় in-memory app-এর জন্য) |
| Billing | Instance charge বন্ধ, EBS charge চলে | একই (hibernating অবস্থায় instance charge নেই) |
| শর্ত | সব EBS-backed instance | Launch-এর সময় enable করতে হয়; **root EBS encrypted**, যথেষ্ট size (RAM ধরার মতো); RAM < 150 GB; supported family/OS; max **60 দিন** hibernate |
| Instance store data | হারায় | হারায় |

**Use case (hibernate):** লম্বা initialization-এর app, pre-warmed cache, দ্রুত আবার চালু করতে চান এমন dev environment।

---

## 💾 Storage (additional)

### Q76. S3 Object Lock vs Bucket Versioning

| | Versioning | Object Lock |
|---|---|---|
| উদ্দেশ্য | পুরনো version রাখা, accidental overwrite/delete থেকে **recover** | **WORM** (Write Once Read Many) — নির্দিষ্ট সময় পর্যন্ত object version **delete/overwrite একেবারেই করা যাবে না** |
| Delete করা যায়? | হ্যাঁ — permission থাকলে যেকোনো version permanently delete | Retention period-এ **না** |
| সম্পর্ক | স্বাধীন | **Versioning enable থাকা আবশ্যক** |
| Compliance | না | হ্যাঁ — SEC 17a-4, FINRA, HIPAA ইত্যাদি |

**Object Lock mode:**
- **Governance mode** — বিশেষ permission (`s3:BypassGovernanceRetention`) থাকলে override করা যায়।
- **Compliance mode** — **কেউই** (root user সহ) retention শেষ হওয়ার আগে delete বা mode পরিবর্তন করতে পারবে না।
- **Legal Hold** — কোনো মেয়াদ ছাড়া lock, হাতে সরানো পর্যন্ত (`s3:PutObjectLegalHold`)।

💡 Ransomware protection: Versioning + Object Lock (compliance)।

---

### Q77. S3 Transfer Acceleration — কী, কখন কাজে লাগে?

User নিকটতম **CloudFront edge location**-এ data upload করে → সেখান থেকে AWS-এর **optimized private backbone network** দিয়ে S3 bucket-এর region-এ যায়। Public internet-এর অনিশ্চিত path এড়ানো যায়।

- Endpoint: `bucketname.s3-accelerate.amazonaws.com`
- Bucket-এ enable করতে হয়; bucket নামে dot (`.`) থাকা যাবে না।
- Extra per-GB charge — কিন্তু দ্রুত না হলে charge হয় না।
- **Speed Comparison tool** দিয়ে লাভ যাচাই করা যায়।

**কখন useful:**
- বিশ্বজুড়ে (দূরবর্তী) user থেকে **একটা central bucket-এ upload**
- **বড় file** (GB–TB) নিয়মিত পাঠানো
- Available bandwidth ভালো কিন্তু দূরত্বের কারণে ধীর

কাছের region থেকে ছোট file হলে লাভ কম। (Multipart upload-এর সাথে combine করুন।)

---

### Q78. S3 Cross-Region Replication (CRR) vs Same-Region Replication (SRR)

উভয়ই **asynchronous, automatic** object copy এক bucket থেকে আরেক bucket-এ।

| | CRR | SRR |
|---|---|---|
| Destination | **ভিন্ন region** | **একই region** |
| Use case | **DR**, compliance (দূরে copy রাখা), **user-এর কাছে latency কমানো**, অন্য region-এর compute-এর কাছে data | **Log aggregation** (একাধিক bucket → একটায়), prod ↔ test account-এ live replication, same-region data sovereignty-র মধ্যে copy, ভিন্ন account-এ ownership |
| Cost | Inter-region data transfer charge | কম |

**সাধারণ নিয়ম:**
- **দুই bucket-এই versioning** enable আবশ্যক।
- S3-কে IAM role দিতে হয়।
- ভিন্ন account-এ সম্ভব (owner override)।
- Enable করার **পরের নতুন object** replicate হয় — পুরনো object-এর জন্য **S3 Batch Replication**।
- **Chaining নেই** (A→B→C auto হয় না)।
- Delete marker replicate optional; version-specific delete replicate হয় না (malicious delete থেকে রক্ষা)।
- **S3 Replication Time Control (RTC)** — 99.99% object ১৫ মিনিটের মধ্যে (SLA)।
- Filter (prefix/tag), storage class পরিবর্তন করে replicate করা যায়।

---

### Q79. AWS Storage Gateway — hybrid environment-এ কোন সমস্যার সমাধান?

**সমস্যা:** On-prem application local protocol (NFS/SMB/iSCSI/tape) ব্যবহার করে, কিন্তু organization চায় cloud-এর unlimited, সস্তা, durable storage (backup, archive, DR, capacity বাড়ানো) — app পরিবর্তন ছাড়াই।

**সমাধান:** Storage Gateway = **on-prem ↔ AWS storage-এর মধ্যে hybrid bridge**। On-prem-এ VM/hardware appliance হিসেবে চলে, **local cache** রাখে (low latency), পেছনে data S3/Glacier/EBS-এ।

| Type | Protocol | Backend | Use case |
|---|---|---|---|
| **S3 File Gateway** | NFS / SMB | S3 object (file = object) | File share-এর backup/archive, data lake-এ on-prem file আনা |
| **FSx File Gateway** | SMB | FSx for Windows File Server | Windows file share-এ low-latency local access *(নতুন customer-দের জন্য বন্ধ)* |
| **Volume Gateway** | iSCSI | S3 + EBS snapshot | **Cached** (primary data S3-এ, hot data local) / **Stored** (full data local, async backup S3-এ) |
| **Tape Gateway** | iSCSI VTL | S3 + Glacier/Deep Archive | Physical tape library replace — Veeam/Veritas backup software-এর সাথে |

---

### Q80. EBS volume types (gp3, io2, st1, sc1)

| Type | Category | Max IOPS | Max Throughput | Boot? | Use case |
|---|---|---|---|---|---|
| **gp3** | General Purpose SSD | 16,000 (baseline 3,000 free) | 1,000 MB/s (baseline 125) | ✅ | **Default** — boot volume, web app, dev/test, মাঝারি DB। **IOPS ও throughput size থেকে আলাদা ভাবে** configure; gp2-এর চেয়ে ~২০% সস্তা |
| gp2 | General Purpose SSD (পুরনো) | 16,000 (3 IOPS/GB, burst) | 250 MB/s | ✅ | Legacy |
| **io2 Block Express** | Provisioned IOPS SSD | **256,000** | 4,000 MB/s | ✅ | Mission-critical DB (Oracle, SAP HANA, SQL Server), sub-ms latency, **99.999% durability**, **Multi-Attach** |
| io1 | Provisioned IOPS SSD | 64,000 | 1,000 MB/s | ✅ | Legacy high IOPS |
| **st1** | Throughput Optimized **HDD** | 500 | 500 MB/s | ❌ | Big data, data warehouse, log processing, Kafka — **sequential, বড় I/O** |
| **sc1** | **Cold HDD** | 250 | 250 MB/s | ❌ | কম access হওয়া data, **সবচেয়ে সস্তা** |

💡 SSD = IOPS-heavy (random I/O); HDD = throughput-heavy (sequential)। HDD boot volume হতে পারে না।

---

### Q81. EBS snapshot দিয়ে backup ও restore

**Snapshot** = EBS volume-এর **point-in-time backup**, AWS-managed S3-এ রাখা।
- **Incremental** — প্রথমটা full, পরেরগুলো শুধু পরিবর্তিত block (খরচ কম); তবু প্রতিটা snapshot থেকে পুরো volume restore করা যায়।
- Snapshot নেওয়ার সময় volume ব্যবহার করা যায়; consistency-র জন্য app I/O pause/flush বা instance stop (বা multi-volume **crash-consistent snapshot**)।
- **Encrypted volume → encrypted snapshot**।

**Backup:**
- Manual: `aws ec2 create-snapshot --volume-id vol-xxx --description "daily"`
- Automate: **Amazon Data Lifecycle Manager (DLM)** বা **AWS Backup** (schedule, retention, cross-region/cross-account copy, vault lock)।

**Restore:**
- Snapshot থেকে **নতুন volume** তৈরি (যেকোনো AZ-এ, চাইলে বড় size/ভিন্ন type/encrypt সহ) → instance-এ attach → mount।
- Root volume replace: **Replace root volume** feature, বা snapshot থেকে AMI বানিয়ে launch।
- Restore-এর পর block lazily load হয় → প্রথম read ধীর; সমাধান: **Fast Snapshot Restore (FSR)** বা `fio`/`dd` দিয়ে pre-warm।

**অন্যান্য:** Cross-region **copy** (DR/migration), অন্য account-এর সাথে share, **Snapshot Archive tier** (৭৫% সস্তা, ৯০ দিন min), **Recycle Bin** (accidental delete থেকে recovery), snapshot lock।

---

### Q82. S3 Glacier Vault Lock — কেন compliance team চাইবে?

**Glacier Vault Lock** = Glacier **vault**-এ একটা **Vault Lock policy** (যেমন "কোনো archive ৭ বছরের আগে delete করা যাবে না") প্রয়োগ করে **lock** করা — lock হয়ে গেলে policy **আর কখনো পরিবর্তন বা মুছা যায় না** (immutable, root user-ও পারবে না)।

**Process (২ ধাপ):**
1. `InitiateVaultLock` → policy attach, lock **in-progress** state-এ, **২৪ ঘণ্টা** test window।
2. `CompleteVaultLock` → চিরস্থায়ী। (২৪ ঘণ্টায় abort করে নতুন করে শুরু করা যায়।)

**Compliance team কেন চায়:**
- Regulatory **WORM** requirement: SEC Rule 17a-4(f), FINRA, HIPAA, CFTC — financial/medical record নির্দিষ্ট বছর অপরিবর্তিত রাখতে হবে।
- **Tamper-proof** audit trail — insider threat বা compromised admin credential-ও data মুছতে পারবে না।
- **Legal hold**, e-discovery।
- Ransomware থেকে রক্ষা।

💡 আধুনিক বিকল্প: **S3 Object Lock (Compliance mode)** + Glacier storage class — S3 API দিয়ে একই WORM সুবিধা (Vault Lock পুরনো Glacier vault API-র জন্য)।

---

## 🌐 Networking (VPC) (additional)

### Q83. Public IP vs Private IP vs Elastic IP

| | Private IP | Public IP | Elastic IP |
|---|---|---|---|
| Reachable | শুধু VPC-র ভেতরে (বা peering/VPN/DX) | Internet থেকে | Internet থেকে |
| Range | RFC 1918 (`10.x`, `172.16–31.x`, `192.168.x`) — subnet CIDR থেকে | AWS pool | AWS pool (বা BYOIP) |
| Persistence | Instance-এর **পুরো জীবনকাল** (stop/start-এ বদলায় না) | **Dynamic** — stop/start-এ বদলে যায় | **Static** — release না করা পর্যন্ত আপনার |
| Assign | সবসময় (primary private IP) | Subnet setting "auto-assign public IP" বা launch-এর সময় | Manually allocate + associate |
| Cost | Free | Charge (~$0.005/hr, public IPv4) | Charge (~$0.005/hr) |

- Instance নিজে public IP জানে না — OS-এ শুধু private IP দেখায়; IGW **1:1 NAT** করে public ↔ private।
- ENI-তে একাধিক private IP (secondary) দেওয়া যায়।

---

### Q84. VPC Endpoint — Gateway vs Interface

**VPC Endpoint** = VPC থেকে AWS service-এ (বা PrivateLink service-এ) **private connection** — IGW, NAT, VPN, public IP ছাড়াই; traffic AWS network-এর বাইরে যায় না।

| | Gateway Endpoint | Interface Endpoint (PrivateLink) |
|---|---|---|
| Services | **শুধু S3 ও DynamoDB** | **প্রায় সব AWS service** (SQS, SNS, KMS, Secrets Manager, ECR, STS, CloudWatch...), S3-ও, 3rd-party/SaaS, নিজের service |
| কীভাবে কাজ করে | **Route table**-এ entry (prefix list → vpce) | Subnet-এ **ENI** তৈরি হয় private IP সহ; **Private DNS** service-এর public DNS নামকে private IP-তে resolve করে |
| Security | **Endpoint policy** | Endpoint policy + **Security Group** |
| On-prem / peered VPC থেকে access | ❌ | ✅ (VPN/DX/TGW দিয়ে) |
| Cross-region | ❌ | ✅ (cross-region PrivateLink) |
| Cost | **Free** | Per AZ per hour + per GB |

💡 Private subnet থেকে S3-এ বড় data → **Gateway endpoint** ব্যবহার করলে **NAT Gateway data processing charge বাঁচে**। Bucket policy-তে `aws:SourceVpce` দিয়ে restrict।

---

### Q85. Direct Connect vs VPN

| | Site-to-Site VPN | Direct Connect (DX) |
|---|---|---|
| Path | **Public internet**-এর উপর **IPsec encrypted tunnel** | **Dedicated private physical fiber** (DX location-এ cross-connect) |
| Setup time | **মিনিট** | **সপ্তাহ–মাস** (partner/port provisioning) |
| Bandwidth | প্রতি tunnel ~1.25 Gbps (ECMP/TGW দিয়ে বাড়ানো যায়) | 50 Mbps – **100/400 Gbps** |
| Latency | Variable (internet-নির্ভর) | **Consistent, কম** |
| Encryption | ✅ Built-in (IPsec) | ❌ Default না — **MACsec** (Layer 2) বা DX-এর উপর VPN চালাতে হয় |
| Cost | কম (hourly + data out) | বেশি port-hour, কিন্তু **data transfer out per-GB সস্তা** |
| HA | ২টা tunnel (দুই AZ endpoint) | Resiliency-র জন্য একাধিক connection, ভিন্ন location |

- Components: VPN → Virtual Private Gateway / TGW + Customer Gateway। DX → Virtual Interface (Private VIF → VPC, Public VIF → public AWS services, Transit VIF → TGW), **Direct Connect Gateway** (বহু region/VPC)।
- **Common pattern:** Primary = Direct Connect, **Backup = VPN** (সস্তা failover)।
- শুধু দ্রুত ও সস্তা শুরু → VPN; বড় data volume, consistent performance, compliance → DX।

---

### Q86. Bastion Host — private subnet access security-তে ভূমিকা

**Bastion Host (Jump box)** = **Public subnet**-এ থাকা একটা hardened EC2 instance, যার মাধ্যমে admin **private subnet**-এর instance-এ SSH/RDP করে।

```
Admin laptop ──SSH──▶ Bastion (public subnet) ──SSH──▶ Private EC2 / DB
```

**Security ভূমিকা ও best practice:**
- Private instance সরাসরি internet-এ exposed না — **একটামাত্র controlled entry point**।
- Bastion SG: port 22 শুধু **company-র নির্দিষ্ট IP** থেকে।
- Private instance SG: port 22 শুধু **Bastion-এর SG** থেকে।
- **SSH agent forwarding / ProxyJump** (`ssh -J`) — private key bastion-এ রাখবেন না।
- Minimal software, নিয়মিত patch, logging (session audit), ASG (min=max=1) দিয়ে self-heal, ছোট instance।

💡 **আধুনিক বিকল্প (recommended):** **AWS Systems Manager Session Manager** — কোনো open inbound port, SSH key, bastion লাগে না; IAM দিয়ে access control, CloudTrail/S3-এ full session log। অথবা **EC2 Instance Connect Endpoint**।

---

### Q87. Route 53 Alias record vs CNAME

| | CNAME | Alias (Route 53 extension) |
|---|---|---|
| Points to | **যেকোনো DNS নাম** (যেকোনো hostname) | শুধু **নির্দিষ্ট AWS resource**: ELB, CloudFront, S3 website, API Gateway, Elastic Beanstalk, VPC endpoint, Global Accelerator, same hosted zone-এর অন্য record |
| **Zone apex** (`example.com`) | ❌ **ব্যবহার করা যায় না** (DNS standard) | ✅ **যায়** |
| Query charge | চার্জ হয় | AWS resource-এ Alias query **free** |
| Resolution | Client-কে আরেকটা lookup করতে হয় | Route 53 নিজে **সরাসরি IP return** করে (A/AAAA record হিসেবে) |
| Target IP পরিবর্তন | — | Automatically track করে |
| TTL | Set করতে হয় | Set করা যায় না (target-এর থেকে নেয়) |
| Health check | — | "Evaluate target health" |

💡 `example.com` → ALB: **Alias** ছাড়া উপায় নেই। `blog.example.com` → অন্য provider-এর hostname: CNAME। (EC2 DNS name-এ Alias করা যায় না।)

---

### Q88. Global Accelerator vs CloudFront

দুটোই AWS **edge location + global backbone** ব্যবহার করে, কিন্তু উদ্দেশ্য ভিন্ন।

| | CloudFront | Global Accelerator |
|---|---|---|
| ধরন | **CDN** — content **cache** করে | **Network layer accelerator** — cache করে না, traffic proxy করে |
| Layer | Layer 7 (HTTP/HTTPS, WebSocket) | **Layer 4 (TCP/UDP)** |
| IP | Dynamic IP (DNS name) | **২টা static anycast IP** (whitelist করা যায়) |
| Best for | Static/cacheable content, website, video streaming, API caching | **Non-HTTP** (gaming, IoT, VoIP), static IP দরকার, দ্রুত **multi-region failover** (< ১ মিনিট, DNS cache সমস্যা নেই) |
| Endpoints | S3, ALB, EC2, any HTTP origin | ALB, NLB, EC2, Elastic IP |
| Edge features | Lambda@Edge, CloudFront Functions, signed URL, WAF | Traffic dial, endpoint weight, client affinity |

💡 **Cacheable HTTP content → CloudFront; TCP/UDP বা static IP + fast regional failover → Global Accelerator।**

---

### Q89. CloudFront — S3 origin vs Custom (EC2/ALB) origin

**S3 Origin:**
- Static content (HTML, CSS, JS, image, video)।
- **Origin Access Control (OAC)** (পুরনো OAI-এর বদলে) — bucket **private** থাকে, শুধু CloudFront (SigV4 sign করে) read করতে পারে; bucket policy-তে CloudFront distribution ARN allow।
- SSE-KMS encrypted object support (OAC-তে)।
- S3 → CloudFront data transfer **free**।
- S3 static website endpoint ব্যবহার করলে সেটা custom origin হিসেবে ধরা হয় (OAC কাজ করে না, bucket public লাগে)।

**Custom Origin (ALB, EC2, any HTTP server, API Gateway, on-prem):**
- **Dynamic content**, API।
- Origin **publicly reachable** হতে হয় (ALB public) — অথবা এখন **VPC Origins** দিয়ে private ALB/EC2।
- Protocol policy (HTTP only / HTTPS only / match viewer), origin timeout, keep-alive।
- Origin-কে শুধু CloudFront থেকে traffic নিতে: SG-তে **CloudFront managed prefix list**, + secret **custom header** (ALB rule-এ check) বা WAF।
- **Cache policy** (কোন header/cookie/query string cache key-তে), **Origin request policy** — dynamic content-এ TTL কম বা caching off।

**একসাথে:** একটা distribution-এ multiple origin + **behavior (path pattern)** — `/static/*` → S3, `/api/*` → ALB। **Origin group** দিয়ে failover।

---

## 💽 Databases (additional)

### Q90. Amazon Redshift vs RDS

| | RDS | Redshift |
|---|---|---|
| Workload | **OLTP** — অনেক ছোট transaction (insert/update/single-row read) | **OLAP** — বিশাল data-র উপর complex **analytical query/aggregation** |
| Storage | **Row-based** | **Columnar** storage + compression |
| Architecture | Single primary + replicas | **MPP (Massively Parallel Processing)** — leader node + compute nodes |
| Scale | GB – ৬৪ TB (Aurora ১২৮ TB) | TB – **Petabyte** (RA3 managed storage, Redshift Serverless) |
| Use case | Web/mobile app backend, e-commerce order | **Data warehouse**, BI dashboard (QuickSight/Tableau), reporting, historical trend |
| Extra | — | **Redshift Spectrum** (S3 data lake সরাসরি query), zero-ETL integration (Aurora/RDS → Redshift), concurrency scaling, ML |

💡 Redshift PostgreSQL-ভিত্তিক SQL ব্যবহার করে, কিন্তু transactional app-এর DB হিসেবে নয়।

---

### Q91. DynamoDB Global Tables — কোন সমস্যার সমাধান?

**Global Tables** = DynamoDB table-কে **একাধিক region-এ fully managed, multi-active (multi-master) replication**। প্রতিটা region-এর replica-তে **read ও write দুটোই** করা যায়, পরিবর্তন অন্য region-এ সাধারণত **১ সেকেন্ডের মধ্যে** (async) পৌঁছায়।

**সমস্যার সমাধান:**
- **Global low latency** — user নিকটতম region-এ read/write করে।
- **Multi-region HA / DR** — একটা region down হলে অন্যটায় traffic (RPO ~seconds, RTO ~0); 99.999% SLA।
- নিজে replication pipeline বানানোর ঝামেলা নেই।

**Details:**
- Conflict resolution: **Last writer wins** (timestamp)।
- DynamoDB Streams লাগে (auto-enabled)।
- **Multi-Region Strong Consistency (MRSC)** option এখন আছে (৩ region, RPO = 0)।
- Cost: replicated write unit + cross-region data transfer।

---

### Q92. DynamoDB Streams — কী, কী কাজে ব্যবহার?

**DynamoDB Streams** = Table-এর প্রতিটা item-level পরিবর্তনের (**INSERT, MODIFY, REMOVE**) **time-ordered sequence**, **২৪ ঘণ্টা** রাখা হয়। প্রতিটা change **exactly once**, item-এর পরিবর্তনের **ক্রম বজায়** রেখে।

**Stream view type:** `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, `NEW_AND_OLD_IMAGES`।

**Consumer:** **Lambda** (event source mapping, সবচেয়ে common), KCL adapter। (বিকল্প: **Kinesis Data Streams for DynamoDB** — বেশি retention, বেশি consumer।)

**Use cases:**
- **Event-driven architecture** — নতুন order insert → Lambda → email/notification পাঠানো।
- **Replication** — অন্য table/region (Global Tables এটার উপর ভিত্তি করে)।
- **Search index sync** — OpenSearch-এ data sync।
- **Analytics** — Firehose → S3/Redshift।
- **Audit log / change history**।
- **Materialized view / aggregation** (counter update)।
- Cache invalidation।

---

### Q93. RDS Proxy — কোন database connection সমস্যার সমাধান?

**সমস্যা:**
- **Lambda/serverless** বা অনেক microservice হাজারো **short-lived connection** খোলে → DB-র **max_connections** শেষ, CPU/memory connection management-এ নষ্ট → "too many connections" error।
- Failover-এর সময় app connection ভেঙে যায়, DNS propagation-এ দেরি।
- DB credential app code-এ রাখা।

**RDS Proxy (fully managed, HA database proxy):**
- **Connection pooling & multiplexing** — অনেক app connection → কম সংখ্যক DB connection share।
- **Failover time ~৬৬% পর্যন্ত কম** — proxy client connection ধরে রাখে, নতুন primary-তে redirect।
- **IAM authentication** + **Secrets Manager** থেকে credential — code-এ password নেই।
- **TLS** enforce।
- Supported: RDS MySQL/PostgreSQL/MariaDB/SQL Server, Aurora MySQL/PostgreSQL।
- VPC-র ভেতরে থাকে (public না)।

💡 Lambda + RDS = প্রায় সবসময় RDS Proxy ব্যবহার করুন। (Aurora Serverless-এর জন্য বিকল্প: **Data API**।)

---

### Q94. RDS database snapshot vs backup

| | Automated Backup | Manual DB Snapshot |
|---|---|---|
| কে নেয় | AWS automatically (daily **backup window**-এ) | আপনি manually (বা script/AWS Backup) |
| Content | Daily full snapshot (incremental) + **transaction logs প্রতি ৫ মিনিটে** S3-এ | ঐ মুহূর্তের storage volume snapshot |
| Restore | **Point-in-Time Recovery (PITR)** — retention-এর মধ্যে **যেকোনো সেকেন্ডে** (latest restorable ~৫ মিনিট আগে) | শুধু **snapshot নেওয়ার মুহূর্তে** |
| Retention | **1–35 দিন** (0 = disable) | **চিরকাল** — আপনি delete না করা পর্যন্ত |
| DB delete করলে | মুছে যায় (আলাদাভাবে retain করার option ছাড়া) | **থেকে যায়** |
| Use case | Daily operational recovery (ভুল `DELETE` চালানো) | Major change-এর আগে, long-term archive, অন্য account/region-এ copy/share, clone |

- দুটোই restore করলে **নতুন DB instance** তৈরি হয় (নতুন endpoint)।
- Long-term/compliance retention-এর জন্য **AWS Backup** ব্যবহার করুন।

---

### Q95. Amazon DocumentDB — কখন DynamoDB-র বদলে?

**DocumentDB** = Fully managed **document database**, **MongoDB API compatible** (JSON document)। Aurora-র মতো architecture: storage-compute আলাদা, ৩ AZ-এ ৬ copy, ১৫টা read replica, auto storage growth।

**DynamoDB-র বদলে DocumentDB কখন:**
- **MongoDB workload migrate** করছেন — driver, code, tool প্রায় অপরিবর্তিত।
- **Rich, ad-hoc query** লাগবে — nested field-এ query, **aggregation pipeline**, flexible secondary index, `$lookup` (join-like), text/geo query।
- Access pattern আগে থেকে সব জানা নেই (DynamoDB-তে access pattern design আগে করতে হয়)।
- Document size বড় (DocumentDB ১৬ MB, DynamoDB item ৪০০ KB max)।
- Developer MongoDB-তে অভ্যস্ত।

**DynamoDB ভালো যখন:** প্রায় unlimited scale, serverless/pay-per-request, single-digit ms guaranteed, simple key-based access, Global Tables multi-region active-active।

---

### Q96. Amazon Neptune কীসের জন্য?

**Neptune** = Fully managed **graph database** — data-র মধ্যে **relationship** (node/vertex + edge) store ও query করতে optimized; কোটি কোটি relationship millisecond-এ traverse করে।

**Query language:** **Gremlin** (Apache TinkerPop, property graph), **openCypher**, **SPARQL** (RDF)।

**Use cases:**
- **Social network** — friends of friends, recommendation ("people you may know")
- **Fraud detection** — shared device/IP/card-এর মধ্যে সন্দেহজনক pattern
- **Recommendation engine** — user-product-purchase relationship
- **Knowledge graph** — Wikipedia-র মতো entity relationship
- **Identity graph**, network/IT topology, **security graph** (attack path)
- Life sciences (drug discovery, protein interaction)

**Features:** ৩ AZ-এ ৬ copy, ১৫ read replica, Neptune Serverless, **Neptune Analytics** (graph algorithm), Neptune ML (GNN), **GraphRAG** (Bedrock-এর সাথে)।

💡 Relational DB-তে অনেক level-এর JOIN লাগলে (deep relationship) → graph DB।

---

## 🔐 Security & IAM (additional)

### Q97. AWS Shield Standard vs Shield Advanced

| | Shield Standard | Shield Advanced |
|---|---|---|
| Cost | **Free**, সবার জন্য automatically enabled | **$3,000/মাস** per organization (১ বছর commitment) + data transfer fee |
| Protection | **Layer 3/4** common DDoS (SYN/UDP flood, reflection attack) | Layer 3/4 **+ Layer 7** (WAF-এর সাথে), larger & sophisticated attack |
| Resources | সব AWS (বিশেষ করে CloudFront, Route 53) | EC2 (EIP), ELB, CloudFront, Global Accelerator, Route 53 — explicitly protect করতে হয় |
| **Shield Response Team (SRT)** | ❌ | ✅ **24/7 DDoS expert** team (Business/Enterprise support লাগে) |
| **Cost protection** | ❌ | ✅ DDoS-এর কারণে scaling-এর বাড়তি খরচ (ELB, CloudFront, EC2, Route 53) **credit** ফেরত |
| Visibility | Basic | Real-time attack diagnostics, CloudWatch metrics, attack history |
| WAF | আলাদা charge | Protected resource-এর WAF fee **included**, **automatic application-layer mitigation** |
| Extra | — | Health-based detection, proactive engagement, Firewall Manager free |

💡 সাধারণ website → Standard + WAF যথেষ্ট; বড় e-commerce, gaming, financial (DDoS-এর high risk/cost) → Advanced।

---

### Q98. Amazon GuardDuty — কী ধরনের threat detect করে?

**GuardDuty** = **Intelligent threat detection** service — ML, anomaly detection এবং threat intelligence (AWS + CrowdStrike/Proofpoint feeds) ব্যবহার করে continuously monitor করে। **Agentless** (বেশিরভাগ ক্ষেত্রে), এক click-এ enable, performance impact নেই।

**Data sources:** **CloudTrail management events**, **VPC Flow Logs**, **DNS logs** (আলাদা করে enable করতে হয় না) + optional protection plans: S3 data events, EKS audit logs, EKS/ECS/EC2 **Runtime monitoring** (agent), **Malware Protection** (EBS, S3), RDS login activity, Lambda network activity।

**Detect করে:**
- **Compromised EC2/container** — **crypto-mining**, known malicious IP/C2 server-এর সাথে যোগাযোগ, port scanning, outbound DDoS, backdoor
- **Compromised credentials** — অস্বাভাবিক location/সময় থেকে API call, **EC2 instance credential অন্য জায়গা থেকে ব্যবহার (exfiltration)**, Tor থেকে access
- **Reconnaissance** — unusual API enumeration, port probe
- **S3** — suspicious data access, public exposure, bucket policy পরিবর্তন
- **Account** — CloudTrail logging বন্ধ করা, password policy দুর্বল করা, root usage
- **Attack sequence (Extended Threat Detection)** — একাধিক signal মিলিয়ে multi-stage attack

**Findings** → severity (Low/Medium/High/Critical) → **EventBridge** → Lambda (auto remediation: instance isolate, key disable) / SNS / **Security Hub**। Organization-wide delegated admin।

---

### Q99. AWS Config vs CloudTrail

| | AWS Config | CloudTrail |
|---|---|---|
| প্রশ্ন | "**Resource দেখতে কেমন ছিল/আছে? Compliant কি না?**" | "**কে কোন API call করেছে?**" |
| Record | Resource **configuration state ও history** (configuration item, timeline, relationship) | **API activity/event** (who, when, from where, what) |
| Compliance | ✅ **Config Rules** (managed/custom Lambda/Guard) — যেমন "সব EBS encrypted?", "S3 public?", **Conformance Packs** (CIS, PCI) | ❌ সরাসরি না |
| Remediation | ✅ SSM Automation দিয়ে auto-remediate | ❌ |
| Use case | Compliance audit, drift, change management, "গত মাসে এই SG-এর rule কী ছিল?" | Security forensics, "SG-এর rule **কে** পরিবর্তন করেছে?" |

💡 **একসাথে:** Config বলবে "SG-তে port 22 `0.0.0.0/0` খোলা (non-compliant), ৩টা বাজে পরিবর্তন হয়েছে"; CloudTrail বলবে "user Alice `AuthorizeSecurityGroupIngress` call করেছে"। Config timeline-এ CloudTrail event link থাকে।

---

### Q100. Amazon Inspector কী, কী scan করে?

**Amazon Inspector** = Automated **vulnerability management** service — workload-এ **software vulnerability (CVE)** ও **unintended network exposure** খোঁজে, **continuously** (নতুন CVE publish হলে বা নতুন software install হলে auto re-scan)।

**Scan করে:**
- **EC2 instance** — OS package ও app-এর CVE (SSM agent দিয়ে, বা **agentless** EBS snapshot scan), **network reachability** (কোন port internet থেকে reachable), CIS benchmark।
- **ECR container image** — push-এর সময় ও continuous (OS + programming language package)।
- **Lambda function** — code dependency-র vulnerability; **Lambda code scanning** (code-এর security flaw: injection, hardcoded secret, weak crypto)।
- **Code Security** — source repo (GitHub/GitLab) SAST, SCA, IaC scan।
- **SBOM export** (CycloneDX/SPDX)।

**Output:** Finding + **Inspector risk score** (CVSS + exploitability + network reachability মিলিয়ে contextual) → Security Hub, EventBridge।

💡 **Inspector = vulnerability (দুর্বলতা)**; **GuardDuty = active threat (হামলা হচ্ছে কি না)**।

---

### Q101. Encryption at rest vs in transit — AWS-এ support

- **At rest** = **Store করা data** (disk, DB, S3, backup) encrypt — disk/media চুরি বা unauthorized storage access-এ data পড়া যাবে না।
- **In transit** = **Network দিয়ে চলাচলরত data** encrypt — eavesdropping/man-in-the-middle রোধ।

**AWS-এ At rest:**
- **KMS** (AWS managed / customer managed key), **CloudHSM** (single-tenant HSM)।
- S3 (SSE-S3 default, SSE-KMS, SSE-C, client-side), EBS, RDS/Aurora (create-এর সময় enable), DynamoDB (default on), EFS, Redshift, SQS/SNS (SSE), Secrets Manager, backup/snapshot।
- Client-side encryption: **AWS Encryption SDK**, DynamoDB Encryption Client।

**AWS-এ In transit:**
- **TLS/HTTPS** — সব AWS API endpoint HTTPS; **ACM** দিয়ে free certificate (ALB, CloudFront, API Gateway)।
- S3 bucket policy: `aws:SecureTransport` দিয়ে HTTPS enforce।
- RDS SSL/TLS connection (`rds.force_ssl`), ElastiCache in-transit encryption।
- **Site-to-Site VPN (IPsec)**, **Direct Connect MACsec**।
- Nitro instance-এর মধ্যে inter-instance traffic automatic encrypted (supported type)।
- ALB → target re-encryption, EFS mount TLS, service mesh mTLS।

💡 Best practice: **দুটোই** — "encrypt everything, everywhere"।

---

### Q102. KMS: Customer Managed Key vs AWS Managed Key

(AWS এখন "CMK" নামটা বাদ দিয়ে **KMS key** বলে; তিন ধরনের: Customer managed, AWS managed, AWS owned।)

| | Customer Managed Key | AWS Managed Key | AWS Owned Key |
|---|---|---|---|
| কে তৈরি করে | **আপনি** | AWS service আপনার account-এ auto তৈরি (`aws/s3`, `aws/ebs`, `aws/rds`) | AWS (অনেক account-এ share) |
| Account-এ দেখা যায় | ✅ | ✅ | ❌ |
| **Key policy control** | ✅ পূর্ণ — কে use/manage করবে | ❌ পরিবর্তন করা যায় না | ❌ |
| **Rotation** | Optional, configurable (৯০ দিন – ৭ বছর), on-demand rotation | **Automatic প্রতি বছর** (বাধ্যতামূলক) | AWS-নির্ধারিত |
| Cross-account share | ✅ | ❌ | ❌ |
| Enable/disable/delete schedule | ✅ | ❌ | ❌ |
| Imported key material (BYOK), CloudHSM custom key store, multi-region key | ✅ | ❌ | ❌ |
| Cost | **$1/মাস/key** + API call | Key free (API call charge) | Free |
| CloudTrail audit | ✅ | ✅ | ❌ |

💡 Compliance, cross-account snapshot share, fine-grained access, key disable করার ক্ষমতা লাগলে → **Customer managed key**।

---

### Q103. Cross-account IAM role assumption (AssumeRole) কীভাবে কাজ করে?

**Scenario:** Account A (111111111111)-এর user/app-কে Account B (222222222222)-এর resource access দিতে হবে।

**ধাপ:**
1. **Account B-তে role তৈরি** (যেমন `CrossAccountS3Read`):
   - **Trust policy** — কে assume করতে পারবে:
   ```json
   {
     "Effect": "Allow",
     "Principal": { "AWS": "arn:aws:iam::111111111111:root" },
     "Action": "sts:AssumeRole",
     "Condition": { "StringEquals": { "sts:ExternalId": "unique-id-123" } }
   }
   ```
   - **Permission policy** — role কী করতে পারবে (যেমন `s3:GetObject` নির্দিষ্ট bucket-এ)।
2. **Account A-তে** user/role-কে permission দেওয়া: `sts:AssumeRole` on `arn:aws:iam::222222222222:role/CrossAccountS3Read`।
3. User **STS `AssumeRole`** call করে → পায় **temporary credentials** (AccessKeyId, SecretAccessKey, SessionToken; ১৫ মিনিট–১২ ঘণ্টা)।
   ```bash
   aws sts assume-role --role-arn arn:aws:iam::222222222222:role/CrossAccountS3Read --role-session-name demo
   ```
4. ঐ temp credential দিয়ে Account B-তে কাজ করে — এই সময় **নিজের original permission থাকে না**, শুধু role-এর permission।

**Key points:**
- **দুই দিকেই allow** লাগবে (A-র identity policy + B-র trust policy)।
- **External ID** — 3rd-party vendor-এর ক্ষেত্রে **confused deputy** problem রোধ।
- MFA condition, `aws:SourceIdentity`, session tags, CloudTrail-এ দুই account-এই log।
- Console-এ "**Switch Role**"; CLI profile-এ `role_arn` + `source_profile`।
- Organization-এ **IAM Identity Center** এটা automate করে।

---

### Q104. AWS Certificate Manager (ACM) — ALB/CloudFront-এর সাথে integration

**ACM** = SSL/TLS (X.509) certificate **provision, manage, deploy ও auto-renew** করার service।
- **Public certificate** — AWS integrated service-এ ব্যবহারের জন্য **free**; **auto-renewal** (DNS validation হলে সম্পূর্ণ automatic)।
- Validation: **DNS validation** (CNAME record, Route 53-এ one-click — recommended) বা Email validation।
- Private certificate — **AWS Private CA** (paid) দিয়ে internal service।
- **Exportable public certificate** option এখন আছে (EC2/on-prem-এ ব্যবহারের জন্য, paid)।
- বাইরের certificate **import** করা যায় (কিন্তু auto-renew হয় না)।
- Private key কখনো দেখা/download করা যায় না (non-exportable-এ)।

**Integration:**
- **ALB/NLB:** HTTPS/TLS listener-এ ACM certificate select → **TLS termination at load balancer**; **SNI** দিয়ে একাধিক domain-এর certificate একটা listener-এ; security policy (TLS version/cipher)। Certificate **ALB-এর same region**-এর হতে হবে।
- **CloudFront:** Custom domain (`www.example.com`)-এর জন্য ACM certificate **অবশ্যই `us-east-1` (N. Virginia) region-এ** তৈরি করতে হবে। Viewer ↔ CloudFront HTTPS।
- API Gateway (edge-optimized → us-east-1; regional → same region), Elastic Beanstalk, App Runner, Cognito।

⚠️ ACM public certificate **সরাসরি EC2-তে install করা যায় না** (exportable certificate ছাড়া) — ALB/CloudFront-এর পেছনে রাখুন।

---

## ⚡ Serverless & Application Integration (additional)

### Q105. Lambda synchronous vs asynchronous invocation

| | Synchronous | Asynchronous |
|---|---|---|
| কীভাবে | Caller invoke করে **response-এর জন্য অপেক্ষা** করে | Lambda event **internal queue**-এ রাখে, caller সঙ্গে সঙ্গে **202 Accepted** পায় |
| InvocationType | `RequestResponse` | `Event` |
| Sources | **API Gateway, ALB**, Cognito, SDK/CLI direct invoke, Lex, Function URL | **S3, SNS, EventBridge**, CloudWatch Logs, CodeCommit, SES |
| Error handling | **Caller-এর দায়িত্ব** — error client-এর কাছে যায়, retry client করে | Lambda **automatic ২ বার retry** (exponential backoff), max event age ৬ ঘণ্টা; ব্যর্থ হলে **DLQ / on-failure Destination** |
| Result পাঠানো | Response-এ | **Destinations** (on-success/on-failure → SQS, SNS, EventBridge, Lambda) |
| Duplicate | — | সম্ভব → function **idempotent** রাখুন |

(তৃতীয় ধরন: **Poll-based / Event source mapping** — SQS, Kinesis, DynamoDB Streams, Kafka, MQ; Lambda নিজে poll করে batch-এ synchronously invoke করে।)

```bash
aws lambda invoke --function-name fn --invocation-type Event --payload '{}' out.json
```

---

### Q106. Lambda concurrency — Reserved vs Provisioned

**Concurrency** = একই সময়ে কতগুলো request চলছে (একসাথে সক্রিয় execution environment সংখ্যা)।
- Formula: **Concurrency ≈ requests per second × average duration (sec)** — যেমন 100 rps × 0.5s = 50।
- Account-level default limit: **প্রতি region-এ ১,০০০** (soft limit, বাড়ানো যায়)। Limit পার হলে **throttling (429)**।
- Scaling rate: প্রতি function প্রতি ১০ সেকেন্ডে ১,০০০ করে বাড়তে পারে।

| | Reserved Concurrency | Provisioned Concurrency |
|---|---|---|
| উদ্দেশ্য | নির্দিষ্ট function-এর জন্য concurrency **সংরক্ষণ এবং সীমা (cap)** | Execution environment **আগে থেকে initialize (warm)** রাখা |
| Cold start | কমায় না | **Cold start দূর করে** (predictable latency) |
| Effect | অন্য function এই অংশ ব্যবহার করতে পারে না; function-এর max-ও এটাই | ঐ সংখ্যক environment সবসময় ready; বাড়তি traffic on-demand concurrency-তে যায় |
| Cost | **Free** | **Charge** (configured amount × time, চালু থাকলেই) |
| Use case | Critical function-এর capacity guarantee; downstream DB রক্ষা করতে cap (যেমন 10); **0 দিয়ে function বন্ধ (kill switch)** | Latency-sensitive API, predictable traffic spike (Application Auto Scaling দিয়ে schedule) |

- Provisioned concurrency version/alias-এ configure হয়; reserved-এর বেশি হতে পারে না।

---

### Q107. AWS AppSync — GraphQL-এর সাথে সম্পর্ক

**GraphQL** = API query language — client **ঠিক যে field দরকার শুধু সেটাই চায়** এক request-এ (over-fetching/under-fetching নেই); একটা endpoint; schema-driven (Query, Mutation, Subscription)।

**AWS AppSync** = Fully managed **serverless GraphQL (ও Pub/Sub) API** service।
- **Schema** define → **Resolver** দিয়ে প্রতিটা field-কে **data source**-এর সাথে যুক্ত: **DynamoDB, Lambda, Aurora (Data API), OpenSearch, HTTP endpoint, EventBridge, Bedrock**।
- Resolver লেখা: **JavaScript (APPSYNC_JS)** বা VTL; **Pipeline resolver** (একাধিক step)।
- **Real-time Subscription** (WebSocket) — mutation হলে subscribed client auto update (chat, live score, dashboard)।
- **Offline sync** (Amplify DataStore-এর সাথে), conflict resolution।
- Auth: API key, **Cognito User Pool**, IAM, OIDC, Lambda authorizer — field-level।
- Server-side **caching**, **Merged APIs** (একাধিক team-এর API একত্রে), **AppSync Events** (serverless WebSocket pub/sub)।

**কখন:** Mobile/web app-এ একাধিক source থেকে data এক request-এ, real-time feature, offline-first app।

💡 REST-এর জন্য **API Gateway**; **GraphQL-এর জন্য AppSync**।

---

### Q108. SQS visibility timeout vs message retention period

| | Visibility Timeout | Message Retention Period |
|---|---|---|
| কী | Consumer message **receive করার পর** কতক্ষণ সেটা **অন্য consumer-দের কাছে অদৃশ্য** থাকবে | Message queue-তে **সর্বোচ্চ কতদিন থাকবে** (delete না হলে) |
| Default | **30 seconds** | **4 দিন** |
| Range | 0 sec – **12 ঘণ্টা** | **60 sec – 14 দিন** |
| শেষ হলে কী হয় | Consumer delete না করলে message **আবার visible** → অন্য consumer আবার process করে (retry) | Message **permanently মুছে যায়** (processed হোক বা না হোক) |
| উদ্দেশ্য | Duplicate processing রোধ, failure-এ retry | Queue-তে data কতদিন রাখা যাবে |

**Best practices:**
- Visibility timeout > processing time; Lambda হলে **≥ 6 × function timeout**।
- লম্বা কাজে **`ChangeMessageVisibility`** দিয়ে বাড়ানো (heartbeat)।
- Processing শেষে অবশ্যই **`DeleteMessage`**।
- DLQ-র retention মূল queue-র চেয়ে **বেশি** রাখুন (FIFO-তে enqueue timestamp original থাকে; standard-এ এখন থেকে নতুন করে গোনা)।

---

### Q109. SNS + একাধিক SQS দিয়ে fan-out architecture

**Fan-out** = একটা event **একসাথে একাধিক independent consumer**-এ পাঠানো, প্রত্যেকে নিজের গতিতে parallel process করবে।

```
                         ┌──▶ SQS: order-email-queue    ──▶ Lambda (email পাঠায়)
Order Service ──▶ SNS ───┼──▶ SQS: order-inventory-queue ──▶ ECS (stock কমায়)
   (publish)   (topic)   ├──▶ SQS: order-analytics-queue ──▶ Firehose/S3
                         └──▶ SQS: order-fraud-queue     ──▶ Fraud service
```

**Setup:**
1. SNS topic তৈরি (`order-created`)।
2. প্রতিটা consumer-এর জন্য আলাদা SQS queue।
3. Queue গুলোকে topic-এ **subscribe** করান।
4. প্রতিটা **SQS queue policy**-তে SNS topic-কে `sqs:SendMessage` allow (`aws:SourceArn` condition)।
5. **Raw message delivery** enable (SNS envelope ছাড়া original message)।
6. **Subscription filter policy** — প্রতিটা queue শুধু তার দরকারি message পাবে (যেমন `{"country": ["BD"]}` বা `order_value > 1000`)।
7. প্রতিটা queue-র জন্য **DLQ**।
8. Encryption থাকলে KMS key policy-তে SNS-কে permission।

**কেন SNS → SQS (সরাসরি SNS → Lambda না):**
- **Durability/buffering** — consumer down থাকলেও message queue-তে ১৪ দিন পর্যন্ত থাকে
- **Retry** ও DLQ, **throttling/load leveling**
- **Loose coupling** — নতুন consumer যোগ করতে publisher পরিবর্তন লাগে না
- প্রতিটা consumer স্বাধীনভাবে scale ও fail করে
- Cross-region/cross-account সম্ভব
- Order লাগলে: **SNS FIFO → SQS FIFO**

(বিকল্প: EventBridge rule → multiple targets।)

---

## 📊 Monitoring, DevOps & Architecture (additional)

### Q110. CodePipeline vs CodeBuild vs CodeDeploy

| Service | Role | কী করে | Config |
|---|---|---|---|
| **CodePipeline** | **Orchestrator** (CI/CD workflow) | Source → Build → Test → Approval → Deploy stage গুলো **ক্রমানুসারে চালায়**, artifact এক stage থেকে পরের stage-এ দেয়; নিজে build/deploy করে না | Pipeline definition (stages, actions), trigger (git push) |
| **CodeBuild** | **Build/CI engine** | Managed, serverless container-এ code **compile, unit test, lint, docker build**, artifact তৈরি (S3/ECR) | `buildspec.yml` (install, pre_build, build, post_build phases) |
| **CodeDeploy** | **Deployment engine** | Artifact **EC2/on-prem, Lambda, ECS**-এ deploy — in-place, rolling, **blue/green**, canary/linear; health check fail → **auto rollback** | `appspec.yml` (lifecycle hooks: BeforeInstall, AfterInstall, ApplicationStart, ValidateService) |

💡 উপমা: **CodePipeline = project manager**, **CodeBuild = builder/tester**, **CodeDeploy = delivery person**।

---

### Q111. Blue/Green vs Canary deployment

| | Blue/Green | Canary |
|---|---|---|
| Idea | দুটো **পূর্ণ** environment; traffic **একবারে (100%)** নতুনটায় switch | নতুন version-এ **প্রথমে ছোট অংশ traffic** (যেমন ৫–১০%), metrics ঠিক থাকলে **ধাপে ধাপে বাড়ানো** |
| Risk exposure | Switch-এর পর সব user নতুন version-এ (আগে test করা থাকলেও) | শুরুতে অল্প user প্রভাবিত — **blast radius কম** |
| Rollback | **Instant** — traffic আবার Blue-তে | দ্রুত — canary-র traffic 0 করা |
| Resource cost | Switch-এর সময় **দ্বিগুণ** infrastructure | কম (ছোট canary fleet) |
| Complexity | সহজ ধারণা | Traffic splitting + ভালো monitoring/automated analysis লাগে |
| Real-user validation | Switch-এর আগে সীমিত | ✅ Production traffic দিয়ে validate |

**AWS implementation:**
- **CodeDeploy** config: `LambdaCanary10Percent5Minutes`, `ECSCanary10Percent15Minutes`, `...Linear10PercentEvery1Minute`, `AllAtOnce` (blue/green)।
- **Lambda alias weighted routing**, **ALB weighted target groups**, **Route 53 weighted**, **API Gateway canary release**, App Mesh/ECS Service Connect।
- **CloudWatch alarm**-ভিত্তিক automatic rollback।

(**Linear** = নির্দিষ্ট সময় পরপর সমান ভাগে বাড়ানো; **Rolling** = batch-এ batch-এ instance update।)

---

### Q112. AWS X-Ray — distributed application debugging-এ কীভাবে সাহায্য করে?

**X-Ray** = **Distributed tracing** service — একটা request microservice-গুলোর মধ্য দিয়ে (API Gateway → Lambda → DynamoDB → SQS → অন্য service) যে পথে যায়, **end-to-end** trace করে।

**Concepts:**
- **Trace** — একটা request-এর পুরো যাত্রা (trace ID header দিয়ে propagate)।
- **Segment** — প্রতিটা service-এর কাজ; **Subsegment** — ভেতরের downstream call (DB query, HTTP call)।
- **Service Map** — service-গুলোর visual graph + latency, error rate (৪xx/৫xx), fault।
- **Annotations** (indexed, filter করা যায়) ও **Metadata**।
- **Sampling rules** — সব request trace না করে একটা অংশ (খরচ নিয়ন্ত্রণ)।

**কীভাবে সাহায্য করে:**
- কোন service/call-এ **latency bottleneck** তা সরাসরি দেখা যায়
- কোথায় **error/exception** হচ্ছে ও কেন (stack trace)
- Dependency বোঝা, **root cause analysis**
- Performance regression ধরা (Insights — anomaly)

**Instrumentation:** X-Ray SDK, বা (recommended) **AWS Distro for OpenTelemetry (ADOT)**; Lambda/API Gateway-এ checkbox দিয়ে enable; EC2/ECS-এ X-Ray daemon/agent। CloudWatch **Application Signals / ServiceLens**-এ integrated।

---

### Q113. AWS Trusted Advisor — কোন categories-এ recommendation দেয়?

**Trusted Advisor** = আপনার AWS environment inspect করে AWS best practice অনুযায়ী **recommendation (check)** দেয়।

**Categories (৬টা):**
1. **Cost Optimization** — idle/underutilized EC2, unassociated Elastic IP, idle load balancer, underused EBS, RI/Savings Plan optimization।
2. **Performance** — high-utilization EC2, CloudFront config, EBS throughput, over-utilized resources।
3. **Security** — **S3 bucket open permission**, SG-তে unrestricted port (22/3389 `0.0.0.0/0`), **root account MFA নেই**, IAM use, exposed access key, CloudTrail logging।
4. **Fault Tolerance** — EBS snapshot নেই, RDS Multi-AZ নেই, single-AZ EC2, ASG/ELB config, Route 53 failover।
5. **Service Limits (Quotas)** — ৮০% এর বেশি ব্যবহৃত limit।
6. **Operational Excellence** — best practice অনুযায়ী operation (logging enable ইত্যাদি)।

**Access level:**
- **Basic/Developer support** — শুধু **core security checks** + service limit checks।
- **Business / Enterprise support** — **সব check**, API access, CloudWatch/EventBridge integration, Organization view, **Trusted Advisor Priority** (Enterprise)।

---

### Q114. Cost Explorer vs AWS Budgets

| | Cost Explorer | AWS Budgets |
|---|---|---|
| উদ্দেশ্য | **Analyze & visualize** — খরচ কোথায় হয়েছে/হচ্ছে (**retrospective + forecast**) | **Plan & alert** — সীমা নির্ধারণ করে threshold পার হলে **notify/action** (**proactive**) |
| Features | Graph, group/filter (service, account, region, **tag**, usage type), **১৩ মাস history** (৩৮ মাস পর্যন্ত optional) ও **১২ মাস forecast**, RI/SP utilization & coverage report, **RI/SP purchase recommendation**, rightsizing recommendation, hourly/resource-level granularity | Budget type: **Cost, Usage, RI utilization/coverage, Savings Plans utilization/coverage**; **actual বা forecasted** threshold-এ SNS/email/Chatbot alert; **Budget Actions** — threshold-এ **automatic** IAM/SCP policy apply বা EC2/RDS stop |
| প্রশ্ন | "গত মাসে EC2-তে কেন খরচ বাড়ল?" | "এই মাসে $1,000 পার হলে আমাকে জানাও / নতুন resource বন্ধ করো" |
| Cost | UI free; API per request charge | প্রথম ২টা budget free, পরে সামান্য charge |

💡 আরও: **Cost Anomaly Detection** (ML দিয়ে অস্বাভাবিক খরচ), **Cost and Usage Report (CUR 2.0)** (সবচেয়ে detailed data, Athena দিয়ে query), **Cost Categories**, **cost allocation tags**।

---

### Q115. Savings Plan vs Reserved Instance

উভয়ই **১ বা ৩ বছরের commitment**-এর বিনিময়ে On-Demand-এর চেয়ে সর্বোচ্চ ~**৭২%** ছাড়; payment: All/Partial/No Upfront।

| | Reserved Instance | Savings Plan |
|---|---|---|
| Commit করেন | **নির্দিষ্ট instance configuration** (instance family/type, region, OS, tenancy; zonal RI হলে AZ) | **$/ঘণ্টা খরচ** (যেমন $10/hour compute usage) |
| Flexibility | কম — Standard RI: বদলানো যায় না (শুধু size flexibility Linux regional RI-তে); **Convertible RI**: exchange করা যায় (কম ছাড়) | **বেশি** — **Compute SP**: যেকোনো family, size, **region**, OS, tenancy, এবং **Fargate ও Lambda**-তেও apply; **EC2 Instance SP**: নির্দিষ্ট family + region-এ, কিন্তু size/OS/tenancy flexible |
| Services | EC2, **RDS, ElastiCache, Redshift, OpenSearch, DynamoDB** (প্রত্যেকের আলাদা RI) | EC2, Fargate, Lambda (Compute SP); **SageMaker SP**; **Database Savings Plans** (নতুন — RDS/Aurora/DynamoDB ইত্যাদি) |
| **Capacity reservation** | ✅ **Zonal RI** নির্দিষ্ট AZ-এ capacity reserve করে | ❌ (আলাদাভাবে On-Demand Capacity Reservation লাগে) |
| Marketplace | Standard RI **RI Marketplace-এ বিক্রি** করা যায় | ❌ বিক্রি করা যায় না |
| Management | জটিল (অনেক RI ট্র্যাক) | সহজ |

💡 EC2-এর জন্য AWS এখন **Savings Plans recommend** করে। RDS/ElastiCache-এর জন্য ঐতিহ্যগতভাবে RI।

---

### Q116. CloudFormation StackSets vs regular stack

- **Regular Stack** — একটা template → **একটা account, একটা region**-এ resource-এর সংগ্রহ।
- **StackSet** — একটা template দিয়ে **একাধিক account এবং/বা একাধিক region**-এ একসাথে stack তৈরি, update, delete। প্রতিটা target-এ একটা **stack instance** তৈরি হয়।

| | Stack | StackSet |
|---|---|---|
| Scope | Single account + region | **Multi-account + multi-region** |
| Management | Stack নিজেই | Administrator account থেকে central |
| Permission model | Normal IAM | **Self-managed** (নিজে admin/execution role তৈরি) বা **Service-managed** (AWS Organizations-এর সাথে, **নতুন account OU-তে যোগ হলে auto-deploy**) |
| Deployment control | — | Max concurrent accounts, failure tolerance, region order |
| Use case | App infrastructure | **Organization-wide baseline**: সব account-এ CloudTrail, Config rule, GuardDuty, IAM role (audit/security role), SNS alarm, VPC baseline |

💡 **Control Tower** ও Landing Zone-এর পেছনেও StackSets ব্যবহৃত হয়।

---

### Q117. CloudFormation drift detection কী?

**Drift** = CloudFormation দিয়ে তৈরি resource-এর **actual configuration** যখন **template/stack-এর expected configuration** থেকে আলাদা হয়ে যায় — সাধারণত কেউ **console/CLI দিয়ে manually** পরিবর্তন করলে (যেমন SG-তে হাতে rule যোগ, instance type বদলানো, resource delete)।

**Drift detection:**
- Stack বা StackSet-এ "**Detect drift**" চালালে CloudFormation প্রতিটা supported resource-এর বর্তমান property template-এর সাথে তুলনা করে।
- Status: `IN_SYNC`, **`MODIFIED`**, **`DELETED`**, `NOT_CHECKED`।
- **Property-level diff** দেখায় (expected vs actual)।
- CLI: `aws cloudformation detect-stack-drift --stack-name my-stack` → `describe-stack-resource-drifts`।

**কেন জরুরি:** Drift থাকলে পরের stack update **fail** বা অপ্রত্যাশিতভাবে manual change overwrite করতে পারে; IaC-কে "single source of truth" রাখা; compliance/security (unauthorized change)।

**Drift ঠিক করার উপায়:**
- Manual change **revert** করা, অথবা
- Template update করে actual state-এর সাথে মেলানো, অথবা
- **Resource import** / নতুন **drift-aware change set** (actual state থেকে template-এ ফেরানো)।
- AWS Config rule `cloudformation-stack-drift-detection-check` দিয়ে নিয়মিত check + alert।
- **প্রতিরোধ:** IAM/SCP দিয়ে manual change সীমিত, সব change শুধু pipeline দিয়ে।

---

## 🚚 Migration & Hybrid Cloud

### Q118. AWS Database Migration Service (DMS) কী, কী করে?

**DMS** = Database **AWS-এ (বা AWS-এর মধ্যে) migrate** করার managed service — migration চলাকালীন **source database চালু থাকে** → **minimal downtime**।

**Components:**
- **Replication instance** (বা **DMS Serverless**) — migration task চালায়।
- **Source & target endpoints** — connection info।
- **Replication task** — কী migrate হবে (table mapping, transformation rules)।

**Migration types:**
1. **Full load** — existing data একবারে copy।
2. **Full load + CDC** — full load-এর পর চলমান পরিবর্তন (source-এর transaction log/binlog পড়ে) **continuous replicate** → cutover-এর সময় কয়েক মিনিট downtime।
3. **CDC only** — শুধু ongoing change।

**Supported:**
- **Homogeneous**: Oracle → Oracle, MySQL → Aurora MySQL
- **Heterogeneous**: Oracle → Aurora PostgreSQL, SQL Server → MySQL (schema convert-এর জন্য **SCT / DMS Schema Conversion** লাগে)
- Sources/targets: Oracle, SQL Server, MySQL, PostgreSQL, MongoDB, SAP, Db2, S3, DynamoDB, Redshift, Kinesis, OpenSearch, Kafka, DocumentDB...

**Use cases:** On-prem → RDS/Aurora migration, DB consolidation, continuous replication (DR, reporting), **data lake-এ stream** (S3), dev/test copy।

**Features:** Data validation, table/column filter ও transformation, Multi-AZ replication instance, **DMS Fleet Advisor** (inventory), CloudWatch monitoring।

---

### Q119. AWS Schema Conversion Tool (SCT) — DMS-এর সাথে সম্পর্ক

**SCT** = **Heterogeneous** migration-এ source DB-র **schema ও code object** (table, index, view, **stored procedure, function, trigger**, package) target engine-এর format-এ **convert** করে। (Data warehouse-এর জন্যও: Teradata/Netezza/Oracle DW → Redshift।)

- **Assessment report** — কতটা automatically convert হবে, কোনগুলো **manual কাজ** লাগবে (action item + effort estimate) → migration planning-এ খুব কাজের।
- Application code-এর embedded SQL-ও convert করতে পারে।
- Desktop application (downloadable); এখন **DMS Schema Conversion** নামে DMS console-এর ভেতরে managed version-ও আছে, এবং **generative AI**-assisted conversion।

**DMS-এর সাথে সম্পর্ক — দুটো একে অপরের পরিপূরক:**

| ধাপ | Tool |
|---|---|
| ১. Schema + code convert (structure) | **SCT** |
| ২. Data move (full load + CDC) | **DMS** |

```
Oracle (on-prem) ──SCT──▶ schema/procedure Aurora PostgreSQL-এ তৈরি
                 ──DMS──▶ data copy + ongoing replication ──▶ cutover
```

💡 **Homogeneous** migration (MySQL → RDS MySQL)-এ **SCT লাগে না** — schema একই।

---

### Q120. Snowball / Snowball Edge — কখন network-এর বদলে?

**AWS Snow Family** = **Physical, rugged, encrypted device** — AWS আপনার কাছে পাঠায়, আপনি local-এ data copy করেন, তারপর ফেরত পাঠালে AWS **S3-এ import** করে (বা S3 থেকে export)।

- **Snowball Edge Storage Optimized** — ~৮০–২১০ TB usable storage, data migration।
- **Snowball Edge Compute Optimized** — বেশি vCPU/GPU, **edge computing** (EC2 instance, Lambda local-এ চালানো)।
- **Snowcone** (ছোট, ৮–১৪ TB) — ⚠️ **discontinued**।
- **Snowmobile** (১০০ PB truck) — ⚠️ **retired**।
- Security: **256-bit encryption** (KMS key), tamper-resistant, TPM, **E Ink shipping label**, কাজ শেষে NIST-standard data wipe।
- ⚠️ নতুন customer-দের জন্য Snow Family-এর availability সীমিত করা হয়েছে — বড় transfer-এর জন্য AWS এখন **DataSync, Data Transfer Terminal**, বা partner solution-ও recommend করে।

**Network-এর বদলে কখন ব্যবহার:**
- **Data অনেক বেশি (দশ TB – PB)** এবং network-এ transfer করতে **এক সপ্তাহের বেশি** লাগবে।
  - উদাহরণ: ১০০ TB, 100 Mbps link → ~**৯০+ দিন**; Snowball-এ ~১ সপ্তাহ।
  - Rule of thumb: network transfer সময় > ~১ সপ্তাহ হলে Snowball বিবেচনা।
- **Bandwidth সীমিত/ব্যয়বহুল** বা শেয়ার্ড (production traffic ক্ষতিগ্রস্ত হবে)।
- **Remote/disconnected location** — জাহাজ, খনি, সামরিক field, বিমান — **edge compute + data collection**।
- Data center **shutdown/decommission**, one-time বড় migration।
- Security policy-তে internet দিয়ে data পাঠানো নিষেধ।

---

### Q121. AWS DataSync — কোন use case solve করে?

**DataSync** = **Online data transfer** service — on-prem storage থেকে AWS storage-এ (এবং AWS storage-এর মধ্যে, অন্য cloud থেকে) **দ্রুত, automated, secure** data move/sync।

**Sources/Destinations:**
- On-prem: **NFS, SMB, HDFS**, object storage (S3-compatible)
- AWS: **S3** (সব storage class), **EFS**, **FSx** (Windows, Lustre, ONTAP, OpenZFS)
- অন্য cloud: Azure Blob, Google Cloud Storage ইত্যাদি

**কীভাবে:** On-prem-এ **DataSync agent** (VM) install → **task** তৈরি (source, destination, schedule, filter) → চালানো।

**Features:**
- নিজস্ব protocol → সাধারণ tool (rsync, cp) এর চেয়ে **~১০x দ্রুত**, parallel, network optimization
- **Incremental** transfer (শুধু পরিবর্তিত file), **scheduling** (hourly/daily)
- **Data integrity verification**, **encryption in transit (TLS)**
- **Metadata/permission preserve** (POSIX, NTFS ACL, timestamp)
- Bandwidth throttling
- CloudWatch, EventBridge monitoring
- Private connectivity (VPC endpoint, Direct Connect)

**Use cases:**
- File share/NAS → S3/EFS/FSx **migration**
- **Recurring sync/replication** (on-prem → AWS DR copy, archive cold data)
- Data lake / analytics / ML-এর জন্য data আনা
- EFS ↔ EFS, S3 ↔ EFS cross-region copy

💡 **DataSync vs Storage Gateway:** DataSync = data **move/sync (migration, periodic transfer)**; Storage Gateway = **ongoing hybrid access** (on-prem app cloud storage-কে local মনে করে ব্যবহার করে)। **DataSync vs Snowball:** network যথেষ্ট হলে DataSync, না হলে Snowball।

---

### Q122. "Lift and Shift" vs "Re-architecture" migration

AWS-এর **7 Rs migration strategy**-র দুটো:

| | Lift and Shift (**Rehost**) | Re-architecture (**Refactor / Re-architect**) |
|---|---|---|
| কী | Application **যেমন আছে তেমনই** (code/architecture পরিবর্তন ছাড়া) AWS-এ সরানো — on-prem VM → EC2 | Application-কে **cloud-native** করে নতুন করে design — monolith → microservices, serverless, managed service, container |
| Speed | **দ্রুত** (সপ্তাহ) | **ধীর** (মাস–বছর) |
| Upfront cost/effort | কম | বেশি (development, testing) |
| Cloud benefit | সীমিত — auto scaling, elasticity, managed service-এর সুবিধা কম; অনেক সময় খরচ কমে না | **সর্বোচ্চ** — scalability, resilience, agility, long-term cost কম |
| Risk | কম | বেশি |
| Tool | **AWS Application Migration Service (MGN)**, VM Import/Export | ECS/EKS, Lambda, DynamoDB, Aurora, SQS... |
| কখন | Data center exit deadline, দ্রুত migrate, legacy app, প্রথম ধাপ হিসেবে | Business-critical app যেটা scale/innovation চায়, technical debt কমাতে, নতুন feature |

**সব 7 Rs:**
1. **Retire** — বন্ধ করে দাও
2. **Retain** — আপাতত on-prem-এ রাখো
3. **Rehost** — lift & shift
4. **Relocate** — hypervisor-level (VMware Cloud on AWS)
5. **Replatform** ("lift, tinker & shift") — সামান্য optimize, যেমন DB → RDS, app → Beanstalk
6. **Repurchase** ("drop & shop") — SaaS-এ যাওয়া (CRM → Salesforce)
7. **Refactor/Re-architect** — cloud-native

💡 প্রচলিত approach: **আগে rehost (দ্রুত migrate), পরে ধাপে ধাপে optimize/refactor।**

---

### Q123. AWS Application Migration Service (MGN)

**MGN** = AWS-এর **primary lift-and-shift (rehost)** service — physical, virtual (VMware, Hyper-V) বা অন্য cloud (Azure, GCP)-এর **server AWS-এ (EC2) migrate** করে, **minimal downtime**-এ। (আগের **CloudEndure Migration** এবং **Server Migration Service (SMS)**-এর উত্তরসূরি।)

**কীভাবে কাজ করে:**
1. Source server-এ **AWS Replication Agent** install।
2. Agent **continuous block-level replication** শুরু করে → AWS-এর **staging area subnet**-এ lightweight replication server ও সস্তা EBS volume-এ data sync (OS, app, DB সব)।
3. **Test launch** — non-disruptive test instance চালু করে যাচাই (source চলতে থাকে)।
4. **Cutover launch** — source-এ write বন্ধ → শেষ sync → EC2-এ production instance চালু → DNS switch। **Downtime সাধারণত মিনিট**।
5. Source decommission।

**Features:**
- OS/application **agnostic** (Windows, Linux; SQL Server, Oracle, SAP ইত্যাদি)
- Automatic **conversion** (boot loader, driver — AWS-এ চালানোর উপযোগী)
- **Launch templates**, post-launch actions (SSM দিয়ে agent install, modernization)
- Wave/application grouping — বড় scale migration
- **Free for 90 days** per server (শুধু staging resource-এর খরচ)
- **Migration Hub**-এর সাথে tracking

💡 **MGN vs DMS:** MGN = **পুরো server** (OS + app + data) rehost; DMS = শুধু **database data** migrate (engine পরিবর্তন সম্ভব)। DR-এর জন্য একই technology: **AWS Elastic Disaster Recovery (DRS)**।

---

## 🧩 Scenario-Based (additional)

### Q124. প্রতি মিনিটে ১০,০০০ image upload, unpredictable spike — serverless architecture

```
Client ──(1) request upload URL──▶ API Gateway ──▶ Lambda (pre-signed URL generate)
   │
   └──(2) direct PUT──▶ S3 (raw-uploads bucket)
                           │ (3) ObjectCreated event
                           ▼
                      SQS queue (buffer)  ◀── DLQ
                           │ (4) batch poll
                           ▼
                      Lambda (resize/thumbnail/validate)  ──▶ S3 (processed bucket) ──▶ CloudFront
                           │
                           ├──▶ DynamoDB (metadata, status)
                           └──▶ EventBridge/SNS (notify, আরও processing: Rekognition moderation)
```

**Design decisions:**
1. **Direct-to-S3 upload with pre-signed URL** — app server/API দিয়ে image যায় না → API Gateway payload limit (10 MB) ও Lambda timeout সমস্যা নেই; S3 অসীম scale। বড় file → multipart upload।
2. **S3 → SQS → Lambda** (সরাসরি S3 → Lambda না) — spike **buffer**, retry, DLQ, **load leveling**; Lambda batch-এ process।
3. **Lambda scaling** — ১০,০০০/মিনিট ≈ ১৬৭/sec; প্রতিটা ~২ sec হলে ~৩৩৪ concurrency — account concurrency limit যাচাই/বাড়ানো, **reserved concurrency** দিয়ে downstream রক্ষা, SQS **maximum concurrency** setting।
4. Heavy processing (video/বড় image, >15 min) → **Step Functions** + **ECS Fargate/Batch**।
5. **DynamoDB on-demand** — metadata, spiky traffic-এ auto।
6. **Idempotency** — S3 event duplicate হতে পারে → object key/ETag দিয়ে dedupe।
7. **Security** — pre-signed URL-এ short expiry, content-type/size condition; S3 private, encryption; CloudFront + OAC দিয়ে serve।
8. **Cost** — Lambda memory tune (Power Tuning), Graviton (arm64), S3 lifecycle (raw image IA/Glacier/delete)।
9. **Observability** — CloudWatch alarm (SQS age of oldest message, DLQ depth, Lambda errors/throttles), X-Ray।

---

### Q125. AWS access key public GitHub repo-তে leak — incident response

**⏱️ তাৎক্ষণিক (মিনিটের মধ্যে) — Contain:**
1. **Key deactivate/delete** — IAM → user → Access keys → **Make inactive** → তারপর delete। (Bot গুলো কয়েক সেকেন্ডের মধ্যে GitHub scan করে!)
2. যদি role session leak হয়: role-এ **"Revoke active sessions"** (`aws:TokenIssueTime` deny policy)।
3. প্রয়োজনে user-এ **explicit Deny-All policy** attach, বা এমনকি SCP দিয়ে account quarantine।
4. AWS হয়তো নিজেই detect করে key-তে **`AWSCompromisedKeyQuarantine`** policy attach করেছে ও email/Health event পাঠিয়েছে — সেটা দেখুন, **সরিয়ে দেবেন না**।

**🔍 Investigate — Scope নির্ধারণ:**
5. **CloudTrail** — ঐ access key ID দিয়ে সব API call (সব region!) — কী তৈরি/পরিবর্তন/পড়া হয়েছে? (CloudTrail Lake/Athena query, `userIdentity.accessKeyId`)
6. খুঁজুন: নতুন **IAM user/role/access key** (persistence), নতুন **EC2 instance (crypto-mining, বিশেষত অব্যবহৃত region-এ)**, Lambda, S3 bucket policy পরিবর্তন, data exfiltration (S3 GetObject), SG পরিবর্তন, CloudTrail বন্ধ করা, **Organizations/billing** পরিবর্তন।
7. **GuardDuty** findings, **Billing / Cost Explorer** (অস্বাভাবিক খরচ spike), IAM credential report, Access Analyzer।

**🧹 Eradicate & Recover:**
8. Attacker-এর তৈরি সব resource ও backdoor (user, key, role, Lambda, trust policy) delete; পরিবর্তিত config restore।
9. সংশ্লিষ্ট অন্য secret (DB password ইত্যাদি) **rotate**।
10. GitHub থেকে secret মুছুন — **git history rewrite** (`git filter-repo`/BFG), force push, cache/fork বিবেচনা (তবে মনে করুন key ইতিমধ্যে compromised)।
11. **AWS Support-এ case** খুলুন — অননুমোদিত usage-এর billing adjustment চাওয়া যায়।
12. Compliance/legal notification দরকার হলে (data breach)।

**🛡️ Lessons learned / Prevent:**
- **Long-term access key ব্যবহার বন্ধ** → IAM Identity Center (SSO), **IAM roles**, CI/CD-এ **OIDC federation** (GitHub Actions → role)।
- Secret → **Secrets Manager/Parameter Store**, `.gitignore`, **git-secrets / pre-commit hook / gitleaks**, **GitHub secret scanning + push protection**।
- Least privilege, SCP (region restrict), MFA, **Budgets + Cost Anomaly Detection** alert, GuardDuty/Security Hub সব account-এ।
- Post-mortem + incident response **runbook/playbook**।

---

### Q126. Growing company-র জন্য multi-account AWS environment (dev/staging/prod)

**Foundation: AWS Organizations + AWS Control Tower (Landing Zone)**

**OU structure (AWS recommended pattern):**
```
Root
├── Security OU
│    ├── Log Archive account   (সব CloudTrail, Config log — immutable)
│    └── Security Tooling/Audit account (GuardDuty, Security Hub, Inspector delegated admin)
├── Infrastructure OU
│    ├── Network account (Transit Gateway, shared VPC, Direct Connect, Route 53, egress/inspection)
│    └── Shared Services (CI/CD, AMI pipeline, artifact repo, directory)
├── Workloads OU
│    ├── Dev OU      → app-a-dev, app-b-dev
│    ├── Staging OU  → app-a-staging ...
│    └── Prod OU     → app-a-prod ...
├── Sandbox OU (developer experiment — budget limit, auto cleanup)
├── Suspended OU (বন্ধ account)
└── Management account (শুধু billing/Org — কোনো workload নয়)
```

**Key elements:**
1. **Identity**: **IAM Identity Center (SSO)** + corporate IdP (Okta/Azure AD/Google) → **permission sets** (Admin, Developer, ReadOnly) প্রতি account-এ; IAM user নেই।
2. **Guardrails**: **SCP** — region restriction, CloudTrail/Config বন্ধ নিষেধ, root user নিষেধ, prod-এ নির্দিষ্ট action নিষেধ; Control Tower **preventive/detective/proactive controls**।
3. **Centralized logging & security**: Organization CloudTrail → Log Archive (S3 Object Lock), Config aggregator, GuardDuty/Security Hub org-wide।
4. **Networking**: Transit Gateway hub-and-spoke, non-overlapping CIDR (**IPAM**), centralized egress/inspection, **RAM** দিয়ে subnet share।
5. **Account vending**: **Account Factory** (Control Tower) / **AFT (Account Factory for Terraform)** — নতুন account-এ baseline auto (VPC, role, budget, tag)।
6. **Billing**: Consolidated billing, **cost allocation tags**, প্রতি account **Budgets**, SP/RI sharing।
7. **CI/CD**: Shared Services-এ pipeline, cross-account role দিয়ে dev → staging → prod promote; prod-এ manual approval।
8. **Backup policy**: AWS Backup org-wide, cross-account backup vault।

**কেন multi-account:** Blast radius isolation, security boundary, সহজ billing attribution, quota আলাদা, prod-এ কঠোর access।

---

### Q127. RDS-এ business hours-এ high read load — বড় re-architecture ছাড়া fix

1. **Diagnose আগে** — **CloudWatch Database Insights / Performance Insights**: কোন query বেশি load দিচ্ছে (top SQL, wait events), CPU, ReadIOPS, connection সংখ্যা, freeable memory।
2. **Query & index optimization** — slow query log, `EXPLAIN`, missing **index** যোগ, N+1 query ঠিক করা, `SELECT *` এড়ানো। (প্রায়ই সবচেয়ে বড় লাভ, খরচ শূন্য।)
3. **Read Replicas** — read traffic replica-তে পাঠানো (app-এ read/write endpoint আলাদা — ছোট code change); Aurora হলে **reader endpoint** + **replica auto scaling** (business hours-এ replica বাড়বে, পরে কমবে)।
4. **Caching layer** — **ElastiCache (Redis)** দিয়ে frequently-read data cache (cache-aside pattern); বা ORM/app-level cache।
5. **Vertical scaling** — বড় instance class (বিশেষত memory-optimized → বেশি buffer cache); Multi-AZ-এ downtime কম।
6. **Storage I/O** — gp2 → **gp3/io2**, IOPS বাড়ানো।
7. **RDS Proxy** — connection surge/pooling সমস্যা হলে।
8. **Scheduled scaling** — Aurora Serverless v2 (ACU auto scale) বা scheduled replica/instance change business hours অনুযায়ী।
9. **Reporting/analytics query আলাদা করা** — heavy report আলাদা replica-তে বা **zero-ETL → Redshift**-এ।
10. **Parameter tuning** — `innodb_buffer_pool_size`, `work_mem`, `shared_buffers` ইত্যাদি parameter group-এ।

💡 সাধারণ ক্রম: **Query/index tune → Cache → Read replica → Scale up**।

---

### Q128. নতুন workload deploy-এর আগে cost estimate ও control

**Estimate (deploy-এর আগে):**
1. **AWS Pricing Calculator** — প্রতিটা service (EC2, RDS, S3, data transfer, NAT, load balancer) configure করে monthly/yearly estimate; বিভিন্ন scenario (low/expected/peak traffic)।
2. **Architecture review** — Well-Architected **Cost Optimization pillar**; hidden cost-এ নজর: **data transfer out**, **NAT Gateway processing**, cross-AZ traffic, CloudWatch Logs ingestion, public IPv4, KMS API call।
3. **Proof of concept / load test** — ছোট environment চালিয়ে actual cost (tag দিয়ে) মাপা, তারপর extrapolate।
4. Pricing model নির্বাচন — baseline-এর জন্য SP/RI, fault-tolerant কাজে Spot, serverless-এ pay-per-use।
5. **Infracost** (Terraform PR-এ cost diff) — CI-তে cost estimate।

**Control (deploy-এর সময় ও পরে):**
6. **Tagging strategy** (Project, Environment, Owner, CostCenter) + **cost allocation tags activate** + **Tag policies / SCP** দিয়ে tag enforce।
7. **AWS Budgets** — actual ও **forecasted** threshold-এ (৫০/৮০/১০০%) alert; **Budget Actions** দিয়ে auto-restrict।
8. **Cost Anomaly Detection** — অস্বাভাবিক spike-এ alert।
9. **Guardrails** — SCP দিয়ে দামি instance type/region নিষেধ; Service Catalog দিয়ে approved template।
10. **Separate account** per workload/environment → খরচ স্পষ্ট।
11. **Cost Explorer**, CUR নিয়মিত review; **Compute Optimizer**, **Trusted Advisor** দিয়ে right-size।
12. Auto scaling, non-prod schedule (রাতে বন্ধ), S3 lifecycle, log retention।
13. **FinOps practice** — owner-কে cost-এর জবাবদিহি, monthly review।

---

### Q129. EU data residency law (GDPR) — AWS architecture-এ প্রভাব

**মূল নীতি:** AWS-এ **data যে region-এ রাখবেন সেখানেই থাকে** — AWS customer-এর content অন্য region-এ নিজে থেকে সরায় না। দায়িত্ব shared: AWS = infrastructure compliance (GDPR DPA, C5, ISO); আপনি = data কোথায় রাখছেন, কে access করছে।

**Architecture decisions:**
1. **Region selection** — শুধু **EU region** (Frankfurt `eu-central-1`, Ireland `eu-west-1`, Paris, Stockholm, Milan, Spain, Zurich)। প্রয়োজনে **AWS European Sovereign Cloud** (EU-র ভেতরে সম্পূর্ণ আলাদা, EU-resident staff দ্বারা পরিচালিত)।
2. **Guardrails দিয়ে enforce:**
   - **SCP** — `aws:RequestedRegion` দিয়ে non-EU region-এ resource তৈরি **deny** (global service যেমন IAM, CloudFront, Route 53 exempt রাখতে হয়)।
   - **Control Tower region deny control**, data residency controls।
3. **Replication/backup EU-র মধ্যেই** — S3 CRR, Aurora Global DB, DynamoDB Global Tables, AWS Backup copy **শুধু অন্য EU region-এ**।
4. **Global service সাবধানে** — CloudFront edge cache (EU-বাইরের edge-এ cache হতে পারে → price class/geo restriction বা personal data cache না করা), Route 53, IAM global; **Global Accelerator**; logging/monitoring destination EU-তে।
5. **Encryption & key control** — **KMS customer managed key** EU region-এ; প্রয়োজনে **External Key Store (XKS)** / CloudHSM — key EU-র নিয়ন্ত্রণে।
6. **Access control** — least privilege, EU বাইরের support/ops টিমের access সীমিত, CloudTrail audit।
7. **Data classification & discovery** — **Amazon Macie** দিয়ে PII খোঁজা; কোন data personal তা চিহ্নিত।
8. **Data subject rights** — right to erasure/access: data model-এ user data খুঁজে delete করার ক্ষমতা (backup সহ), retention policy (lifecycle)।
9. **Third-party service/SaaS** — data EU-র বাইরে পাঠালে SCC/DPA।
10. **AWS Artifact** — GDPR DPA, compliance report download; **AWS Config conformance pack** দিয়ে continuous compliance।
11. **Multi-region global app হলে** — EU user-এর data EU-তে, অন্যদের অন্য region-এ (**data partitioning by geography**, Route 53 geolocation routing)।

---

### Q130. Stateful application-এর জন্য zero-downtime deployment strategy

**চ্যালেঞ্জ:** Stateful app-এ in-memory session, open connection (WebSocket), local data, DB schema — এগুলো deployment-এ ভাঙতে পারে।

**Strategy:**

1. **State externalize করা (সবচেয়ে গুরুত্বপূর্ণ)**
   - Session → **ElastiCache Redis / DynamoDB**; file → **S3/EFS**; app instance-কে যতটা সম্ভব stateless বানানো → তারপর যেকোনো instance replace করা নিরাপদ।
2. **Deployment method**
   - **Blue/Green** (ALB weighted target groups বা CodeDeploy) বা **Rolling/Canary** — ধীরে traffic shift, alarm-এ auto rollback।
   - ECS/EKS: rolling update with `minimumHealthyPercent=100`, `maxSurge`; K8s **StatefulSet** + PodDisruptionBudget, readiness probe।
3. **Connection draining / graceful shutdown**
   - ALB **deregistration delay** — চলমান request শেষ হওয়ার সময় দেওয়া; app-এ **SIGTERM handle** করে নতুন request বন্ধ, চলমান কাজ শেষ, WebSocket client-কে reconnect signal।
   - ASG **lifecycle hook** (terminate-এর আগে cleanup/flush)।
   - **Sticky session** থাকলে duration কম রাখা, বা session externalize করে বাদ দেওয়া।
4. **Database changes — Expand/Contract (parallel change) pattern**
   - **Expand**: শুধু backward-compatible change (নতুন column nullable যোগ, নতুন table) → পুরনো ও নতুন দুই version-ই কাজ করবে।
   - নতুন code deploy (দুই column-এ লেখা, backfill)।
   - **Contract**: সব instance নতুন version-এ গেলে পরের release-এ পুরনো column সরানো।
   - কখনো একই deploy-এ destructive schema change না।
   - DB engine upgrade: **RDS Blue/Green Deployments** (১ মিনিটের কম switchover), Aurora fast failover, **RDS Proxy** দিয়ে connection ধরে রাখা।
5. **Stateful data store নিজেই (যেমন self-managed cluster)**
   - Node-by-node rolling (replica আগে, তারপর primary failover), quorum বজায় রাখা, replication lag monitor।
6. **Backward/forward compatibility** — API versioning, message schema compatible (queue-তে পুরনো message নতুন code পড়তে পারবে), **feature flags** দিয়ে deploy ≠ release।
7. **Health checks + automated rollback** — ALB/ELB health check, CloudWatch alarm (error rate, latency) → CodeDeploy auto rollback।
8. **Test** — staging-এ production-like data, synthetic canary (CloudWatch Synthetics) deploy-এর সময় চালু।

💡 সারাংশ: **"State বাইরে নাও → traffic ধীরে শিফট করো → connection drain করো → DB change backward-compatible রাখো → metric দেখে auto rollback।"**

---

> ✍️ এই notes [প্রশ্ন তালিকার](./01-Questions.md) ক্রম অনুসারে। বিস্তারিত topic-ভিত্তিক ব্যাখ্যার জন্য [README](../README.md)-র Day-wise note গুলো দেখুন।
