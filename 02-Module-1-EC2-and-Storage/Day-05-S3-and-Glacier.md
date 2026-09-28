

# 📚 Day 5 — S3 & Glacier

**সময়:** ১.৫ ঘণ্টা | **Module:** ১ (EC2 & Storage Fundamentals)

## 🎯 আজকের লক্ষ্য
- S3-এর object storage architecture গভীরে বুঝবেন
- Bucket, Object, Key, Metadata concept পরিষ্কার হবে
- ৮টা Storage Class এবং কোনটা কখন ব্যবহার শিখবেন
- Versioning, Lifecycle Policy, Replication বুঝবেন
- S3 Security (Bucket Policy, ACL, Encryption) জানবেন
- Glacier (archive storage) কীভাবে কাজ করে শিখবেন
- Real-world use case ও cost optimization

---

## Part 1: S3 — ভিত্তি বুঝুন

### 🤔 S3 কী?

**S3 = Simple Storage Service**

AWS-এর flagship object storage service। ২০০৬ সালে AWS প্রথম launch করা service এটাই।

### 📊 S3-এর Scale — Mind-blowing Numbers

- **১০০+ trillion object** store করা
- প্রতি সেকেন্ডে **millions of requests** handle
- **11 nines durability** (99.999999999%) — মানে ১০,০০,০০,০০,০০০ object-এ বছরে ১টা লস হওয়ার সম্ভাবনা
- **99.99% availability** (Standard tier)
- **Virtually unlimited** storage
- Single object size: **0 bytes to 5 TB**

### 🏗️ Object Storage — আবার বুঝুন

Day 4-এ বলেছিলাম, আজ গভীরে দেখি।

**Traditional file system (hierarchical):**
```
/home/user/documents/project/file.txt
```
- Folder → subfolder → file
- Tree structure
- OS নিজে manage করে

**S3 object storage (flat):**
```
bucket-name/documents/project/file.txt
```
- কোনো folder নেই আসলে — পুরোটা একটা **key**
- সবকিছু flat structure-এ bucket-এর ভেতরে
- Folder-এর mockup (prefix) থাকে দেখানোর জন্য
- HTTP API দিয়ে access

---

### 🧩 S3-এর ৪টা Core Concept

#### ১. Bucket

**Bucket = S3-এ একটা container।**

Analogy: একটা hard drive। আপনার বিভিন্ন hard drive-এ বিভিন্ন জিনিস রাখেন।

**Bucket-এর properties:**
- **Globally unique name** — পৃথিবীতে কেউ একই নামে bucket বানাতে পারবে না
- **Region-specific** — একটা specific region-এ তৈরি (যেমন Mumbai)
- **Unlimited objects** রাখা যায়
- **100 bucket per account** default (request করে বাড়ানো যায়)

**Naming rules:**
- 3-63 character
- Lowercase only
- Letters, numbers, hyphens
- IP address-এর মতো format না (`192.168.1.1` pattern invalid)
- `xn--` দিয়ে শুরু হতে পারে না
- AWS-এর reserved prefix avoid করুন

**Good names:** `my-company-backups`, `acme-public-images-2026`
**Bad names:** `My_Bucket`, `192.168.1.1`, `a`, `backup.` (ends with period)

#### ২. Object

**Object = Bucket-এ stored individual data।**

একটা object-এর ৫টা অংশ:

| Component | মানে |
|---|---|
| **Key** | Object-এর unique identifier (full path) |
| **Value** | Actual data (file content) |
| **Version ID** | Versioning enabled থাকলে |
| **Metadata** | Key-value pairs of info |
| **Subresources** | ACL, torrent ইত্যাদি |

#### ৩. Key

**Key = bucket-এর ভেতরে object-এর "address"।**

**উদাহরণ:**
```
Bucket: my-company-files
Key: photos/2024/summer/beach.jpg
```

পুরো S3 URL হবে:
```
https://my-company-files.s3.ap-south-1.amazonaws.com/photos/2024/summer/beach.jpg
```

**গুরুত্বপূর্ণ:** `photos/2024/summer/` — এটা আসলে folder না, **prefix**। S3-এ ঠিকই flat, কিন্তু `/` থাকলে console-এ folder-এর মতো দেখায়।

#### ৪. Metadata

**Metadata = Object সম্পর্কে extra information।**

**System-defined metadata** (AWS automatic):
- Content-Length
- Content-Type (MIME type)
- Last-Modified
- ETag (checksum)

**User-defined metadata** (আপনি add করেন):
- `x-amz-meta-` prefix দিয়ে
- উদাহরণ: `x-amz-meta-author: John`, `x-amz-meta-project: launch`

---

### 📐 S3 Architecture Summary

```
AWS Region (Mumbai)
│
├── Bucket 1: "my-photos"
│   ├── Object: "vacation/paris.jpg"
│   ├── Object: "profile.png"
│   └── Object: "logo.svg"
│
├── Bucket 2: "my-backups"
│   ├── Object: "database-2026-01.sql.gz"
│   └── Object: "database-2026-02.sql.gz"
│
└── Bucket 3: "my-website-assets"
    ├── Object: "index.html"
    └── Object: "style.css"
```

---

## Part 2: S3 Storage Classes — ৮টা option

AWS বিভিন্ন access pattern-এর জন্য আলাদা storage class তৈরি করেছে। দাম ও performance trade-off।

### ⭐ S3 Standard

**Default class, most common।**

**Characteristics:**
- **High performance** (low latency, milliseconds)
- **11 nines durability**
- **99.99% availability**
- **Multi-AZ** replication (3+ AZ)
- কোনো minimum storage duration নেই
- কোনো retrieval fee নেই

**Pricing:** ~$0.025/GB/month (Mumbai)

**কখন:**
- Frequently accessed data
- Website assets
- Active content distribution
- Real-time analytics
- Mobile/gaming application data

---

### 💡 S3 Intelligent-Tiering

**AI-driven automatic tier movement।**

**কীভাবে কাজ করে:**
- Object-এর access pattern monitor করে
- কম access হলে **automatic** cheaper tier-এ move
- বেশি access হলে দ্রুত tier-এ ফেরত
- **৪টা access tier:**
  - Frequent Access
  - Infrequent Access (30 days+ no access)
  - Archive Instant Access (90 days+)
  - Archive Access (90+ days, configurable)
  - Deep Archive Access (180+ days)

**Pricing:**
- Standard-এর কাছাকাছি dam
- Small monthly monitoring fee per object (~$0.0025 per 1,000 objects)
- **No retrieval fee** auto-tiering-এ

**কখন:**
- Unknown or changing access patterns
- Long-lived data যার access কমে যেতে পারে
- You don't want to manage lifecycle manually

---

### 📉 S3 Standard-IA (Infrequent Access)

**কম access হওয়া data-র জন্য, কিন্তু দরকার হলে দ্রুত পেতে চান।**

**Characteristics:**
- Same performance as Standard (low latency)
- **11 nines durability**
- **99.9% availability** (Standard-এর চেয়ে একটু কম)
- Multi-AZ
- **Retrieval fee** আছে (per-GB)
- **Minimum storage duration: 30 days**
- Minimum object size: 128 KB (ছোট object-এ round up হয়)

**Pricing:** Standard-এর ~40% সস্তা, কিন্তু retrieval-এ পয়সা

**কখন:**
- Monthly backup
- Older user data
- Disaster recovery backup
- Old log files যা quarterly review হয়

---

### 🏢 S3 One Zone-IA

**Single AZ-এ stored (multi-AZ না), সস্তা।**

**Characteristics:**
- **Single AZ only** — AZ fail করলে data loss!
- Same 11 nines durability within that AZ
- **99.5% availability**
- ~20% cheaper than Standard-IA
- Minimum 30 days, 128 KB

**⚠️ Warning:** এটা ব্যবহারে খুব সাবধান। AZ destroy হলে data gone।

**কখন:**
- **Re-creatable** data (এমন কিছু যা অন্য জায়গায় আছে বা recreate করা যায়)
- Secondary backup copy
- Easily reproducible data

**কখন না:**
- Primary data
- Irreplaceable content

---

### ❄️ S3 Glacier Instant Retrieval

**Archive, কিন্তু সাথে সাথে access চান।**

**Characteristics:**
- **Millisecond retrieval** (Standard-এর মতো fast)
- **11 nines durability**
- Multi-AZ
- Minimum storage: **90 days**
- Minimum object size: 128 KB
- Cheaper than Standard-IA

**Pricing:** Standard-এর ~60% সস্তা

**কখন:**
- Quarterly accessed data
- Medical images (rarely accessed কিন্তু দরকার পড়লে instant)
- News media archive
- Compliance data

---

### ❄️❄️ S3 Glacier Flexible Retrieval (আগের "Glacier")

**Archive storage, retrieval-এ সময় লাগে।**

**Retrieval options:**
| Speed | Time |
|---|---|
| **Expedited** | 1-5 minutes (ছোট object) |
| **Standard** | 3-5 hours |
| **Bulk** | 5-12 hours (সবচেয়ে সস্তা) |

**Characteristics:**
- **11 nines durability**
- Multi-AZ
- Minimum storage: **90 days**
- Retrieval fee
- ~70% cheaper than Standard

**কখন:**
- Rarely accessed backup (yearly)
- Digital preservation
- Compliance archives
- Tape backup replacement

---

### ❄️❄️❄️ S3 Glacier Deep Archive

**সবচেয়ে সস্তা, retrieval-এ সবচেয়ে সময়।**

**Retrieval:**
- **Standard:** 12 hours
- **Bulk:** 48 hours

**Characteristics:**
- **11 nines durability**
- Multi-AZ
- Minimum storage: **180 days**
- ~95% cheaper than Standard
- $0.00099/GB/month (USD <$1 per TB per month!)

**কখন:**
- 7-10 বছর compliance storage
- Rarely accessed historical records
- Tape backup replacement (long-term)
- Financial records, healthcare records

---

### 🚀 S3 Express One Zone (newest)

**Highest performance, single AZ।**

**Characteristics:**
- **Single-digit millisecond latency** (fastest S3)
- Single AZ
- 10x faster than Standard for requests
- বেশি দামি per GB
- Frequent access use case

**কখন:**
- ML training
- Real-time analytics
- Interactive applications
- যেখানে latency critical

---

### 📊 Storage Classes — Comparison Table

| Class | Min Duration | Retrieval Time | AZs | Use Case |
|---|---|---|---|---|
| **Standard** | None | ms | 3+ | Active data |
| **Intelligent-Tiering** | None | ms | 3+ | Unknown patterns |
| **Standard-IA** | 30 days | ms | 3+ | Monthly access |
| **One Zone-IA** | 30 days | ms | 1 | Secondary backup |
| **Glacier Instant** | 90 days | ms | 3+ | Quarterly access |
| **Glacier Flexible** | 90 days | min-hrs | 3+ | Yearly access |
| **Deep Archive** | 180 days | 12-48 hrs | 3+ | Compliance archive |
| **Express One Zone** | 1 hour | ms | 1 | Low latency |

---

## Part 3: S3 Features — গভীরে

### 🔄 Versioning

**Versioning কী?**

Bucket-এ enable করলে, একই key-এ upload করা প্রতিটা file-এর আলাদা version save থাকে। পুরানো version overwrite হয় না।

**Why version?**
- Accidental delete protection
- Accidental overwrite protection
- History tracking
- Rollback capability

**কীভাবে কাজ করে:**

```
Version enabled:

Upload file.txt v1 → Version ID: abc123
Upload file.txt v2 → Version ID: def456 (v1 still exists)
Upload file.txt v3 → Version ID: ghi789 (v1, v2 still exist)

GET file.txt → Returns latest (v3)
GET file.txt?versionId=abc123 → Returns v1
DELETE file.txt → Adds "delete marker" but versions still exist
```

**Versioning states:**
- **Unversioned** (default) — no version tracking
- **Versioning-enabled** — new versions created
- **Versioning-suspended** — stop creating new versions, existing versions remain

**⚠️ Important:** একবার enable করলে suspend করা যায়, কিন্তু পুরোপুরি disable করা যায় না।

**Cost:** প্রতিটা version আলাদা object হিসেবে count, তাই storage cost বাড়ে। Lifecycle policy দিয়ে old version auto-delete করুন।

---

### 🗑️ Lifecycle Policy — Auto Management

**কী:** Object-এর age-এর ভিত্তিতে automatic action।

**Actions:**
1. **Transition** — storage class change
2. **Expiration** — delete

**Example Policy:**

```
Rule: "backup-lifecycle"
Prefix: "backups/"

Day 0-30:   S3 Standard
Day 30-90:  Move to Standard-IA
Day 90-365: Move to Glacier Flexible
Day 365+:   Move to Deep Archive
Day 2555:   Delete (7 years)
```

**Use cases:**
- Cost optimization — old data সস্তা tier-এ
- Compliance — x years পরে auto-delete
- Version cleanup — old version 30 days পরে delete

**JSON example:**
```json
{
  "Rules": [{
    "Id": "Archive-old-logs",
    "Status": "Enabled",
    "Filter": {"Prefix": "logs/"},
    "Transitions": [
      {"Days": 30, "StorageClass": "STANDARD_IA"},
      {"Days": 90, "StorageClass": "GLACIER"}
    ],
    "Expiration": {"Days": 2555}
  }]
}
```

---

### 🔁 Replication

**কী:** S3 bucket-এর data automatically অন্য bucket-এ copy।

**দুই ধরনের:**

#### Cross-Region Replication (CRR)
- এক region থেকে আরেক region-এ
- Disaster recovery
- Compliance (data in specific region)
- Latency reduction (কাছাকাছি region)

#### Same-Region Replication (SRR)
- একই region-এর মধ্যে দুই bucket
- Log aggregation
- Production/Test sync
- Different account backup

**Requirements:**
- Both bucket-এ **Versioning enabled** থাকতে হবে
- Source bucket-এ proper IAM role
- Destination bucket আগে থেকে তৈরি

**কী replicate হয়:**
- New object (enable করার পর)
- Object metadata
- Tags
- ACL

**কী replicate হয় না (default):**
- Enable করার আগে-এর object (Batch Replication আলাদাভাবে)
- Delete markers (optional)
- Lifecycle actions

---

### 🔐 Encryption

S3-এ ৪ ধরনের encryption at rest:

#### 1. SSE-S3 (Server-Side Encryption with S3-Managed Keys)
- AWS automatic key manage করে
- AES-256
- **Default এখন** সব নতুন bucket-এ
- কোনো extra কাজ নেই
- **Free**

#### 2. SSE-KMS (Server-Side Encryption with KMS)
- AWS KMS (Key Management Service) keys
- আপনি key control করেন
- Audit log (কে access করেছে)
- Per-request KMS charge

#### 3. SSE-C (Server-Side Encryption with Customer-Provided Keys)
- আপনি key provide করেন
- AWS store করে না
- আপনার key হারালে data lost
- Rarely used

#### 4. Client-Side Encryption
- Upload-এর আগে আপনি client-এ encrypt করেন
- AWS-এর কিছু দেখার নেই
- সর্বোচ্চ security

**Transit Encryption:**
- HTTPS/TLS default
- Bucket policy দিয়ে enforce: `aws:SecureTransport: true`

---

### 🛡️ S3 Security — Access Control

S3-এ ৪ layer security:

#### 1. Bucket Policy
**JSON-based policy,** bucket-level।

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-public-bucket/*",
    "Condition": {
      "IpAddress": {"aws:SourceIp": "203.0.113.0/24"}
    }
  }]
}
```

**Use:**
- Public website hosting
- Cross-account access
- IP-based access

#### 2. ACL (Access Control List)
- **Legacy** system (AWS এখন discourage করে)
- Object-level এবং bucket-level
- Read, Write, Full Control
- **Best practice:** ACL disable করুন, Bucket Policy + IAM use করুন

#### 3. IAM Policy
- User/role-এ attach করা permission
- Bucket/object access allow/deny

#### 4. Block Public Access (Account/Bucket level)
- Master switch
- ৪টা option block করতে পারে
- Accidental public exposure prevent
- **Recommended: সব ON রাখুন**, শুধু public bucket-এ off

---

### 🌐 S3 Website Hosting

**Static website** host করা যায় S3-এ:

**Supported:**
- HTML, CSS, JavaScript
- Images, videos
- Client-side code

**Not supported:**
- Server-side code (PHP, Node.js backend)
- Databases

**Setup:**
1. Bucket-এ static website hosting enable
2. Index document: `index.html`
3. Error document: `error.html`
4. Block Public Access disable (selective)
5. Bucket Policy: everyone can `GetObject`
6. Endpoint: `bucket-name.s3-website-region.amazonaws.com`

**With CloudFront:**
- Custom domain (`www.mywebsite.com`)
- HTTPS
- CDN caching
- Faster worldwide

---

### 📡 Event Notifications

S3-এ কিছু হলে notification পাঠাতে পারবেন।

**Triggers:**
- Object created
- Object deleted
- Object restored (from Glacier)
- Replication events

**Destinations:**
- Lambda function
- SNS topic
- SQS queue
- EventBridge

**Use cases:**
- New image upload → Lambda auto-resize
- File upload → SNS notify team
- Video upload → SQS queue for processing

---

### 🚄 Transfer Acceleration

**কী:** CloudFront edge location use করে faster upload।

**কীভাবে কাজ:**
- User Dhaka থেকে Mumbai bucket-এ upload করছে
- Normal: Direct internet routing, slow
- Acceleration: Dhaka edge location → AWS backbone → Mumbai
- 50-500% faster

**Cost:** Extra charge per GB

**কখন:**
- Global user base
- Large file uploads
- High-latency regions

---

### 🔗 Presigned URLs

**কী:** Temporary URL that grants access to a private object।

**Use case:**
- Private object শুধু নির্দিষ্ট user-কে দিতে চান
- URL expire হয় x সময় পরে
- Direct download link email-এ পাঠান

**Example:** `https://bucket.s3.amazonaws.com/file.pdf?X-Amz-Algorithm=...&X-Amz-Expires=3600&X-Amz-Signature=...`

এই URL শুধু ১ ঘণ্টা (3600 seconds) valid।

---

## Part 4: Glacier — Archive Storage

Glacier আসলে **S3-এর storage class**, কিন্তু এর আলাদা characteristic আছে।

### 🧊 Glacier History

- Glacier শুরুতে ছিল S3 থেকে **আলাদা service**
- "Vaults" and "Archives" ছিল terminology
- এখন S3-এ integrate, তিনটা Glacier tier:
  1. **Glacier Instant Retrieval** — ms retrieval
  2. **Glacier Flexible Retrieval** — min-hrs
  3. **Glacier Deep Archive** — 12-48 hrs

### 🎯 Glacier-এর Design Principles

**Trade-off:**
- Cheap storage ↔ slow retrieval
- Long-term retention ↔ not for frequent access

**Where Glacier excels:**
- Regulatory compliance (7-10 years data retention)
- Tape backup replacement
- Media archive (old movies, news footage)
- Medical records long-term
- Legal documents

**Cost example:**
- 1 TB in S3 Standard: ~$23/month
- 1 TB in Deep Archive: ~$1/month
- **96% savings** over a year for rarely accessed data

### 📥 Retrieval Costs

**Free tier benefits যায় না এখানে:**

| Tier | Retrieval Cost | Speed |
|---|---|---|
| Glacier Instant | $0.03/GB retrieved | ms |
| Glacier Flexible (Expedited) | $0.03/GB | 1-5 min |
| Glacier Flexible (Standard) | $0.01/GB | 3-5 hrs |
| Glacier Flexible (Bulk) | $0.0025/GB | 5-12 hrs |
| Deep Archive (Standard) | $0.02/GB | 12 hrs |
| Deep Archive (Bulk) | $0.0025/GB | 48 hrs |

**একটা trap:** ১ TB retrieve করতে $10-30 লাগতে পারে। Archive retrieval চিন্তা-ভাবনা করে।

### 🗝️ Vault Lock (Compliance)

**Glacier Vault Lock** — WORM (Write Once, Read Many) policy।

- একটা policy set করলেন: "এই archive ৭ বছর delete করা যাবে না"
- Lock হয়ে যায় — কেউ আর change করতে পারে না (root user-ও না)
- Financial, legal compliance-এর জন্য

**Use case:** SEC Rule 17a-4(f) compliance (US financial firms)।

---

## Part 5: S3 Real-World Use Cases

### Use Case 1: Web Application Backend

**Setup:**
- User profile images → **S3 Standard**
- Application logs → **Standard-IA after 30 days**
- Old logs (archive) → **Glacier Deep Archive after 90 days**
- Auto-delete after 7 years → **Lifecycle expiration**

**Features used:**
- Versioning for profile pictures (undo delete)
- CloudFront CDN for fast delivery
- Lifecycle policy for cost optimization
- Server-side encryption

### Use Case 2: Data Lake for Analytics

**Setup:**
- Raw data from IoT sensors → **S3 Standard**
- Processed data → **Standard-IA**
- Historical data → **Glacier**
- Query with Athena/Redshift Spectrum

**Features used:**
- Intelligent-Tiering (unknown access pattern)
- Event notifications → Lambda for processing
- Partition structure (prefix-based)

### Use Case 3: Media Streaming Service

**Setup:**
- Popular videos → **S3 Standard** + CloudFront
- Older videos → **Standard-IA**
- Unused content → **One Zone-IA** (recreatable from master)
- Master copies → **Glacier Deep Archive**

**Features used:**
- Transfer Acceleration for upload
- Replication across regions
- Presigned URLs for paid content

### Use Case 4: Backup Solution

**Setup:**
- Daily backups → **S3 Standard** (7 days)
- Weekly backups → **Standard-IA** (4 weeks)
- Monthly backups → **Glacier** (1 year)
- Yearly backups → **Deep Archive** (7 years)

**Features used:**
- Lifecycle policy automation
- Versioning for point-in-time recovery
- Cross-region replication for DR

### Use Case 5: Static Website Hosting

**Setup:**
- HTML/CSS/JS files → **S3 Standard**
- Bucket configured for website hosting
- CloudFront for HTTPS + CDN
- Route 53 for custom domain

**Features used:**
- Static website hosting
- Block Public Access (selective)
- CloudFront distribution
- Cost: usually few dollars/month

---

## Part 6: Pricing Model — বুঝে রাখুন

S3-এ ৪ ধরনের charge:

### 1. Storage
- Per-GB per-month
- Tier-dependent
- Mumbai Standard: ~$0.025/GB/month

### 2. Requests
- PUT, COPY, POST, LIST: ~$0.005 per 1,000
- GET, SELECT: ~$0.0004 per 1,000
- Free tier: 2,000 PUT, 20,000 GET per month

### 3. Data Transfer
- **IN** (upload to S3): **Free**
- **OUT** (download): Tiered pricing
  - First 100 GB/month: Free
  - Next up to 10 TB: ~$0.09/GB
- Within same region: Free
- Cross-region: Charged

### 4. Management Features
- Inventory, analytics, Object Lambda
- Small per-object/per-request charges

**Cost monitoring:**
- Cost Explorer
- S3 Storage Lens (organization-wide)
- Billing alerts

---

## Part 7: Best Practices

### 🔒 Security Best Practices

1. **Block Public Access by default** — account-level enable
2. **Versioning enable** production bucket-এ
3. **Encryption by default** (SSE-S3 minimum)
4. **HTTPS enforce** via bucket policy
5. **CloudTrail logging** — all S3 API calls log
6. **MFA Delete** critical bucket-এ
7. **Use IAM roles** EC2-তে, not access keys
8. **Periodic access review** — who has access

### 💰 Cost Optimization

1. **Lifecycle policy always** — old data সস্তা tier-এ
2. **Intelligent-Tiering** unknown patterns-এর জন্য
3. **Storage Lens** use — insights
4. **Old version cleanup** — versioning expensive
5. **Incomplete multipart upload cleanup** — silent cost
6. **Right storage class** — don't put backup in Standard
7. **Compression** — large file compress করে upload

### ⚡ Performance Best Practices

1. **Prefix distribution** — random prefix for high request rate
2. **Multipart upload** for >100 MB files
3. **Transfer Acceleration** global users
4. **CloudFront** for read-heavy workload
5. **S3 Select** — partial object retrieval (save bandwidth)

---

## 🎯 আজকের মূল Takeaways

1. **S3** = AWS object storage, unlimited, 11 nines durability
2. **Bucket** globally unique, **region-specific**
3. **Key** = object identifier (looks like path)
4. **৮টা storage class** — cost/access trade-off
5. **Standard** = active, **Glacier** = archive
6. **Versioning** = delete/overwrite protection
7. **Lifecycle** = automatic tier movement
8. **Replication** = CRR (cross-region), SRR (same-region)
9. **Encryption default** — SSE-S3 free
10. **Security layers:** Bucket Policy + IAM + Block Public Access

---

## 📝 Self-check Questions

১. S3 bucket name কেন globally unique হতে হয়?
২. Object ও Key-এর পার্থক্য কী?
৩. একটা এরকম বুঝান — folder কি আসলে S3-এ আছে?
৪. Intelligent-Tiering কখন ব্যবহার করবেন?
৫. One Zone-IA-এ risk কী?
৬. Glacier Deep Archive থেকে data আনতে সর্বোচ্চ কত সময়?
৭. Versioning enable করলে কী হয়?
৮. Bucket-এ public access দিতে কী করতে হবে?
৯. Lifecycle policy কী কী action করতে পারে?
১০. Cross-Region Replication-এর prerequisite কী?
১১. Presigned URL কখন use করবেন?
১২. S3 Standard থেকে Glacier Deep Archive-এ cost difference কত %?
১৩. SSE-S3 আর SSE-KMS-এর পার্থক্য কী?
১৪. Static website S3-এ host করতে কী কী configure করতে হবে?
১৫. Transfer Acceleration কীভাবে কাজ করে?

---

## 💡 Pro Tips

- **Block Public Access ALWAYS ON** রাখুন account-level-এ। যতই "public bucket" লাগুক — selective disable।
- **MFA Delete enable করুন** production bucket-এ — accidental delete থেকে বাঁচবেন।
- **Lifecycle policy না থাকলে** S3 bill রাতারাতি বাড়বে।
- **S3 Storage Lens enable** করুন — organization-wide insight।
- **Incomplete multipart upload cleanup** lifecycle-এ add করুন — hidden cost।
- **Cross-account access-এ Bucket Policy** preferred, ACL না।
- **Object Lock** enable immutable বানাতে — compliance need-এ।

---

## 🚨 Real-world Horror Stories

**Story 1:** Capital One breach 2019 — misconfigured S3 bucket (Block Public Access disabled), 100 million customer records leaked। CEO stepped down, $80M fine।

**Story 2:** একটা startup prod S3 bucket accidentally public। Sensitive user data Google-এ index হয়ে গেল। 3 দিনে discover করে ঠিক করে, কিন্তু reputation damage।

**Story 3:** Developer অজান্তে public bucket-এ API key upload করে GitHub-এ push। Bot 5 মিনিটে discover, crypto mining চালিয়ে $15,000 bill।

**Story 4:** Versioning enabled, lifecycle policy নেই। 2 বছরে শুধু old version-এ $20,000/month bill।

**Moral:** S3 security ও cost management critical।

---

## 🎁 Free Tier Reminder

আপনার নতুন AWS account-এ **১২ মাস S3 free tier:**
- 5 GB Standard storage
- 20,000 GET requests
- 2,000 PUT requests
- 15 GB outbound data transfer

শেখার জন্য যথেষ্ট। ছোট bucket বানিয়ে experiment করুন।

---
