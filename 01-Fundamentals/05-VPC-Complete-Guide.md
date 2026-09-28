## VPC — সম্পূর্ণ Technical ব্যাখ্যা

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![VPC Public/Private Subnet](../images/03-vpc-public-private.png)

![Security Group vs NACL](../images/09-sg-vs-nacl.png)


---

### সমস্যাটা আগে বুঝি

AWS এর একটা physical data center এ হাজার হাজার customer এর server একসাথে থাকে। তুমি একটা server কিনলে, সেটা physically ওই shared building এই আছে।

```
AWS Physical Data Center (Singapore)
┌─────────────────────────────────────────────┐
│                                             │
│  Facebook এর server                         │
│  Google এর server                           │
│  তোমার server          ← সব একই জায়গায়!   │
│  অন্য কারো server                           │
│                                             │
└─────────────────────────────────────────────┘
```

সমস্যা হলো — এরা কি একে অপরের data দেখতে পাবে? পাবে না, কারণ VPC।

---

### VPC কী করে?

VPC একটা **logically isolated network** তৈরি করে। Physical hardware shared হলেও network আলাদা।

```
AWS Physical Data Center
┌─────────────────────────────────────────────┐
│                                             │
│  ┌───────────────┐    ┌───────────────┐     │
│  │  তোমার VPC    │    │  অন্যের VPC   │     │
│  │               │    │               │     │
│  │  10.0.0.0/16  │    │  10.0.0.0/16  │     │
│  │               │    │               │     │
│  │  তোমার server │    │  তাদের server │     │
│  └───────────────┘    └───────────────┘     │
│                                             │
│  এরা একে অপরকে দেখতেই পাবে না ✅           │
└─────────────────────────────────────────────┘
```

Same IP range দুই জনের VPC তে থাকতে পারে — কারণ এরা logically আলাদা।

---

### CIDR — IP Range বোঝো

VPC বানানোর সময় একটা IP range দিতে হয়। এটাই CIDR block।

```
VPC CIDR: 10.0.0.0/16

IP address = 32 bits মোট
/16 মানে = প্রথম 16 bits fixed, বাকি 16 bits তোমার

10  .  0  .  0  .  0
│      │    │    │
└──────┘    └────┘
Fixed(16)  Flexible(16)

Flexible part: 0.0 → 255.255
মানে: 10.0.0.0 থেকে 10.0.255.255
Total IP: 2^16 = 65,536 টা
```

**কোন CIDR কতটা বড়:**
```
/16 → 65,536 IPs  (বড় production)
/24 → 256 IPs     (ছোট subnet)
/28 → 16 IPs      (খুব ছোট)

নিয়ম: / এর পরের সংখ্যা বড় = IP কম
```

---

### VPC এর ভেতরে কী থাকে?

```
VPC: 10.0.0.0/16
│
├── Subnet (network ভাগ)
│   ├── Public Subnet  10.0.1.0/24
│   ├── Public Subnet  10.0.2.0/24
│   ├── Private Subnet 10.0.3.0/24
│   └── Private Subnet 10.0.4.0/24
│
├── Route Table (traffic কোথায় যাবে)
│
├── Internet Gateway (বাইরের দরজা)
│
├── NAT Gateway (পেছনের দরজা)
│
└── Security Group (প্রতিটার নিজস্ব firewall)
```

---

### Subnet কেন লাগে?

VPC একটা বড় network। Subnet সেটাকে ছোট ছোট ভাগে ভাগ করে। দুই কারণে:

**কারণ ১ — Security:**
```
Public Subnet:
  Internet থেকে access করা যায়
  এখানে রাখো: Nginx, API Server, Load Balancer

Private Subnet:
  Internet থেকে access করা যায় না
  এখানে রাখো: Database, Cache, Internal services

Database কখনো Public Subnet এ রাখবে না!
```

**কারণ ২ — Availability Zone:**
```
AWS এর প্রতিটা Region এ একাধিক data center আছে।
এগুলোকে বলে Availability Zone (AZ)।

ap-south-1 (Mumbai):
  ├── ap-south-1a (Data center 1)
  ├── ap-south-1b (Data center 2)
  └── ap-south-1c (Data center 3)

একটা AZ তে আগুন লাগলে বা flood হলে?
অন্য AZ তে server চলতে থাকবে।

তাই দুটো AZ তে subnet রাখো:
  Public Subnet  → ap-south-1a
  Public Subnet  → ap-south-1b  ← backup
  Private Subnet → ap-south-1a
  Private Subnet → ap-south-1b  ← backup
```

---

### Route Table — Traffic কোথায় যাবে

প্রতিটা Subnet এর একটা Route Table আছে। এটা দেখে packet কোথায় যাবে সিদ্ধান্ত নেয়।

**Public Subnet এর Route Table:**
```
┌─────────────────┬──────────────┬─────────────────────┐
│ Destination     │ Target       │ মানে                │
├─────────────────┼──────────────┼─────────────────────┤
│ 10.0.0.0/16    │ local        │ VPC এর ভেতরে যাও   │
│ 0.0.0.0/0      │ igw-xxxxxxx  │ বাকি সব IGW দিয়ে   │
└─────────────────┴──────────────┴─────────────────────┘

Packet আসলো → destination কোথায়?
  10.0.x.x → VPC এর ভেতরে → local route
  অন্য যেকোনো IP → 0.0.0.0/0 → IGW দিয়ে বাইরে
```

**Private Subnet এর Route Table:**
```
┌─────────────────┬──────────────┬─────────────────────┐
│ Destination     │ Target       │ মানে                │
├─────────────────┼──────────────┼─────────────────────┤
│ 10.0.0.0/16    │ local        │ VPC এর ভেতরে যাও   │
│ 0.0.0.0/0      │ nat-xxxxxxx  │ বাইরে NAT দিয়ে     │
└─────────────────┴──────────────┴─────────────────────┘

IGW নেই → বাইরে থেকে কেউ আসতে পারবে না
NAT আছে → ভেতর থেকে বাইরে যাওয়া যাবে
```

---

### Default VPC vs Custom VPC

AWS account খুললে automatically একটা **Default VPC** তৈরি হয়।

```
Default VPC:
  CIDR: 172.31.0.0/16
  সব Subnet public
  IGW attached
  সহজে use করা যায়

  সমস্যা:
  ❌ সব কিছু public → Database ও বাইরে থেকে accessible
  ❌ Production এ ব্যবহার করা উচিত না

Custom VPC (তুমি নিজে বানাও):
  ✅ Public + Private Subnet আলাদা
  ✅ Database সম্পূর্ণ isolated
  ✅ Production ready
```

---

### VPC Peering — দুটো VPC কে connect করা

কখনো দুটো আলাদা VPC কে connect করতে হয়। যেমন production VPC আর monitoring VPC।

```
Production VPC        Monitoring VPC
10.0.0.0/16    ←→    10.1.0.0/16
                ↑
          VPC Peering Connection

এখন দুটো VPC একে অপরের সাথে কথা বলতে পারবে।
কিন্তু Internet এর মাধ্যমে না — সরাসরি AWS এর ভেতর দিয়ে।

Important:
  CIDR overlap করা যাবে না!
  10.0.0.0/16 ↔ 10.0.0.0/16 → ❌ conflict
  10.0.0.0/16 ↔ 10.1.0.0/16 → ✅ okay
```

---

### পুরো VPC Architecture একসাথে

```
Internet
    │
    │ HTTPS request
    ▼
Internet Gateway (IGW)
    │
    ▼
┌─────────────────────────────────────────────────┐
│                  VPC 10.0.0.0/16                │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐     │
│  │  Public Subnet   │  │  Public Subnet   │     │
│  │  10.0.1.0/24     │  │  10.0.2.0/24     │     │
│  │  AZ: 1a          │  │  AZ: 1b          │     │
│  │                  │  │                  │     │
│  │  ┌────────────┐  │  │  ┌────────────┐  │     │
│  │  │    ALB     │  │  │  │  NAT GW    │  │     │
│  │  └─────┬──────┘  │  │  └────────────┘  │     │
│  │        │         │  │                  │     │
│  │  ┌─────▼──────┐  │  │  ┌────────────┐  │     │
│  │  │  EC2 API   │  │  │  │  EC2 API   │  │     │
│  │  │  :3000     │  │  │  │  :3000     │  │     │
│  │  └────────────┘  │  │  └────────────┘  │     │
│  └──────────────────┘  └──────────────────┘     │
│            │                    │               │
│            ▼                    ▼               │
│  ┌──────────────────┐  ┌──────────────────┐     │
│  │  Private Subnet  │  │  Private Subnet  │     │
│  │  10.0.3.0/24     │  │  10.0.4.0/24     │     │
│  │  AZ: 1a          │  │  AZ: 1b          │     │
│  │                  │  │                  │     │
│  │  ┌────────────┐  │  │  ┌────────────┐  │     │
│  │  │  RDS       │  │  │  │  RDS       │  │     │
│  │  │  Primary   │  │  │  │  Standby   │  │     │
│  │  └────────────┘  │  │  └────────────┘  │     │
│  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────┘
```

---

### VPC বানানোর Step by Step

```bash
Step 1: VPC তৈরি করো
  Name: my-app-vpc
  CIDR: 10.0.0.0/16

Step 2: Subnet তৈরি করো
  Public-1a:  10.0.1.0/24  (AZ: ap-south-1a)
  Public-1b:  10.0.2.0/24  (AZ: ap-south-1b)
  Private-1a: 10.0.3.0/24  (AZ: ap-south-1a)
  Private-1b: 10.0.4.0/24  (AZ: ap-south-1b)

Step 3: Internet Gateway তৈরি করো
  IGW create → VPC তে attach করো

Step 4: NAT Gateway তৈরি করো
  Public Subnet এ বানাও
  Elastic IP allocate করো

Step 5: Route Table বানাও
  Public RT:
    0.0.0.0/0 → IGW
    Public-1a, Public-1b associate করো

  Private RT:
    0.0.0.0/0 → NAT GW
    Private-1a, Private-1b associate করো

Step 6: Security Group বানাও
  ALB-SG:  inbound 80, 443 → internet
  EC2-SG:  inbound 3000   → ALB-SG only
           inbound 22     → তোমার IP only
  RDS-SG:  inbound 5432   → EC2-SG only
```

---

### মূল কথা

```
VPC = তোমার নিজের isolated network

ভেতরে:
  Public Subnet  → Internet accessible (API, Nginx)
  Private Subnet → Internet থেকে hidden (Database)

Traffic control:
  Route Table   → কোথায় যাবে
  IGW           → বাইরে থেকে আসা-যাওয়া
  NAT Gateway   → শুধু বের হওয়া
  Security Group → কে ঢুকতে পারবে

সবচেয়ে গুরুত্বপূর্ণ নিয়ম:
  Database = Private Subnet এ
  বাইরের কেউ directly ছুঁতে পারবে না
```
