# 📚 Day 60 — Amazon ECS: Cluster, Task Definition ও Service

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![ECS Cluster, Task Definition and Service](../images/64-ecs-cluster-task-service.png)

**সময়:** ২ ঘণ্টা | **Module:** ১০ (Containers: ECS, EKS & Fargate) — Day 2

## 🎯 আজকের লক্ষ্য
- Amazon ECS কী, কোন সমস্যার সমাধান করে
- **Task Definition**: container-এর blueprint (CPU/memory, image, port, IAM role)
- **Task** বনাম **Service**: একবার চালানো বনাম সবসময় সচল রাখা
- **Launch Type**: EC2 বনাম Fargate
- ECS Service-এর **desired count** ও self-healing
- ALB-এর সাথে ECS Service ইন্টিগ্রেশন (Day 47-এর সাথে সংযোগ)

---

## Part 1: Amazon ECS কী সমস্যা সমাধান করে?

**সমস্যা:** নিজে নিজে কয়েকশ container চালাতে গেলে — কোন container কোথায় চলবে, কোনটা crash করলে কীভাবে restart হবে, load কীভাবে ভাগ হবে — সব manually সামলানো অসম্ভব।

**সমাধান: Amazon ECS (Elastic Container Service)** — AWS-এর নিজস্ব **container orchestrator**, container **schedule, scale, monitor ও self-heal** করে।

---

## Part 2: Task Definition — Container-এর Blueprint

**Task Definition** হলো একটা JSON blueprint যা বলে দেয় কোন image, কত CPU/memory, কোন পোর্ট, কোন IAM role দিয়ে একটা (বা একাধিক related) container চলবে।

```json
{
  "family": "webapp",
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "<account>.dkr.ecr.ap-south-1.amazonaws.com/myapp:latest",
      "portMappings": [{ "containerPort": 3000 }],
      "logConfiguration": { "logDriver": "awslogs" }
    }
  ],
  "taskRoleArn": "arn:aws:iam::...:role/webapp-task-role",
  "executionRoleArn": "arn:aws:iam::...:role/ecs-execution-role"
}
```

### Task Role বনাম Execution Role (গুরুত্বপূর্ণ পার্থক্য)
| | **Task Role** | **Execution Role** |
|---|---|---|
| ব্যবহার করে | Container-এর ভেতরের **app code** (যেমন S3/DynamoDB access) | **ECS agent** নিজে (image pull, log push) |
| তুলনা | Lambda-এর execution role-এর মতো (Day 26) | Infrastructure-level permission |

---

## Part 3: Task বনাম Service

| | **Standalone Task** | **Service** |
|---|---|---|
| ব্যবহার | একবার চালিয়ে শেষ (batch job, migration script) | সবসময় চালু থাকা app (web server, API) |
| Desired Count | প্রযোজ্য না | নির্দিষ্ট সংখ্যক task সবসময় সচল রাখে |
| Self-healing | না | হ্যাঁ — task crash করলে ECS নতুন task চালু করে |
| Load Balancer | না | ALB/NLB-এর সাথে integrate করা যায় |

**Desired Count**-এর ধারণা EC2 Auto Scaling Group-এর মতোই (Day 7) — ECS Service ক্রমাগত monitor করে actual running task-এর সংখ্যা desired count-এর সমান আছে কিনা, না থাকলে নতুন task চালায়।

---

## Part 4: Launch Type — EC2 বনাম Fargate

| | **EC2 Launch Type** | **Fargate Launch Type** |
|---|---|---|
| Infrastructure | আপনি EC2 instance manage করেন (patch, scale) | সম্পূর্ণ **serverless** — কোনো EC2 নেই |
| Control | বেশি (instance type বাছা যায়, GPU ইত্যাদি) | কম, কিন্তু ঝামেলাও কম |
| Billing | EC2 instance-এর জন্য (idle capacity-ও বিল হতে পারে) | শুধু task-এর ব্যবহৃত CPU/memory-এর জন্য (per-second) |
| উপযুক্ত | Cost-optimize করা predictable workload, বিশেষ hardware দরকার | দ্রুত শুরু, ops overhead কমাতে চাইলে, spiky/unpredictable workload |

> **সহজ নিয়ম:** নতুন প্রজেক্টে বা কম operational overhead চাইলে **Fargate** দিয়ে শুরু করুন; বড় স্কেলে খরচ optimize করতে বা বিশেষ instance type দরকার হলে EC2 launch type বিবেচনা করুন।

---

## Part 5: ALB-এর সাথে ECS Service Integration (Day 47-এর সাথে সংযোগ)

```
ALB ──► Target Group (type: IP, for Fargate) ──► ECS Service ──► Task 1, Task 2, Task 3
```

- ALB health check task-এর health দেখে; unhealthy task হলে ECS সেটাকে replace করে নতুন task চালায়
- **Rolling deployment**: নতুন task definition version deploy করলে ECS ধীরে ধীরে পুরনো task সরিয়ে নতুন task আনে (minimum healthy percent সেট করে zero-downtime deployment)

---

## Part 6: Hands-on Lab

1. একটা ECS Cluster তৈরি করুন (Fargate)
2. Day 59-এর push করা ECR image দিয়ে একটা Task Definition তৈরি করুন
3. সেই Task Definition দিয়ে একটা Service চালু করুন, desired count = 2
4. ALB-এর সাথে Service integrate করুন, target group type "IP" বাছুন
5. একটা task manually stop করে দেখুন ECS নতুন task চালু করে কিনা (self-healing)
6. Task Definition-এর নতুন revision তৈরি করে (image tag বদলে) Service আপডেট করুন, rolling deployment দেখুন
7. Cluster ও সব resource মুছুন

---

## 🎯 আজকের মূল Takeaways
- Task Definition = blueprint; Task = running instance; Service = desired count বজায় রাখা + load balancer integration
- Task Role (app permission) আর Execution Role (ECS agent permission) সম্পূর্ণ ভিন্ন জিনিস
- Fargate = serverless (কম ops, per-second billing); EC2 launch type = বেশি control, খরচ optimize
- ALB + ECS Service মিলে self-healing, zero-downtime rolling deployment দেয়

## 📝 Self-check Questions
1. Task Role আর Execution Role গুলিয়ে ফেললে কী সমস্যা হতে পারে?
2. Desired count 3 থাকা অবস্থায় একটা task crash করলে ECS কী করে?
3. Fargate বনাম EC2 launch type কবে কোনটা বাছবেন?
4. ALB টার্গেট গ্রুপ type "IP" কেন Fargate-এর সাথে ব্যবহার হয় (Instance না)?

## 💡 Pro Tips
- Execution role-এ শুধু ECR pull আর CloudWatch Logs push permission দিন, বেশি দেবেন না
- CPU/memory ঠিক মাপে সেট করুন — অতিরিক্ত মানে অপচয়, কম মানে throttling/OOM
- Rolling deployment-এ `minimumHealthyPercent` আর `maximumPercent` ঠিকভাবে সেট করুন, না হলে deployment-এর সময় capacity কমে যেতে পারে
- Fargate দিয়ে শুরু করুন, প্রয়োজন হলেই পরে EC2 launch type-এ migrate করুন

## 🎨 Quick Reference
```
Task Definition: blueprint (image, CPU/mem, port, roles)
Task: running instance of a task definition | Service: desired count + self-healing + LB
Task Role: app permissions | Execution Role: ECS agent permissions (pull image, push logs)
Launch type: EC2 (control, manage instances) | Fargate (serverless, per-second billing)
```

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** App-এর কোডে S3 access করতে হচ্ছিল, কিন্তু permission দেওয়া হয়েছিল Execution Role-এ (Task Role-এ না) — সবসময় Access Denied error।
**শিক্ষা:** App-এর নিজের permission সবসময় **Task Role**-এ দিন।

**পরিস্থিতি ২:** Deployment-এর সময় সব পুরনো task একসাথে বন্ধ করে নতুন task চালু করা হচ্ছিল, ফলে কয়েক সেকেন্ডের downtime হতো প্রতিবার।
**শিক্ষা:** Rolling deployment configuration (minimum healthy percent > 100%-এর কম না) ঠিকভাবে সেট করুন।

---

**⏮ আগের দিন:** [Day 59 — Docker ও Container Fundamentals, ECR](./Day-59-Docker-Container-Fundamentals-ECR.md) | **⏭ পরের দিন:** [Day 61 — Amazon EKS ও ECS বনাম EKS বনাম Fargate](./Day-61-EKS-Fundamentals-ECS-vs-EKS-vs-Fargate.md)
