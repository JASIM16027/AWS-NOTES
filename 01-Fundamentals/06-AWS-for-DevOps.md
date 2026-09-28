# AWS — DevOps এর জন্য বিস্তারিত গাইড

---

## AWS আসলে কী সমস্যা সমাধান করে?

**আগে যা হতো:**
```
অ্যাপ বানালে → নিজের server কিনতে হতো
Server আসতে → ২ সপ্তাহ
Setup করতে → আরো ১ সপ্তাহ
Traffic বাড়লে → আরো server কিনো, আরো ২ সপ্তাহ অপেক্ষা
Server নষ্ট হলে → সব শেষ 😭
```

**AWS দিয়ে:**
```
৫ মিনিটে server চালু
Traffic বাড়লে → automatic আরো server যোগ হয়
Server নষ্ট হলে → automatic নতুন server চালু হয়
ব্যবহার না করলে → pay করতে হয় না ✅
```

---

## AWS এর মূল ধারণা — Region & AZ

```
AWS Global Infrastructure:
├── Region (ap-southeast-1 = Singapore)
│   ├── Availability Zone 1 (AZ-1a) ← আলাদা data center
│   ├── Availability Zone 2 (AZ-1b) ← আলাদা data center
│   └── Availability Zone 3 (AZ-1c) ← আলাদা data center
│
└── Region (us-east-1 = N. Virginia)
    ├── AZ-1a
    ├── AZ-1b
    └── AZ-1c
```

**কেন একাধিক AZ?** একটা data center আগুন লাগলে বা flood হলে বাকিগুলো চলতে থাকে। তোমার অ্যাপ down হয় না।

Bangladesh থেকে সবচেয়ে কাছের region: **ap-southeast-1 (Singapore)**

---

## সবচেয়ে গুরুত্বপূর্ণ Services — একটা অ্যাপের জন্য কী কী লাগে

```
Internet
    │
    ▼
Route 53          ← DNS (domain → IP)
    │
    ▼
CloudFront        ← CDN (static file fast delivery)
    │
    ▼
Load Balancer     ← Traffic ভাগ করে দেয়
    │
   / \
  ▼   ▼
EC2  EC2          ← তোমার অ্যাপ চলে
  │
  ▼
RDS               ← Database (PostgreSQL/MySQL)
  │
  ▼
ElastiCache       ← Redis cache
  │
  ▼
S3                ← File storage
```

---

## ১. IAM — পরিচয় ও অনুমতি

IAM (Identity and Access Management) হলো AWS এর **security এর ভিত্তি**। কে কী করতে পারবে সেটা IAM দিয়ে control করো।

### মূল ধারণা:

```
IAM User     → একজন মানুষ বা program
IAM Group    → User এর দল
IAM Role     → AWS service এর পরিচয়
IAM Policy   → কী করতে পারবে তার নিয়ম
```

### Policy দেখতে কেমন:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Deny",
      "Action": "s3:DeleteObject",
      "Resource": "*"
    }
  ]
}
```

**এই policy মানে:** S3 bucket থেকে file নামাতে ও upload করতে পারবে, কিন্তু delete করতে পারবে না।

### Role কেন দরকার?

```
ভুল পদ্ধতি ❌:
EC2 server এ AWS credentials hardcode করো
→ কেউ server hack করলে credentials চুরি হবে

সঠিক পদ্ধতি ✅:
EC2 তে IAM Role attach করো
→ EC2 automatically permission পায়
→ কোনো credentials লাগে না
→ hack হলেও credentials চুরি হওয়ার কিছু নেই
```

```bash
# Role attach করা EC2 তে credentials ছাড়াই:
aws s3 cp file.txt s3://my-bucket/
# ✅ কাজ করে! EC2 এর Role থেকে permission নেয়
```

### Best Practice:

```
root account    → শুধু billing দেখো, কখনো use করো না
admin user      → IAM user বানাও, MFA enable করো
developer user  → শুধু দরকারি permission দাও
EC2/Lambda      → Role use করো, কখনো credentials না
```

---

## ২. VPC — তোমার Private Network

VPC (Virtual Private Cloud) হলো AWS এ তোমার **নিজস্ব isolated network**।

```
VPC (10.0.0.0/16) — তোমার পুরো network
├── Public Subnet (10.0.1.0/24)
│   ├── Load Balancer    ← internet থেকে accessible
│   └── NAT Gateway      ← private subnet কে internet দেয়
│
└── Private Subnet (10.0.2.0/24)
    ├── EC2 (অ্যাপ)      ← internet থেকে সরাসরি accessible না
    └── RDS (database)   ← একদম বাইরে যাওয়া যাবে না
```

### কেন Public ও Private Subnet আলাদা?

```
Database internet এ expose করলে:
→ hacker সরাসরি database attack করতে পারবে
→ SQL injection, brute force attack সহজ

Private Subnet এ রাখলে:
→ শুধু একই VPC এর EC2 access করতে পারবে
→ বাইরে থেকে কোনো connection সম্ভব না ✅
```

### Security Group — Virtual Firewall

```
EC2 Security Group:
┌─────────────────────────────────────┐
│ Inbound Rules:                      │
│  Port 80  ← Load Balancer থেকে    │
│  Port 22  ← তোমার IP থেকে         │
│                                     │
│ Outbound Rules:                     │
│  Port 5432 → RDS Security Group    │
│  Port 443  → Internet (0.0.0.0/0)  │
└─────────────────────────────────────┘

RDS Security Group:
┌─────────────────────────────────────┐
│ Inbound Rules:                      │
│  Port 5432 ← EC2 Security Group    │
│  (শুধু EC2 থেকে আসতে পারবে)       │
│                                     │
│ Outbound Rules:                     │
│  None (database বাইরে যাবে না)    │
└─────────────────────────────────────┘
```

---

## ৩. EC2 — তোমার Virtual Server

EC2 (Elastic Compute Cloud) হলো AWS এর **virtual machine**।

### Instance Types:

```
t3.micro    → 1 vCPU, 1GB RAM   → dev/test (free tier)
t3.small    → 2 vCPU, 2GB RAM   → ছোট অ্যাপ
t3.medium   → 2 vCPU, 4GB RAM   → মাঝারি অ্যাপ
c5.large    → 2 vCPU, 4GB RAM   → CPU intensive
r5.large    → 2 vCPU, 16GB RAM  → Memory intensive
```

### EC2 তে অ্যাপ Deploy করা:

```bash
# ১. EC2 তে SSH করো
ssh -i mykey.pem ubuntu@54.123.456.789

# ২. Docker install করো
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker ubuntu

# ৩. অ্যাপ চালাও
docker pull username/myapp:latest
docker run -d \
  --name myapp \
  --restart always \
  -p 80:5000 \
  --env-file .env \
  username/myapp:latest
```

### User Data — EC2 চালু হলে Automatic Setup:

```bash
# EC2 তৈরির সময় এই script দাও
# Server চালু হলে automatically চলবে
#!/bin/bash
apt update -y
apt install docker.io -y
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# অ্যাপ চালু করো
docker pull username/myapp:latest
docker run -d \
  --name myapp \
  --restart always \
  -p 80:5000 \
  username/myapp:latest
```

এটা দিলে নতুন EC2 চালু হলেই automatically সব setup হয়ে যাবে।

---

## ৪. Auto Scaling — Traffic অনুযায়ী Server

```
সকাল ৯টা (কম traffic):
[EC2] [EC2]
↑ দুটো server চলছে

দুপুর ১টা (বেশি traffic):
[EC2] [EC2] [EC2] [EC2]
↑ automatic চারটা হয়ে গেছে

রাত ১১টা (আবার কম):
[EC2] [EC2]
↑ আবার দুটোতে নামলো
```

### Launch Template বানাও:

```json
{
  "ImageId": "ami-0abcdef1234567890",
  "InstanceType": "t3.medium",
  "KeyName": "my-key",
  "SecurityGroupIds": ["sg-12345"],
  "IamInstanceProfile": {
    "Name": "MyEC2Role"
  },
  "UserData": "base64 encoded script"
}
```

### Auto Scaling Group:

```
Min instances: 2    ← কখনো ২ এর নিচে যাবে না
Max instances: 10   ← কখনো ১০ এর বেশি হবে না
Desired: 2          ← এখন ২টা চালাও

Scaling Policy:
  CPU > 70%  → আরো ১টা EC2 যোগ করো
  CPU < 30%  → ১টা EC2 কমাও
```

---

## ৫. Load Balancer — Traffic ভাগ করা

```
Internet
    │
    ▼
┌─────────────────┐
│  Load Balancer  │  ← একটাই IP/domain
│  (ALB)          │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│  EC2  │ │  EC2  │  ← traffic ভাগ হয়ে যায়
│ :5000 │ │ :5000 │
└───────┘ └───────┘
```

### ALB Rules — Path Based Routing:

```
myapp.com/api/*     → Backend EC2 group
myapp.com/static/*  → S3 bucket
myapp.com/*         → Frontend EC2 group
```

### Health Check:

```
ALB প্রতি ৩০ সেকেন্ডে check করে:
GET /health → HTTP 200?

✅ 200 → EC2 সুস্থ, traffic পাঠাও
❌ 500 → EC2 অসুস্থ, traffic পাঠানো বন্ধ
         Auto Scaling কে জানাও
         নতুন EC2 চালু করো
```

---

## ৬. RDS — Managed Database

RDS (Relational Database Service) — AWS নিজে database manage করে।

```
তুমি নিজে করলে:
  PostgreSQL install
  Backup configure
  Replication setup
  Security patch
  Monitoring
  ↑ এসব করতে সপ্তাহ লাগে

RDS দিলে:
  → সব automatic ✅
  → তুমি শুধু database use করো
```

### Multi-AZ Setup:

```
AZ-1a                    AZ-1b
┌──────────┐             ┌──────────┐
│  Primary │────sync────►│ Standby  │
│   RDS    │             │   RDS    │
└──────────┘             └──────────┘
      │
   AZ-1a down হলে:
      │
      ▼
┌──────────┐
│ Standby  │ ← automatic primary হয়ে যায়
│ promoted │   (~60 সেকেন্ড downtime)
└──────────┘
```

### Read Replica — Read Load কমাতে:

```
Primary RDS ← write করো (INSERT, UPDATE)
      │
      │ automatic sync
      ▼
Read Replica ← read করো (SELECT)
Read Replica ← read করো

ফলে Primary এর load কমে,
overall performance বাড়ে
```

---

## ৭. S3 — File Storage

S3 (Simple Storage Service) — unlimited file storage।

```
S3 Bucket: my-app-bucket
├── uploads/
│   ├── user-photos/
│   └── documents/
├── static/
│   ├── js/
│   └── css/
└── backups/
    └── db-backup-2024-01-01.sql
```

### S3 দিয়ে যা করা যায়:

```bash
# File upload
aws s3 cp photo.jpg s3://my-bucket/uploads/

# Folder sync
aws s3 sync ./dist s3://my-bucket/static/

# Presigned URL — temporary access
aws s3 presign s3://my-bucket/private/file.pdf \
  --expires-in 3600   # ১ ঘণ্টার জন্য URL

# Static website hosting
aws s3 website s3://my-bucket \
  --index-document index.html \
  --error-document error.html
```

### S3 Lifecycle Policy:

```json
{
  "Rules": [{
    "Status": "Enabled",
    "Transitions": [
      {
        "Days": 30,
        "StorageClass": "STANDARD_IA"
      },
      {
        "Days": 90,
        "StorageClass": "GLACIER"
      }
    ],
    "Expiration": {
      "Days": 365
    }
  }]
}
```

```
০-৩০ দিন    → STANDARD (fast, বেশি দাম)
৩০-৯০ দিন   → STANDARD_IA (কম access, কম দাম)
৯০-৩৬৫ দিন → GLACIER (archive, অনেক কম দাম)
৩৬৫+ দিন   → Delete (automatically মুছে যায়)
```

---

## ৮. ECS + ECR — Docker Container Deploy

ECR = Docker Hub এর AWS version
ECS = Container চালানোর service

```
তোমার PC
    │
    ▼
docker build → docker push → ECR (registry)
                                   │
                                   ▼
                              ECS Service
                              ├── Task 1 (container)
                              ├── Task 2 (container)
                              └── Task 3 (container)
                                   │
                                   ▼
                              Load Balancer
```

### ECR এ Image Push:

```bash
# ECR এ login করো
aws ecr get-login-password --region ap-southeast-1 | \
  docker login --username AWS \
  --password-stdin \
  123456789.dkr.ecr.ap-southeast-1.amazonaws.com

# Image tag করো
docker tag myapp:latest \
  123456789.dkr.ecr.ap-southeast-1.amazonaws.com/myapp:latest

# Push করো
docker push \
  123456789.dkr.ecr.ap-southeast-1.amazonaws.com/myapp:latest
```

### ECS Task Definition:

```json
{
  "family": "myapp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [{
    "name": "myapp",
    "image": "123456789.dkr.ecr.ap-southeast-1.amazonaws.com/myapp:latest",
    "portMappings": [{
      "containerPort": 5000,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "NODE_ENV", "value": "production"}
    ],
    "secrets": [
      {
        "name": "DATABASE_URL",
        "valueFrom": "arn:aws:ssm:region:account:parameter/myapp/db-url"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/myapp",
        "awslogs-region": "ap-southeast-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}
```

**Fargate** মানে EC2 manage করতে হবে না। AWS নিজে infrastructure handle করে, তুমি শুধু container দাও।

---

## ৯. CloudWatch — Monitoring & Alerting

```
তোমার অ্যাপ চলছে
      │
      ▼ metrics পাঠাচ্ছে
CloudWatch
├── Metrics    → CPU, Memory, Request count, Error rate
├── Logs       → অ্যাপের সব log এখানে আসে
├── Alarms     → threshold পার হলে notify করে
└── Dashboard  → সব একসাথে দেখো
```

### Alarm বানাও:

```
Alarm: High CPU
  Metric: EC2 CPUUtilization
  Threshold: > 80%
  Period: 5 মিনিট
  Action: SNS → তোমার email/phone এ notify
          Auto Scaling → নতুন EC2 যোগ করো
```

### Log Insights — Log থেকে তথ্য বের করো:

```sql
-- Error গুলো বের করো
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50

-- Response time বিশ্লেষণ
fields @timestamp, duration
| stats avg(duration), max(duration)
  by bin(5m)
```

---

## ১০. GitHub Actions + AWS — পুরো CI/CD

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      # AWS credentials configure
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-southeast-1

      # ECR login
      - name: Login to ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      # Build ও ECR তে push
      - name: Build and push to ECR
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        run: |
          docker build -t $ECR_REGISTRY/myapp:${{ github.sha }} .
          docker push $ECR_REGISTRY/myapp:${{ github.sha }}

      # ECS deploy
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster myapp-cluster \
            --service myapp-service \
            --force-new-deployment

      # Deploy সম্পন্ন হওয়া পর্যন্ত অপেক্ষা
      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster myapp-cluster \
            --services myapp-service
```

---

## সব একসাথে — Production Architecture

```
Bangladesh User
      │
      ▼
Route 53 (DNS)
myapp.com → ALB এর IP
      │
      ▼
CloudFront (CDN)
Static files cache করে রাখে
      │
      ▼
ALB (Load Balancer)
      │
   ┌──┴──┐
   ▼     ▼
ECS    ECS         ← Fargate container
Task   Task           Auto Scaling: 2-10
   │
   ▼
┌─────────────────────────────┐
│     Private Subnet          │
│  RDS PostgreSQL (Multi-AZ)  │
│  ElastiCache Redis          │
└─────────────────────────────┘
   │
   ▼
S3 (File Storage)
   │
   ▼
CloudWatch (Monitoring)
→ Alarm → SNS → Email/SMS
```

---

## Cost সম্পর্কে ধারণা (Singapore Region)

```
t3.micro EC2      → $0.0104/ঘণ্টা  (~$7.5/মাস)
t3.medium EC2     → $0.0416/ঘণ্টা  (~$30/মাস)
RDS t3.micro      → $0.018/ঘণ্টা   (~$13/মাস)
ALB               → $0.008/ঘণ্টা   (~$6/মাস)
S3                → $0.023/GB/মাস
CloudWatch Logs   → $0.50/GB

Free Tier (প্রথম ১২ মাস):
  EC2 t2.micro   → 750 ঘণ্টা/মাস free
  RDS t2.micro   → 750 ঘণ্টা/মাস free
  S3             → 5GB free
```

---

পুরো AWS infrastructure টা বুঝলে এবার **Terraform** দিয়ে এই সব কোড হিসেবে লেখা, অথবা সরাসরি **Kubernetes (EKS)** — কোনটা দেখতে চাও?









## AWS — কেন দরকার? কী Problem Solve করে? 🌐

---

### আগে বুঝি — AWS ছাড়া কী সমস্যা?

ধরো তুমি একটা app বানালে। এখন সবাইকে দেখাতে চাও।

```
তোমার laptop এ চলছে ✅
বন্ধু access করতে পারছে না ❌

কারণ:
  তোমার laptop এ public IP নেই
  Internet থেকে কেউ তোমার machine এ আসতে পারে না
  তুমি laptop বন্ধ করলে app বন্ধ!
```

**Solution 1: নিজে server কিনো**

```
সমস্যা:
  ❌ দামি (লক্ষ টাকা)
  ❌ জায়গা লাগে (data center)
  ❌ বিদ্যুৎ লাগে সবসময়
  ❌ Internet connection লাগে
  ❌ নিজে maintain করতে হবে
  ❌ হার্ডওয়্যার নষ্ট হলে তুমি fix করো
  ❌ User বাড়লে নতুন server কিনতে হবে
```

**Solution 2: AWS** ✅

```
  ✅ ভাড়া নাও (যতটুকু দরকার)
  ✅ যেকোনো জায়গা থেকে access
  ✅ AWS maintain করে
  ✅ User বাড়লে আরো resource নাও
  ✅ Pay করো শুধু use করলে
```

---

## AWS যে Problems Solve করে

---

## ১. 🖥️ Server Problem → EC2

### Problem:
```
App চালাতে একটা computer দরকার
যেটা 24/7 চলবে
Internet এ accessible থাকবে
```

### AWS Solution: EC2 (Elastic Compute Cloud)

```
EC2 = Virtual Computer ভাড়া

তুমি বলো:
  CPU: 2 core চাই
  RAM: 4GB চাই
  OS: Ubuntu চাই

AWS দেয়:
  একটা virtual machine
  Public IP address
  24/7 চলবে
  তুমি SSH দিয়ে ঢুকতে পারবে
```

### Real example:

```bash
# EC2 তে ঢুকে তোমার app চালাও:
ssh -i my-key.pem ubuntu@54.123.456.789

# Docker install করো
sudo apt install docker.io

# তোমার app চালাও
docker run -p 80:3000 myapp:latest

# এখন সবাই access করতে পারবে:
# http://54.123.456.789
```

### EC2 Types:
```
t3.micro   → 1 CPU, 1GB RAM  → ছোট app, free tier
t3.small   → 2 CPU, 2GB RAM  → medium app
t3.medium  → 2 CPU, 4GB RAM  → বড় app
c5.xlarge  → 4 CPU, 8GB RAM  → heavy computation
```

---

## ২. 🗄️ Database Problem → RDS

### Problem:
```
Database EC2 তে রাখলে:
  ❌ EC2 বন্ধ হলে data যাবে
  ❌ Backup নিজে করতে হবে
  ❌ Security নিজে maintain করতে হবে
  ❌ Scale করা কঠিন
```

### AWS Solution: RDS (Relational Database Service)

```
RDS = Managed Database

AWS তোমার জন্য:
  ✅ Automatic backup নেয় (daily)
  ✅ Automatic failover (একটা crash করলে আরেকটা ready)
  ✅ Encryption করে রাখে
  ✅ Patch/update নিজে করে
  ✅ Storage automatically বাড়ায়

তুমি শুধু:
  Database এ connect করো
  Query করো
  বাকি সব AWS করে!
```

### Connection:

```python
# তোমার app এ শুধু endpoint দাও:
DB_HOST = "mydb.abc123.ap-southeast-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "myapp"
DB_USER = "admin"
DB_PASS = "secret"

# AWS বাকি সব handle করে!
```

---

## ৩. 📦 File Storage Problem → S3

### Problem:
```
User photo upload করলো।
EC2 তে রাখলে:
  ❌ EC2 storage শেষ হবে
  ❌ EC2 বন্ধ হলে file যাবে
  ❌ অনেক user = অনেক file = বিশাল storage
```

### AWS Solution: S3 (Simple Storage Service)

```
S3 = Unlimited File Storage

বৈশিষ্ট্য:
  ✅ Unlimited storage (terabyte, petabyte)
  ✅ 99.999999999% durability (কখনো হারায় না)
  ✅ যেকোনো file (image, video, PDF, backup)
  ✅ Public বা private access control
  ✅ অনেক সস্তা ($0.023/GB per month)
```

### Real example:

```python
import boto3

s3 = boto3.client('s3')

# File upload করো
s3.upload_file(
    'user_photo.jpg',           # local file
    'my-bucket',                # bucket name
    'photos/user123/photo.jpg'  # S3 এ path
)

# Public URL পাবে:
# https://my-bucket.s3.amazonaws.com/photos/user123/photo.jpg
```

### S3 Use Cases:
```
User photos/videos → S3
App backups        → S3
Static website     → S3
Log files          → S3
Docker images      → ECR (S3 এর উপরে বানানো)
```

---

## ৪. 🐳 Docker Image Problem → ECR

### Problem:
```
Docker image কোথায় রাখবো?

Docker Hub:
  ❌ Public (সবাই দেখতে পাবে)
  ❌ Private repo = paid
  ❌ AWS থেকে pull করতে slow
```

### AWS Solution: ECR (Elastic Container Registry)

```
ECR = Private Docker Registry

বৈশিষ্ট্য:
  ✅ Private (শুধু তুমি access করতে পারবে)
  ✅ AWS এর ভেতরে (ECS/EKS থেকে pull অনেক fast)
  ✅ Automatic vulnerability scan
  ✅ IAM দিয়ে access control
```

### Real example (ShareTrip pipeline থেকে):

```bash
# ECR এ login করো
aws ecr get-login-password --region ap-southeast-1 \
  | docker login --username AWS \
  --password-stdin 123456.dkr.ecr.ap-southeast-1.amazonaws.com

# Image build করো
docker build -t flight-engine:abc123 .

# ECR এ tag করো
docker tag flight-engine:abc123 \
  123456.dkr.ecr.ap-southeast-1.amazonaws.com/production/flight-engine:abc123

# ECR এ push করো
docker push \
  123456.dkr.ecr.ap-southeast-1.amazonaws.com/production/flight-engine:abc123
```

---

## ৫. 🔄 Container Orchestration Problem → ECS / EKS

### Problem:
```
Docker container চালাতে হবে।
EC2 তে manually চালালে:
  ❌ Container crash করলে নিজে restart করতে হবে
  ❌ Traffic বাড়লে manually নতুন container চালাতে হবে
  ❌ Multiple server manage করা কঠিন
  ❌ Zero downtime deploy কঠিন
```

### AWS Solution: ECS (Elastic Container Service)

```
ECS = Managed Container Platform

তুমি বলো:
  "এই Docker image চালাও"
  "সবসময় ৩টা container চলুক"
  "CPU 70% হলে নতুন container চালু করো"

AWS করে:
  ✅ Container চালায়
  ✅ Crash হলে restart করে
  ✅ Health check করে
  ✅ Automatically scale করে
  ✅ Load balance করে
```

### ECS Task Definition:

```json
{
  "family": "flight-engine",
  "containerDefinitions": [
    {
      "name": "flight-engine",
      "image": "123456.ecr.aws/production/flight-engine:abc123",
      "memory": 512,
      "cpu": 256,
      "portMappings": [
        { "containerPort": 3000, "hostPort": 80 }
      ],
      "environment": [
        { "name": "DB_HOST", "value": "mydb.rds.amazonaws.com" }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost/health || exit 1"],
        "interval": 30
      }
    }
  ]
}
```

### ECS vs EKS:

```
ECS → AWS এর নিজের system (সহজ, AWS specific)
EKS → Kubernetes on AWS (complex, কিন্তু portable)

ছোট-মাঝারি team → ECS
বড় company, K8s জানলে → EKS
```

---

## ৬. 🌐 Traffic Distribution Problem → ALB

### Problem:
```
১০০০ user একসাথে আসলো।
একটা server এ সব traffic:
  ❌ Server overload
  ❌ কিছু user timeout পাবে
  ❌ একটা server down হলে সব বন্ধ
```

### AWS Solution: ALB (Application Load Balancer)

```
ALB = Traffic ভাগ করার system

        Internet
           ↓
          ALB
        ↙  ↓  ↘
  Server1 Server2 Server3
  (33%)   (33%)   (33%)

বৈশিষ্ট্য:
  ✅ Traffic সমানভাবে ভাগ করে
  ✅ Unhealthy server বাদ দেয়
  ✅ SSL termination করে (HTTPS handle করে)
  ✅ Path based routing (/api → backend, / → frontend)
```

### Path based routing:

```
ALB Rules:
  /api/*        → Backend servers
  /static/*     → S3
  /* (বাকি সব) → Frontend servers

মানে:
  api.myapp.com/api/users  → Node.js servers
  api.myapp.com/           → React servers
```

---

## ৭. 🔐 Security Problem → IAM, Security Groups, VPC

### Problem:
```
সব service সব কিছু access করতে পারলে:
  ❌ Security breach হলে সব যাবে
  ❌ Database publicly accessible = বিপদ
  ❌ কে কী করলো trace করা যায় না
```

### AWS Solution: IAM + VPC + Security Groups

**IAM (Identity and Access Management):**
```
কে কী করতে পারবে সেটা define করো।

Example:
  GitHub Actions → শুধু ECR push করতে পারবে
  ECS → শুধু ECR pull আর RDS connect করতে পারবে
  Developer → শুধু logs দেখতে পারবে

Principle of Least Privilege:
  যতটুকু দরকার ঠিক ততটুকুই permission দাও।
```

**VPC (Virtual Private Cloud):**
```
তোমার নিজের private network

Internet
   ↓
VPC (তোমার private network)
  ├── Public Subnet  → ALB, NAT Gateway (internet access আছে)
  └── Private Subnet → EC2, RDS, ElastiCache (internet নেই!)
      (database কে internet থেকে hide করো)
```

**Security Groups:**
```
Firewall rules

RDS Security Group:
  Inbound: Port 5432, Source: EC2 Security Group only
  → শুধু তোমার EC2 database access করতে পারবে
  → Internet থেকে কেউ সরাসরি database access করতে পারবে না ✅

EC2 Security Group:
  Inbound: Port 80, Source: ALB only
  → শুধু ALB traffic পাঠাতে পারবে
```

---

## ৮. 📊 Monitoring Problem → CloudWatch

### Problem:
```
App deploy হলো।
কিন্তু কিছু জানি না:
  ❌ Error হচ্ছে কিনা?
  ❌ CPU কত?
  ❌ কতজন user আসছে?
  ❌ Database slow কিনা?
```

### AWS Solution: CloudWatch

```
CloudWatch = সব কিছুর চোখ

Logs:
  Container এর সব output এখানে
  Error search করো
  Pattern খোঁজো

Metrics:
  CPU usage graph
  Memory usage
  Request count
  Error rate

Alarms:
  CPU > 80% → Slack notification পাঠাও
  Error rate > 5% → PagerDuty alert
  Disk > 90% → Email করো
```

---

## ৯. 🔑 Secret Management Problem → Parameter Store / Secrets Manager

### Problem:
```
DB password, API key কোথায় রাখবো?

Code এ রাখলে:
  ❌ GitHub এ দেখা যাবে
  ❌ সবাই জানবে

Environment variable এ রাখলে:
  ❌ কে set করলো trace নেই
  ❌ Rotate করা কঠিন
```

### AWS Solution: Parameter Store / Secrets Manager

```
# Secrets Manager এ secret রাখো:
aws secretsmanager create-secret \
  --name "prod/db-password" \
  --secret-string "super_secret_password"

# Container এ automatically inject হবে:
{
  "secrets": [
    {
      "name": "DB_PASSWORD",
      "valueFrom": "arn:aws:secretsmanager:...:prod/db-password"
    }
  ]
}

বৈশিষ্ট্য:
  ✅ Encrypted
  ✅ Audit log (কে কখন access করলো)
  ✅ Automatic rotation (password নিজে বদলায়)
  ✅ Code এ কোনো secret নেই
```

---

## ১০. ⚡ DNS & Domain Problem → Route 53

### Problem:
```
IP address দিয়ে website চালানো যায় না।
  ❌ http://54.123.456.789 → ugly
  ❌ IP বদলালে user জানবে না
  ✅ https://myapp.com → সুন্দর
```

### AWS Solution: Route 53

```
Route 53 = DNS Management

myapp.com → 54.123.456.789 (ALB IP)
api.myapp.com → ALB
cdn.myapp.com → CloudFront

বৈশিষ্ট্য:
  ✅ Health check based routing
  ✅ Latency based routing (কাছের server এ পাঠাও)
  ✅ Failover (primary down হলে backup এ যাও)
```

---

## পুরো AWS Architecture একসাথে

```
User → myapp.com
          ↓
      Route 53 (DNS)
          ↓
    CloudFront (CDN, HTTPS)
          ↓
    ALB (Load Balancer)
       ↙        ↘
  ECS Tasks    ECS Tasks
  (Container)  (Container)
       ↓              ↓
    ┌──────────────────────────┐
    │      Private Subnet      │
    │   RDS (PostgreSQL)       │
    │   ElastiCache (Redis)    │
    └──────────────────────────┘
          ↓
    S3 (File Storage)
    ECR (Docker Images)
    CloudWatch (Logs)
    Secrets Manager (Passwords)
    IAM (Permissions)
```

---

## কখন কোনটা দরকার?

```
ছোট project শুরু:
  EC2 + RDS + S3
  (সহজ, সস্তা)

Medium project:
  + ECR + ECS + ALB
  (Containerized, scalable)

বড় project:
  + EKS + CloudFront
  + Parameter Store
  + CloudWatch Alarms
  (Enterprise grade)

ShareTrip এর মতো:
  ECR → Docker image রাখো
  ECS/EKS → Container চালাও
  RDS → Database
  ElastiCache → Redis
  ALB → Traffic ভাগ করো
  CloudWatch → Monitor করো
  Secrets Manager → Password রাখো
```

---

## Learning Order 📚

```
Week 1: EC2
  → একটা server চালাও
  → SSH দিয়ে ঢোকো
  → App manually deploy করো

Week 2: S3 + RDS
  → File upload করো
  → Database connect করো

Week 3: ECR + ECS
  → Docker image push করো
  → Container deploy করো

Week 4: ALB + VPC
  → Load balancer setup করো
  → Private network বানাও

Month 2+: CloudWatch, IAM, Route 53
  → Monitor, secure, domain setup
```

> AWS এর সব service একসাথে না শিখে
> **একটা একটা করে হাতে কলমে** practice করো।
> Free tier দিয়ে শুরু করো — প্রথম ১ বছর অনেক কিছু free! 💡
