# 🛡 Domain 2: Design Resilient Architectures (26%)

> প্রশ্ন ইংরেজিতে, ব্যাখ্যা বাংলায়। প্রথমে নিজে উত্তর ভাবুন, তারপর **▶ উত্তর দেখুন**-এ click করুন।

**এই domain-এর topic:** Multi-AZ, Auto Scaling, ELB, SQS/SNS decoupling, stateless design, RDS/Aurora HA, Route 53 failover, DR strategy (Backup & Restore → Multi-site), backup।

---

### Q1. Web tier high availability
A web application runs on a single EC2 instance. The company needs the application to be highly available and to scale automatically with traffic. What should the solutions architect do?

- A. Use a larger instance type.
- B. Create an Auto Scaling group across multiple Availability Zones behind an Application Load Balancer.
- C. Create an Auto Scaling group in a single AZ with a minimum of 4 instances.
- D. Take hourly EBS snapshots.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

HA আর auto scaling দুটোই পেতে **ALB + multi-AZ ASG** লাগবে।
- ❌ A: বড় instance-এও একটাই machine থাকে, তাই single point of failure থেকে যায়।
- ❌ C: পুরো AZ down হলে সব instance একসাথে বন্ধ হয়ে যাবে।
- ❌ D: Snapshot হলো backup, এটা HA দেয় না।
</details>

---

### Q2. Decouple order processing
An e-commerce application's order service calls a payment service synchronously. During traffic spikes the payment service is overwhelmed and orders are lost. How can the architecture be made more resilient?

- A. Place an Amazon SQS queue between the order service and the payment service.
- B. Increase the payment service instance size.
- C. Use Amazon SNS to send orders directly to the payment service over HTTP.
- D. Use a Network Load Balancer.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**SQS** মাঝখানে বসালে দুই service আলাদা হয়ে যায় (decouple)। Spike-এর সময় order queue-তে জমা থাকে, হারায় না, আর payment service নিজের গতিতে process করে।
- ❌ B: এটা সাময়িক সমাধান, আরও বড় spike এলে আবার একই সমস্যা হবে।
- ❌ C: SNS push করে, সব retry ব্যর্থ হলে message হারাতে পারে, আর buffer করে না।
- ❌ D: Load balancer load ভাগ করে, কিন্তু buffer করে না।
</details>

---

### Q3. RDS automatic failover
A company runs a production MySQL database on Amazon RDS. The database must remain available if an Availability Zone fails, with automatic failover. What should be configured?

- A. A read replica in another AZ
- B. Daily automated snapshots
- C. RDS Multi-AZ deployment
- D. A read replica in another Region

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Multi-AZ** ভিন্ন AZ-এ একটা standby রাখে (synchronous replication)। Primary fail করলে **automatic failover** হয়, endpoint বদলায় না।
- ❌ A, D: Read replica-কে **হাতে promote** করতে হয়, আর এর মূল কাজ read scaling।
- ❌ B: Snapshot থেকে restore করতে সময় লাগে, এটা automatic failover না।
</details>

---

### Q4. Stateless web tier
Users of a web application are logged out whenever the Auto Scaling group scales in. Sessions are stored in memory on each instance. How should this be fixed?

- A. Enable sticky sessions on the ALB and disable scale-in.
- B. Use a larger instance.
- C. Store sessions on the instance store.
- D. Store session data in Amazon ElastiCache or DynamoDB.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

Session **instance-এর বাইরে** (ElastiCache/DynamoDB) রাখলে app **stateless** হয়। তখন যেকোনো instance বন্ধ হলেও user logout হয় না।
- ❌ A: Sticky session-এ instance terminate হলে session হারিয়ে যায়, আর scale-in বন্ধ রাখলে elasticity-ই থাকে না।
- ❌ C: Instance store ephemeral, instance-এর সাথে সাথে data-ও চলে যায়।
</details>

---

### Q5. DR with low cost and RTO of hours
A company needs a disaster recovery plan for a workload. The RPO is 24 hours and RTO is 12 hours. Cost must be minimized. Which DR strategy is appropriate?

- A. Multi-site active/active
- B. Backup and restore
- C. Pilot light
- D. Warm standby

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

RPO/RTO **ঘণ্টার হিসাবে** আর খরচ সবচেয়ে কম রাখতে হবে, তাই **Backup & Restore** যথেষ্ট।
- ক্রম মনে রাখুন (সস্তা/ধীর থেকে দামি/দ্রুত): **Backup & Restore → Pilot Light → Warm Standby → Multi-site**
- RTO মিনিটের মধ্যে চাইলে → Warm standby; প্রায় শূন্য চাইলে → Multi-site।
</details>

---

### Q6. DR with RTO of minutes
A company requires an RTO of 15 minutes and RPO of 1 minute for its application in another Region. A scaled-down but fully functional copy of the environment can run in the DR Region. Which strategy fits?

- A. Warm standby
- B. Pilot light
- C. Backup and restore
- D. Cold site

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

"**Scaled-down but fully functional copy always running**" হলো **Warm Standby**-র সংজ্ঞা। Failover-এর সময় শুধু scale up করতে হয়।
- ❌ B: Pilot light-এ শুধু core অংশ (DB replica) চালু থাকে, app server বন্ধ থাকে।
</details>

---

### Q7. Route 53 failover
A company runs its primary application in `us-east-1` and a standby static maintenance page in S3 in `us-west-2`. Traffic should automatically go to the standby if the primary becomes unhealthy. What should be configured?

- A. Route 53 weighted routing
- B. Route 53 geolocation routing
- C. Route 53 failover routing with health checks
- D. CloudFront with two origins and no health checks

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

Primary থেকে secondary-তে automatic সরে যাওয়া মানে **Failover routing + health check**।
- ❌ A: Weighted routing traffic ভাগ করে, failover-এর জন্য নয়।
- ❌ B: Geolocation routing location দেখে পাঠায়।
- (CloudFront **origin group**-ও failover করতে পারে, কিন্তু D-তে "no health checks" বলা আছে।)
</details>

---

### Q8. Lambda processing failures
A Lambda function processes messages from an SQS queue. Some malformed messages fail repeatedly and block processing. What should be done?

- A. Increase the Lambda timeout.
- B. Switch to SNS.
- C. Delete the queue and recreate it.
- D. Configure a dead-letter queue (DLQ) with a `maxReceiveCount` redrive policy on the source queue.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**Redrive policy + DLQ** থাকলে কোনো message `maxReceiveCount` বারের বেশি fail করলে DLQ-তে সরে যায়। বাকি message আটকে থাকে না, আর পরে DLQ দেখে কী ভুল হয়েছে খুঁজে বের করা যায়।
</details>

---

### Q9. Aurora read and failover
An application on Aurora MySQL needs fast failover (under 30 seconds) and scalable reads. What should be configured?

- A. RDS MySQL with Multi-AZ
- B. Aurora Replicas in multiple AZs and use the reader endpoint for reads
- C. A single Aurora instance with backups
- D. DynamoDB Global Tables

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**Aurora Replica** একসাথে failover target আর read scaling দুটো কাজই করে। Reader endpoint নিজে থেকেই replica-গুলোর মধ্যে load ভাগ করে।
- ❌ A: Classic Multi-AZ-এর standby-তে read করা যায় না, আর failover-এ ১–২ মিনিট লাগে।
</details>

---

### Q10. Protect S3 data from accidental deletion
Users sometimes accidentally delete or overwrite important objects in S3. The company needs to be able to recover previous versions. What should be enabled?

- A. S3 Versioning (optionally with MFA Delete)
- B. S3 Transfer Acceleration
- C. S3 Intelligent-Tiering
- D. S3 server access logging

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**Versioning** চালু থাকলে overwrite-এ নতুন version তৈরি হয়, আর delete-এ শুধু delete marker বসে। তাই আগের version ফেরত আনা যায়। **MFA Delete** দিলে permanent delete করতে MFA লাগে।
</details>

---

### Q11. Multi-Region S3 durability
Compliance requires that all objects in an S3 bucket have a copy stored in another AWS Region automatically. What should be used?

- A. S3 Same-Region Replication
- B. S3 lifecycle policy
- C. S3 Cross-Region Replication
- D. AWS Backup in the same Region

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

অন্য region-এ automatic copy রাখে **CRR**। (দুই bucket-এই versioning চালু থাকতে হবে।)
- ❌ A: SRR একই region-এর মধ্যে copy করে।
- ❌ B: Lifecycle policy শুধু storage class বদলায় বা object মুছে দেয়।
</details>

---

### Q12. Unpredictable workload with EC2 health
An Auto Scaling group uses EC2 status checks only. Instances sometimes keep running while the application process has crashed, and the ALB continues to send traffic. What should be changed?

- A. Increase the ASG maximum capacity.
- B. Disable the health check grace period.
- C. Use a Network Load Balancer.
- D. Configure the ASG to use ELB health checks.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

EC2 status check শুধু দেখে machine ঠিক আছে কিনা, app চলছে কিনা দেখে না। **ELB health check** app-এর health endpoint check করে, আর app ব্যর্থ হলে ASG instance-টা replace করে দেয়।
</details>

---

### Q13. Global database with DR
A global application needs a relational database with fast local reads in multiple Regions and the ability to promote another Region in under a minute during a regional outage. What should be used?

- A. RDS cross-Region read replicas
- B. Amazon Aurora Global Database
- C. DynamoDB Global Tables
- D. RDS Multi-AZ

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**Aurora Global Database**: relational, region-গুলোর মধ্যে replication lag সাধারণত <1 সেকেন্ড, secondary region-এ local read, আর দ্রুত failover।
- ❌ C: DynamoDB NoSQL, কিন্তু প্রশ্নে relational চাওয়া হয়েছে।
- ❌ D: Multi-AZ একটাই region-এর ভেতরে।
</details>

---

### Q14. Handle a sudden predictable spike
Traffic to an application increases sharply every weekday at 9:00 AM. Instances take 10 minutes to boot and warm up, so users see errors at the start of the spike. What should be done?

- A. Use scheduled scaling to increase capacity before 9:00 AM (or predictive scaling).
- B. Use target tracking scaling only.
- C. Use a larger instance type.
- D. Use Spot Instances.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

Spike **কখন আসবে জানা** আছে, আর instance চালু হতে সময় লাগে। তাই **scheduled scaling** (বা predictive scaling) দিয়ে আগে থেকেই capacity বাড়িয়ে রাখুন।
- ❌ B: Target tracking spike শুরু হওয়ার **পরে** scale করে, ততক্ষণে দেরি হয়ে যায়।
</details>

---

### Q15. Centralized backups
A company must back up EBS volumes, RDS databases, DynamoDB tables, and EFS file systems across multiple accounts with a central policy and cross-Region copies. What is the LEAST operational overhead solution?

- A. Custom Lambda scripts for each service
- B. Manual snapshots each week
- C. AWS Backup with backup plans and AWS Organizations backup policies
- D. S3 lifecycle policies

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**AWS Backup** সব service-এর backup এক জায়গা থেকে চালায়। Organization policy আর cross-region/cross-account copy-ও করতে পারে।
</details>

---

## 📌 Domain 2 Quick Revision

- HA = **Multi-AZ**; DR (region down হলে) = **Multi-Region**
- RDS **Multi-AZ** = HA (sync, auto failover) | **Read Replica** = read scale (async, manual promote)
- Decouple = **SQS**; fan-out = **SNS → SQS**; ব্যর্থ message = **DLQ**
- App **stateless** রাখতে: session → **ElastiCache/DynamoDB**, file → **S3/EFS**
- ASG-তে app-এর health দেখতে **ELB health check** চালু করুন
- DR ক্রম: **Backup & Restore → Pilot Light → Warm Standby → Multi-site**
- Route 53 **Failover** + health check = automatic DR switch
