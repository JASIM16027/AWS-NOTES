
# 📚 Day 6 — EC2 Pricing Models

**সময়:** ১.৫ ঘণ্টা | **Module:** ১ (EC2 & Storage Fundamentals)

## 🎯 আজকের লক্ষ্য
- AWS-এর ৬টা pricing model গভীরে বুঝবেন
- On-Demand vs Reserved vs Spot — পার্থক্য ও trade-off
- Savings Plans কেন এসেছে, কীভাবে কাজ করে
- Spot Instance-এর advanced concept ও best practices
- Dedicated Host vs Dedicated Instance
- Real-world mix করে কীভাবে ৮০% পর্যন্ত save করা যায়

---

## Part 1: কেন এত Pricing Model?

### 🤔 AWS-এর Business Problem

AWS-এর কাছে বিশাল capacity আছে — millions of server। কিন্তু সব সময় সব server ব্যবহার হয় না।

**Reality:**
- Peak hours: 80% server used
- Off-peak: 40% server used
- বাকি 40-60% server idle → AWS-এর loss

**AWS-এর Solution:**
- যারা commit করবে long-term → discount দাও (Reserved)
- যারা spare capacity ব্যবহার করবে → extra discount (Spot)
- যারা flexible না → full price (On-Demand)

এই mechanism দিয়ে AWS নিজেদের utilization maximize করে, আপনিও সস্তায় পান। Win-win।

### 🎨 ৬টা Pricing Models

1. **On-Demand** — পুরো দাম, কোনো commitment নেই
2. **Reserved Instances (RI)** — ১-৩ বছর commit, ৭২% পর্যন্ত ছাড়
3. **Savings Plans** — Flexible commitment, ৭২% পর্যন্ত ছাড়
4. **Spot Instances** — Spare capacity, ৯০% পর্যন্ত ছাড়
5. **Dedicated Hosts** — পুরো physical server ভাড়া
6. **Dedicated Instances** — Dedicated hardware, কম control

---

## Part 2: On-Demand Instances

### 💵 On-Demand কী?

**"Pay-as-you-go" — যতটুকু ব্যবহার, ততটুকু bill।**

Default pricing, AWS console-এ কিছু না select করলে এটাই পাবেন।

### ⚙️ কীভাবে কাজ করে:

- Per-second billing (minimum 60 seconds)
- কিছু OS-এ per-hour (Windows SQL Server)
- Instance launch করলে billing start, stop করলে billing stop
- কোনো upfront payment নেই
- কোনো commitment নেই

### 📊 Pricing Example:

**Mumbai region (ap-south-1), Linux:**

| Instance | On-Demand $/hr | $/month (24x7) |
|---|---|---|
| t3.micro | $0.0112 | ~$8 |
| t3.small | $0.0224 | ~$16 |
| t3.medium | $0.0448 | ~$32 |
| m5.large | $0.1050 | ~$76 |
| m5.xlarge | $0.2100 | ~$152 |
| c5.xlarge | $0.1870 | ~$135 |
| r5.large | $0.1380 | ~$100 |

**হিসাব:** $0.105/hr × 24 hr × 30 days = $75.6/month

### ✅ On-Demand Advantages:

**১. Zero Commitment**
- কেনো long-term contract নেই
- যেকোনো সময় stop/start

**২. Perfect for Unpredictable Workload**
- আপনার app কেমন চলবে জানেন না? On-Demand ideal
- Traffic spike হলে scale up, কমলে scale down

**৩. Short-term Use Cases**
- Development & testing
- Proof of concept
- Short duration project (< 1 year)

**৪. New Applications**
- Usage pattern জানা নেই? On-Demand দিয়ে শুরু করুন

### ❌ On-Demand Disadvantages:

**সবচেয়ে দামি pricing model।** আপনি যদি ১ বছর বা তার বেশি একই workload চালান, On-Demand-এ ৭২% পর্যন্ত বেশি pay করছেন।

### 🎯 কখন ব্যবহার:

- Short-term workloads (< 1 year)
- Unpredictable traffic
- Development, testing
- First time AWS user, workload analyze করছেন
- Stateful apps যা interrupt করা যায় না এবং long-term commit করতে চান না

---

## Part 3: Reserved Instances (RI)

### 🔒 Reserved Instance কী?

**১ বা ৩ বছরের জন্য একটা specific instance type কিনে রাখা, discount-এ।**

Analogy: ফ্লাট ভাড়া দেওয়ার সময় advance মাস-মাস payment-এর বদলে পুরো বছর এককালীন দিলে landlord discount দেয়। RI-তে AWS-ও একই কাজ করে।

### ⚙️ কীভাবে কাজ করে:

- আপনি নির্দিষ্ট instance type, region, tenancy, OS কিনুন
- ১ বা ৩ বছরের জন্য
- যে instance আপনি launch করেন সেটা RI criteria match করলে automatic discount
- Match না করলে full On-Demand price

### 💰 Discount Structure:

**Commitment Length:**
- **1-year:** ~40% discount
- **3-year:** ~60-72% discount

**Payment Option:**
- **All Upfront:** সর্বোচ্চ discount (পুরো টাকা আগে)
- **Partial Upfront:** মাঝারি discount (কিছু আগে, বাকি মাসে)
- **No Upfront:** সর্বনিম্ন discount (মাসে মাসে, কিন্তু RI-এর চেয়ে সস্তা)

**Example — m5.large Mumbai Linux:**

| Option | Effective $/hr | Savings vs On-Demand |
|---|---|---|
| On-Demand | $0.105 | — |
| 1yr No Upfront | $0.068 | 35% |
| 1yr Partial Upfront | $0.065 | 38% |
| 1yr All Upfront | $0.063 | 40% |
| 3yr No Upfront | $0.047 | 55% |
| 3yr Partial Upfront | $0.042 | 60% |
| 3yr All Upfront | $0.038 | 64% |

### 🎭 RI Types — ২ ধরনের

#### Standard RI

**Characteristics:**
- সর্বোচ্চ discount (up to 72%)
- Instance type change করা **যায় না**
- Region change **যায় না**
- AZ change যায় (if regional scope)
- OS change **যায় না**
- Sell করা যায় RI Marketplace-এ

**কখন:** নিশ্চিত stable workload, এক instance type সবসময় দরকার।

#### Convertible RI

**Characteristics:**
- কম discount (up to 54%)
- **Instance family change করা যায়** (m5 → c5 → r5)
- **Region change করা যায় না** (but 3-year-এর মধ্যে exchange possible)
- OS/tenancy change যায়
- Sell করা **যায় না**

**কখন:** Future requirement অনিশ্চিত, flexibility দরকার।

### 🌐 RI Scope — Regional vs Zonal

#### Regional RI
- কোনো specific AZ নেই
- Discount apply হয় region-এর যেকোনো AZ-এ
- **AZ flexibility**, **size flexibility**
- Most common choice

#### Zonal RI
- Specific AZ-এ reserved
- **Capacity reservation guaranteed**
- Disaster recovery critical apps-এর জন্য

### 🔄 Instance Size Flexibility

Regional RI-তে একটা cool feature আছে — **size flexibility**।

**Example:** আপনি `m5.large` RI কিনলেন, কিন্তু চালাচ্ছেন ২টা `m5.medium`।

AWS "normalization factor" use করে:
- `m5.medium` = 2 units
- `m5.large` = 4 units
- `m5.xlarge` = 8 units
- `m5.2xlarge` = 16 units

১টা `m5.large` RI = ২টা `m5.medium` discount।

**Conditions:**
- Same family (m5 ↔ m5, না m5 ↔ c5)
- Same OS
- Same tenancy
- Linux only (Windows-এ কাজ করে না)

### 🛒 RI Marketplace

আর দরকার নেই এমন RI sell করা যায় (Standard RI only):
- Remaining tenure কাউকে sell
- কেউ সস্তায় কিনতে পারে
- Non-US account-দের কিছু restriction আছে

### 🎯 কখন Reserved Instance:

**✅ ব্যবহার করুন:**
- Known baseline capacity
- Database server (24x7 চলবেই)
- Production web server
- Monitoring tools
- Core infrastructure

**❌ ব্যবহার করবেন না:**
- Unpredictable workload
- Short-term project
- Development/testing (off-hours বন্ধ)
- Frequently changing requirement

### ⚠️ Common Mistake:

**১ বছর আগেই RI কিনে ফেলা।** ৩-৬ মাস usage pattern analyze করে তবেই RI কিনুন।

---

## Part 4: Savings Plans

### 💡 Savings Plans কী?

**Reserved Instance-এর newer, more flexible version।**

২০১৯-এ introduce। "$X/hour কমপক্ষে ১ বা ৩ বছর ব্যবহার করব" — এই commitment-এ discount।

### 🆚 RI vs Savings Plans

**RI-এর সমস্যা:**
- Specific instance type-এ lock
- Future-এ technology change-এ stuck

**Savings Plans-এর solution:**
- শুধু $ amount commit
- Instance family, size, region change করেও discount continue

### 📦 ৩ ধরনের Savings Plans

#### 1. Compute Savings Plans (সবচেয়ে Flexible)

**কী cover করে:**
- EC2 (সব instance family, region)
- Fargate
- Lambda

**Flexibility:**
- Instance family change OK (m5 → c6 → r6)
- Region change OK
- OS/tenancy change OK
- Service change (EC2 → Fargate) OK

**Discount:** Up to 66%

**Use case:** Maximum flexibility দরকার।

#### 2. EC2 Instance Savings Plans (সর্বোচ্চ Discount)

**কী cover করে:**
- Specific instance family in specific region (যেমন `m5` in `ap-south-1`)

**Flexibility:**
- Same family-এর মধ্যে size change (m5.large → m5.xlarge)
- OS change OK
- Region change **না**

**Discount:** Up to 72% (Reserved Instance-এর সমান)

**Use case:** Specific family in specific region stable.

#### 3. SageMaker Savings Plans

**কী cover করে:** Amazon SageMaker usage (ML)।

**Discount:** Up to 64%।

### 💵 Savings Plans কীভাবে কাজ করে

**Example:** আপনি commit করলেন "$১/hour Compute Savings Plan for 1 year"।

**Monthly calculation:**
- $1/hr × 24 hr × 30 days = $720/month
- আপনার actual EC2 bill হয়তো $1000/month
- $720 Savings Plan rate-এ (discounted)
- বাকি $280 On-Demand rate-এ

**Important:** Commit-এর থেকে কম use করলেও $720 pay করতে হবে। তাই carefully commit।

### 🧮 Savings Plans Payment Options:

Same as RI:
- All Upfront (সর্বোচ্চ discount)
- Partial Upfront
- No Upfront

### 🎯 কখন কোনটা:

| Need | Best Choice |
|---|---|
| Maximum flexibility | Compute Savings Plan |
| Maximum discount, stable infra | EC2 Instance Savings Plan |
| Specific legacy needs, resale option | Reserved Instance (Standard) |
| Flexibility + some discount | Reserved Instance (Convertible) |

### 📊 Decision Matrix:

```
Known exact instance for 3+ years → Standard RI
Known instance family, region for 1+ year → EC2 Instance Savings Plan
Flexible compute needs for 1+ year → Compute Savings Plan
Less than 1 year commitment → On-Demand
Fault-tolerant, can be interrupted → Spot
```

---

## Part 5: Spot Instances

### 🔥 Spot Instance কী?

**AWS-এর spare capacity, up to 90% discount।**

যখন AWS-এর data center-এ idle server আছে, সেগুলো cheap-এ offer করে। কিন্তু AWS দরকার হলে ২ মিনিট notice-এ আপনার instance terminate করবে।

### ⚡ কীভাবে কাজ করে:

1. আপনি Spot Request submit করেন
2. AWS Spot pool থেকে capacity allocate করে
3. Instance launch হয়
4. যতক্ষণ চলে, ততক্ষণ Spot price pay
5. AWS-এর যখন capacity দরকার → ২ minute warning → instance terminate

### 💰 Pricing:

Spot price dynamically change হয় supply-demand-এর উপরে:
- Low demand: 90% discount
- High demand: 50-70% discount
- Average: 70-80% discount from On-Demand

**Example:** `m5.large` On-Demand $0.105/hr → Spot typically $0.02-0.04/hr।

### 🚨 Interruption — এটাই Spot-এর main risk

AWS যখন আপনার instance terminate করবে, ২ মিনিট আগে warning পাবেন:

**Interruption Notice:**
- CloudWatch Event
- Instance metadata query: `http://169.254.169.254/latest/meta-data/spot/termination-time`

**২ মিনিটে কী করতে হবে:**
- Current work save
- Connection close
- State checkpoint
- Graceful shutdown

### 🎭 Spot Strategies

#### Strategy 1: Stateless & Fault-Tolerant

**Use case:** Web server behind load balancer
- ১০টা instance চলছে
- AWS ২টা terminate করল
- Load balancer automatically 8 চালিয়ে নেবে
- Auto Scaling নতুন Spot instance add করবে

#### Strategy 2: Checkpoint-based Processing

**Use case:** Long-running batch job
- প্রতি ৫ মিনিটে progress save
- Interruption হলে পরের instance সেখান থেকে continue

#### Strategy 3: Mixed Instance Types

**Use case:** Spot Fleet
- "আমার 100 vCPU দরকার, এই 5টা instance type-এর যেকোনো একটা দাও"
- AWS সস্তায় allocate করে
- এক type-এ interruption হলে অন্যটায় move

### 📋 Spot Request Types

#### 1. One-time Request
- Request submit করলেন
- Instance launch হলো
- Interrupt হলে আর নেই

#### 2. Persistent Request
- Interrupt হলে auto-replace
- নতুন Spot instance launch হয়
- যতক্ষণ request active

#### 3. Spot Fleet / EC2 Fleet
- Multiple instance type একসাথে request
- Diversification strategy
- Capacity guarantee বেশি

### 🛡️ Spot Instance Best Practices

**১. Use for Stateless Workloads**
- Batch processing
- CI/CD builds
- Data analysis
- Image/video processing
- ML training (with checkpointing)
- Big data jobs (Spark, Hadoop)

**২. Never Use For:**
- Database (primary)
- Long-running stateful apps
- User-facing critical services (unless behind LB)
- Apps that can't handle interruption

**৩. Use Spot Diversification:**
- Multiple instance types
- Multiple AZs
- Spot Fleet allocation strategy

**৪. Checkpoint Everything:**
- Every task-এর state save
- Retry logic
- Idempotent operations

**৫. Mix with On-Demand:**
- Baseline capacity: On-Demand
- Burst capacity: Spot
- Best of both

### 🎯 Spot Instance Real-world Use Cases

**CI/CD Pipeline:**
- Jenkins build agents
- Build fail হলে auto-retry
- 80% cost savings vs On-Demand

**ML Training:**
- Hours-long training job
- Checkpoint every epoch
- Interrupt হলে resume from checkpoint
- 90% savings for model training

**Big Data Analytics:**
- Spark clusters on Spot
- Task-level retry built into Spark
- Huge cost savings on nightly ETL

**Scientific Computing:**
- Genomic analysis
- Financial simulations
- Research workloads

### ⚠️ Spot Limits:

- Default Spot limit per region (request করে বাড়ানো)
- Some instance types-এ Spot availability কম
- Peak time-এ less availability

---

## Part 6: Dedicated Hosts & Dedicated Instances

### 🏢 Why Dedicated?

Normal EC2-তে **shared hardware** — অন্য customer-ও same physical server-এ আছে (isolated তবে)।

কিছু কিছু use case-এ এটা allow না:
- Compliance requirement (HIPAA, financial)
- License requirement (Oracle, Microsoft server license)
- Audit requirement

### 💼 Dedicated Host

**কী:** পুরো physical server আপনার — কেউ share করছে না।

**Features:**
- Host level visibility (socket, core count দেখা যায়)
- **Bring Your Own License (BYOL)** — already bought license use
- Host affinity — instance same host-এ restart
- Consistent hardware

**Pricing:**
- Per-host per-hour
- দামি
- 1-year বা 3-year commitment options-এ discount

**Use Case:**
- Oracle Database (license per-core based)
- Microsoft SQL Server BYOL
- Regulatory compliance
- Software licensing audit

### 🏠 Dedicated Instance

**কী:** Instance dedicated hardware-এ চলে (কেউ share করে না), কিন্তু আপনার host-level visibility নেই।

**Dedicated Host vs Dedicated Instance:**

| Feature | Dedicated Host | Dedicated Instance |
|---|---|---|
| Hardware visibility | হ্যাঁ (socket, core) | না |
| BYOL | হ্যাঁ | সীমিত |
| Affinity control | হ্যাঁ | না |
| Billing | Per host | Per instance |
| Price | বেশি | মাঝারি |
| Use case | Compliance, licensing | Simple isolation |

**বেশির ভাগ use case-এ normal shared instance যথেষ্ট। Dedicated-এর দরকার পড়ে শুধু specific compliance বা licensing-এ।**

---

## Part 7: Capacity Reservations

**এটা pricing model না, কিন্তু related।**

### 🎫 Capacity Reservation কী?

**Specific AZ-এ specific instance type guarantee।**

RI-এর billing discount ছাড়া শুধু "capacity lock"।

**Use case:**
- Disaster recovery: standby capacity ready চাই
- Event (sale, launch): guaranteed capacity
- Compliance: specific AZ-এ থাকতে হবে

**Pricing:** Full On-Demand rate, কিন্তু capacity guaranteed।

**Combined with Savings Plan:** Capacity Reservation + Savings Plan/RI — discount + capacity guarantee।

---

## Part 8: Putting It All Together — Cost Strategy

### 🎯 Real-world Example: E-commerce Platform

**Infrastructure:**
- 10 web servers (24x7)
- 3 database servers (24x7)
- 5 background workers (batch jobs)
- Daily analytics (nightly, 4 hours)
- Development environment (business hours only)
- Sale events (temporary scale 3x)

**Optimal Pricing Mix:**

| Component | Pricing Model | Reason |
|---|---|---|
| 8 web servers | 3-year EC2 Savings Plan | Stable baseline, max discount |
| 2 web servers | On-Demand | Burst buffer |
| 3 database | 3-year Standard RI | 24x7, stable, long-term |
| 3 background workers | 1-year Compute Savings Plan | Stable but future may change |
| 2 background workers | Spot | Fault-tolerant |
| Analytics (nightly) | Spot | Batch, interruptible |
| Dev environment | On-Demand + scheduled stop | Turn off nights/weekends |
| Sale event scale | Spot Fleet | Short-term, can retry |

**Savings Calculation:**

Without optimization (all On-Demand): ~$10,000/month

With optimized mix:
- Savings Plan (8 web): 72% savings on $2,400 = $1,728 saved
- RI (3 DB): 60% savings on $1,500 = $900 saved
- Spot (workers + analytics): 85% savings on $1,200 = $1,020 saved
- Dev stop (16 hrs down): ~67% savings = $400 saved

**Total savings:** ~$4,000/month = **40% reduction**

Bill: $6,000/month instead of $10,000/month। বছরে $48,000 save।

---

### 🏆 Cost Optimization Playbook

**Step 1: Analyze Usage (3-6 months)**
- CloudWatch metrics
- Cost Explorer
- Right-sizing recommendations
- AWS Compute Optimizer

**Step 2: Identify Baseline**
- কত capacity সবসময় দরকার?
- কত peak-এ লাগে?
- কোনগুলো interruption tolerate করতে পারে?

**Step 3: Apply Mixed Strategy**
- **Baseline (80%):** Savings Plans / RI
- **Variable (15%):** On-Demand
- **Fault-tolerant (5%):** Spot

**Step 4: Monitor & Adjust**
- Monthly cost review
- Utilization review
- Convertible RI exchange if needed

**Step 5: Tag Everything**
- Cost allocation tags
- Department, project, environment
- Know where money goes

---

## Part 9: Cost Calculation Examples

### Example 1: Small Startup

**Monthly usage:** 2 t3.medium running 24x7

**On-Demand:** 2 × $0.0448 × 24 × 30 = $64.5

**1-year EC2 Instance Savings Plan (No Upfront):**
- ~40% discount
- $38.7/month
- **Savings: $25.8/month = $309/year**

### Example 2: Batch Processing

**Workload:** Nightly processing, 8 hours, m5.xlarge × 10

**On-Demand:** 10 × $0.210 × 8 × 30 = $504/month

**Spot:** 10 × $0.04 × 8 × 30 = $96/month

**Savings: $408/month (81%)**

### Example 3: Enterprise Database

**Workload:** r5.4xlarge, 24x7, 3 years

**On-Demand:** $1.10 × 24 × 365 × 3 = $28,908

**3-year Standard RI All Upfront:** ~$11,000 total

**Savings: $17,908 over 3 years (62%)**

---

## 🎯 আজকের মূল Takeaways

1. **৬টা pricing model** — কোনটাই একা best না, mix করাই key
2. **On-Demand** = flexible, expensive, testing-এর জন্য
3. **Reserved Instance** = 1-3 yr commit, up to 72% off
4. **Savings Plans** = RI-এর flexible version, similar discount
5. **Spot** = 90% off, কিন্তু interruption risk
6. **Dedicated Host** = compliance/licensing need
7. **Baseline → Savings Plans, Variable → On-Demand, Interruptible → Spot**
8. **Analyze before commit** — 3-6 months usage দেখুন
9. **Tag everything** cost tracking-এর জন্য
10. **Monthly review** করুন বিল

---

## 📝 Self-check Questions

১. On-Demand instance-এ billing কীভাবে হয় (per-hour না per-second)?
২. 1-year vs 3-year RI — কোনটায় বেশি discount?
৩. Standard RI-এ instance type change করা যায়?
৪. Convertible RI-এর main advantage কী?
৫. Compute Savings Plan আর EC2 Instance Savings Plan-এর পার্থক্য?
৬. Spot instance-এ interruption-এর কত সময় notice পান?
৭. একটা production MySQL database-এর জন্য কোন pricing?
৮. Jenkins build agent-এর জন্য কোন pricing?
৯. Oracle Database license-এর জন্য কী লাগে?
১০. Regional RI-এ size flexibility কীভাবে কাজ করে?
১১. Spot Fleet মানে কী?
১২. Capacity Reservation আর RI-এর পার্থক্য?
১৩. যদি workload-এর future uncertain থাকে, Standard না Convertible RI?
১৪. Dev environment-এর জন্য cost optimization strategy কী?
১৫. একটা 24x7 web server-এর জন্য optimal mix কী?

---

## 💡 Pro Tips

- **নতুন AWS user হলে ৩ মাস On-Demand-এ থাকুন** — usage analyze করে তারপর commit।
- **3-year RI শুধু core, stable infrastructure-এ** — risky business model-এ না।
- **Dev environment-এ On-Demand + auto-stop script** — nights/weekends বন্ধ = 70% save।
- **Spot-এ stateless worker only** — retry logic থাকতে হবে।
- **Convertible RI ideal compromise** — future flexibility + discount।
- **AWS Cost Explorer daily check** — surprise avoid।
- **Compute Optimizer enable করুন** — right-sizing recommendation free।

---

## 🚨 Cost Horror Stories

**Story 1:** একটা company সব production-এ On-Demand — বছরে $500,000 extra pay। ৩ বছরে $1.5M loss।

**Story 2:** Developer Spot-এ production database চালাল — AWS terminate, 4 hour downtime, customer churn।

**Story 3:** Team ৩-বছরের All Upfront RI কিনল, ৬ মাসে architecture change হলো, $200K stuck।

**Story 4:** Forgot to stop dev instance weekend — $3,000 extra bill এক মাসে।

**Moral:** Pricing model choose করা strategic decision, monthly review লাগবে।

---

## 💰 Cost Management Tools

**Free tools (AWS provided):**
- **Cost Explorer** — trend analysis
- **Budgets** — alert set করুন
- **Cost Anomaly Detection** — unusual spike
- **Compute Optimizer** — right-sizing suggestion
- **Trusted Advisor** — cost optimization checks
- **Savings Plans Recommendations**
- **Reserved Instance Recommendations**

**Best practice:**
- Monthly budget set করুন
- Alert 50%, 80%, 100%-এ
- Tag enforcement policy
- Weekly cost review meeting

---
