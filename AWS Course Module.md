
## AWS Course — ৮টি মডিউলের বিস্তারিত পাঠ্যক্রম

---

### মডিউল ১ — EC2 & Storage Fundamentals

AWS ক্লাউডের সবচেয়ে মৌলিক কম্পিউট সার্ভিস EC2 এবং বিভিন্ন স্টোরেজ অপশন সম্পর্কে শেখা হয়।

**EC2 বেসিক্স**
- Instance types (t2, m5, c5, r5)
- AMI (Amazon Machine Image)
- EC2 Launch & Configure
- Key Pairs ও Security Groups
- Elastic IP Address

**Storage Types**
- EBS (Elastic Block Store)
- EBS Volume Types: gp2, gp3, io1
- Instance Store (Ephemeral)
- EFS (Elastic File System)
- S3 ও Glacier overview

**EC2 Pricing Models**
- On-Demand Instances
- Reserved Instances (1yr/3yr)
- Spot Instances
- Savings Plans
- Dedicated Hosts

**Auto Scaling**
- Launch Templates
- Auto Scaling Groups
- Scaling Policies (Target, Step)
- Cooldown Periods
- Health Checks

---

### মডিউল ২ — VPC Design & Network Architecture

Virtual Private Cloud দিয়ে সম্পূর্ণ আইসোলেটেড নেটওয়ার্ক তৈরি করা এবং ইন্টারনেট কানেক্টিভিটি ম্যানেজ করা।

**VPC Core Components**
- CIDR Block planning
- Subnets (Public vs Private)
- Internet Gateway (IGW)
- Route Tables
- Network ACL vs Security Groups

**NAT & Connectivity**
- NAT Gateway (Managed)
- NAT Instance (EC2-based)
- Bastion Host / Jump Server
- VPC Endpoints (Interface & Gateway)
- AWS PrivateLink

**DNS & IP Management**
- Route 53 Resolver
- DHCP Option Sets
- Elastic IP (EIP)
- IPv6 support in VPC
- DNS Resolution & Hostnames

**Network Design Patterns**
- Hub-and-Spoke Model
- 3-Tier Architecture
- Public/Private Subnet layout
- Multi-AZ deployment
- High Availability Design

---

### মডিউল ৩ — Application Deployment on EC2 with systemd

EC2-তে রিয়েল অ্যাপ্লিকেশন ডিপ্লয় করা এবং systemd দিয়ে সার্ভিস ম্যানেজ করা।

**EC2 Setup & Config**
- User Data scripts (cloud-init)
- EC2 Instance Connect
- SSM Session Manager
- IAM Instance Profile
- CloudWatch Agent setup

**systemd Service Management**
- Unit file তৈরি করা (.service)
- ExecStart, WorkingDirectory
- Environment Variables
- Restart policies (always, on-failure)
- systemctl enable/start/status

**Application Stack**
- Nginx Reverse Proxy config
- Node.js / Python app deploy
- PM2 Process Manager
- Environment-based config (.env)
- Log management with journald

**CI/CD Integration**
- CodeDeploy Agent setup
- AppSpec.yml configuration
- Rolling vs Blue/Green deploy
- GitHub Actions to EC2
- Deployment Lifecycle Hooks

---

### মডিউল ৪ — Serverless & Lambda Fundamentals

সার্ভার ম্যানেজ ছাড়াই কোড রান করার পদ্ধতি — AWS Lambda দিয়ে ইভেন্ট-ড্রিভেন কম্পিউটিং।

**Lambda Basics**
- Execution model (cold/warm start)
- Runtime: Node.js, Python, Java
- Handler function structure
- Memory & Timeout config
- Deployment packages & Layers

**Lambda Triggers**
- API Gateway (HTTP trigger)
- S3 Event notifications
- DynamoDB Streams
- SQS / SNS triggers
- CloudWatch Events / EventBridge

**Permissions & Security**
- Execution Role (IAM)
- Resource-based policies
- VPC Lambda configuration
- Environment Variables (encrypted)
- Secrets Manager integration

**Monitoring & Performance**
- CloudWatch Logs & Metrics
- X-Ray Tracing
- Provisioned Concurrency
- Reserved Concurrency
- Lambda Power Tuning

---

### মডিউল ৫ — Event-Driven Architectures with Lambda

Loosely-coupled, scalable সিস্টেম তৈরি করা যেখানে কম্পোনেন্টগুলো ইভেন্টের মাধ্যমে যোগাযোগ করে।

**Messaging Services**
- SQS (Simple Queue Service)
- Standard Queue vs FIFO Queue
- Dead Letter Queue (DLQ)
- SNS (Simple Notification Service)
- Fan-out pattern

**EventBridge**
- Event Bus (Default vs Custom)
- Event Rules & Patterns
- Targets (Lambda, SQS, Step Fn)
- Scheduled Events (cron)
- Cross-account events

**Step Functions**
- State Machine basics
- Task, Choice, Wait, Parallel states
- Express vs Standard workflows
- Error handling & Retry
- Lambda orchestration

**Design Patterns**
- Saga Pattern (distributed txn)
- Event Sourcing
- CQRS with DynamoDB Streams
- Async request/response
- Idempotency handling

---

### মডিউল ৬ — Multi-VPC & Private Connectivity

একাধিক VPC, অ্যাকাউন্ট এবং অন-প্রিমিস নেটওয়ার্কের মধ্যে নিরাপদ সংযোগ স্থাপন।

**VPC Peering & TGW**
- VPC Peering (limitations)
- Transit Gateway (TGW)
- TGW Route Tables
- TGW Attachments
- Inter-region peering

**Hybrid Connectivity**
- Site-to-Site VPN
- AWS Direct Connect
- Direct Connect Gateway
- VPN over Direct Connect
- BGP routing basics

**AWS Organizations**
- Organizational Units (OUs)
- Service Control Policies (SCPs)
- AWS RAM (Resource Access Mgr)
- Centralized VPC sharing
- Multi-account strategy

**Private Connectivity**
- AWS PrivateLink
- VPC Endpoint Services
- Interface Endpoints
- Gateway Endpoints (S3, DynamoDB)
- DNS resolution for endpoints

---

### মডিউল ৭ — Edge Services, DNS & Load Balancing

গ্লোবাল ট্র্যাফিক ম্যানেজমেন্ট, কনটেন্ট ডেলিভারি এবং লোড ব্যালেন্সিং আর্কিটেকচার।

**CloudFront CDN**
- Distributions (Web vs RTMP)
- Origins (S3, ALB, Custom)
- Cache Behaviors & TTL
- Lambda@Edge / CloudFront Fn
- Geo Restriction & WAF

**Route 53 DNS**
- Hosted Zones (Public/Private)
- Routing Policies: Simple, Weighted
- Latency-based, Failover
- Geolocation, Geoproximity
- Health Checks & DNS Failover

**Load Balancers**
- ALB (Application Load Balancer)
- NLB (Network Load Balancer)
- GWLB (Gateway Load Balancer)
- Target Groups & Health Checks
- Listener Rules & Redirects

**Global Accelerator**
- Anycast IP addresses
- Endpoints & Endpoint Groups
- Traffic dial & weights
- Client affinity
- Accelerator vs CloudFront

---

### মডিউল ৮ — Network Security & Monitoring

AWS নেটওয়ার্ককে থ্রেট থেকে রক্ষা করা এবং সম্পূর্ণ ভিজিবিলিটি নিশ্চিত করা।

**Firewalls & DDoS**
- AWS WAF (Web ACL, Rules)
- AWS Shield Standard & Advanced
- AWS Network Firewall
- Firewall Policy & Rule Groups
- Centralized firewall deployment

**Network Monitoring**
- VPC Flow Logs
- CloudWatch Logs Insights
- Traffic Mirroring
- AWS Config for network rules
- GuardDuty (DNS & traffic analysis)

**Security Services**
- AWS Security Hub
- Amazon Inspector (network reach)
- IAM Access Analyzer
- Macie (S3 data sensitivity)
- Detective (investigation)

**Compliance & Audit**
- CloudTrail (API audit log)
- AWS Config Rules
- Service Control Policies
- Encryption in transit (TLS)
- Secrets rotation (Secrets Mgr)
