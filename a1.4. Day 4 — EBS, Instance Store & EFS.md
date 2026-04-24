
# 📚 Day 4 — EBS, Instance Store & EFS

**সময়:** ১.৫ ঘণ্টা | **Module:** ১ (EC2 & Storage Fundamentals)

## 🎯 আজকের লক্ষ্য
- Storage-এর ৩ ধরনের পার্থক্য বুঝবেন: Block vs File vs Object
- EBS-এর পুরো concept ও volume types (gp2, gp3, io1, io2, st1, sc1)
- Instance Store কী ও কখন ব্যবহার
- EFS কী ও কেন দরকার
- Snapshot ও Backup strategy
- Encryption ও performance consideration

---

## Part 1: Storage-এর ৩ ধরন — ভিত্তি বুঝুন

AWS-এর storage শেখার আগে computer storage-এর ৩ ধরনের architecture বুঝতে হবে।

### 📦 Block Storage

**কী:** Storage-কে ছোট ছোট "block"-এ ভাগ করা হয়। OS সেই block-গুলো নিজে manage করে।

**Analogy:** একটা বিশাল warehouse-এ ছোট ছোট locker। আপনি (OS) নিজে ঠিক করেন কোন locker-এ কী রাখবেন।

**বৈশিষ্ট্য:**
- Low-level access (OS-এর নিজস্ব file system)
- দ্রুত (random read/write)
- একটা block একসাথে শুধু এক server-এ attach হতে পারে
- Database, OS install-এর জন্য perfect

**উদাহরণ:** আপনার laptop-এর hard drive, SSD, AWS-এর EBS।

### 📂 File Storage

**কী:** Folder-file structure-এ organize। Network-এর মাধ্যমে multiple computer share করতে পারে।

**Analogy:** Shared office folder। সবাই একই folder-এ access পায়, file দেখতে/edit করতে পারে।

**বৈশিষ্ট্য:**
- Hierarchical (folder → subfolder → file)
- Multiple server একসাথে access করতে পারে
- NFS / SMB protocol use করে
- File permission, locking সাপোর্ট

**উদাহরণ:** Google Drive-এ shared folder, AWS-এর EFS, FSx।

### 🗄️ Object Storage

**কী:** Data "object" হিসেবে store — flat structure, no folder hierarchy (শুধু দেখতে folder-এর মতো)। প্রতিটা object-এর একটা unique key থাকে।

**Analogy:** Parcel delivery company। প্রতিটা parcel-এর একটা tracking number। Warehouse-এ কোথায় আছে সেটা matter করে না, tracking number দিয়ে পাওয়া যায়।

**বৈশিষ্ট্য:**
- HTTP API দিয়ে access (REST)
- Metadata attach করা যায়
- Unlimited scale
- Random edit করা যায় না — whole object overwrite
- Slow individual access, কিন্তু parallel-এ ভালো

**উদাহরণ:** AWS S3, Dropbox-এর backend।

---

### তুলনামূলক চিত্র

| Feature | Block (EBS) | File (EFS) | Object (S3) |
|---|---|---|---|
| **Access** | Low-level blocks | Folders/files | HTTP API |
| **Protocol** | iSCSI (behind the scenes) | NFS | HTTPS/REST |
| **Multi-server access** | না | হ্যাঁ | হ্যাঁ |
| **Performance** | Fastest | Medium | Slower per-request |
| **Use case** | OS, DB | Shared files | Backup, web assets |
| **Typical size** | GB-TB | TB-PB | Unlimited |
| **Price** | মাঝারি | বেশি | সবচেয়ে সস্তা |

---

## Part 2: EBS (Elastic Block Store) — Main Focus

### 🤔 EBS কী?

**EBS = AWS-এর network-attached block storage।**

সহজ কথায়: EC2 instance-এর **hard drive**, কিন্তু physically আলাদা server-এ থাকে, network দিয়ে connect করা।

### 📐 EBS-এর Architecture

```
EC2 Instance (compute)
        │
        │ (network connection over AWS backbone)
        │
    EBS Volume (storage, in another server)
```

**গুরুত্বপূর্ণ:** EBS volume EC2-র সাথে **physically attached না**। এটা একটা আলাদা storage system যেটা network দিয়ে connect করা। তাই:

- Instance terminate হলেও EBS volume থাকতে পারে (যদি "Delete on Termination" off থাকে)
- একটা EBS volume detach করে অন্য instance-এ attach করা যায় (একই AZ-এ)
- Instance fail করলে data safe

### 🏢 EBS-এর key properties

**১. AZ-bound**
- EBS volume একটা নির্দিষ্ট AZ-এ তৈরি হয়
- Same AZ-এর EC2 থেকে attach করা যায়
- অন্য AZ-এ নিতে হলে snapshot নিয়ে copy করতে হবে

**২. Instance-এ attach**
- একসময়ে একটা volume শুধু একটা instance-এ attach হতে পারে (সাধারণত)
- **Exception:** Multi-Attach enabled io1/io2 volume একাধিক instance-এ attach হতে পারে (সীমিত use case)

**৩. Persistent**
- EC2 stop/start করলেও data থাকে
- EC2 terminate করলে volume-এর কী হবে সেটা setting-এ ঠিক করা যায়

**৪. Resizable**
- Online-এ volume size বাড়ানো যায় (shrink করা যায় না)
- IOPS ও throughput modify করা যায়

**৫. Automatic replication**
- প্রতিটা EBS volume একই AZ-এর মধ্যে auto-replicate হয়
- Single disk failure-এ data loss হয় না

---

### 🎨 EBS Volume Types — ৬টা choice

AWS ৬ ধরনের EBS volume দেয়। দুই বড় ভাগে:

**SSD-based** (fast, expensive)
- gp2, gp3 (General Purpose)
- io1, io2 (Provisioned IOPS)

**HDD-based** (slow, cheap)
- st1 (Throughput Optimized)
- sc1 (Cold HDD)

---

### ⚡ Performance Metrics — আগে বুঝুন

EBS-এ ৩টা performance metric আছে:

**১. IOPS (Input/Output Operations Per Second)**
- এক সেকেন্ডে কতগুলো read/write operation হতে পারে
- **Random, small** operation-এর জন্য important
- Database-এর জন্য critical (প্রতি query = multiple IOPS)

**২. Throughput (MB/s)**
- এক সেকেন্ডে কত MB data transfer হতে পারে
- **Sequential, large** operation-এর জন্য important
- Video streaming, backup-এর জন্য matter করে

**৩. Latency**
- একটা operation complete হতে কত সময় লাগে
- Milliseconds-এ measured
- কম = ভালো

**Analogy:**
- **IOPS** = এক ঘণ্টায় কতজন customer cashier handle করতে পারে
- **Throughput** = এক ঘণ্টায় কত kg product বিক্রি হয়
- **Latency** = একজন customer-এর waiting time

---

### 🔵 gp2 — General Purpose SSD (পুরানো generation)

**কী:** Default choice, balanced performance।

**Characteristics:**
- Size: 1 GiB - 16 TiB
- IOPS: **Volume size-এর সাথে linked** (3 IOPS per GB)
- Max IOPS: 16,000
- Max throughput: 250 MB/s
- **Burst capability:** ছোট volume-এ temporary 3,000 IOPS পর্যন্ত burst

**সমস্যা:** IOPS বাড়াতে size বাড়াতে হয়। ছোট kintu fast চাই? Possible না।
- ১০০ GB volume = ৩০০ baseline IOPS
- ১০০০ GB volume = ৩০০০ baseline IOPS

**Pricing:** $0.10/GB/month (Mumbai region, approx)

**কখন ব্যবহার:** Small workload, development environment। এখন gp3 available, তাই gp3 recommend।

---

### 🟢 gp3 — General Purpose SSD (Latest generation) ⭐

**কী:** gp2-র replacement, cheaper + flexible।

**Characteristics:**
- Size: 1 GiB - 16 TiB
- **Baseline IOPS: 3,000** (volume size নির্বিশেষে!)
- **Baseline throughput: 125 MB/s**
- Max IOPS: 16,000 (additional পয়সা দিয়ে)
- Max throughput: 1,000 MB/s

**Key advantage:** Size ও IOPS আলাদা করে configure করা যায়।
- ১০ GB volume? তাও 3,000 IOPS পাবেন (gp2-তে মাত্র ৩০ IOPS)
- বড় size চাই কিন্তু কম IOPS? পয়সা বাঁচাতে পারবেন

**Pricing:**
- ~20% সস্তা gp2 থেকে
- Extra IOPS/throughput দিতে হলে পয়সা

**কখন ব্যবহার:** **Default choice** সব general use case-এ।
- Boot volume
- Small-to-medium database
- Development
- Web server
- Most applications

**Pro tip:** পুরানো gp2 volume থাকলে gp3-তে migrate করুন — একই performance, সস্তা।

---

### 🔴 io1 / io2 — Provisioned IOPS SSD

**কী:** সর্বোচ্চ performance-এর জন্য, mission-critical application।

**Characteristics:**
- Size: 4 GiB - 16 TiB
- IOPS: **50 - 64,000** (up to 1,000 IOPS per GB)
- Max throughput: 1,000 MB/s
- **Latency consistent** (sub-millisecond)
- **Multi-Attach** supported (একাধিক instance-এ attach)

**io1 vs io2:**

| Feature | io1 | io2 |
|---|---|---|
| Max IOPS | 64,000 | 64,000 |
| Durability | 99.8-99.9% | 99.999% (৫টা nine) |
| Price | একই | একই (কিন্তু better durability) |

**io2 Block Express (newer):**
- Up to **256,000 IOPS**
- Up to **4,000 MB/s throughput**
- Sub-millisecond latency
- Largest databases-এর জন্য

**কখন ব্যবহার:**
- Large transactional database (Oracle, SAP, SQL Server)
- SAP HANA
- High-traffic e-commerce database
- Consistent low latency critical applications

**Pricing:** অনেক বেশি — per-IOPS charge আলাদা। সাবধান।

---

### 🟡 st1 — Throughput Optimized HDD

**কী:** Large sequential workload-এর জন্য। Boot volume হিসেবে ব্যবহার করা যায় না।

**Characteristics:**
- Size: 125 GiB - 16 TiB
- Max IOPS: 500 (কম!)
- **Max throughput: 500 MB/s** (high)
- Latency বেশি

**কখন ব্যবহার:**
- **Big data processing** (Hadoop, Spark)
- **Log processing**
- **Data warehouse**
- **Streaming workload**
- যেখানে large sequential read/write দরকার

**কখন ব্যবহার করবেন না:**
- Database (IOPS কম)
- Random access workload
- Boot volume

**Pricing:** SSD-এর তুলনায় অনেক সস্তা (~45% কম)।

---

### ❄️ sc1 — Cold HDD

**কী:** সবচেয়ে সস্তা, rarely accessed data-র জন্য।

**Characteristics:**
- Size: 125 GiB - 16 TiB
- Max IOPS: 250
- Max throughput: 250 MB/s
- সবচেয়ে কম performance

**কখন ব্যবহার:**
- Rarely accessed archived data
- Old backup
- Infrequent access log storage

**কখন ব্যবহার করবেন না:**
- Active workload
- Boot volume

**Pricing:** সবচেয়ে সস্তা — EBS-এর সবচেয়ে cheap option।

---

### 📊 EBS Types — Quick Comparison

| Type | Media | Max Size | Max IOPS | Max MB/s | Boot Volume? | Price | Use Case |
|---|---|---|---|---|---|---|---|
| **gp3** | SSD | 16 TiB | 16,000 | 1,000 | হ্যাঁ | $ | Default, all purpose |
| **gp2** | SSD | 16 TiB | 16,000 | 250 | হ্যাঁ | $ | Legacy, use gp3 instead |
| **io1** | SSD | 16 TiB | 64,000 | 1,000 | হ্যাঁ | $$$ | High-performance DB |
| **io2** | SSD | 16 TiB | 64,000 | 1,000 | হ্যাঁ | $$$ | High-durability DB |
| **io2 Block Express** | SSD | 64 TiB | 256,000 | 4,000 | হ্যাঁ | $$$$ | Largest DBs |
| **st1** | HDD | 16 TiB | 500 | 500 | **না** | $ | Big data, logs |
| **sc1** | HDD | 16 TiB | 250 | 250 | **না** | ¢ | Archive, cold storage |

---

### 📸 EBS Snapshots — Backup System

#### Snapshot কী?

**Snapshot = EBS volume-এর point-in-time backup।**

EBS volume-এর একটা picture নেওয়া হলো একটা সময়ে। সেটা থেকে পরে volume restore করা যায়।

#### কীভাবে কাজ করে (Incremental):

**First snapshot:** পুরো volume copy (যতটুকু data আছে)
- যেমন 100 GB volume-এ 40 GB data → 40 GB snapshot

**Second snapshot:** শুধু **যা পরিবর্তন হয়েছে** (incremental)
- যদি 2 GB change হয় → 2 GB extra storage

এটা AWS-কে efficient রাখে, আপনার cost-ও কম রাখে।

#### Snapshot-এর Properties:

**1. S3-তে stored**
- EBS snapshot actually S3-এ save হয়
- আপনার S3 bucket-এ দেখতে পাবেন না (AWS-এর internal S3)

**2. Region-bound**
- Snapshot যে region-এ তৈরি, সে region-এ থাকে
- অন্য region-এ নিতে হলে **Copy Snapshot**

**3. Cross-AZ available**
- Snapshot থেকে volume restore করলে যেকোনো AZ-এ করা যায়
- এটাই হলো AZ change করার উপায়

**4. AMI-এর ভিত্তি**
- Custom AMI তৈরির সময় snapshot তৈরি হয়
- AMI = Snapshot + metadata

#### Snapshot ব্যবহার:

**Backup তৈরি:**
1. EC2 Dashboard → Volumes
2. Volume select → Actions → Create Snapshot
3. Description দিন
4. Create

**Restore:**
1. Snapshots page → Snapshot select
2. Actions → Create Volume From Snapshot
3. Size, AZ, Type select
4. Create

**Cross-region copy:**
1. Snapshot select → Actions → Copy
2. Destination Region select
3. Data transfer হবে (সময় লাগে, data-transfer charge আছে)

#### Snapshot Lifecycle Manager (DLM)

Manually snapshot নিতে ভুলে যাবেন? DLM automate করে:
- Policy তৈরি করুন: "প্রতিদিন রাত ২টায় snapshot নাও, ৭ দিন রাখো"
- Tag-based targeting
- Cross-region copy automation

**Pricing:** Snapshot storage S3-এ save হয়, তাই S3 pricing। সাধারণত ~$0.05/GB/month।

---

### 🔐 EBS Encryption

#### কেন Encryption দরকার?

**Scenario:**
- আপনার EBS volume-এ sensitive data (credit card, personal info)
- AWS-এর internal physical disk চুরি গেল (extremely rare, কিন্তু possible)
- Encrypted না থাকলে data read করা যাবে

#### EBS Encryption কীভাবে কাজ করে:

- **AES-256** encryption (military-grade)
- **AWS KMS (Key Management Service)** key manage করে
- Data at rest (volume-এ) এবং data in transit (EC2 ↔ EBS) — দুই জায়গায় encrypted
- **Performance impact নেই** — transparent

#### কী কী encrypt হয়:

- Volume-এ stored data
- Snapshot থেকে তৈরি হওয়া volume (inherit করে)
- Boot volume
- EBS-এর মধ্যে data movement

#### Encryption চালু করা:

**Option 1: Volume তৈরির সময়**
- "Encrypt this volume" checkbox enable
- KMS key select (default-aws/ebs or custom key)

**Option 2: Account-level default**
- EC2 Dashboard → Settings → Data Protection & Privacy
- "Always encrypt new EBS volumes" enable
- সব নতুন volume automatic encrypted

**Existing unencrypted volume encrypt করতে:**
1. Snapshot নিন
2. Snapshot-এর encrypted copy তৈরি করুন
3. Encrypted copy থেকে new volume তৈরি করুন
4. Original volume detach, new volume attach

---

## Part 3: Instance Store — Ephemeral Storage

### 🤔 Instance Store কী?

**Instance Store = EC2 host-এ physically attached local disk।**

EBS-এর মতো network storage না — এটা hypervisor-এর নিচে physical server-এর ভেতরে disk।

### 🏃 Characteristics:

**Pros (ভালো দিক):**
- **Extremely fast** (locally attached, no network)
- Millions of IOPS possible
- **Free** (instance cost-এর মধ্যে included)
- সর্বোচ্চ throughput

**Cons (খারাপ দিক):**
- **Ephemeral (অস্থায়ী)** — এটাই মূল সমস্যা
- Instance stop/terminate করলে **data permanently lost**
- Hardware failure-এ data lost
- Manual backup নিজে করতে হবে
- সব instance type-এ available না
- Resize করা যায় না
- Detach/re-attach করা যায় না

### 🎯 কখন ব্যবহার:

**✅ ব্যবহার করুন:**
- **Cache** (Redis, Memcached-এর underlying storage)
- **Temporary data** — processing-এর পর delete হবে
- **Buffer/scratch space**
- **Distributed database** যার নিজস্ব replication আছে (Cassandra, MongoDB)
- **Batch job intermediate data**

**❌ ব্যবহার করবেন না:**
- Primary database
- OS boot volume (সাধারণত)
- Important persistent data
- যেকোনো কিছু যা hardware fail-এ হারাবে

### Instance Store-এর Available Instance Types:

সব instance-এ Instance Store আসে না। সাধারণত যেগুলোতে আসে:
- **i3/i4** — storage-optimized
- **d2/d3** — HDD storage optimized
- **c5d, m5d, r5d** — সেই family-র "d" version (NVMe SSD)
- `t3.micro` — **Instance Store নেই**

### Instance Store vs EBS:

| Feature | Instance Store | EBS |
|---|---|---|
| Location | Host server | Network-attached |
| Persistence | Ephemeral | Persistent |
| Speed | Fastest | Fast |
| Cost | Included in instance | Separate billing |
| Resize | Not possible | Possible (online) |
| Detach | Not possible | Possible |
| Snapshot | No | Yes |
| Available on all instance types? | No | Yes |

---

## Part 4: EFS (Elastic File System)

### 🤔 EFS কী?

**EFS = Managed NFS file system for Linux EC2 instances।**

Multiple EC2 একসাথে একই file system access করতে পারে।

### 🏢 Architecture:

```
       EFS File System
      /       |       \
     /        |        \
  EC2-1    EC2-2    EC2-3
  (AZ-a)   (AZ-b)   (AZ-c)
```

একটা EFS একসাথে ১০০০+ EC2-তে mount করা যায়, সব একই file দেখবে, edit করতে পারবে।

### ⭐ Key Features:

**১. Shared Access**
- Multi-AZ access
- Multiple EC2 simultaneously
- NFS v4.1 protocol

**২. Auto-scaling**
- Size automatically বাড়ে/কমে
- No pre-provisioning
- Petabyte scale possible

**৩. POSIX-compliant**
- Linux file permissions (user, group, chmod)
- File locking support

**৪. Multi-AZ durability**
- Data replicated across multiple AZ
- 11 nines durability

**৫. Linux only**
- Windows supported না (Windows-এর জন্য FSx)

### 🎯 Use Cases:

**✅ Perfect for:**
- **Web server farm** — সব server একই static content serve করবে
- **CMS** (WordPress, Drupal) — upload folder shared
- **Container shared storage**
- **Developer collaboration** — team-এর shared workspace
- **Big data analytics** — multiple node একই data access
- **CI/CD** — build artifact sharing

**❌ Good না for:**
- Database (use EBS instead)
- Windows environment (use FSx)
- Extreme low latency (use EBS)

### 💰 EFS Storage Classes:

**Standard** — frequently accessed
- High performance
- Multi-AZ
- বেশি দামি

**Infrequent Access (IA)** — 30+ days unused
- সস্তা (~85% কম)
- Access-এ extra charge
- Auto-tiering policy থাকলে AWS automatically move করে

**Archive** — rarely accessed (90+ days)
- সবচেয়ে সস্তা
- Access-এ বেশি delay

### EFS Performance Modes:

**General Purpose** (default)
- Low latency
- 7,000 operations/sec max
- Most use case

**Max I/O**
- High throughput, high latency
- Thousands of concurrent clients
- Big data workload

### EFS Throughput Modes:

**Bursting** (default)
- Size-এর সাথে throughput grow করে
- Burst credit system

**Provisioned**
- Fixed throughput buy করুন
- Predictable performance

**Elastic**
- Automatic scaling
- Pay per use

---

## Part 5: Comparison — কোনটা কখন?

### Quick Decision Tree:

```
আমার কি shared access দরকার (multiple EC2)?
│
├── হ্যাঁ → Linux? → EFS
│         Windows? → FSx
│
└── না → Ephemeral OK? (data loss acceptable)
         │
         ├── হ্যাঁ → Instance Store (fast, cheap, temp)
         │
         └── না → EBS
                 │
                 ├── Database, high IOPS? → io2
                 ├── General use? → gp3
                 ├── Big sequential? → st1
                 └── Archive? → sc1
```

### Practical Examples:

**Example 1: WordPress website**
- OS on gp3 EBS
- Database on gp3 EBS (different volume)
- Static media files (images) on EFS (multiple web server access)

**Example 2: High-traffic e-commerce**
- OS on gp3 EBS
- Primary database on io2 EBS (high IOPS)
- Cache on Instance Store (fast, ephemeral OK — Redis persist elsewhere)
- Backup to S3

**Example 3: Big data analytics**
- OS on gp3 EBS
- Data processing on st1 EBS (sequential read)
- Shared dataset on EFS
- Intermediate results on Instance Store

---

## Part 6: Performance Tips ও Best Practices

### EBS Performance Best Practices:

**১. EBS-Optimized instance ব্যবহার করুন**
- কিছু instance "EBS-optimized" — dedicated network bandwidth EBS-এর জন্য
- Modern instance (m5+, c5+, r5+) সব EBS-optimized by default

**২. RAID configuration (advanced)**
- Multiple EBS volume মিলিয়ে higher performance পেতে পারেন
- **RAID 0** — performance boost (কিন্তু durability কমে)
- **RAID 1** — extra durability (performance একই)

**৩. Pre-warming** (less important now)
- পুরানো দিনে snapshot-থেকে তৈরি volume প্রথম access-এ slow ছিল
- এখন "fast snapshot restore" option আছে paid

**৪. Monitoring:**
- CloudWatch metrics দেখুন
- `VolumeReadOps`, `VolumeWriteOps` (IOPS)
- `VolumeReadBytes`, `VolumeWriteBytes` (throughput)
- `VolumeQueueLength` — বেশি হলে IOPS কম পড়ছে

### Cost Optimization Tips:

**১. Right-size করুন**
- অনেকে 500 GB volume নিয়ে 50 GB ব্যবহার করে — waste
- GP3-এ আলাদাভাবে size ও performance set করুন

**২. Old snapshot delete করুন**
- Snapshot storage খরচ হয়
- পুরানো, unused snapshot remove করুন
- DLM দিয়ে auto-retention policy

**৩. gp2 থেকে gp3 migrate করুন**
- 20%+ savings, same performance
- Online migration possible

**৪. st1/sc1 cold data-র জন্য**
- Log, backup, archive — SSD-তে রাখার দরকার নেই

**৫. EBS-backed AMI vs Instance Store-backed**
- Instance Store-backed AMI-র volume cost নেই

---

## 🎯 আজকের মূল Takeaways

1. **৩ ধরনের storage:** Block (EBS), File (EFS), Object (S3)
2. **EBS = Network-attached block storage**, EC2-র hard drive
3. **gp3** = default choice most workload-এর জন্য
4. **io1/io2** = high-performance database
5. **st1/sc1** = big data, archive (HDD, cheap)
6. **Instance Store** = ephemeral, fast, physically attached
7. **EFS** = shared file system, multiple EC2 access
8. **Snapshot** = incremental backup, S3-এ stored, region-bound
9. **Encryption** = free, transparent, AES-256, KMS-managed
10. **EBS = AZ-bound**, snapshot দিয়ে cross-AZ/region move

---

## 📝 Self-check Questions

১. Block, File, Object storage-এর পার্থক্য কী?
২. gp2 আর gp3-এর মূল পার্থক্য কী?
৩. একটা MySQL database-এর জন্য কোন EBS type?
৪. EC2 terminate করলে EBS-এর কী হয়?
৫. Instance Store-এর data কখন হারায়?
৬. Snapshot incremental মানে কী?
৭. একটা EBS volume কি Mumbai AZ-a থেকে AZ-b-তে move করা যায়?
৮. EFS কোন protocol use করে?
৯. Web server farm-এ shared content store করতে কী ব্যবহার করবেন?
১০. io2 Block Express কখন দরকার?
১১. EBS encryption-এ performance loss হয়?
১২. st1 কেন boot volume হতে পারে না?

---

## 💡 Pro Tips

- **Default-এ gp3 নিন** — সব নতুন volume-এ। পুরানো gp2 থাকলে migrate করুন।
- **Snapshot policy set করুন** DLM দিয়ে — প্রতিদিন/সপ্তাহে backup automate।
- **Encryption default-এ enable করুন** account-এ — সব নতুন volume encrypted।
- **Instance Store-কে cache-এর মতো treat করুন** — primary data না।
- **Old snapshot audit করুন quarterly** — hidden cost।
- **EFS-এর access point** use করুন multi-user environment-এ — permission isolation।

---

## 🚨 Real-world Mistakes

**Mistake 1:** MongoDB database on Instance Store — instance terminate, পুরো data gone। Million-dollar loss।

**Mistake 2:** 500 GB gp2 boot volume — শুধু 20 GB use। মাসে $50 extra।

**Mistake 3:** Production-এ encryption না — audit-এ fail, compliance violation।

**Mistake 4:** Snapshot lifecycle policy না — 5 বছরে $10,000+ snapshot storage cost।

---
