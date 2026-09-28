# 🗂 Module 9 Cheat Sheet — Databases: RDS & DynamoDB

> **এক পাতায় পুরো module।** বিস্তারিত লাগলে Day 54–58-এ যান।

📚 বিস্তারিত নোট: [10-Module-9-Databases-RDS-DynamoDB](../10-Module-9-Databases-RDS-DynamoDB/)

---

## 🖼 Visual Summary

![RDS Multi-AZ vs Read Replica](../images/11-rds-multiaz-vs-replica.png)

![Aurora ও RDS Proxy](../images/59-aurora-rds-proxy.png)

![DynamoDB Partitioning ও Indexes](../images/60-dynamodb-partitioning-indexes.png)

---

## ⚡ Service at a Glance

| Service | কী | মূল পয়েন্ট |
|---|---|---|
| **RDS** | Managed relational DB | MySQL/PostgreSQL/MariaDB/Oracle/SQL Server |
| **Aurora** | AWS-optimized relational DB | ১৫ read replica, ৬ কপি ডেটা, দ্রুত failover |
| **Multi-AZ** | High availability | Standby readable নয় (instance), Multi-AZ **cluster**-এ readable |
| **Read Replica** | Read scaling | Async replication, manual promote to standalone |
| **RDS Proxy** | Connection pooling | Lambda-র মতো burst connection handle করতে |
| **DynamoDB** | Managed NoSQL, key-value | Partition key দিয়ে scale, single-digit ms latency |
| **DAX** | DynamoDB-only cache | Microsecond latency |

---

## 🔀 RDS vs Aurora vs DynamoDB

| | RDS | Aurora | DynamoDB |
|---|---|---|---|
| Model | Relational (SQL) | Relational (SQL), AWS-optimized | Key-value / document (NoSQL) |
| Scale | Vertical + read replica | ১৫ replica, storage auto-scale | Virtually unlimited (partition-based) |
| Use case | সাধারণ SQL app | High-performance SQL app | Massive scale, predictable latency |

---

## ⚠️ Top Gotchas

1. **Multi-AZ (instance) standby-তে read করা যায় না** — শুধু failover-এর জন্য; read scaling লাগলে Read Replica।
2. **Multi-AZ DB Cluster (নতুন feature) দুটো readable standby দেয়** — পুরনো Multi-AZ instance থেকে আলাদা।
3. **DynamoDB hot partition** — poorly designed partition key দিয়ে throttling হতে পারে।
4. **Read Replica async** — সামান্য lag থাকে, strong consistency দরকার হলে primary-তে read করুন।
5. **RDS Proxy ছাড়া Lambda বেশি concurrent connection খুললে DB connection limit শেষ হয়ে যেতে পারে।**

---

## 🔢 মনে রাখার সংখ্যা

- Aurora max read replica: **১৫টা**
- Aurora storage copy: **৬টা (৩ AZ-এ ২টা করে)**
- DynamoDB item max size: **400 KB**
- DynamoDB default read/write: **On-demand বা Provisioned (auto-scaling সহ)**

---

**⏮ পূর্ববর্তী:** [Module 8 Cheat Sheet](./08-Module-8-Network-Security-Cheat-Sheet.md) | **⏭ পরবর্তী:** [Module 10 Cheat Sheet](./10-Module-10-Containers-Cheat-Sheet.md)
