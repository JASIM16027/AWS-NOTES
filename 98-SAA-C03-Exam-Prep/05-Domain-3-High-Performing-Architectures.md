# 🚀 Domain 3: Design High-Performing Architectures (24%)

> প্রশ্ন ইংরেজিতে, ব্যাখ্যা বাংলায়। প্রথমে নিজে উত্তর ভাবুন, তারপর **▶ উত্তর দেখুন**-এ click করুন।

**এই domain-এর topic:** সঠিক compute/storage/database বাছাই, caching (ElastiCache, DAX, CloudFront), EBS volume type, Global Accelerator, Kinesis streaming, placement group, S3 performance।

---

### Q1. Shared file system for Linux instances
Hundreds of Linux EC2 instances across multiple AZs need concurrent read/write access to the same file system with POSIX permissions. What should be used?

- A. Amazon EBS Multi-Attach
- B. Instance store
- C. Amazon S3
- D. Amazon EFS

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**EFS** = NFS, multi-AZ, হাজারো instance একসাথে mount করতে পারে, POSIX permission support করে।
- ❌ A: EBS Multi-Attach শুধু io1/io2 volume-এ, একই AZ-এ, সর্বোচ্চ ১৬টা instance-এ কাজ করে।
- ❌ C: S3 হলো object storage, POSIX file system নয়।
</details>

---

### Q2. Reduce database read latency
An application running on DynamoDB has read-heavy traffic and needs microsecond read latency without changing much application code. What should be added?

- A. ElastiCache for Memcached
- B. DynamoDB Accelerator (DAX)
- C. DynamoDB Streams
- D. Read replicas

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**DAX** DynamoDB-র নিজস্ব in-memory cache, **microsecond** latency দেয়। DynamoDB API-র সাথে compatible, তাই code প্রায় বদলাতে হয় না।
- ❌ A: ElastiCache-এর জন্য app-এ caching logic নিজে লিখতে হয়।
- ❌ D: DynamoDB-তে read replica বলে কিছু নেই।
</details>

---

### Q3. Global static content latency
Users worldwide experience slow load times for images and videos stored in an S3 bucket in `us-east-1`. What is the MOST effective solution?

- A. Serve the content through Amazon CloudFront.
- B. Enable S3 Transfer Acceleration.
- C. Replicate the bucket to every Region.
- D. Use a larger S3 storage class.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**CloudFront** content user-এর কাছের edge location-এ cache করে রাখে, তাই download দ্রুত হয়।
- ❌ B: Transfer Acceleration মূলত **upload** দ্রুত করার জন্য।
- ❌ C: সব region-এ copy রাখা দামি আর জটিল।
</details>

---

### Q4. Non-HTTP global gaming traffic
A multiplayer game uses UDP and has servers in several Regions. Players need consistent low latency and static IP addresses. What should be used?

- A. Amazon CloudFront
- B. Route 53 latency routing only
- C. AWS Global Accelerator
- D. Application Load Balancer

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Global Accelerator**: TCP/UDP support করে, **২টা static anycast IP** দেয়, আর traffic AWS backbone দিয়ে কাছের healthy region-এ পাঠায়।
- ❌ A: CloudFront HTTP-কেন্দ্রিক আর static IP দেয় না।
- ❌ D: ALB শুধু HTTP/HTTPS বোঝে, UDP না।
</details>

---

### Q5. High-IOPS database volume
A self-managed Oracle database on EC2 requires 100,000 IOPS with sub-millisecond latency. Which EBS volume type should be used?

- A. gp3
- B. sc1
- C. st1
- D. io2 Block Express

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**io2 Block Express** সর্বোচ্চ ২,৫৬,০০০ IOPS আর sub-ms latency দেয়।
- ❌ A: gp3 সর্বোচ্চ ১৬,০০০ IOPS।
- ❌ B, C: এগুলো HDD, throughput-এর জন্য, IOPS-এর জন্য না।
</details>

---

### Q6. Big data sequential throughput
A log processing application reads large files sequentially and needs high throughput at low cost. Data is on EBS. Which volume type is MOST cost-effective?

- A. io2
- B. st1
- C. gp3
- D. sc1

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**st1** (Throughput Optimized HDD) বড় sequential read/write-এর জন্য বানানো, আর দামও কম।
- ❌ D: sc1 আরও সস্তা, কিন্তু কম access হওয়া "cold" data-র জন্য (throughput কম)। "High throughput" চাইলে st1।
</details>

---

### Q7. Real-time clickstream processing
A company needs to ingest millions of clickstream events per second, process them in real time with multiple consumer applications, and replay data from the last 24 hours if needed. What should be used?

- A. Amazon Kinesis Data Streams
- B. Amazon SQS Standard
- C. Amazon SNS
- D. Amazon S3 event notifications

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**Kinesis Data Streams**: real-time, একাধিক consumer একই data পড়তে পারে, data retention (default ২৪ ঘণ্টা, ৩৬৫ দিন পর্যন্ত বাড়ানো যায়) থাকায় **replay** করা যায়।
- ❌ B: SQS-এ একটা message একজন consumer process করার পর মুছে যায়, replay করা যায় না।
- ❌ C: SNS data store করে না।
</details>

---

### Q8. Load streaming data into S3 with no code
IoT devices send data that must be delivered to Amazon S3 in near real time, optionally converted to Parquet, with no servers or custom consumer code. What should be used?

- A. Kinesis Data Streams with a custom EC2 consumer
- B. Amazon SQS
- C. Amazon Data Firehose
- D. AWS Glue batch jobs

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Firehose** fully managed: কোনো code ছাড়াই data S3/Redshift/OpenSearch-এ পৌঁছে দেয়, আর Parquet-এ convert করতে পারে। একে "near real time" বলা হয় কারণ data buffer করে (seconds–minutes) তারপর পাঠায়।
</details>

---

### Q9. HPC low-latency networking
A tightly coupled HPC application requires the lowest possible network latency and highest throughput between EC2 instances. What should be used?

- A. Spread placement group
- B. Instances in multiple AZs
- C. Partition placement group
- D. Cluster placement group

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**Cluster placement group** সব instance একই AZ-এ কাছাকাছি hardware-এ রাখে, তাই latency সবচেয়ে কম। (সাথে **EFA** ব্যবহার করলে আরও ভালো।)
- ❌ A: Spread উল্টো কাজ করে, instance-গুলো ইচ্ছা করে দূরে দূরে রাখে (isolation-এর জন্য)।
</details>

---

### Q10. Offload reads from RDS
An RDS PostgreSQL database is overloaded by reporting queries during business hours, slowing the main application. What is the simplest solution with minimal code changes?

- A. Migrate to DynamoDB.
- B. Create a read replica and point reporting queries to it.
- C. Enable Multi-AZ and send reports to the standby.
- D. Increase backup retention.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

Reporting query **read replica**-তে পাঠালে primary DB-র উপর চাপ কমে যায়। Code-এ শুধু একটা connection string বদলাতে হয়।
- ❌ A: পুরো DB migrate করা অনেক বড় কাজ।
- ❌ C: Classic Multi-AZ standby-তে read করা যায় না।
</details>

---

### Q11. Serverless SQL on S3 data
Analysts want to run ad-hoc SQL queries on CSV and Parquet files in S3 without provisioning servers, paying only per query. What should be used?

- A. Amazon Athena
- B. Amazon Redshift provisioned cluster
- C. Amazon RDS
- D. Amazon EMR

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**Athena**: serverless, S3-এর file-এ সরাসরি SQL চালায়, আর যতটুকু data scan হয় সেই অনুযায়ী টাকা দিতে হয়।
- ❌ B: Redshift provisioned cluster চালু রাখতে হয় আর manage করতে হয়।
- ❌ D: EMR-এ cluster setup ও manage করতে হয়।
</details>

---

### Q12. Large file uploads to S3
Users upload 5 GB video files to S3 and uploads often fail on unreliable networks. What should the application use to improve reliability and speed?

- A. Single PUT operations
- B. S3 Select
- C. S3 multipart upload
- D. S3 Glacier

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Multipart upload** বড় file-কে ছোট ছোট অংশে ভাগ করে parallel-এ পাঠায়। কোনো অংশ ব্যর্থ হলে শুধু সেই অংশটা আবার পাঠাতে হয়। (১০০ MB-এর বেশি হলে recommended; single PUT-এর সীমা ৫ GB।) দূরের user হলে সাথে **Transfer Acceleration** দিন।
</details>

---

### Q13. High-performance ML training storage
An ML training job on hundreds of EC2 instances needs a high-performance parallel file system that can lazily load training data from S3. What should be used?

- A. Amazon EFS
- B. EBS gp3
- C. Amazon FSx for Windows File Server
- D. Amazon FSx for Lustre linked to the S3 bucket

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**FSx for Lustre**: HPC/ML-এর জন্য বানানো, sub-ms latency আর বিশাল throughput দেয়। **S3 bucket-এর সাথে link** করা যায়।
</details>

---

### Q14. Choose the right load balancer
An application needs to route `/api/*` requests to one set of containers and `/images/*` to another, and support WebSockets. Which load balancer should be used?

- A. Network Load Balancer
- B. Application Load Balancer
- C. Gateway Load Balancer
- D. Classic Load Balancer

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**Path-based routing** Layer 7-এর feature, তাই **ALB**। ALB WebSocket-ও support করে।
- ❌ A: NLB Layer 4, path দেখতে পারে না।
- ❌ C: GWLB firewall appliance-এর জন্য।
</details>

---

### Q15. Caching database query results
A web application repeatedly runs the same expensive SQL queries on RDS. The team wants sub-millisecond reads and support for complex data structures like sorted sets for a leaderboard. What should be used?

- A. ElastiCache for Redis (or Valkey)
- B. ElastiCache for Memcached
- C. DAX
- D. CloudFront

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**Redis/Valkey**-এ sorted set আছে (leaderboard বানাতে লাগে), সাথে persistence আর replication।
- ❌ B: Memcached শুধু simple key-value রাখে।
- ❌ C: DAX শুধু DynamoDB-র জন্য, RDS-এর জন্য না।
</details>

---

### Q16. Serverless variable SQL workload
A new application has unpredictable, intermittent traffic and needs a MySQL-compatible database that scales capacity automatically with minimal management. What should be used?

- A. RDS MySQL on a large instance
- B. MySQL on EC2
- C. Amazon Aurora Serverless v2
- D. Amazon Redshift

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Aurora Serverless v2** load অনুযায়ী নিজে থেকে capacity (ACU) বাড়ায় আর কমায়, MySQL/PostgreSQL compatible।
- ❌ A: বড় instance সারাক্ষণ চালু থাকে, idle থাকলেও টাকা লাগে।
- ❌ B: EC2-তে নিজে DB চালালে সব manage নিজেকেই করতে হয়।
</details>

---

## 📌 Domain 3 Quick Revision

- Shared Linux file → **EFS** | Windows → **FSx Windows** | HPC/ML → **FSx Lustre**
- IOPS → **io2** | সস্তা general-purpose → **gp3** | Sequential throughput → **st1** | Cold → **sc1**
- DynamoDB cache → **DAX** | RDS/app cache → **ElastiCache Redis**
- Static content global → **CloudFront** | TCP/UDP + static IP → **Global Accelerator**
- Real-time stream + replay → **Kinesis Data Streams** | Stream → S3 (code ছাড়া) → **Firehose**
- S3-এর data-তে SQL → **Athena** | Data warehouse → **Redshift**
- HPC → **Cluster placement group**
- Path/host routing → **ALB** | Extreme performance, TCP/UDP → **NLB**
