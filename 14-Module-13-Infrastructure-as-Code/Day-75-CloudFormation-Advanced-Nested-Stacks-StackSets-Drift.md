# 📚 Day 75 — CloudFormation Advanced: Nested Stacks, StackSets ও Drift Detection

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![CloudFormation Nested Stacks and StackSets](../images/78-cloudformation-nested-stacksets.png)

**সময়:** ২ ঘণ্টা | **Module:** ১৩ (Infrastructure as Code) — Day 2

## 🎯 আজকের লক্ষ্য
- **Nested Stacks**: বড় টেমপ্লেট ছোট, reusable অংশে ভাগ করা
- **StackSets**: multi-account/multi-region-এ একই template একবারে deploy (Day 40, Day 67-এর সাথে সংযোগ)
- **Drift Detection**: কেউ console-এ ম্যানুয়ালি বদলালে ধরা
- **DeletionPolicy** ও **UpdateReplacePolicy**: stateful resource সুরক্ষা
- CloudFormation-এর সীমাবদ্ধতা (কখন যথেষ্ট না)

---

## Part 1: Nested Stacks — বড় Template ভাগ করা

**সমস্যা:** একটা মনোলিথিক ৫০০ লাইনের টেমপ্লেটে VPC, security group, ECS cluster, database সব একসাথে থাকলে maintain করা কঠিন, reuse করা যায় না।

**সমাধান: Nested Stack** — একটা root (parent) stack অন্য stack-কে resource হিসেবে reference করে।

```yaml
# root-stack.yaml
Resources:
  NetworkStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.../network.yaml
      Parameters:
        EnvironmentName: !Ref EnvironmentName

  ECSStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.../ecs-cluster.yaml
      Parameters:
        VpcId: !GetAtt NetworkStack.Outputs.VpcId
```

**সুবিধা:** `network.yaml` একবার লিখে বিভিন্ন প্রজেক্টে reuse করা যায় (Module 10-এর প্রতিটা microservice-এর জন্য একই VPC template)। একটা nested stack-এর output আরেকটার input হিসেবে পাস হয়।

---

## Part 2: StackSets — Multi-Account/Multi-Region Deployment (Day 40-এর সাথে সংযোগ)

**সমস্যা:** Day 40-এ multi-account architecture শিখেছেন — dev/staging/prod আলাদা account-এ। একই baseline resource (যেমন CloudTrail organization trail, SCP guardrail, Day 52-53) **প্রতিটা** account-এ বসাতে হবে।

**সমাধান: StackSet** — একটা টেমপ্লেট থেকে **একাধিক account এবং region**-এ automatically stack instance deploy করা।

```
StackSet template (baseline-security.yaml)
        │
        ├──► Stack instance: Dev Account (ap-south-1)
        ├──► Stack instance: Staging Account (ap-south-1)
        └──► Stack instance: Prod Account (ap-south-1, ap-southeast-1)
```

**ব্যবহার:** Organization-wide guardrail (CloudTrail, Config rule, IAM baseline) — নতুন account যোগ হলে StackSet automatically সেখানেও apply করা যায় (Organizations integration-এ)।

---

## Part 3: Drift Detection — কেউ Console-এ বদলালে ধরা

**সমস্যা:** CloudFormation দিয়ে একটা Security Group তৈরি হয়েছিল, কিন্তু পরে কেউ জরুরি অবস্থায় console-এ গিয়ে সরাসরি একটা ইনবাউন্ড রুল যোগ করেছে। এখন **টেমপ্লেট আর actual resource-এর মধ্যে অমিল** তৈরি হয়ে গেছে — এটাকে বলে **drift**।

**সমাধান: Drift Detection** — CloudFormation actual resource-এর state আর টেমপ্লেটের expected state তুলনা করে দেখায় কোনটা `MODIFIED` বা `DELETED`।

```
Stack Drift Detection চালান ──► Resource: SecurityGroup ──► Status: MODIFIED
                                                          ──► ইনবাউন্ড রুল টেমপ্লেটে নেই, কিন্তু আসলে আছে
```

> **নীতি:** IaC দিয়ে manage করা resource-এ **কখনো** console/CLI দিয়ে সরাসরি পরিবর্তন করা উচিত না — সব পরিবর্তন টেমপ্লেটের মাধ্যমে হওয়া উচিত। Drift Detection দিয়ে নিয়মিত চেক করুন কেউ এই নিয়ম ভেঙেছে কিনা।

---

## Part 4: DeletionPolicy ও UpdateReplacePolicy

Day 74-এ সংক্ষেপে এসেছিল, আজ বিস্তারিত:

```yaml
OrdersDB:
  Type: AWS::RDS::DBInstance
  DeletionPolicy: Snapshot        # Stack delete হলে final snapshot নিয়ে তারপর delete
  UpdateReplacePolicy: Retain     # Update-এ resource replace হলে পুরনোটা delete না করে রেখে দেওয়া
```

| Policy | মান | আচরণ |
|---|---|---|
| `DeletionPolicy` | `Delete` (default) | Stack delete হলে resource-ও delete |
| | `Retain` | Stack delete হলেও resource থেকে যায় |
| | `Snapshot` | Delete করার আগে snapshot নেওয়া (RDS, EBS, ElastiCache-এ প্রযোজ্য) |
| `UpdateReplacePolicy` | (একই অপশন) | Update-এ resource **replace** হলে পুরনোটার কী হবে |

---

## Part 5: CloudFormation-এর সীমাবদ্ধতা

- **শুধু AWS** — অন্য cloud provider বা on-prem resource manage করতে পারে না
- Syntax (YAML/JSON) কখনো কখনো verbose ও পড়া কঠিন, বিশেষ করে conditional logic-এ
- State আলাদাভাবে manage করতে হয় না (AWS নিজেই track করে) — এটা Terraform-এর তুলনায় একটা সুবিধা (Day 76-77-এ দেখবেন)

---

## Part 6: Hands-on Lab

1. একটা `network.yaml` (VPC + subnet) আর একটা `root.yaml` (network.yaml-কে nested stack হিসেবে ব্যবহার করে) লিখুন
2. একটা StackSet তৈরি করুন (যদি একাধিক account/organization access থাকে; না থাকলে single-account-এ concept বুঝুন)
3. একটা Security Group CloudFormation দিয়ে তৈরি করুন, তারপর console-এ গিয়ে ম্যানুয়ালি একটা রুল যোগ করুন
4. Drift Detection চালান, `MODIFIED` status দেখুন
5. একটা RDS resource-এ `DeletionPolicy: Snapshot` যোগ করে টেস্ট করুন

---

## 🎯 আজকের মূল Takeaways
- Nested Stacks বড় infrastructure ছোট, reusable অংশে ভাগ করে
- StackSets multi-account/region-এ একই baseline resource একসাথে deploy করে (organization guardrail-এর জন্য আদর্শ)
- Drift Detection ধরে ফেলে কখন কেউ IaC-বহির্ভূতভাবে console-এ resource বদলেছে
- DeletionPolicy/UpdateReplacePolicy stateful resource-কে দুর্ঘটনাজনিত data loss থেকে রক্ষা করে

## 📝 Self-check Questions
1. Nested Stack ব্যবহারের মূল সুবিধা কী?
2. StackSet কোন পরিস্থিতিতে সবচেয়ে বেশি কাজে লাগে?
3. Drift Detection কী সমস্যা ধরার জন্য তৈরি হয়েছিল?
4. `DeletionPolicy: Snapshot` আর `Retain`-এর পার্থক্য কী?

## 💡 Pro Tips
- Organization-wide baseline (CloudTrail, SCP-সাপোর্টিং resource) StackSets দিয়ে deploy করুন, প্রতিটা account-এ আলাদা আলাদা manual deploy না
- নিয়মিত (সাপ্তাহিক) Drift Detection চালান, বিশেষ করে যেসব resource-এ "emergency fix" হওয়ার সম্ভাবনা আছে
- সব stateful resource (database, storage)-এ default `DeletionPolicy: Delete` পরিবর্তন করে `Retain`/`Snapshot` সেট করুন
- Nested stack template-গুলো S3-তে version-controlled রাখুন, ঠিক কোন version কোন root stack ব্যবহার করছে ট্র্যাক করুন

## 🎨 Quick Reference
```
Nested Stack: AWS::CloudFormation::Stack, TemplateURL দিয়ে child template reference
StackSet: multi-account + multi-region, single template, organization-wide baseline
Drift Detection: actual resource vs template তুলনা, MODIFIED/DELETED status
DeletionPolicy/UpdateReplacePolicy: Delete (default) | Retain | Snapshot
```

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** একটা emergency-তে কেউ console-এ গিয়ে সরাসরি Security Group-এ রুল যোগ করেছিল, মাসখানেক পরে সেই টেমপ্লেট আপডেট করতে গিয়ে CloudFormation সেই ম্যানুয়াল রুল মুছে দিল — প্রোডাকশন আউটেজ।
**শিক্ষা:** IaC দিয়ে manage করা resource-এ কখনো সরাসরি console পরিবর্তন করবেন না; নিয়মিত Drift Detection চালান।

**পরিস্থিতি ২:** একটা organization-এ ৩০টা account-এ ম্যানুয়ালি একই CloudTrail সেটআপ করা হচ্ছিল, প্রতিটাতে ছোটখাটো ভিন্নতা তৈরি হচ্ছিল।
**শিক্ষা:** StackSets ব্যবহার করুন, প্রতিটা account একই, consistent baseline পাবে।

---

**⏮ আগের দিন:** [Day 74 — CloudFormation Fundamentals](./Day-74-CloudFormation-Fundamentals-Template-Anatomy.md) | **⏭ পরের দিন:** [Day 76 — Terraform Fundamentals: HCL, Provider ও State](./Day-76-Terraform-Fundamentals-HCL-Provider-State.md)
