# 🎓 AWS Solutions Architect – Associate (SAA-C03): Exam Overview ও Strategy

> ⚠️ Exam-এর version, দাম ও নিয়ম সময়ের সাথে বদলায়। Exam book করার আগে AWS-এর অফিসিয়াল **Exam Guide** একবার মিলিয়ে নিন।
> এই folder-এর সব প্রশ্ন **নিজে লেখা practice প্রশ্ন**। আসল exam-এর প্রশ্ন নয়, তবে একই ধরন ও একই topic-এর।

---

## 📋 Exam এক নজরে

| বিষয় | তথ্য |
|---|---|
| Code | **SAA-C03** |
| প্রশ্ন সংখ্যা | **65টা** (৫০টা score হয় + ১৫টা unscored, কোনটা unscored তা বোঝা যায় না) |
| সময় | **130 মিনিট** (প্রতি প্রশ্নে ~২ মিনিট) |
| Passing score | **720 / 1000** (scaled score) |
| প্রশ্নের ধরন | **Multiple choice** (৪টা option থেকে ১টা) এবং **Multiple response** (৫+ option থেকে ২–৩টা) |
| Negative marking | **নেই** → কোনো প্রশ্ন খালি রাখবেন না |
| দাম | ~150 USD |
| মেয়াদ | ৩ বছর |

---

## 🧩 ৪টা Domain (কোন ধরনের প্রশ্ন কত %)

| Domain | Weight | কী ধরনের প্রশ্ন আসে | Practice file |
|---|---|---|---|
| **1. Design Secure Architectures** | **30%** | IAM, SCP, KMS, S3 security, SG/NACL, WAF, Shield, Secrets Manager, Cognito, encryption | [03-Domain-1-Secure-Architectures.md](./03-Domain-1-Secure-Architectures.md) |
| **2. Design Resilient Architectures** | **26%** | Multi-AZ, Auto Scaling, ELB, SQS decoupling, DR strategy, Route 53 failover, backup | [04-Domain-2-Resilient-Architectures.md](./04-Domain-2-Resilient-Architectures.md) |
| **3. Design High-Performing Architectures** | **24%** | সঠিক storage/DB/compute বাছাই, caching, CloudFront, Global Accelerator, EBS type, Kinesis | [05-Domain-3-High-Performing-Architectures.md](./05-Domain-3-High-Performing-Architectures.md) |
| **4. Design Cost-Optimized Architectures** | **20%** | Pricing model, S3 class/lifecycle, Spot, Savings Plan, NAT cost, data transfer, right-sizing | [06-Domain-4-Cost-Optimized-Architectures.md](./06-Domain-4-Cost-Optimized-Architectures.md) |

---

## 🧠 প্রশ্নের ধরন (Question Types)

### ১. Scenario-based single answer (সবচেয়ে বেশি)
একটা company-র অবস্থা বর্ণনা থাকে, তারপর জিজ্ঞেস করে "**Which solution meets these requirements?**"।

### ২. Multiple response
"**Select TWO**" বা "**Select THREE**" লেখা থাকে। সবগুলো ঠিক না হলে নম্বর পাবেন না, আংশিক নম্বর নেই।

### ৩. Qualifier-ভিত্তিক প্রশ্ন (সবচেয়ে গুরুত্বপূর্ণ!)
প্রায়ই একাধিক option **কাজ করবে**, কিন্তু প্রশ্নের **qualifier word** ঠিক করে দেয় কোনটা **সবচেয়ে ভালো**:

| প্রশ্নে এই কথা থাকলে | যে ধরনের উত্তর খুঁজবেন |
|---|---|
| **MOST cost-effective / LEAST expensive** | সবচেয়ে সস্তা যেটা requirement পূরণ করে: Spot, S3 IA/Glacier, Savings Plan, serverless, Gateway endpoint |
| **LEAST operational overhead / minimal management** | **Managed/serverless** service: Lambda, Fargate, DynamoDB, Aurora Serverless, RDS (EC2-তে নিজে DB না) |
| **MOST secure** | Private connectivity (VPC endpoint), encryption with KMS CMK, least privilege, IAM role |
| **Highly available / fault tolerant** | **Multi-AZ**, Auto Scaling across AZs, ELB |
| **Lowest latency / best performance** | Caching (ElastiCache/DAX/CloudFront), Global Accelerator, Provisioned IOPS, placement group |
| **Minimal downtime / no code changes** | DMS + CDC, RDS Proxy, Blue/Green, Aurora, drop-in replacement |
| **Decouple** | **SQS** (বা SNS/EventBridge) |
| **As quickly as possible (migration)** | Managed tool: DataSync, Snowball (খুব বড় data), MGN |

---

## 🎯 Exam Strategy

1. **শেষ লাইন আগে পড়ুন**: প্রশ্নটা আসলে কী চাইছে (cost? HA? security?), সেটা আগে ধরুন।
2. **Keyword underline করুন**: "serverless", "millions of requests", "on-premises", "real-time", "7 years", "infrequently accessed", "SQL", "key-value"।
3. **ভুল option বাদ দিন**: সাধারণত ২টা option পরিষ্কার ভুল হয় (যে service ঐ কাজ করেই না, বা requirement ভাঙে)। বাকি ২টার মধ্যে qualifier দেখে বাছুন।
4. **"Custom script on EC2"** ধরনের option সাধারণত ভুল, যদি একটা managed service থাকে যেটা একই কাজ করে।
5. **অতিরিক্ত জটিল** option (৫টা service জোড়া লাগানো) সাধারণত ভুল, সহজ managed option সাধারণত ঠিক।
6. **Flag for review**: ২ মিনিটের বেশি লাগলে একটা উত্তর বেছে flag করে এগিয়ে যান, শেষে ফিরে আসুন।
7. **Time plan**: প্রথম pass ~৯০ মিনিট, review ~৩০ মিনিট, বাফার ১০ মিনিট।

---

## 📚 পড়ার ক্রম (এই folder)

1. [02-Keyword-to-Service-Cheat-Sheet.md](./02-Keyword-to-Service-Cheat-Sheet.md) — প্রশ্নের keyword দেখে service চেনার cheat sheet (**সবচেয়ে গুরুত্বপূর্ণ**)
2. Domain 1–4 practice প্রশ্ন (উত্তর ও ব্যাখ্যাসহ), প্রতিটা উত্তর `▶ উত্তর দেখুন`-এ click করলে খোলে
3. [07-Common-Traps-and-Comparisons.md](./07-Common-Traps-and-Comparisons.md) — যেসব জায়গায় সবাই ভুল করে
4. [99-Interview-QA](../99-Interview-QA/02-Answers-Q1-Q130.md) — বিস্তারিত concept ব্যাখ্যা

### ✅ Exam-এর আগে checklist
- [ ] Cheat sheet ২-৩ বার পড়া
- [ ] Practice প্রশ্নে ৮০%+ সঠিক
- [ ] AWS Skill Builder-এর **Official Practice Question Set** (free) দেওয়া
- [ ] অন্তত ১টা full-length timed practice exam
- [ ] ভুল উত্তরগুলোর ব্যাখ্যা আবার পড়া
