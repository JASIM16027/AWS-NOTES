# ☁️ AWS-NOTES

AWS শেখার জন্য বাংলায় লেখা note-এর সংগ্রহ। আছে fundamentals, day-wise course note আর interview Q&A।

---

## 📂 Repository Structure

```
AWS-NOTES/
├── 00-Getting-Started/                 → Syllabus ও learning roadmap
├── 01-Fundamentals/                    → Cloud, IAM, EC2, VPC — technical deep dive
├── 02-Module-1-EC2-and-Storage/        → Day 1–7
├── 03-Module-2-VPC-and-Networking/     → Day 8–14
├── 04-Module-3-Application-Deployment/ → Day 15–16 (চলমান)
├── 98-SAA-C03-Exam-Prep/               → Solutions Architect Associate exam: cheat sheet + ৬২টা practice প্রশ্ন
├── 99-Interview-QA/                    → ১৩০টা interview প্রশ্ন + উত্তর
└── images/                             → Diagram (PNG) + src/ (Mermaid source)
```

---

## 🔰 00 — Getting Started

| # | Note |
|---|---|
| 1 | [Course Syllabus — ৮টি মডিউল](./00-Getting-Started/01-Course-Syllabus-8-Modules.md) |
| 2 | [Step-by-Step AWS Learning (Beginner → Job Ready)](./00-Getting-Started/02-Step-by-Step-Learning-Path.md) |
| 3 | [AWS Learning Topics Roadmap](./00-Getting-Started/03-AWS-Learning-Topics-Roadmap.md) |

## 📘 01 — Fundamentals (Deep Dive)

| # | Note |
|---|---|
| 1 | [Traditional IT Approach-এর সমস্যাগুলো](./01-Fundamentals/01-Traditional-IT-Problems.md) |
| 2 | [Cloud Computing — Technical Deep Dive](./01-Fundamentals/02-Cloud-Computing-Deep-Dive.md) |
| 3 | [AWS IAM — Technical Deep Dive](./01-Fundamentals/03-AWS-IAM-Deep-Dive.md) |
| 4 | [EC2 + VPC — Technical Deep Dive](./01-Fundamentals/04-EC2-and-VPC-Deep-Dive.md) |
| 5 | [VPC — সম্পূর্ণ Technical ব্যাখ্যা](./01-Fundamentals/05-VPC-Complete-Guide.md) |
| 6 | [AWS — DevOps-এর জন্য বিস্তারিত গাইড](./01-Fundamentals/06-AWS-for-DevOps.md) |
| 7 | [AWS Basics — Cloud, Pricing, Console, Shared Responsibility, IAM (English)](./01-Fundamentals/07-AWS-Basics-Cloud-Pricing-IAM.md) |

## 🖥 02 — Module 1: EC2 & Storage Fundamentals

| Day | Topic |
|---|---|
| 1 | [Cloud Computing, AWS Infrastructure & Account Setup](./02-Module-1-EC2-and-Storage/Day-01-Cloud-Computing-AWS-Infrastructure-Account-Setup.md) |
| 2 | [EC2 Instance Types, AMI ও EC2 Launch Process](./02-Module-1-EC2-and-Storage/Day-02-EC2-Instance-Types-AMI-Launch.md) |
| 3 | [Key Pairs, Security Groups & Elastic IP](./02-Module-1-EC2-and-Storage/Day-03-Key-Pairs-Security-Groups-Elastic-IP.md) |
| 4 | [EBS, Instance Store & EFS](./02-Module-1-EC2-and-Storage/Day-04-EBS-Instance-Store-EFS.md) |
| 5 | [S3 & Glacier](./02-Module-1-EC2-and-Storage/Day-05-S3-and-Glacier.md) |
| 6 | [EC2 Pricing Models](./02-Module-1-EC2-and-Storage/Day-06-EC2-Pricing-Models.md) |
| 7 | [Auto Scaling + Module 1 Revision](./02-Module-1-EC2-and-Storage/Day-07-Auto-Scaling-Module-1-Revision.md) |
| ➕ | [Extra: EC2 Launch, Security Group & EBS Basics (English)](./02-Module-1-EC2-and-Storage/Extra-EC2-Launch-SG-EBS-Basics.md) |

## 🌐 03 — Module 2: VPC Design & Network Architecture

| Day | Topic |
|---|---|
| 8 | [VPC Core Components & CIDR](./03-Module-2-VPC-and-Networking/Day-08-VPC-Core-Components-CIDR.md) |
| 9 | [IGW & Route Tables (Even Deeper)](./03-Module-2-VPC-and-Networking/Day-09-IGW-and-Route-Tables.md) |
| 10 | [Network ACL vs Security Group](./03-Module-2-VPC-and-Networking/Day-10-Network-ACL-vs-Security-Group.md) |
| 11 | [NAT Gateway, NAT Instance & Bastion Host](./03-Module-2-VPC-and-Networking/Day-11-NAT-Gateway-NAT-Instance-Bastion-Host.md) |
| 12 | [VPC Endpoints & PrivateLink](./03-Module-2-VPC-and-Networking/Day-12-VPC-Endpoints-PrivateLink.md) |
| 13 | [Route 53 Resolver, DHCP Options, EIP & IPv6](./03-Module-2-VPC-and-Networking/Day-13-Route53-Resolver-DHCP-EIP-IPv6.md) |
| 14 | [Network Design Patterns + Module 2 Revision](./03-Module-2-VPC-and-Networking/Day-14-Network-Design-Patterns-Module-2-Revision.md) |

## 🚀 04 — Module 3: Application Deployment on EC2 with systemd

| Day | Topic |
|---|---|
| 15 | [User Data, Cloud-init & EC2 Instance Connect](./04-Module-3-Application-Deployment/Day-15-User-Data-Cloud-init-EC2-Instance-Connect.md) |
| 16 | [SSM Session Manager & IAM Instance Profile](./04-Module-3-Application-Deployment/Day-16-SSM-Session-Manager-IAM-Instance-Profile.md) |

## 🎓 98 — AWS Solutions Architect Associate (SAA-C03) Exam Prep

| # | Note |
|---|---|
| 1 | [Exam Overview ও Strategy](./98-SAA-C03-Exam-Prep/01-Exam-Overview-and-Strategy.md) |
| 2 | [Keyword → Service Cheat Sheet](./98-SAA-C03-Exam-Prep/02-Keyword-to-Service-Cheat-Sheet.md) |
| 3 | [Domain 1: Secure Architectures — ১৬টা প্রশ্ন](./98-SAA-C03-Exam-Prep/03-Domain-1-Secure-Architectures.md) |
| 4 | [Domain 2: Resilient Architectures — ১৫টা প্রশ্ন](./98-SAA-C03-Exam-Prep/04-Domain-2-Resilient-Architectures.md) |
| 5 | [Domain 3: High-Performing Architectures — ১৬টা প্রশ্ন](./98-SAA-C03-Exam-Prep/05-Domain-3-High-Performing-Architectures.md) |
| 6 | [Domain 4: Cost-Optimized Architectures — ১৫টা প্রশ্ন](./98-SAA-C03-Exam-Prep/06-Domain-4-Cost-Optimized-Architectures.md) |
| 7 | [Common Traps ও Comparisons](./98-SAA-C03-Exam-Prep/07-Common-Traps-and-Comparisons.md) |

## 🎯 99 — Interview Q&A

| # | Note |
|---|---|
| 1 | [AWS Interview Questions (Q1–Q130)](./99-Interview-QA/01-Questions.md) |
| 2 | [উত্তরসহ Notes (Q1–Q130)](./99-Interview-QA/02-Answers-Q1-Q130.md) |

---

## 🧭 কীভাবে পড়বেন

1. **00-Getting-Started** — Syllabus দেখে পুরো roadmap বুঝে নিন।
2. **01-Fundamentals** — Cloud, IAM, EC2, VPC-এর মূল ধারণা।
3. **02 → 04 Modules** — Day-wise hands-on note ক্রমানুসারে।
4. **98-SAA-C03-Exam-Prep**: certification দিতে চাইলে cheat sheet পড়ে practice প্রশ্নগুলো নিজে solve করুন।
5. **99-Interview-QA** — প্রতিটা module শেষে সংশ্লিষ্ট প্রশ্নগুলো নিজে উত্তর দিয়ে practice করুন, তারপর answer মিলিয়ে দেখুন।

### ✍️ নতুন note যোগ করার নিয়ম
- নতুন Day note → সংশ্লিষ্ট module folder-এ `Day-XX-Topic-Name.md` নামে রাখুন (যেমন `Day-17-CloudWatch-Agent-Setup.md`)।
- নতুন module শুরু হলে → `05-Module-4-Serverless-and-Lambda/` এর মতো নতুন folder খুলুন।
- এই README-র টেবিলে link যোগ করুন।
- নতুন diagram → `images/src/`-এ `.mmd` (Mermaid) file লিখে PNG render করুন:
  `npx -p @mermaid-js/mermaid-cli mmdc -i images/src/xx.mmd -o images/xx.png -b white -s 2`
