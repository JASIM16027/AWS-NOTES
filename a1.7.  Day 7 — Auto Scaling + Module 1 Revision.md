# 📚 Day 7 — Auto Scaling + Module 1 Revision

**সময়:** ১.৫ ঘণ্টা | **Module:** ১ (EC2 & Storage Fundamentals) — শেষ দিন

## 🎯 আজকের লক্ষ্য
- Auto Scaling কেন দরকার ও কী problem solve করে
- Launch Template vs Launch Configuration
- Auto Scaling Group (ASG)-এর architecture
- Scaling Policies: Target Tracking, Step, Simple, Scheduled, Predictive
- Cooldown Period ও Health Checks
- Real-world scenario ও best practices
- পুরো Module 1-এর revision ও interconnection

---

## Part 1: Auto Scaling — ভিত্তি থেকে

### 🤔 Auto Scaling কেন দরকার?

### Scenario: Traditional Setup

একটা e-commerce website ভাবুন (যেমন Daraz)।

**Normal day traffic:** 1,000 user/hour → ২টা server যথেষ্ট

**Eid sale day:** 50,000 user/hour → ২০টা server দরকার

**Traditional-এ কী করেন?**

**Option A:** সবসময় ২০টা server রাখুন
- সমস্যা: ৩৬০ দিন ১৮টা server idle
- Cost: 10x বেশি যা দরকার

**Option B:** ২টা server রাখুন, Eid-এ manually add করুন
- সমস্যা: কখন add করবেন? Server বানাতে সময় লাগবে
- User wait করবে, website slow → customer হারাবেন

**Option C:** ৫টা server মাঝামাঝি
- সমস্যা: Normal day-এ 3টা waste, Eid-এ ১৫টা কম

### ✨ Auto Scaling-এর Solution

**Auto Scaling automatically instance-এর সংখ্যা বাড়ায়-কমায় demand-এর সাথে সাথে।**

- Morning 9 AM: 2 instances (কম traffic)
- Afternoon 2 PM: 5 instances (বেশি traffic)
- Night 12 AM: 1 instance (খুব কম)
- Eid 11 AM: 20 instances (peak)
- Eid 6 AM: 5 instances (ফিরে আসছে)

**সব automatic, কেউ manually কিছু করছে না।**

### 🎯 Auto Scaling-এর 3 টা Benefit

**1. Cost Optimization**
- যখন দরকার শুধু তখনই instance চলে
- Idle capacity pay না
- 30-70% cost saving typically

**2. High Availability**
- Instance fail করলে auto-replace
- Traffic spike-এ auto-scale up
- কমলে auto-scale down

**3. Better User Experience**
- Response time consistent
- No overload slowness
- No capacity crashes

---

## Part 2: Auto Scaling-এর Components

Auto Scaling work করতে ৩টা জিনিস লাগে:

### 🧩 Component 1: Launch Template (বা Launch Configuration)

**"কেমন instance launch করবো"-র blueprint।**

### Launch Template (Recommended)

**Modern approach, flexible।**

**Contains:**
- AMI ID (কোন image)
- Instance Type (t3.micro, m5.large)
- Key Pair
- Security Group
- User Data script
- IAM Instance Profile
- Block Device Mapping (EBS config)
- Network interface settings
- Tags
- Monitoring settings
- **Versioning** supported

**Versioning Example:**
```
Version 1: AMI v1, t3.small
Version 2: AMI v1, t3.medium (scaled up)
Version 3: AMI v2 (new image), t3.medium
```

ASG-তে "latest version" বা specific version choose করা যায়।

### Launch Configuration (Legacy)

**পুরানো system, AWS discourage করে এখন।**

- Immutable (change করা যায় না, নতুন বানাতে হয়)
- কোনো versioning নেই
- কম features
- **নতুন project-এ use করবেন না**

**AWS-এর suggestion:** Always use Launch Templates।

---

### 🧩 Component 2: Auto Scaling Group (ASG)

**সবচেয়ে গুরুত্বপূর্ণ component — logical group of instances।**

**ASG defines:**
- **Minimum capacity** — কমপক্ষে কয়টা instance
- **Maximum capacity** — সর্বোচ্চ কয়টা
- **Desired capacity** — বর্তমানে কয়টা দরকার
- **VPC & Subnets** — কোথায় launch হবে
- **Load Balancer** — কোনটার সাথে attach
- **Health Check type** — কীভাবে check
- **Cooldown period**
- **Termination policy**

**Example ASG:**
```
Name: web-server-asg
Min: 2
Desired: 4
Max: 10
Subnets: subnet-az-a, subnet-az-b, subnet-az-c (multi-AZ)
```

এই setup-এ:
- কখনো ২ এর কম instance থাকবে না
- কখনো ১০ এর বেশি না
- বর্তমানে ৪টা চলছে
- Demand অনুযায়ী 2-10 এর মধ্যে বাড়া-কমা হবে

### Multi-AZ Deployment

**ASG automatically multi-AZ balance করে।**

**Example:** Desired 6 instances, 3 subnets (3 AZ)
- AWS evenly distribute: 2 in AZ-a, 2 in AZ-b, 2 in AZ-c

**AZ fail করলে:**
- AWS detect করে
- Other AZs-এ extra instance launch করে
- High availability maintain

---

### 🧩 Component 3: Scaling Policy

**"কখন বাড়াবো-কমাবো" এর rules।**

পরবর্তী part-এ বিস্তারিত।

---

## Part 3: Scaling Policies — ৫ ধরনের

### 📊 Type 1: Target Tracking Scaling (Most Popular)

**"এই metric-এ এই value maintain করো" — AWS automatic।**

**Example:** "Average CPU 50%-এ রাখো।"

AWS automatically calculate করবে:
- CPU 70% → scale up (more instance)
- CPU 30% → scale down
- CPU 50% → stable

**Common metrics:**
- `CPUUtilization` (default)
- `ALBRequestCountPerTarget` (load balancer request/instance)
- `NetworkIn`/`NetworkOut`
- Custom CloudWatch metrics

**Advantages:**
- Simple
- Self-adjusting
- AWS calculation automatic

**When:** Most use cases — default choice এটা।

---

### 📊 Type 2: Step Scaling

**Threshold-based granular control।**

**Example:**
```
If CPU > 60% → Add 1 instance
If CPU > 75% → Add 2 instances
If CPU > 90% → Add 4 instances
If CPU < 40% → Remove 1 instance
```

**Granularity control যা Target Tracking-এ নেই।**

**Use case:**
- Custom scaling behavior দরকার
- Response গ্রান্যুলার করতে চান
- Traffic pattern অনেক variable

---

### 📊 Type 3: Simple Scaling

**Legacy, simplest version।**

**Example:** "CPU > 70% → Add 1 instance"

**সমস্যা:**
- Cooldown period শেষ না হওয়া পর্যন্ত next scaling হবে না
- Step Scaling-এর চেয়ে কম flexible
- AWS discourage করছে

**Use:** Step Scaling preferred।

---

### 📊 Type 4: Scheduled Scaling

**Time-based automatic scaling।**

**Use case:** Traffic pattern predictable।

**Examples:**

```
Monday-Friday 9 AM: Scale up to 10 instances (office hours)
Monday-Friday 6 PM: Scale down to 2 instances (after office)
Weekend: Keep at 2 instances
Black Friday at midnight: Scale to 50 instances
```

**Perfect for:**
- Business hour apps
- Known peak times
- Scheduled events
- Daily/weekly patterns

---

### 📊 Type 5: Predictive Scaling (AI-based)

**Machine Learning দিয়ে forecast।**

**কীভাবে কাজ করে:**
- AWS আপনার past 14 days-এর traffic pattern analyze করে
- Future traffic predict করে
- **Demand আসার আগেই** scale up

**Advantages:**
- Proactive (reactive না)
- Spike-এর কারণে initial slowness avoid
- Target Tracking-এর সাথে combine করা যায়

**Use:** Traffic-এ regular pattern আছে এমন apps।

---

### 🎨 Scaling Policy Decision Matrix

| Scenario | Best Policy |
|---|---|
| Simple CPU management | Target Tracking |
| Granular custom thresholds | Step Scaling |
| Predictable business hours | Scheduled |
| Regular daily/weekly pattern | Predictive + Target Tracking |
| Unknown/unpredictable | Target Tracking |
| Event-based spikes | Scheduled + Target Tracking |

**Pro tip:** Target Tracking + Scheduled + Predictive — একসাথে ব্যবহার করা যায়।

---

## Part 4: Cooldown Period

### 🕐 Cooldown কী?

**Scaling action-এর পরে একটা "waiting period" — পরবর্তী action নেওয়ার আগে।**

**কেন দরকার?**

### Scenario (Without Cooldown):

- CPU spike 80% → ASG adds 1 instance
- New instance boot হচ্ছে (2 মিনিট)
- এই ২ মিনিটে বাকি instances-এ CPU এখনও high
- ASG thinks: "Still high, add another!"
- 1 minute later: "Still high, add another!"
- ৫ মিনিটে 10 extra instances (actually only 1 needed)
- **Thrashing problem**

### Cooldown-এর Solution:

- Scaling action-এর পর 300 seconds (5 min default) wait
- Wait period-এ নতুন scaling action block
- New instance-এর impact settle হওয়ার সময় দেয়
- তারপর আবার evaluate

**Default: 300 seconds (5 minutes)**

**Customizable:**
- Application fast boot করলে কম cooldown
- Slow boot-এ বেশি cooldown

**Warmup period:**
- Launch-এর পর instance "warm-up" সময়
- এই সময়ে traffic forward হবে না
- Application ready হওয়ার সময়

---

## Part 5: Health Checks

### 🏥 Health Check কী?

**ASG regular check করে instance healthy আছে কি না।**

Unhealthy হলে:
- ASG টা terminate করে
- নতুন replacement instance launch করে

### ২ ধরনের Health Check

#### 1. EC2 Health Check (Default)

**কী check করে:**
- Instance running state-এ আছে?
- System status check pass?
- Instance status check pass?

**কী check করে না:**
- Application up আছে কি?
- Port 80 responding?
- Database connection?

**সমস্যা:** Instance চলছে কিন্তু application crash — EC2 check pass করবে, ASG health mark করবে, কিন্তু user-রা error পাবে।

#### 2. ELB (Load Balancer) Health Check

**কী check করে:**
- Application port responding? (80, 443)
- Custom health endpoint responding? (`/health`)
- HTTP status code 200 পাচ্ছে?

**Better choice production-এ।**

**Configuration:**
```
Health check path: /health
Healthy threshold: 2 consecutive success
Unhealthy threshold: 3 consecutive failure
Timeout: 5 seconds
Interval: 30 seconds
```

### Health Check Grace Period

**Launch-এর পর কত সময় health check delay করবেন।**

**কেন?** New instance boot হতে সময় লাগে। Application start হওয়ার আগে health check fail করবে, ASG terminate করবে → infinite loop।

**Default:** 300 seconds (5 minutes)

**App slow boot হলে:** 600 seconds বা বেশি।

---

## Part 6: Termination Policy

যখন scale down দরকার, ASG কোন instance terminate করবে?

### Default Termination Logic:

1. **AZ Balance** — most instance আছে এমন AZ থেকে
2. **Launch Configuration/Template** — oldest version
3. **Closest to billing hour** — billing waste কম
4. **Random**

### Custom Termination Policies:

**Options:**
- `OldestInstance` — সবচেয়ে পুরানো আগে
- `NewestInstance` — সবচেয়ে নতুন আগে
- `OldestLaunchConfiguration` — outdated config
- `ClosestToNextInstanceHour` — billing optimize
- `Default` — combined

**Custom use case:**
- Rolling update: oldest first
- Testing: newest first
- Cost: nearest billing hour

---

## Part 7: Auto Scaling + Load Balancer = Power Couple

### Architecture:

```
             Internet
                │
                ▼
         Load Balancer (ALB/NLB)
        /       |       \
       ▼        ▼        ▼
    EC2-1    EC2-2    EC2-3
   (AZ-a)   (AZ-b)   (AZ-c)
      │        │        │
      └────────┼────────┘
               │
         Auto Scaling Group
         (managing 3 instances)
```

**কীভাবে কাজ করে:**

**1. User request আসে Load Balancer-এ**

**2. Load Balancer distribute করে instance-দের মধ্যে**
- Round-robin
- Least connections
- বা custom algorithm

**3. ASG monitor করছে load**
- CPU, request count
- Threshold cross হলে scale

**4. Scale up হলে:**
- ASG নতুন instance launch
- LB automatic detect করে
- Traffic forward শুরু

**5. Scale down হলে:**
- LB draining (existing connection finish)
- ASG terminate
- Graceful shutdown

### Key Integrations:

**Target Group:**
- LB-র target = ASG-র instances
- Health check LB level-এ

**Connection Draining:**
- Terminate-এর আগে existing request complete হতে দেয়
- Default: 300 seconds
- User-দের কাছে graceful

---

## Part 8: Real-world Scenarios

### Scenario 1: E-commerce Website (Stable + Spike)

**Setup:**
- ASG: Min 3, Max 20, Desired auto
- Launch Template: m5.large, Amazon Linux, latest AMI
- Policy 1: Target Tracking — CPU 60%
- Policy 2: Scheduled — Black Friday 10 AM, Scale to 15
- Health Check: ELB, /health endpoint, 60 sec grace
- Cooldown: 180 seconds

**Result:**
- Normal: 3-5 instances
- Peak hours: 6-10
- Black Friday: 15-20
- Automatic, no manual intervention

---

### Scenario 2: Batch Processing (Scheduled)

**Setup:**
- ASG: Min 0, Max 10, Desired 0
- Launch Template: c5.xlarge, Spot
- Schedule:
  - 2 AM: Desired = 10 (start batch)
  - 6 AM: Desired = 0 (stop after done)
- No target tracking needed

**Result:**
- 4 hours-এ batch complete
- বাকি 20 hours 0 instance = কোনো cost না
- Spot pricing = 80% savings

---

### Scenario 3: B2B SaaS (Business Hours)

**Setup:**
- ASG: Min 2, Max 15
- Schedule:
  - Weekday 8 AM: Min=5, Desired=5
  - Weekday 8 PM: Min=2, Desired=2
  - Weekend: Min=2
- Policy: Target Tracking — ALB request count/instance

**Result:**
- Office hours: 5-10 instances
- After hours: 2
- 50% cost savings on compute

---

## Part 9: Auto Scaling Best Practices

### ✅ Do's

**1. Multi-AZ always**
- Minimum 2 AZ, preferably 3
- Single AZ = single point of failure

**2. Use Launch Templates (not Launch Configuration)**
- Versioning
- More features
- Future-proof

**3. ELB Health Checks production-এ**
- EC2 check inadequate
- Application-level check

**4. Appropriate grace period**
- Slow-boot app = longer grace
- Fast app = shorter

**5. Min capacity > 0 for critical apps**
- 0-এ গেলে cold start slow
- Minimum 1 always available

**6. Tag your instances**
- ASG name, environment, purpose
- Cost tracking

**7. Use Mixed Instance Types**
- Spot + On-Demand combination
- Cost + reliability balance

### ❌ Don'ts

**1. Instances-এ local data store না**
- Auto-terminate হলে data gone
- Stateless design

**2. Min == Max না**
- Auto scaling-এর মানে হারাল
- Fixed capacity হয়ে গেল

**3. Too aggressive scaling না**
- Thrashing
- Cost spike

**4. Health check ignore না**
- Application check essential

**5. One big instance না**
- বরং multiple small
- Better fault tolerance

---

## Part 10: Auto Scaling Limits

**Default limits (per region):**
- ASGs per region: 200 (request করে বাড়ানো)
- Instances per ASG: 1,000
- Launch Templates per region: 10,000
- Launch Template versions: 10,000 per template

**Scaling cooldown minimum:** 0 seconds
**Grace period maximum:** Unlimited

---

## 🎯 Module 1 Revision — পুরো সপ্তাহ একসাথে

### Day 1: Cloud Computing Foundations
- Cloud = internet দিয়ে IT resource ভাড়া
- Service Models: IaaS, PaaS, SaaS
- Region = ভৌগোলিক এলাকা
- AZ = region-এ আলাদা data center
- Edge Location = CDN caching
- AWS account setup + billing alert

### Day 2: EC2 & Instance Types
- EC2 = virtual server
- 5 families: General (t,m), Compute (c), Memory (r), Storage (i,d), GPU (p,g)
- Naming: `<family><gen><options>.<size>`
- AMI = instance blueprint
- Region-specific AMI

### Day 3: Key Pairs, Security Groups, IPs
- SSH encrypted login
- Key Pair: public (server), private (you)
- Security Group = stateful firewall, allow-only rules
- Private IP vs Public IP vs Elastic IP
- EIP static, unused-এ charge

### Day 4: EBS, Instance Store, EFS
- Block (EBS) vs File (EFS) vs Object (S3)
- EBS types: gp3 (default), io2 (high perf), st1/sc1 (HDD)
- Instance Store = ephemeral, fast, physical
- EFS = shared file system Linux
- Snapshot = incremental, S3-based

### Day 5: S3 & Glacier
- Object storage, 11 nines durability
- 8 storage classes (Standard, IA, Glacier, Deep Archive)
- Bucket global unique, region-specific
- Versioning, Lifecycle, Replication
- Encryption (SSE-S3 default)
- Security: Bucket Policy + IAM + Block Public Access

### Day 6: EC2 Pricing Models
- On-Demand: flexible, expensive
- RI: 1-3 yr commit, 40-72% off
- Savings Plans: flexible RI
- Spot: 90% off, interruptible
- Dedicated Host: compliance/licensing
- Mix strategy: Baseline → SP, Variable → OD, Interruptible → Spot

### Day 7: Auto Scaling
- Automatic instance management
- Launch Template + ASG + Scaling Policy
- Target Tracking (most common), Step, Scheduled, Predictive
- Cooldown prevents thrashing
- ELB Health Check + grace period

---

### 🔗 Interconnections (বড় চিত্র)

এই সব service একসাথে কীভাবে কাজ করে?

**Example: Production Web Application**

```
User Request
   │
   ▼
Route 53 (DNS) → Module 7
   │
   ▼
CloudFront (CDN, Edge) → Module 7
   │
   ▼
Application Load Balancer → Module 7
   │
   ▼
Auto Scaling Group (Day 7) ←── CloudWatch monitoring
   │                              (Module 8)
   ├── EC2-1 (Day 2, 3)
   ├── EC2-2 ──── Security Group (Day 3)
   └── EC2-3 ──── Launch Template (Day 7)
         │
         ├── Root Volume: EBS gp3 (Day 4)
         ├── User Images: EFS (Day 4) or S3 (Day 5)
         └── Cache: Instance Store (Day 4)
   │
   ▼
All running in VPC → Module 2 (কাল থেকে)
   │
   ▼
Multi-AZ deployment → Day 1 concept
   │
   ▼
Pricing: Mix of RI (baseline) + Spot (batch) → Day 6
```

এটাই AWS architecture — ইট-পাথর দিয়ে building বানানোর মতো, সব service একসাথে।

---

## 📝 Final Module 1 Self-check (১৫টা প্রশ্ন)

আজ নিজেকে test করুন:

১. Region, AZ, Edge Location — পার্থক্য কী?
২. t3.micro আর m5.large-এ কোনটা কাজে ব্যবহার?
৩. AMI region-specific কেন?
৪. SSH-এ private key কেন network-এ যায় না?
৫. Security Group-এ deny rule লেখা যায়?
৬. Elastic IP কখন paid?
৭. EBS snapshot কোথায় store হয়?
৮. Instance Store-এ data কখন হারায়?
৯. S3 bucket name globally unique কেন?
১০. Glacier Deep Archive-এর retrieval time?
১১. 3-year RI All Upfront কত % discount (typical)?
১২. Spot instance interruption-এ কত মিনিট warning?
১৩. Auto Scaling-এ Cooldown period কেন?
১৪. Launch Template vs Launch Configuration-এ key পার্থক্য?
১৫. একটা production web app multi-AZ-এ deploy করতে minimum কী কী লাগে?

---

## 🏆 Module 1 Completion Checklist

- [ ] AWS Free Tier account তৈরি করেছি
- [ ] MFA root account-এ enable করেছি
- [ ] Billing alert set করেছি ($5 threshold)
- [ ] Region/AZ concept পরিষ্কার
- [ ] EC2 instance types জানি (t, m, c, r families)
- [ ] AMI, Key Pair, Security Group — clear
- [ ] EBS volume types (gp3, io2, st1, sc1) জানি
- [ ] S3 storage classes ৮টা বুঝি
- [ ] 6টা pricing model বুঝি
- [ ] Auto Scaling concept clear

---

## 💡 Module 1 Pro Tips (সব একসাথে)

**Architecture:**
- Multi-AZ always production-এ
- Stateless application design
- Auto Scaling + Load Balancer = winning combo

**Security:**
- Least privilege principle
- MFA everywhere
- SSH restricted IP only
- Block Public Access S3-এ default

**Cost:**
- Tag everything
- Right-size instances (Compute Optimizer)
- Mix pricing models
- Lifecycle policy S3-এ
- Delete unused EBS volumes, snapshots, EIPs

**Monitoring:**
- CloudWatch metrics
- Billing dashboard weekly check
- Set anomaly alerts

**Automation:**
- Infrastructure as Code (Terraform/CloudFormation) — পরে শিখবেন
- Auto Scaling for dynamic capacity
- Scheduled actions for predictable patterns

---

## 🎉 Congratulations!

**Module 1 complete! ৭ দিনে আপনি শিখেছেন:**
- AWS-এর foundational compute service
- Storage-এর সব option
- Security-এর ভিত্তি
- Pricing optimization
- Auto scaling for reliability

এইটুকু জানলেই আপনি একটা simple production application AWS-এ deploy করতে পারবেন।

---

## 🚀 সামনে কী?

**Module 2: VPC Design & Network Architecture** (Day 8-14)

- VPC, Subnets, CIDR
- Internet Gateway, Route Tables
- NAT Gateway, Bastion Host
- Network ACL vs Security Group (deeper)
- VPC Endpoints, PrivateLink
- 3-tier architecture design

VPC হলো সব কিছু কোথায় চলে — AWS-এ কাজ করতে VPC without ১ ইঞ্চিও এগুতে পারবেন না।

---

## 💪 একটা Suggestion

আজ রাতে একটা **mini project** try করতে পারেন (optional):
- একটা t3.micro launch করুন
- SSH দিয়ে connect
- Nginx install
- Security Group-এ port 80 open
- Browser-এ public IP visit → "Welcome to Nginx!" দেখা যায়

এতে Day 1-7 এর সব concept একসাথে experience হবে।

**⚠️ Remember:** কাজ শেষে instance terminate করুন, EBS volume delete করুন। Free tier-এ থাকলে charge হবে না, কিন্তু অভ্যাস রাখুন।

---
