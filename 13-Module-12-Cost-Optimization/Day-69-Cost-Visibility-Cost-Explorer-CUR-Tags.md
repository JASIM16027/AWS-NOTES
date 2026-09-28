# 📚 Day 69 — Cost Visibility: Cost Explorer, Cost & Usage Report ও Tags

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![Cost Visibility Pipeline](../images/72-cost-visibility-pipeline.png)

**সময়:** ২ ঘণ্টা | **Module:** ১২ (Cost Optimization & FinOps) — Day 1

## 🎯 আজকের লক্ষ্য
- কেন cost visibility ছাড়া optimization অসম্ভব ("যা দেখা যায় না, তা কমানো যায় না")
- **Cost Explorer**: trend, filter, group by, forecast
- **Cost & Usage Report (CUR)**: সবচেয়ে granular ডেটা, Athena/QuickSight দিয়ে বিশ্লেষণ
- **Cost Allocation Tags**: কোন team/project/environment কত খরচ করছে
- **Cost Categories**: rule-based grouping (একাধিক tag/account একসাথে)
- Multi-account billing (Day 40-এর Organizations-এর সাথে সংযোগ): Consolidated Billing

---

## Part 1: কেন Cost Visibility প্রথম ধাপ?

**সমস্যা:** মাস শেষে বড় বিল দেখে অবাক হওয়া, কিন্তু **কোন সার্ভিস, কোন টিম, কোন environment** এই খরচের জন্য দায়ী তা না জানা।

**সমাধান:** Optimize করার আগে **measure** করতে হবে — কোথায় খরচ হচ্ছে, কেন হচ্ছে, ট্রেন্ড কেমন।

```
Visibility (কোথায় খরচ?) → Analysis (কেন এত?) → Optimization (কীভাবে কমানো?) → Governance (ভবিষ্যতে নিয়ন্ত্রণ)
```

---

## Part 2: AWS Cost Explorer

**Cost Explorer** একটা visual UI টুল যা গত ১৩ মাসের খরচ দেখায়, আর ১২ মাস পর্যন্ত **forecast** করে।

### মূল ফিচার
- **Filter**: service, region, account, tag অনুযায়ী
- **Group by**: কোন dimension-এ ভাগ করে দেখতে চান (Service, Linked Account, Tag)
- **Granularity**: daily বা monthly
- **RI/Savings Plans utilization report**: কেনা reservation কতটা ব্যবহার হচ্ছে (Day 6-এর সাথে সংযোগ — না ব্যবহার হলে টাকা নষ্ট)

```
প্রশ্ন: "গত ৩ মাসে EC2 খরচ কেন বেড়েছে?"
Cost Explorer: Group by = Service, Filter = EC2, Granularity = Daily
→ কোন দিন থেকে বাড়া শুরু হয়েছে সেটা visually দেখা যায়
```

---

## Part 3: Cost & Usage Report (CUR) — সবচেয়ে Granular ডেটা

Cost Explorer UI-তে যতটা বিস্তারিত দেখা যায় তার চেয়েও গভীর বিশ্লেষণ দরকার হলে (custom dashboard, resource-ID পর্যায়ে) — **CUR** ব্যবহার হয়।

```
CUR (hourly/daily, প্রতিটা line item resource ID পর্যন্ত) ──► S3 bucket ──► Athena (SQL query) / QuickSight (dashboard)
```

- সবচেয়ে granular billing ডেটা AWS যা দেয় (প্রতিটা resource, প্রতিটা ঘণ্টা)
- নিজস্ব custom cost dashboard বা automated report বানাতে ব্যবহার হয়
- অনেক third-party cost management tool (CloudHealth, Cloudability) CUR-এর উপর ভিত্তি করেই কাজ করে

---

## Part 4: Cost Allocation Tags — কে খরচ করছে?

**সমস্যা:** ১০০টা EC2 instance আছে, কিন্তু কোনটা কোন টিমের, কোন project-এর — tag ছাড়া বোঝা অসম্ভব।

**সমাধান: Cost Allocation Tags** — resource-এ tag (`Team=Payments`, `Environment=Production`, `Project=ShopBD`) লাগিয়ে সেটা billing-এ activate করলে Cost Explorer/CUR-এ সেই dimension দিয়ে filter/group করা যায়।

```
EC2 Instance (Tag: Team=Payments) ┐
RDS Instance (Tag: Team=Payments) ├──► Cost Explorer "Group by: Tag=Team" ──► Payments team-এর মোট খরচ
Lambda Function (Tag: Team=Payments) ┘
```

### দুই ধরনের Tag
| ধরন | উৎস |
|---|---|
| **AWS-generated tags** | AWS নিজে কিছু default tag দেয় (যেমন `aws:createdBy`) |
| **User-defined tags** | আপনি নিজে লাগান (`Team`, `Environment`, `CostCenter`) — Billing-এ Cost Allocation Tags সেকশনে activate করতে হয় |

---

## Part 5: Cost Categories — জটিল Grouping

কখনো খরচ ভাগ করা একটামাত্র tag দিয়ে সম্ভব না (একাধিক account, একাধিক tag মিলিয়ে একটা business unit)। **Cost Categories** rule-based grouping দেয়:

```
Rule: (Account = "Prod-Payments" OR Tag:Team = "Payments") → Category = "Payments BU"
```

---

## Part 6: Multi-Account Billing (Day 40-এর সাথে সংযোগ)

AWS Organizations-এ **Consolidated Billing** থাকলে সব member account-এর বিল একটা management account-এ একত্র হয়, আর ভলিউম discount (RI/Savings Plans শেয়ারিং) সব account জুড়ে প্রযোজ্য হয়।

---

## Part 7: Hands-on Lab

1. Cost Explorer-এ গিয়ে গত ৩ মাসের খরচ "Group by: Service" দেখুন
2. একটা resource-এ `Team` আর `Environment` tag লাগান, Billing Console-এ Cost Allocation Tags activate করুন (activate হতে ২৪ ঘণ্টা পর্যন্ত লাগতে পারে)
3. পরের দিন Cost Explorer-এ "Group by: Tag" দিয়ে filter করুন
4. একটা CUR export সেটআপ করুন (S3-তে delivery)
5. Athena দিয়ে CUR ডেটার উপর একটা সাধারণ SQL query চালান (যেমন "গত মাসে সবচেয়ে বেশি খরচ করা ৫টা resource")

---

## 🎯 আজকের মূল Takeaways
- Optimize করার আগে visibility (measure) দরকার — Cost Explorer, CUR, Tags তিনটাই ভিন্ন গভীরতায় সাহায্য করে
- Cost Explorer UI-ভিত্তিক দ্রুত বিশ্লেষণ; CUR সবচেয়ে granular, custom analysis-এর জন্য
- Tag activate না করলে সেই dimension দিয়ে filter করা যায় না — শুরু থেকেই tagging strategy ঠিক করুন
- Cost Categories জটিল, multi-dimension grouping-এর জন্য
- Consolidated Billing multi-account-এ ভলিউম discount শেয়ার করে

## 📝 Self-check Questions
1. Cost Explorer আর CUR-এর মধ্যে granularity-র পার্থক্য কী?
2. Tag লাগানোর পরেও কেন সাথে সাথে Cost Explorer-এ দেখা নাও যেতে পারে?
3. Cost Categories কখন দরকার হয় শুধু tag দিয়ে যথেষ্ট না হলে?
4. Consolidated Billing multi-account-এ কী সুবিধা দেয়?

## 💡 Pro Tips
- Resource তৈরির শুরু থেকেই tagging enforce করুন (SCP বা Config rule দিয়ে, Day 52) — পরে tag লাগানো অনেক কঠিন
- একটা standard tag set ঠিক করুন (`Team`, `Environment`, `Project`, `CostCenter`) আর পুরো organization-এ consistent রাখুন
- মাসে অন্তত একবার Cost Explorer রিভিউ করুন, শুধু বিল আসার পর অবাক হবেন না
- CUR + Athena/QuickSight সেটআপ করে রাখুন, ভবিষ্যতে জটিল প্রশ্নের উত্তর দ্রুত পাবেন

## 🎨 Quick Reference
```
Cost Explorer: UI, 13 মাসের history, 12 মাসের forecast, filter/group by
CUR: সবচেয়ে granular (hourly, resource-level), S3 → Athena/QuickSight
Cost Allocation Tags: activate করতে হয়, filter/group-এর dimension হিসেবে ব্যবহার
Cost Categories: rule-based, multi-tag/multi-account grouping
Consolidated Billing: Organizations-এ shared volume discount
```

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** কোনো tagging policy ছিল না, ১ বছর পর কেউ জানত না কোন resource কোন প্রজেক্টের — cleanup করতে গিয়ে ভয়ে কিছুই মোছা হলো না।
**শিক্ষা:** শুরু থেকেই standard tag enforce করুন।

**পরিস্থিতি ২:** একটা বড় বিল দেখে টিম হতবাক হলো, কিন্তু Cost Explorer কখনো দেখা হয়নি বলে কোন সার্ভিস দায়ী বুঝতে কয়েকদিন লাগল।
**শিক্ষা:** নিয়মিত (সাপ্তাহিক/মাসিক) Cost Explorer রিভিউ করুন, শুধু বিল আসলে না।

---

**⏮ আগের module:** [Day 68 — Module 11 Revision](../12-Module-11-CICD-CodePipeline-CodeBuild/Day-68-Module-11-Revision-End-to-End-CICD-Project.md) | **⏭ পরের দিন:** [Day 70 — AWS Budgets, Alerts ও Anomaly Detection](./Day-70-Budgets-Alerts-Anomaly-Detection.md)
