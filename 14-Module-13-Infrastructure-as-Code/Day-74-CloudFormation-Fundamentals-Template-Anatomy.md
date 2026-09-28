# 📚 Day 74 — CloudFormation Fundamentals: Template Anatomy

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![CloudFormation Template Anatomy](../images/77-cloudformation-template-anatomy.png)

**সময়:** ২ ঘণ্টা | **Module:** ১৩ (Infrastructure as Code) — Day 1

## 🎯 আজকের লক্ষ্য
- Infrastructure as Code (IaC) কী সমস্যা সমাধান করে (console click-এর বিকল্প)
- CloudFormation Template-এর মূল সেকশন: Parameters, Resources, Outputs, Mappings
- Intrinsic Function: `!Ref`, `!GetAtt`, `!FindInMap`, `!Sub`
- Stack: তৈরি, আপডেট, ডিলিট — সব-অথবা-কিছুই-না (automatic rollback)
- Change Sets: apply করার আগে কী বদলাবে তা preview করা

---

## Part 1: Infrastructure as Code (IaC) কেন?

**সমস্যা (console-এ ম্যানুয়ালি রিসোর্স বানানো):** প্রতিবার ক্লিক করে VPC, subnet, EC2, RDS বানালে — মানুষের ভুল, কোনো documentation নেই, dev/staging/prod-এ হুবহু একই infrastructure বানানো কঠিন, আর কেউ চলে গেলে "ঠিক কী বানানো হয়েছিল" কেউ জানে না।

**সমাধান: Infrastructure as Code** — infrastructure-কে **কোড হিসেবে লেখা**, version control-এ রাখা, আর automation দিয়ে deploy করা।

```
আগে: Console-এ ক্লিক ক্লিক ক্লিক (মনে নেই ঠিক কী করা হয়েছিল)
এখন: template.yaml (Git-এ কমিট, PR review, একই টেমপ্লেট dev/staging/prod-এ পুনরায় ব্যবহার)
```

---

## Part 2: CloudFormation Template-এর মূল সেকশন

**AWS CloudFormation** হলো AWS-এর নিজস্ব, নেটিভ IaC টুল — YAML বা JSON template দিয়ে resource define করা হয়।

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: "ShopBD orders-service infrastructure"

Parameters:
  EnvironmentName:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

Mappings:
  RegionAMIMap:
    ap-south-1:
      AMI: ami-0abcdef1234567890

Resources:
  OrdersBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "shopbd-orders-${EnvironmentName}"

  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap [RegionAMIMap, !Ref "AWS::Region", AMI]
      InstanceType: t3.micro

Outputs:
  BucketName:
    Value: !Ref OrdersBucket
  WebServerPublicIP:
    Value: !GetAtt WebServer.PublicIp
```

| সেকশন | কাজ |
|---|---|
| `Parameters` | ব্যবহারকারীর দেওয়া input (যেমন `EnvironmentName`) — টেমপ্লেটকে reusable করে |
| `Mappings` | Static lookup table (যেমন region অনুযায়ী ভিন্ন AMI ID) |
| **`Resources`** | **একমাত্র বাধ্যতামূলক সেকশন** — কোন AWS resource তৈরি হবে |
| `Outputs` | Stack তৈরি হওয়ার পর দরকারি মান বের করে দেখানো (অন্য stack থেকে ব্যবহারের জন্য export করাও যায়) |

---

## Part 3: Intrinsic Function

| Function | কাজ |
|---|---|
| `!Ref` | একটা resource/parameter-এর মান/ID ফেরত দেয় |
| `!GetAtt` | একটা resource-এর নির্দিষ্ট attribute (যেমন `WebServer.PublicIp`) |
| `!FindInMap` | Mapping থেকে মান খোঁজে |
| `!Sub` | String-এর ভেতরে variable substitute করে (যেমন `"shopbd-orders-${EnvironmentName}"`) |

---

## Part 4: Stack — সব-অথবা-কিছুই-না

একটা টেমপ্লেট deploy করলে একটা **Stack** তৈরি হয় — টেমপ্লেটের সব resource-এর একটা logical group।

- **Create**: নতুন stack, সব resource তৈরি হয়
- **Update**: টেমপ্লেট বদলে আবার deploy করলে CloudFormation বের করে কোন resource বদলাতে হবে
- **Delete**: পুরো stack ডিলিট করলে তার **সব** resource ডিলিট হয় (DeletionPolicy দিয়ে নির্দিষ্ট resource বাঁচানো যায়, যেমন RDS snapshot রেখে)

### Automatic Rollback
কোনো resource তৈরি করতে গিয়ে fail করলে (যেমন quota শেষ), CloudFormation **automatically** পুরো stack-কে আগের অবস্থায় ফিরিয়ে নেয় — অর্ধেক তৈরি হওয়া infrastructure রেখে যায় না।

---

## Part 5: Change Sets — Preview করে তারপর Apply

**সমস্যা:** একটা existing production stack আপডেট করলে ঠিক কী বদলাবে (নতুন resource, নাকি existing resource **replace** হবে — যেমন RDS instance রিক্রিয়েট হয়ে ডেটা হারানো) তা আগে থেকে না জানলে বিপজ্জনক।

**সমাধান: Change Set** — আসলে apply না করে শুধু **preview** দেখায় কোন resource Add/Modify/Remove হবে।

```
Template আপডেট ──► Create Change Set ──► Review: "OrdersDB will be REPLACED (data loss risk!)" ──► Execute বা বাতিল
```

---

## Part 6: Hands-on Lab

1. একটা সাধারণ template লিখুন: একটা S3 bucket + একটা EC2 instance
2. `aws cloudformation deploy` দিয়ে stack তৈরি করুন
3. Outputs-এ bucket name আর instance public IP দেখুন
4. Template-এ instance type বদলে Change Set তৈরি করুন, preview দেখুন
5. Change Set execute করুন, তারপর stack delete করুন
6. ইচ্ছাকৃতভাবে একটা ভুল (নেই এমন AMI ID) দিয়ে deploy করে automatic rollback দেখুন

---

## 🎯 আজকের মূল Takeaways
- IaC infrastructure-কে version-controlled, reproducible কোড বানায়
- `Resources` একমাত্র বাধ্যতামূলক সেকশন; বাকিগুলো টেমপ্লেটকে reusable/readable করে
- Stack-এর যেকোনো resource তৈরি fail করলে পুরো stack automatically rollback হয়
- Change Set দিয়ে production আপডেটের আগে ঠিক কী বদলাবে (বিশেষ করে replace/data-loss risk) যাচাই করুন

## 📝 Self-check Questions
1. CloudFormation টেমপ্লেটের একমাত্র বাধ্যতামূলক সেকশন কোনটা?
2. `!Ref` আর `!GetAtt`-এর পার্থক্য কী?
3. Stack তৈরির মাঝপথে একটা resource fail করলে কী হয়?
4. Change Set কী সমস্যা প্রতিরোধ করে?

## 💡 Pro Tips
- Production stack আপডেটের আগে সবসময় Change Set দিয়ে preview করুন, বিশেষ করে "Replacement: True" চিহ্নিত resource-এ সতর্ক থাকুন
- Stateful resource (RDS, DynamoDB)-এ `DeletionPolicy: Retain` বা `Snapshot` ব্যবহার করুন, stack delete-এ ডেটা যেন না হারায়
- Template-এ hardcode না করে Parameters ব্যবহার করুন, dev/staging/prod-এ একই টেমপ্লেট পুনরায় ব্যবহার করা যাবে
- Output-কে `Export` করলে অন্য stack থেকে `Fn::ImportValue` দিয়ে ব্যবহার করা যায় (cross-stack reference)

## 🎨 Quick Reference
```
Sections: Parameters | Mappings | Resources (required) | Outputs
Intrinsic functions: !Ref | !GetAtt | !FindInMap | !Sub
Stack lifecycle: Create → Update → Delete, fail হলে automatic rollback
Change Set: apply করার আগে preview (Add/Modify/Remove, replacement risk)
```

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** একটা টিম সরাসরি (Change Set ছাড়াই) production stack আপডেট করল, একটা property বদলানোয় RDS instance **replace** হয়ে গেল — পুরো ডেটা হারিয়ে গেল।
**শিক্ষা:** Production-এ সবসময় Change Set দিয়ে আগে replacement risk যাচাই করুন।

**পরিস্থিতি ২:** Stack delete করার সময় কোনো DeletionPolicy সেট করা ছিল না, RDS instance-সহ পুরো stack মুছে গেল, কোনো final snapshot ছাড়াই।
**শিক্ষা:** Stateful resource-এ `DeletionPolicy: Retain`/`Snapshot` দিন।

---

**⏮ আগের module:** [Day 73 — Module 12 Revision](../13-Module-12-Cost-Optimization/Day-73-Module-12-Revision-FinOps-Cost-Optimization-Project.md) | **⏭ পরের দিন:** [Day 75 — CloudFormation Advanced: Nested Stacks, StackSets ও Drift Detection](./Day-75-CloudFormation-Advanced-Nested-Stacks-StackSets-Drift.md)
