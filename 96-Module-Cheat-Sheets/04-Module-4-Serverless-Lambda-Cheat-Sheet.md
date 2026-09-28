# 🗂 Module 4 Cheat Sheet — Serverless & Lambda Fundamentals

> **এক পাতায় পুরো module।** বিস্তারিত লাগলে Day 22–28-এ যান।

📚 বিস্তারিত নোট: [Day 22](../05-Module-4-Serverless-and-Lambda/Day-22-Lambda-Basics-Execution-Model.md) → [Day 28](../05-Module-4-Serverless-and-Lambda/Day-28-Module-4-Revision-Serverless-API-Project.md)

---

## 🖼 Visual Summary

![Lambda Cold Start](../images/06-lambda-cold-start.png)

![Lambda Invocation Models](../images/33-lambda-invocation-models.png)

![Lambda Concurrency](../images/36-lambda-concurrency.png)

---

## ⚡ Service at a Glance

| Concept | কী | মূল সংখ্যা |
|---|---|---|
| **Lambda** | Event-driven, no-server compute | Max timeout **15 min**, max memory **10240 MB** |
| **Cold Start** | নতুন execution environment তৈরি হওয়ার latency | Provisioned Concurrency দিয়ে কমানো যায় |
| **Layers** | Shared code/library, বারবার bundle করতে হয় না | Max 5 layers per function |
| **Version/Alias** | Immutable snapshot / mutable pointer | Blue-green deploy-তে alias শিফট করা হয় |
| **Invocation model** | Sync (API GW) / Async (S3, SNS) / Poll-based (SQS, DynamoDB Streams) | Retry ও error handling ভিন্ন |
| **Reserved/Provisioned Concurrency** | Guaranteed capacity | অন্য function-এর concurrency কমিয়ে দিতে পারে |

---

## 💻 Practical Commands

```bash
# Alias তৈরি (blue-green deployment-এর জন্য)
aws lambda create-alias --function-name my-fn --name prod --function-version 5

# Function URL enable
aws lambda create-function-url-config --function-name my-fn --auth-type AWS_IAM

# Resource policy দেখা (কে invoke করতে পারে)
aws lambda get-policy --function-name thumbnailer

# ECR-এ container image push (container-based Lambda)
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
aws ecr create-repository --repository-name my-fn
```

---

## ⚠️ Top Gotchas

1. **Lambda সীমা ১৫ মিনিট** — এর বেশি লাগলে Step Functions/ECS/Batch ব্যবহার করুন।
2. **VPC-এর ভেতরে Lambda বসালে cold start বাড়ে** (ENI attach করতে সময় লাগে) — VPC endpoint বা Hyperplane ENI দিয়ে কমানো যায়।
3. **Reserved Concurrency = 0 মানে function সম্পূর্ণ বন্ধ** — accidentally 0 সেট করলে সব invocation throttle হবে।
4. **SQS trigger-এ Lambda fail করলে message আবার queue-তে ফিরে আসে** — idempotent handler লিখতে হবে।
5. **Environment variable-এ secret রাখা উচিত না** — KMS encrypt বা Secrets Manager ব্যবহার করুন।

---

## 🔢 মনে রাখার সংখ্যা

- Max timeout: **900 সেকেন্ড (15 মিনিট)**
- Max memory: **10,240 MB** (128 MB থেকে শুরু, CPU memory অনুপাতে scale করে)
- Deployment package (zip) সীমা: **50 MB (compressed)**, **250 MB (uncompressed, layers সহ)**
- Container image সীমা: **10 GB**

---

**⏮ পূর্ববর্তী:** [Module 3 Cheat Sheet](./03-Module-3-App-Deployment-Cheat-Sheet.md) | **⏭ পরবর্তী:** [Module 5 Cheat Sheet](./05-Module-5-Event-Driven-Cheat-Sheet.md)
