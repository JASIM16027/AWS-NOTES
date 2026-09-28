# 🗂 Module 11 Cheat Sheet — CI/CD with CodePipeline & CodeBuild

> **এক পাতায় পুরো module।** বিস্তারিত লাগলে Day 64–68-এ যান।

📚 বিস্তারিত নোট: [12-Module-11-CICD-CodePipeline-CodeBuild](../12-Module-11-CICD-CodePipeline-CodeBuild/)

---

## 🖼 Visual Summary

![CI/CD Pipeline](../images/15-cicd-pipeline.png)

![CI/CD Automation](../images/98-cicd-pipeline.png)

![CodePipeline ECS Blue-Green](../images/69-codepipeline-ecs-bluegreen.png)

---

## ⚡ Service at a Glance

| Service | কী | মূল পয়েন্ট |
|---|---|---|
| **CodePipeline** | Pipeline orchestrator | Source → Build → Test → Deploy stages |
| **CodeBuild** | Build/test runner | `buildspec.yml` দিয়ে phases নির্ধারণ |
| **CodeDeploy** | Deployment automation | EC2/on-prem/ECS/Lambda-তে deploy |
| **Blue-Green Deployment** | Zero-downtime deploy | নতুন version আলাদা এনভায়রনমেন্টে, তারপর traffic শিফট |
| **Cross-account pipeline** | Multi-account CI/CD | KMS + IAM role দিয়ে cross-account access |

---

## ⚠️ Top Gotchas

1. **`buildspec.yml`-এ phase order ভুল হলে** (install → pre_build → build → post_build) build fail করতে পারে।
2. **Blue-green deployment-এ database migration backward-compatible না হলে** old version broken হয়ে যায় (rollback window-এ)।
3. **Cross-account pipeline-এ artifact bucket-এর KMS key policy ভুল থাকলে** অন্য account থেকে read/write fail করে।
4. **Manual approval stage ভুলে গেলে** pipeline pending অবস্থায় আটকে থাকে, কেউ খেয়াল না করলে deploy কখনো হয় না।
5. **CodeBuild-এ environment variable-এ secret plaintext রাখা উচিত না** — Secrets Manager/Parameter Store reference ব্যবহার করুন।

---

## 🔢 মনে রাখার সংখ্যা

- CodeBuild default timeout: **৬০ মিনিট** (বাড়ানো যায় ৮ ঘণ্টা পর্যন্ত)
- CodePipeline stage: **Source → Build → Test → Deploy** (custom stage যোগ করা যায়)
- Blue-green: ২টা identical environment, traffic shift **all-at-once বা linear/canary**

---

**⏮ পূর্ববর্তী:** [Module 10 Cheat Sheet](./10-Module-10-Containers-Cheat-Sheet.md) | **⏭ পরবর্তী:** [Module 12 Cheat Sheet](./12-Module-12-Cost-Optimization-Cheat-Sheet.md)
