# 💰 Domain 4: Design Cost-Optimized Architectures (20%)

> প্রশ্ন ইংরেজিতে, ব্যাখ্যা বাংলায়। প্রথমে নিজে উত্তর ভাবুন, তারপর **▶ উত্তর দেখুন**-এ click করুন।

**এই domain-এর topic:** EC2 pricing model, Savings Plans, Spot, S3 storage class ও lifecycle, data transfer cost, NAT cost, serverless, right-sizing, cost tool (Budgets, Cost Explorer)।

---

### Q1. Steady 24/7 workload
A company runs a fleet of EC2 instances 24/7 for the next 3 years. The instance families may change as the application evolves, and some workloads may move to Fargate. What is the MOST cost-effective purchasing option?

- A. On-Demand Instances
- B. Standard Reserved Instances for the current instance type
- C. Spot Instances
- D. Compute Savings Plan (3-year)

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**Compute Savings Plan** যেকোনো instance family, region, এমনকি **Fargate আর Lambda**-তেও discount দেয়। Family বদলালেও এবং Fargate-এ গেলেও discount থাকে।
- ❌ B: Standard RI নির্দিষ্ট instance family-তে আটকে থাকে।
- ❌ C: Spot যেকোনো সময় interrupt হতে পারে, 24/7 production-এর জন্য নির্ভরযোগ্য না।
</details>

---

### Q2. Fault-tolerant batch jobs
A company runs nightly image rendering jobs that can be interrupted and restarted without issue. The jobs must be as cheap as possible. What should be used?

- A. On-Demand Instances
- B. Spot Instances
- C. Reserved Instances
- D. Dedicated Hosts

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

"**Can be interrupted**" আর "**as cheap as possible**" থাকলে উত্তর **Spot** (৯০% পর্যন্ত ছাড়)।
</details>

---

### Q3. Unknown access pattern
A company stores data in S3 whose access patterns are unpredictable: some objects are read often, others not at all for months. The company wants to minimize cost without operational effort. What storage class should be used?

- A. S3 Intelligent-Tiering
- B. S3 Standard-IA
- C. S3 Standard
- D. S3 Glacier Deep Archive

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

Access pattern **অজানা বা বদলায়** হলে **Intelligent-Tiering**। এটা নিজে থেকেই object-গুলো সঠিক tier-এ সরিয়ে দেয়, retrieval fee নেই।
- ❌ B: IA-তে বেশি বার access হলে retrieval fee-তে খরচ বেড়ে যায়।
</details>

---

### Q4. Log retention lifecycle
Application logs are written to S3. They are accessed frequently for 30 days, rarely for the next 60 days, and must be kept for 7 years for compliance but are almost never read. What is the MOST cost-effective approach?

- A. Keep all logs in S3 Standard.
- B. Store logs in EBS volumes.
- C. Lifecycle policy: Standard → Standard-IA after 30 days → Glacier Deep Archive after 90 days → expire after 7 years.
- D. Move logs to One Zone-IA immediately.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Lifecycle policy** দিয়ে data-র বয়স অনুযায়ী ধাপে ধাপে সস্তা storage class-এ সরানো হয়। ৭ বছর রাখতে হবে কিন্তু প্রায় কখনো পড়া হবে না, তাই **Deep Archive** (সবচেয়ে সস্তা)।
- ❌ B: EBS S3-এর চেয়ে অনেক দামি।
- ❌ D: প্রথম ৩০ দিন ঘন ঘন access হয়, তখন IA-র retrieval fee লাগবে। তাছাড়া compliance data single AZ-এ রাখা ঝুঁকিপূর্ণ।
</details>

---

### Q5. Reduce NAT gateway data charges
EC2 instances in private subnets download large amounts of data from S3 through a NAT gateway, and the NAT data processing bill is high. How can costs be reduced?

- A. Add more NAT gateways.
- B. Use S3 Transfer Acceleration.
- C. Move instances to public subnets.
- D. Create an S3 Gateway VPC endpoint and update route tables.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**Gateway endpoint free**। S3-এর traffic NAT-কে পাশ কাটিয়ে সরাসরি যায়, ফলে NAT-এর per-GB charge আর লাগে না। (প্রশ্নে "NAT cost + S3/DynamoDB" থাকলে প্রায় সবসময় এটাই উত্তর।)
</details>

---

### Q6. Infrequent short tasks
A company runs a script that processes a small file each time one is uploaded to S3 (about 200 times per day, each taking 5 seconds). It currently runs on an always-on EC2 instance. How can cost be minimized?

- A. Use a smaller EC2 instance.
- B. Replace it with an AWS Lambda function triggered by S3 events.
- C. Use Reserved Instances.
- D. Use an Auto Scaling group with a minimum of 1.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

দিনে মাত্র ~১৭ মিনিট কাজ, অথচ EC2 সারাদিন চালু থাকে। **Lambda**-তে শুধু যতটুকু চলে ততটুকুর টাকা লাগে, আর এই পরিমাণ কাজ সম্ভবত free tier-এর মধ্যেই পড়বে।
</details>

---

### Q7. Right-size over-provisioned instances
CloudWatch shows that most EC2 instances average 5% CPU utilization. The company wants recommendations to reduce cost. What should be used?

- A. AWS Compute Optimizer
- B. AWS Shield
- C. Amazon Inspector
- D. AWS X-Ray

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**Compute Optimizer** usage দেখে কোন instance ছোট করা যায় (right-size) তার recommendation দেয়। (Trusted Advisor-ও idle instance দেখায়।)
</details>

---

### Q8. Alert when spend exceeds a limit
A startup wants to receive an email when its forecasted monthly AWS spending exceeds 1,000 USD. What should be used?

- A. AWS Cost Explorer
- B. AWS CloudTrail
- C. AWS Budgets
- D. AWS Config

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Budgets** actual আর **forecasted** দুই ধরনের threshold-এ alert পাঠাতে পারে।
- ❌ A: Cost Explorer খরচ বিশ্লেষণ করে, alert পাঠায় না।
</details>

---

### Q9. Dev/test instances
Development EC2 instances are used only during business hours (8 hours/day, weekdays). What is the MOST cost-effective approach?

- A. Buy 3-year Reserved Instances.
- B. Run them 24/7 on Spot.
- C. Use Dedicated Instances.
- D. Keep On-Demand instances and stop them outside business hours using AWS Instance Scheduler or EventBridge Scheduler.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

সপ্তাহে চলে মাত্র ~৪০ ঘণ্টা, অথচ সপ্তাহে ১৬৮ ঘণ্টা থাকে। বাকি সময় বন্ধ রাখলে ~৭৫% খরচ বাঁচে।
- ❌ A: RI কিনলে ব্যবহার না করলেও পুরো সময়ের টাকা দিতে হয়।
</details>

---

### Q10. Archive retrieval within hours
A company must archive 500 TB of data for 10 years. Retrieval happens once or twice a year, and retrieval within 12 hours is acceptable. What is the LOWEST cost storage?

- A. S3 Standard-IA
- B. S3 Glacier Deep Archive
- C. S3 Glacier Instant Retrieval
- D. EBS sc1

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

বছরে ১-২ বার access, **১২ ঘণ্টায় পেলেই চলবে**, আর **সবচেয়ে সস্তা** চাই, তাই **Deep Archive** (standard retrieval ১২ ঘণ্টার মধ্যে)।
- ❌ C: Glacier Instant Retrieval মিলিসেকেন্ডে data দেয়, কিন্তু দামও বেশি। এখানে তার দরকার নেই।
</details>

---

### Q11. Reduce data transfer cost for global users
A company serves large downloadable files from EC2 instances to users worldwide, and data transfer out costs are high. What can reduce cost and improve performance?

- A. Use Amazon CloudFront in front of the origin.
- B. Use larger EC2 instances.
- C. Use a NAT gateway.
- D. Use VPC peering.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**CloudFront**-এর data transfer rate সাধারণত EC2-র সরাসরি internet-এ পাঠানোর চেয়ে কম। Cache hit হলে origin-এ load-ও কমে। আর origin (EC2/S3) থেকে CloudFront-এ data পাঠানো free।
</details>

---

### Q12. Containers without managing servers at lowest cost for fault-tolerant tasks
A company runs stateless, interruption-tolerant containerized batch tasks on ECS and wants the lowest cost without managing EC2 instances. What should be used?

- A. ECS on EC2 On-Demand
- B. EKS on Dedicated Hosts
- C. ECS on Fargate Spot
- D. ECS on Fargate On-Demand

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

Server manage করতে চায় না, তাই **Fargate**। Task interrupt হলে সমস্যা নেই, তাই **Spot**। দুটো মিলিয়ে **Fargate Spot** (৭০% পর্যন্ত ছাড়)।
</details>

---

### Q13. DynamoDB unpredictable traffic
A new application's DynamoDB table has spiky, unpredictable traffic with long idle periods. What capacity mode is MOST cost-effective?

- A. Provisioned capacity with high fixed RCUs/WCUs
- B. DAX
- C. Reserved capacity
- D. On-demand capacity mode

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

Traffic অনিয়মিত আর মাঝে মাঝে কেউ ব্যবহার করে না, তাই **On-demand**: যতটুকু request হয় ততটুকুর টাকা।
- ❌ A: Idle সময়েও fixed capacity-র পুরো টাকা দিতে হয়।
- ❌ C: Reserved capacity steady, predictable traffic-এর জন্য।
</details>

---

### Q14. Cost allocation by team
Finance needs to see AWS costs broken down by department and project. What should the solutions architect recommend?

- A. Create a separate VPC per department.
- B. Apply cost allocation tags (for example, `Department`, `Project`), activate them in Billing, and analyze in Cost Explorer. Use separate accounts per team where possible.
- C. Use CloudTrail.
- D. Use AWS Config.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**Cost allocation tags** activate করলে Cost Explorer/CUR-এ tag অনুযায়ী খরচ ভাগ করে দেখা যায়। আলাদা account রাখলে ভাগ করা আরও সহজ হয় (consolidated billing)।
</details>

---

### Q15. EBS cost reduction
A company uses many gp2 volumes. They want to reduce cost while keeping the same or better performance, without downtime. What should they do?

- A. Modify the volumes to gp3 using Elastic Volumes.
- B. Migrate to io2.
- C. Change to st1 for boot volumes.
- D. Take snapshots and delete the volumes.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**gp3** প্রতি GB-তে gp2-র চেয়ে ~২০% সস্তা, আর baseline 3,000 IOPS free দেয়। **Elastic Volumes** দিয়ে volume চালু অবস্থাতেই (downtime ছাড়া) বদলানো যায়।
- ❌ C: st1 boot volume হতে পারে না।
</details>

---

## 📌 Domain 4 Quick Revision

- 24/7 steady → **Savings Plans / RI** (Compute SP সবচেয়ে flexible)
- Interrupt হলেও চলবে → **Spot** (container → **Fargate Spot**)
- অনিয়মিত, ছোট কাজ → **Lambda**; unpredictable DynamoDB → **On-demand**
- S3: অজানা pattern → **Intelligent-Tiering**; পুরনো data → **Lifecycle** → IA → Glacier → Deep Archive
- NAT খরচ + S3/DynamoDB → **Gateway Endpoint (free)**
- Global data transfer → **CloudFront**
- gp2 → **gp3**; অব্যবহৃত EIP/EBS/snapshot মুছে ফেলুন
- Alert → **Budgets**; বিশ্লেষণ → **Cost Explorer**; right-size → **Compute Optimizer**; tag → **cost allocation tags**
