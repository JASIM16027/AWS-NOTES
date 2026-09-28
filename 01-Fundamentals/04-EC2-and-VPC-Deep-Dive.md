# 🖥️ EC2 + VPC — Technical Deep Dive

---

## 1. VPC কী — Core Concept

<img width="758" height="597" alt="image" src="https://github.com/user-attachments/assets/8c767627-cf8c-4e67-86bd-c7d7f5e235fe" />


VPC = **Virtual Private Cloud**

```
Real World:        AWS World:
Office Building  = VPC
Floor            = Subnet
Room             = EC2 Instance
Security Guard   = Security Group
Building Rules   = Network ACL
Main Gate        = Internet Gateway
```

AWS এ তুমি যখন কিছু create করো, সব কিছু একটা VPC এর ভিতরে থাকে। VPC ছাড়া কোনো resource exist করে না।

---

## 2. VPC — Full Architecture

Production এ কেমন দেখতে হয়:

```
VPC: 10.0.0.0/16  (65,536 IPs)
│
├── Public Subnet 10.0.1.0/24  (AZ-1a)
│   ├── EC2: NestJS API Server
│   ├── EC2: Nginx (Reverse Proxy)
│   └── NAT Gateway
│
├── Public Subnet 10.0.2.0/24  (AZ-1b)
│   └── EC2: NestJS API Server (replica)
│
├── Private Subnet 10.0.3.0/24 (AZ-1a)
│   └── RDS: PostgreSQL (Primary)
│
└── Private Subnet 10.0.4.0/24 (AZ-1b)
    └── RDS: PostgreSQL (Standby)
```

---

## 3. CIDR — IP Range বোঝো

```
VPC CIDR: 10.0.0.0/16

/16 মানে:
├── First 16 bits fixed:  10.0
├── Last 16 bits flexible: 0.0 → 255.255
└── Total IPs: 65,536

Subnet CIDR: 10.0.1.0/24
├── First 24 bits fixed:  10.0.1
├── Last 8 bits flexible:  0 → 255
└── Total IPs: 256 (251 usable, AWS 5টা reserve করে)

Reserved by AWS (10.0.1.0/24):
├── 10.0.1.0   → Network address
├── 10.0.1.1   → VPC Router
├── 10.0.1.2   → DNS Server
├── 10.0.1.3   → Future use
└── 10.0.1.255 → Broadcast
```

---

## 4. Networking Components

### 4.1 Internet Gateway (IGW)

```
Role: VPC কে public internet এ connect করে

Flow:
Internet ←→ IGW ←→ VPC (Public Subnet)

Rules:
├── একটা VPC তে একটাই IGW
├── Public Subnet এর route table এ থাকতে হবে
└── EC2 এর public IP থাকতে হবে
```

এখন বিস্তারিত diagram এবং explanation তৈরি করছি।এখন প্রতিটি অংশ বিস্তারিত বুঝি।

<img width="801" height="674" alt="image" src="https://github.com/user-attachments/assets/7879548a-2a16-4f9c-83ca-89bb049cabb0" />


---

## IGW (Internet Gateway) — সম্পূর্ণ ব্যাখ্যা

### IGW কী করে?

IGW হলো VPC আর public internet-এর মধ্যে একটা **দরজা**। এটা দুটো কাজ করে:

**১. Routing target** — Route table-এ `0.0.0.0/0 → igw-xxx` লেখা থাকলে সব বাইরের traffic এই দরজা দিয়ে আসবে।

**২. NAT (1-to-1)** — EC2-এর private IP (`10.0.1.15`) আর public IP (`54.23.11.7`) এর মধ্যে mapping করে। Internet packet আসলে IGW সেটা private IP-তে forward করে দেয়, reply যাওয়ার সময় আবার public IP-তে বদলে দেয়।

---

### তিনটি Rule কেন জরুরি

**Rule #1 — একটা VPC তে একটাই IGW**
একটা VPC-তে দুটো IGW attach করা যায় না। AWS এটা enforce করে কারণ routing ambiguity হবে — দুটো default gateway থাকলে packet কোনটা দিয়ে বের হবে সেটা নির্ধারণ করা যাবে না।

**Rule #2 — Route table-এ `0.0.0.0/0 → IGW` থাকতে হবে**
শুধু IGW attach করলেই হয় না। Subnet-এর route table-এ explicitly `0.0.0.0/0` এর destination হিসেবে IGW-এর ID দিতে হবে। এই entry না থাকলে subnet টা private-ই থাকবে — IGW attach থাকলেও traffic বের হবে না।

**Rule #3 — EC2-এর Public IP থাকতে হবে**
IGW NAT করতে পারবে শুধুমাত্র তখন, যখন EC2-এর একটা public IP address আছে। Public IP না থাকলে internet থেকে কেউ reach করতে পারবে না, EC2 থেকেও বাইরে যাওয়া যাবে না। Public IP দুই ভাবে পাওয়া যায় — auto-assign বা Elastic IP।

---

### Private Subnet এর সাথে পার্থক্য

| বিষয় | Public Subnet | Private Subnet |
|---|---|---|
| Route table | `0.0.0.0/0 → IGW` | `0.0.0.0/0 → NAT GW` বা নেই |
| EC2 Public IP | লাগবে | লাগবে না |
| Internet থেকে reach | সরাসরি সম্ভব | সম্ভব না |
| Internet-এ যাওয়া | IGW দিয়ে | NAT Gateway দিয়ে |


### 4.2 Route Table

```
Public Subnet Route Table:
┌─────────────────┬──────────────┐
│ Destination     │ Target       │
├─────────────────┼──────────────┤
│ 10.0.0.0/16    │ local        │ ← VPC internal
│ 0.0.0.0/0      │ igw-xxxxxxx  │ ← internet
└─────────────────┴──────────────┘

Private Subnet Route Table:
┌─────────────────┬──────────────┐
│ Destination     │ Target       │
├─────────────────┼──────────────┤
│ 10.0.0.0/16    │ local        │ ← VPC internal only
│ 0.0.0.0/0      │ nat-xxxxxxx  │ ← NAT (outbound only)
└─────────────────┴──────────────┘
```

### 4.3 NAT Gateway

```
Problem:
Private Subnet এ RDS আছে
RDS কে OS update করতে internet দরকার
কিন্তু internet থেকে directly access দেওয়া যাবে না

Solution: NAT Gateway

Flow:
RDS (Private) → NAT Gateway (Public) → Internet
                      ↑
              Outbound only!
              Internet থেকে initiate করা যাবে না
```

### 4.4 Security Group (SG)

```
Type: Stateful Firewall
Level: Instance level

Stateful মানে:
├── Outbound allow করলে
└── Response automatically inbound allow হয়

Example — NestJS API Server SG:
┌──────────┬──────────┬───────────────┬──────────────────┐
│ Type     │ Protocol │ Port          │ Source           │
├──────────┼──────────┼───────────────┼──────────────────┤
│ Inbound  │ TCP      │ 22 (SSH)      │ Your IP only     │
│ Inbound  │ TCP      │ 3000 (API)    │ ALB SG only      │
│ Inbound  │ TCP      │ 443 (HTTPS)   │ 0.0.0.0/0        │
├──────────┼──────────┼───────────────┼──────────────────┤
│ Outbound │ All      │ All           │ 0.0.0.0/0        │
└──────────┴──────────┴───────────────┴──────────────────┘

RDS Security Group:
┌──────────┬──────────┬───────────────┬──────────────────┐
│ Inbound  │ TCP      │ 5432 (PG)     │ EC2 SG only      │
└──────────┴──────────┴───────────────┴──────────────────┘
```

### 4.5 Network ACL (NACL)

```
Type: Stateless Firewall
Level: Subnet level

Stateless মানে:
├── Inbound allow করলে
└── Outbound আলাদা করে allow করতে হবে

SG vs NACL:
┌─────────────┬──────────────┬──────────────┐
│             │ Security Grp │ NACL         │
├─────────────┼──────────────┼──────────────┤
│ Level       │ Instance     │ Subnet       │
│ State       │ Stateful     │ Stateless    │
│ Rules       │ Allow only   │ Allow + Deny │
│ Order       │ All evaluate │ Number order │
└─────────────┴──────────────┴──────────────┘
```

---

## 5. EC2 — Technical Deep Dive

### 5.1 Instance Types

```
Naming: [Family][Generation].[Size]

t3.micro breakdown:
├── t  → Family (General Purpose, Burstable)
├── 3  → Generation (3rd)
└── micro → Size (smallest)

Families:
├── t → General Purpose (Burstable)    → Dev/Test
├── m → General Purpose (Balanced)     → Production API
├── c → Compute Optimized              → CPU intensive
├── r → Memory Optimized               → Database, Cache
└── i → Storage Optimized              → Big Data

Common sizes:
nano < micro < small < medium < large < xlarge < 2xlarge
```

### 5.2 Storage Types

```
EBS (Elastic Block Store):
├── EC2 এর hard drive মতো
├── EC2 terminate হলেও data থাকে (optional)
│
├── gp3 (General Purpose SSD)
│   ├── 3,000 IOPS baseline
│   ├── Up to 16,000 IOPS
│   └── Use: Most workloads
│
├── io2 (Provisioned IOPS SSD)
│   ├── Up to 64,000 IOPS
│   └── Use: High-performance DB
│
└── st1 (Throughput HDD)
    ├── Cheap
    └── Use: Log storage, cold data

Instance Store:
├── Physical disk on host machine
├── Extremely fast
└── ⚠️ EC2 stop/terminate = data LOST
```

### 5.3 AMI (Amazon Machine Image)

```
AMI = EC2 এর template

Contains:
├── OS (Ubuntu 22.04, Amazon Linux 2, etc.)
├── Pre-installed software
└── Storage configuration

Types:
├── AWS provided (Ubuntu, Amazon Linux)
├── AWS Marketplace (pre-configured apps)
└── Custom AMI (তুমি নিজে বানাও)

Custom AMI workflow:
EC2 setup করো
    ↓
Node.js, NestJS install করো
    ↓
Configure করো
    ↓
"Create Image" → AMI ready
    ↓
এই AMI দিয়ে নতুন EC2 তৈরি করো (identical)
```

### 5.4 User Data Script

```bash
# EC2 launch এর সময় automatically run হয়
#!/bin/bash

# System update
apt-get update -y

# Node.js install
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# PM2 install (process manager)
npm install -g pm2

# App clone
git clone https://github.com/yourrepo/nestjs-app.git /app
cd /app

# Dependencies install
npm install

# Build
npm run build

# Start with PM2
pm2 start dist/main.js --name "nestjs-app"
pm2 startup
pm2 save
```

---

## 6. Full Request Flow — Technical

```
Client (Browser/Mobile)
        ↓ HTTPS Request
        
Route 53 (DNS)
├── Domain → ALB IP resolve করে
        ↓
        
CloudFront (Optional CDN)
├── Static assets cache করে
├── DDoS protection
        ↓
        
Application Load Balancer (ALB)
├── SSL Termination (HTTPS → HTTP)
├── Health check করে
├── Round-robin routing
        ↓ HTTP (port 3000)
        
EC2: NestJS App (Public Subnet)
├── Business logic
├── JWT verify
        ↓              ↓
        
RDS PostgreSQL    S3 Bucket
(Private Subnet)  (File Storage)
├── Query run     ├── File upload
└── Data return   └── URL return
        ↓
        
Response back same path এ
```

---

## 7. Step-by-Step: VPC তৈরি করো

```
Step 1: VPC Create
├── Name: my-app-vpc
├── CIDR: 10.0.0.0/16
└── Tenancy: Default

Step 2: Subnets Create
├── Public-1:  10.0.1.0/24 (ap-south-1a)
├── Public-2:  10.0.2.0/24 (ap-south-1b)
├── Private-1: 10.0.3.0/24 (ap-south-1a)
└── Private-2: 10.0.4.0/24 (ap-south-1b)

Step 3: Internet Gateway
├── Create IGW
└── Attach to VPC

Step 4: NAT Gateway
├── Create in Public Subnet
└── Allocate Elastic IP

Step 5: Route Tables
├── Public RT:
│   ├── 0.0.0.0/0 → IGW
│   └── Associate: Public-1, Public-2
└── Private RT:
    ├── 0.0.0.0/0 → NAT
    └── Associate: Private-1, Private-2

Step 6: Security Groups
├── ALB-SG:    inbound 80, 443 from internet
├── EC2-SG:    inbound 3000 from ALB-SG only
│              inbound 22 from your IP only
└── RDS-SG:    inbound 5432 from EC2-SG only
```

---

## 8. EC2 তে NestJS Deploy

```bash
# 1. EC2 তে SSH করো
ssh -i "my-key.pem" ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# 2. Node.js install
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 3. App deploy
git clone https://github.com/your/nestjs-app.git
cd nestjs-app
npm install
npm run build

# 4. Environment variables
sudo nano /etc/environment
# Add:
# DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/db
# AWS_REGION=ap-south-1

# 5. PM2 দিয়ে run
sudo npm install -g pm2
pm2 start dist/main.js --name nestjs-app
pm2 startup systemd
pm2 save

# 6. Nginx reverse proxy
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/default
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 9. IAM Role EC2 তে Attach করো

```
NestJS app থেকে S3 access করতে:

Step 1: IAM Role বানাও
├── Trusted Entity: EC2
└── Policy: AmazonS3FullAccess (or custom)

Step 2: EC2 তে attach করো
EC2 Console → Actions → Security
→ Modify IAM Role → Select Role

Step 3: Code এ credentials লাগবে না
```

```typescript
// NestJS এ S3 upload — No credentials needed!
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({ 
  region: "ap-south-1"
  // IAM Role automatically handle করে
});

async uploadFile(file: Buffer, key: string) {
  await s3.send(new PutObjectCommand({
    Bucket: "my-app-bucket",
    Key: key,
    Body: file,
  }));
}
```

---

## 10. Complete Architecture Summary

```
Internet
    ↓
IGW (Internet Gateway)
    ↓
┌─────────────────────────────────────┐
│           VPC 10.0.0.0/16           │
│                                     │
│  ┌──────────────────────────────┐   │
│  │      Public Subnets          │   │
│  │  ┌──────────┐ ┌──────────┐  │   │
│  │  │  ALB     │ │NAT GW    │  │   │
│  │  └────┬─────┘ └──────────┘  │   │
│  │       ↓                     │   │
│  │  ┌──────────┐ ┌──────────┐  │   │
│  │  │  EC2     │ │  EC2     │  │   │
│  │  │ NestJS   │ │ NestJS   │  │   │
│  │  └──────────┘ └──────────┘  │   │
│  └──────────────────────────┘   │   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │      Private Subnets         │   │
│  │  ┌──────────┐ ┌──────────┐  │   │
│  │  │   RDS    │ │   RDS    │  │   │
│  │  │ Primary  │ │ Standby  │  │   │
│  │  └──────────┘ └──────────┘  │   │
│  └──────────────────────────┘   │   │
└─────────────────────────────────────┘
```

---

এখন বলো — **RDS setup + NestJS connection** দেখবো নাকি **Load Balancer + Auto Scaling** implement করবো? 🔥



# EC2 + VPC — Technical Deep Dive

AWS-এর দুটো ফাউন্ডেশনাল সার্ভিস, যেগুলো বুঝলে cloud infrastructure-এর ৭০% ক্লিয়ার হয়ে যায়। চলো গভীরে যাই।

---

## VPC (Virtual Private Cloud) — তোমার নিজস্ব নেটওয়ার্ক

VPC হলো AWS-এর ভেতরে তোমার **logically isolated** একটা নেটওয়ার্ক। ভাবো, AWS-এর বিশাল ডেটা সেন্টারের ভেতরে তুমি একটা "প্রাইভেট এলাকা" ভাড়া নিলে — সেখানে কে ঢুকবে, কে বের হবে, কীভাবে ট্রাফিক চলবে — সব তুমি নিয়ন্ত্রণ করো।

### CIDR Block — ঠিকানার সীমানা

VPC তৈরি করার সময় প্রথমেই একটা **CIDR block** দিতে হয়, যেমন `10.0.0.0/16`। এর মানে তুমি 65,536টা IP address নিজের জন্য reserve করলে (10.0.0.0 থেকে 10.0.255.255)। `/16` মানে প্রথম 16 bit fixed, বাকি 16 bit তোমার খেলার জায়গা।

সাধারণত তিনটা **private IP range** ব্যবহার হয় (RFC 1918):
- `10.0.0.0/8` — সবচেয়ে বড়, enterprise-এ common
- `172.16.0.0/12`
- `192.168.0.0/16` — home network-এ দেখা যায়

### Subnet — VPC-এর ভেতরে বিভাগ

VPC পুরোটা এক region-এ থাকে, কিন্তু subnet থাকে এক নির্দিষ্ট **Availability Zone (AZ)**-এ। এখানেই high availability-এর ম্যাজিক — তুমি একই VPC-তে multiple AZ-এ subnet বানিয়ে disaster-proof architecture বানাতে পারো।

দুই ধরনের subnet:

**Public Subnet** — এই subnet-এর route table-এ **Internet Gateway (IGW)**-এর route আছে। এখানে launch করা EC2-কে public IP দিলে সেটা সরাসরি internet-এ পৌঁছাতে পারে। Web server এখানে বসে।

**Private Subnet** — IGW-এর direct route নেই। Database, internal API — এগুলো এখানে থাকে। Internet-এ যেতে হলে **NAT Gateway**-এর মাধ্যমে যেতে হয় (outbound only, inbound নেই)।

### Routing — ট্রাফিক কোন দিকে যাবে

প্রতিটা subnet একটা **Route Table**-এর সাথে associated। Route table বলে দেয়: "এই destination-এর জন্য এই path নাও।"

একটা সাধারণ public subnet-এর route table:
```
10.0.0.0/16    →    local          (VPC-এর ভেতরে)
0.0.0.0/0      →    igw-xxxxx      (বাইরের সব internet traffic)
```

`0.0.0.0/0` মানে "সব কিছু" — এটাই default route, internet-এ যাওয়ার পথ।

### Security — দুই স্তরের দেয়াল

AWS দুইটা firewall layer দিয়েছে, দুটোর কাজ আলাদা:

**Security Group** — EC2 instance-এর level-এ কাজ করে। **Stateful** — মানে outbound request-এর response automatic allow হয়, আলাদা rule লাগে না। শুধু *allow* rule লেখা যায়, *deny* নেই।

**Network ACL (NACL)** — Subnet-এর level-এ কাজ করে। **Stateless** — inbound এবং outbound দুইদিকেই explicit rule লাগে। Allow এবং deny দুটোই লেখা যায়। Rule number অনুযায়ী evaluate হয় (সবচেয়ে ছোট number আগে)।

Practical tip: ৯০% ক্ষেত্রে Security Group দিয়েই কাজ হয়ে যায়। NACL ব্যবহার হয় যখন তুমি পুরো subnet-কে কোনো specific IP থেকে block করতে চাও।

### অন্যান্য গুরুত্বপূর্ণ component

**Internet Gateway (IGW)** — VPC-কে internet-এর সাথে connect করে। এক VPC-তে একটাই IGW attach করা যায়।

**NAT Gateway** — Private subnet-এর EC2-কে outbound internet access দেয় (software update-এর জন্য, ধরো)। কিন্তু বাইরে থেকে কেউ ঢুকতে পারে না। Managed service, AZ-specific — high availability-র জন্য প্রতিটা AZ-তে আলাদা NAT Gateway দরকার।

**VPC Endpoints** — S3 বা DynamoDB-র মতো AWS service-এ যেতে public internet-এ না গিয়ে AWS-এর internal network দিয়ে যাওয়ার রাস্তা। Security আর cost দুটোই বাঁচে।

**VPC Peering** — দুটো VPC-কে directly connect করা। কিন্তু transitive routing নেই — A↔B আর B↔C থাকলেও A automatically C-তে পৌঁছাবে না।

**Transit Gateway** — অনেকগুলো VPC আর on-premise network-কে একটা hub-এ connect করার solution। Enterprise-scale-এ essential।

---

## EC2 (Elastic Compute Cloud) — Virtual Server

EC2 হলো AWS-এর virtual machine service। তুমি OS, CPU, RAM, storage বেছে একটা server "launch" করো — মিনিটে ready।

### Instance Type — কোন machine নেবে

Naming convention বুঝলে ৫০% কাজ সহজ। যেমন `m5.large`:
- **m** — instance family (general purpose)
- **5** — generation (নতুন generation মানে better performance, প্রায়ই cheaper)
- **large** — size

Family-গুলো মনে রাখার সহজ উপায়:
- **T** (t3, t4g) — burstable, সস্তা, dev/test-এ ভালো। CPU credit system — idle থাকলে credit জমে, load এলে খরচ হয়।
- **M** (m5, m6i) — general purpose, balanced CPU/RAM
- **C** (c5, c6i) — compute-optimized, CPU-heavy workload (gaming server, batch processing)
- **R** (r5, r6i) — memory-optimized (in-memory DB, cache, Redis)
- **I** (i3, i4i) — storage-optimized, high IOPS NVMe SSD
- **G, P** — GPU (ML training, graphics)

`g` suffix (যেমন `t4g`) মানে Graviton processor — ARM-based, AWS-এর নিজের চিপ, ২০% পর্যন্ত সস্তা।

### AMI (Amazon Machine Image) — Server-এর template

AMI হলো একটা snapshot — OS, pre-installed software, configuration সব নিয়ে। চার ধরনের source:
- AWS-provided (Amazon Linux, Ubuntu, Windows)
- Marketplace (vendor-packaged, যেমন pre-configured WordPress)
- Community AMI
- Custom AMI (তোমার নিজের বানানো — golden image pattern)

Production-এ best practice: নিজের AMI বানাও Packer দিয়ে, version control-এ রাখো।

### Storage — EBS vs Instance Store

**EBS (Elastic Block Store)** — Network-attached persistent storage। Instance terminate হলেও data থাকে (যদি "delete on termination" off করা থাকে)। AZ-specific — এক AZ-এর EBS volume অন্য AZ-এ attach হয় না, snapshot নিয়ে copy করতে হয়।

EBS volume types:
- **gp3** — general purpose SSD, এখন default choice। IOPS আর throughput আলাদাভাবে tune করা যায়।
- **gp2** — পুরোনো generation, size-এর সাথে IOPS bundled
- **io2 / io2 Block Express** — high performance, critical database-এর জন্য
- **st1** — throughput-optimized HDD, big data, log processing
- **sc1** — cold HDD, সবচেয়ে সস্তা, rarely accessed data

**Instance Store** — Physical host-এর সাথে attached local NVMe SSD. অসম্ভব fast, কিন্তু **ephemeral** — instance stop বা terminate হলে data হারায়। Cache, temporary data-র জন্য ব্যবহার হয়।

### IP Address-এর গল্প

একটা EC2-এর IP তিন ধরনের হতে পারে:

**Private IP** — VPC-এর ভেতরের IP, instance-এর সারা জীবন একই থাকে।

**Public IP** — Internet-facing IP, কিন্তু instance stop/start করলে বদলে যায়। Auto-assigned।

**Elastic IP (EIP)** — Static public IP যেটা তুমি reserve করো। Instance-এর সাথে bind করলে stop/start-এও বদলায় না। Unused থাকলে charge হয় (AWS চায় না তুমি IP hoard করো)।

### Instance Lifecycle এবং Pricing

**Lifecycle states:** pending → running → stopping → stopped → terminated। Terminate মানে instance চিরতরে শেষ (EBS-ও delete হতে পারে)। Stop মানে pause — EBS থাকে, compute charge বন্ধ।

**Pricing models:**
- **On-Demand** — pay-per-hour/second, কোনো commitment নেই। সবচেয়ে expensive, কিন্তু flexible।
- **Reserved Instance (RI)** — ১ বা ৩ বছরের commitment, ৭২% পর্যন্ত discount।
- **Savings Plans** — RI-এর modern version, আরো flexible (instance family বদলানো যায়)।
- **Spot Instance** — AWS-এর unused capacity, ৯০% পর্যন্ত cheap। কিন্তু ২ মিনিটের notice দিয়ে AWS যেকোনো সময় instance নিয়ে নিতে পারে। Fault-tolerant workload-এর জন্য perfect (batch jobs, CI/CD runners)।
- **Dedicated Host** — পুরো physical server তোমার, compliance বা licensing-এর জন্য।

### User Data এবং IAM Role

**User Data** — Instance launch-এর সময় একটা bootstrap script চালানো যায় (bash বা cloud-init)। Package install, service start — automation-এর প্রথম ধাপ।

**IAM Instance Profile** — EC2-কে AWS credential হার্ডকোড না করে S3, DynamoDB-তে access দেওয়ার উপায়। SDK automatically এই role-এর credential use করে। **কখনোই** EC2-তে AWS access key রাখবে না।

### Auto Scaling + Load Balancer — Production Pattern

একটা real-world architecture সাধারণত এরকম:

**Application Load Balancer (ALB)** public subnet-এ বসে, traffic receive করে। পেছনে **Auto Scaling Group (ASG)** আছে যেটা multiple AZ-এর private subnet-এ EC2 launch করে। Load বাড়লে ASG instance বাড়ায়, কমলে কমায়। Launch Template-এ AMI, instance type, user data — সব define করা থাকে।

Database (RDS) থাকে আরেকটা private subnet-এ, শুধু application-এর security group থেকে access allowed।

---

## EC2 + VPC — কিভাবে মিলে কাজ করে

একটা EC2 instance **অবশ্যই** একটা VPC-র subnet-এ launch হয়। VPC ছাড়া EC2 হয় না (legacy EC2-Classic এখন deprecated)।

Connection flow এভাবে ভাবো:

একজন user তোমার website visit করলো। Request DNS resolve হয়ে ALB-র public IP-তে গেলো। ALB (public subnet, IGW-র মাধ্যমে reachable) request receive করে, target group-এর EC2-তে (private subnet) forward করলো। EC2 RDS (আরো deeper private subnet)-কে query করলো। Response একই path-এ ফিরে আসলো।

এই entire journey-তে security group আর route table প্রতি hop-এ check করছে — "এই traffic allowed?"

---

## কিছু practical best practice

High availability-র জন্য minimum ২টা AZ ব্যবহার করো, auto scaling group multi-AZ রাখো, RDS Multi-AZ enable করো। Security-র দিক থেকে: database কখনো public subnet-এ রাখবে না, security group-এ `0.0.0.0/0` SSH (port 22) allow করা মানে disaster invite করা — Session Manager ব্যবহার করো, এতে SSH key আর bastion host-এর ঝামেলাই থাকে না। Cost control-এর জন্য: NAT Gateway expensive ($0.045/hour + data), VPC Endpoint দিয়ে S3/DynamoDB traffic bypass করো; unused Elastic IP release করো; dev environment-এ Spot instance ব্যবহার করো।

---

কোন specific অংশ আরো deep dive করতে চাও? যেমন security group আর NACL-এর subtle পার্থক্য, NAT Gateway vs NAT Instance, বা Auto Scaling Group-এর scaling policy — বললে detail-এ যাবো।
