
---

# 📚 Day 3 — Key Pairs, Security Groups & Elastic IP

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![Security Group vs NACL](../images/09-sg-vs-nacl.png)


**সময়:** ১.৫ ঘণ্টা | **Module:** ১ (EC2 & Storage Fundamentals)

## 🎯 আজকের লক্ষ্য
- SSH কীভাবে কাজ করে এবং Key Pair কেন দরকার বুঝবেন
- Public key/Private key-র পুরো concept শিখবেন
- Security Group কী ও কীভাবে firewall হিসেবে কাজ করে জানবেন
- Inbound vs Outbound rules বুঝবেন
- Public IP, Private IP, Elastic IP-র পার্থক্য শিখবেন
- একটা EC2 launch-এর পুরো flow দেখবেন

---

## Part 1: SSH & Key Pairs — ভিত্তি থেকে

### 🔑 প্রথমে SSH বুঝুন

**SSH = Secure Shell**

SSH হলো একটা protocol যেটা দিয়ে আপনি দূরের একটা computer-এ **secure ভাবে** login করতে পারেন এবং command চালাতে পারেন — যেন ওটার সামনে বসে আছেন।

**পুরানো দিনে (Telnet era):**
- Username/password plain text-এ যেত network-এ
- যে কেউ intercept করে দেখতে পারত
- Hackers-রা password চুরি করে server দখল করত

**SSH এসে সমাধান করল:**
- সব communication **encrypted**
- Password-এর বদলে **cryptographic key** দিয়ে authentication
- Man-in-the-middle attack prevent

### 🤔 কেন Password-এর বদলে Key?

**Password-এর সমস্যা:**
- মানুষ weak password রাখে (`123456`, `password`)
- Brute force attack — Bot দিনে লাখ লাখ password try করতে পারে
- Password চুরি গেলে server hack

**Key-এর সুবিধা:**
- 2048-bit RSA key = ২^২০৪৮ সম্ভাবনা — brute force করতে universe-এর বয়স লাগবে
- Key একটা file-এ থাকে, মনে রাখতে হয় না
- Password-এর মতো network-এ transmit হয় না

---

### 🔐 Public Key Cryptography — গভীরে

Key Pair বোঝার আগে **asymmetric encryption** বুঝতে হবে।

#### দুই ধরনের Encryption:

**Symmetric Encryption (একটা key):**
- এক key দিয়েই encrypt এবং decrypt
- Problem: Key কীভাবে অন্যজনকে securely পাঠাবেন?

**Asymmetric Encryption (দুইটা key — Key Pair):**
- **Public Key** (সবাইকে দেওয়া যায়)
- **Private Key** (শুধু আপনার কাছে থাকে, কাউকে দেবেন না)
- Public key দিয়ে encrypt → শুধু private key দিয়ে decrypt
- Private key দিয়ে sign → public key দিয়ে verify

#### Analogy: Lock এবং Key

ভাবুন আপনি একটা বিশেষ তালা বানালেন:
- **Public key** = তালা (অনেকগুলো copy বানিয়ে পৃথিবীর যে কাউকে দিতে পারেন)
- **Private key** = চাবি (শুধু আপনার কাছে, একটাই)

যে কেউ আপনার তালা দিয়ে একটা বাক্স lock করে আপনাকে পাঠাতে পারে। কিন্তু **শুধু আপনিই** খুলতে পারবেন কারণ চাবি আপনার কাছে।

---

### 🔄 SSH Login-এ Key Pair কীভাবে কাজ করে

পুরো process step by step:

**Setup (একবার):**
1. আপনি local computer-এ Key Pair তৈরি করলেন (২টা file):
   - `mykey.pub` (public key)
   - `mykey.pem` (private key)
2. Public key server-এ upload করলেন (`~/.ssh/authorized_keys` file-এ)
3. Private key আপনার local-এ রাখলেন (safe)

**Login (প্রতিবার):**

```
আপনার Laptop                          EC2 Server
     │                                      │
     │ "আমি login করতে চাই"                 │
     ├─────────────────────────────────────>│
     │                                      │
     │                      Random challenge তৈরি করল
     │                      Your public key দিয়ে encrypt করল
     │                                      │
     │        Encrypted challenge           │
     │<─────────────────────────────────────┤
     │                                      │
     │ Private key দিয়ে decrypt             │
     │ Original message পেল                 │
     │                                      │
     │     Decrypted message পাঠাল          │
     ├─────────────────────────────────────>│
     │                                      │
     │                     Match! Login granted
     │                                      │
     │       Shell access                   │
     │<────────────────────────────────────>│
```

**মূল কথা:** Private key **কখনোই network-এ যায় না**। শুধু প্রমাণ হয় যে আপনার কাছে ওটা আছে।

---

### 🛠️ AWS-এ Key Pair তৈরি ও ব্যবহার

#### Creation (AWS Console-এ):

**Steps:**
1. EC2 Dashboard → **Key Pairs** (বাঁ দিকে menu)
2. **Create Key Pair** ক্লিক
3. **Name:** আপনার key-র নাম (যেমন `my-aws-key`)
4. **Key pair type:**
   - **RSA** (recommended, widely supported)
   - **ED25519** (newer, faster, smaller key size)
5. **Private key file format:**
   - **`.pem`** — Linux/Mac/OpenSSH (সবচেয়ে common)
   - **`.ppk`** — Windows (PuTTY software-এর জন্য)
6. **Create** → Private key file automatically download হবে

**⚠️ গুরুত্বপূর্ণ:**
- Private key file শুধু **একবারই download** হবে, আবার কখনো পাবেন না
- File হারালে সেই key ব্যবহার করে launched instance-এ আর login করতে পারবেন না
- Multiple জায়গায় backup রাখুন (password manager, encrypted drive)
- কাউকে share করবেন না — যদি করেন, revoke করে নতুন key বানান

#### Key Pair Launch-এ ব্যবহার:

EC2 launch করার সময়:
- **Key pair (login)** option আসবে
- আপনার তৈরি করা key select করুন
- Instance boot হওয়ার সময় AWS **automatically** public key-টা instance-এর `~/.ssh/authorized_keys` file-এ বসিয়ে দেয়

#### Connection (local থেকে):

**Linux/Mac terminal:**
```bash
# প্রথমে key file-এর permission ঠিক করুন
chmod 400 my-aws-key.pem

# SSH connect
ssh -i my-aws-key.pem ec2-user@<instance-public-ip>
```

**Windows:**
- PuTTY software ব্যবহার করুন `.ppk` file দিয়ে
- অথবা Windows 10/11-এর built-in OpenSSH

**প্রতিটা OS-এর default username আলাদা:**

| OS/AMI | Username |
|---|---|
| Amazon Linux 2023 | `ec2-user` |
| Ubuntu | `ubuntu` |
| Red Hat (RHEL) | `ec2-user` |
| Debian | `admin` |
| CentOS | `centos` |
| SUSE | `ec2-user` |
| Windows | `Administrator` (RDP) |

#### Key Pair-এর Best Practices:

1. **প্রতিটা environment-এ আলাদা key** (dev, staging, prod)
2. **Team member-দের জন্য আলাদা key** (audit করা যাবে কে login করেছে)
3. **Private key-তে password (passphrase) set করুন** — চুরি হলেও কাজে আসবে না
4. **Key rotate করুন** — প্রতি ৬ মাস-১ বছরে নতুন key বানান
5. **SSH Session Manager ব্যবহার করুন** production-এ (SSH ছাড়াই access)

---

## Part 2: Security Groups — Virtual Firewall

### 🛡️ Security Group কী?

**Security Group = EC2 instance-এর চারপাশে একটা virtual firewall।**

কী traffic instance-এর ভেতরে ঢুকতে পারবে (**inbound**) এবং কী traffic বের হতে পারবে (**outbound**) — সেটা control করে।

### 🏠 Analogy: বাড়ির security guard

ভাবুন আপনার একটা বাড়ি আছে। Security Guard দরজায় বসে আছে।

**Inbound rules (ভেতরে ঢোকা):**
- "Port 22 (SSH) থেকে কেউ আসলে, শুধু আমার office IP থেকে হলে ঢুকতে দাও"
- "Port 80 (HTTP) থেকে কেউ আসলে, পৃথিবীর যে কেউ হোক, ঢুকতে দাও"
- "Port 3306 (MySQL) থেকে কেউ আসলে, শুধু application server থেকে হলে ঢুকতে দাও"

**Outbound rules (বের হওয়া):**
- "ভেতর থেকে বের হওয়া সব traffic allow করো" (default)

### 🔒 Default Behavior — খুব গুরুত্বপূর্ণ

Security Group-এর একটা key concept — **implicit deny**।

| Direction | Default |
|---|---|
| Inbound | সব **block** |
| Outbound | সব **allow** |

অর্থাৎ আপনি কিছু না বললে, ভেতরে কিছু আসতে পারবে না।

**এবং আরেকটা critical point:**
> আপনি শুধু **allow rule** লিখতে পারেন, **deny rule** লিখতে পারেন না।
> যা explicitly allow করা নেই, সব automatically denied।

এটা Network ACL (NACL)-এর সাথে পার্থক্য। NACL-এ deny rule-ও লেখা যায়।

---

### 📋 Security Group Rule-এর Components

প্রতিটা rule-এ ৫টা জিনিস থাকে:

| Field | মানে | উদাহরণ |
|---|---|---|
| **Type** | Protocol-এর preset | SSH, HTTP, HTTPS, Custom TCP |
| **Protocol** | TCP / UDP / ICMP | TCP |
| **Port Range** | কোন port(s) | 22, 80, 8080, 1000-2000 |
| **Source/Destination** | কোথা থেকে/কোথায় | IP, CIDR, অন্য SG |
| **Description** | Human-readable note | "SSH from office" |

---

### 🌐 Common Ports — অবশ্যই মনে রাখুন

| Port | Protocol | Service |
|---|---|---|
| 22 | TCP | SSH (Linux login) |
| 3389 | TCP | RDP (Windows login) |
| 80 | TCP | HTTP (web) |
| 443 | TCP | HTTPS (secure web) |
| 21 | TCP | FTP |
| 25 | TCP | SMTP (email) |
| 53 | TCP/UDP | DNS |
| 3306 | TCP | MySQL |
| 5432 | TCP | PostgreSQL |
| 6379 | TCP | Redis |
| 27017 | TCP | MongoDB |
| 1433 | TCP | Microsoft SQL Server |
| 8080 | TCP | Alternative HTTP (dev) |

---

### 📝 Source/Destination — ৩ ধরনের specify করা যায়

#### ১. একটা specific IP
- Format: `203.0.113.45/32` (/32 মানে exact একটা IP)
- Use case: "শুধু আমার office থেকে SSH"

#### ২. IP Range (CIDR block)
- Format: `203.0.113.0/24` (256টা IP), `10.0.0.0/16` (65,536টা IP)
- `0.0.0.0/0` — **পৃথিবীর সব IP** (এটা ব্যবহার সাবধানে)
- Use case: "পুরো office network থেকে"

#### ৩. অন্য Security Group
- Source-এ আরেকটা Security Group ID দিতে পারেন
- Use case: "Web server SG থেকে আসা traffic database SG-তে allow"
- **এটা সবচেয়ে powerful feature** — IP চেঞ্জ হলেও rule কাজ করবে

---

### 🎨 Practical Example: 3-tier Web Application

ভাবুন একটা web app আছে:
- **Web Server** (public internet থেকে access হবে)
- **App Server** (শুধু Web Server থেকে access হবে)
- **Database** (শুধু App Server থেকে access হবে)

#### SG-Web (Web Server-এর জন্য)

**Inbound:**
| Type | Port | Source | কেন |
|---|---|---|---|
| HTTP | 80 | 0.0.0.0/0 | যে কেউ website visit করতে পারবে |
| HTTPS | 443 | 0.0.0.0/0 | Secure website |
| SSH | 22 | Your-office-IP/32 | শুধু আপনি login করতে পারবেন |

**Outbound:** All traffic allowed (default)

#### SG-App (Application Server-এর জন্য)

**Inbound:**
| Type | Port | Source | কেন |
|---|---|---|---|
| Custom TCP | 8080 | sg-web | শুধু Web server থেকে app port-এ access |
| SSH | 22 | Your-office-IP/32 | Management |

**Outbound:** All traffic allowed

#### SG-DB (Database-এর জন্য)

**Inbound:**
| Type | Port | Source | কেন |
|---|---|---|---|
| MySQL | 3306 | sg-app | শুধু App server থেকে database access |
| SSH | 22 | Your-office-IP/32 | Management |

**Outbound:** All traffic allowed

এই design-এ:
- Internet থেকে সরাসরি database-এ পৌঁছানোর কোনো উপায় নেই
- App server-কে compromise করলেও SSH ছাড়া database-এ যাওয়া যাবে না
- Defense in depth — multiple layer of security

---

### ⚙️ Security Group-এর Important Features

#### ১. Stateful (এটা critical concept)

**মানে:** Security Group "মনে রাখে" কোন traffic কোথা থেকে শুরু হয়েছিল।

**Example:**
- আপনি SSH দিয়ে instance-এ login করলেন (inbound port 22 allow)
- Server আপনাকে response পাঠাচ্ছে (outbound)
- Outbound-এ আলাদা rule লাগবে না, কারণ SG জানে এই connection allowed ছিল

**পার্থক্য NACL-এর সাথে:** NACL stateless — inbound allow করলে return traffic-এর জন্য outbound-ও আলাদা allow লাগে।

#### ২. Instance-level (NACL subnet-level)
- Security Group EC2 instance-এর সাথে attach হয়
- একটা instance-এ ৫টা পর্যন্ত Security Group attach করা যায়
- একই SG একাধিক instance-এ ব্যবহার করা যায়

#### ৩. Changes Immediate
- Rule change করলে সাথে সাথে effect হয়
- Restart লাগে না

#### ৪. Multiple SG = Union of Rules
- Instance-এ যদি SG-A আর SG-B থাকে
- Effective rules = SG-A + SG-B (দুটোর rule-ই apply হবে)

---

### ❌ Common Mistakes — এড়িয়ে চলুন

**Mistake 1:** SSH সবার জন্য open (`0.0.0.0/0` on port 22)
- বট-রা সারাদিন brute force attack করবে
- **Fix:** শুধু আপনার office/home IP allow করুন

**Mistake 2:** Database internet-এ expose
- Port 3306 on `0.0.0.0/0`
- **Fix:** শুধু app server-এর SG থেকে allow

**Mistake 3:** সব port allow (All Traffic from 0.0.0.0/0)
- **Fix:** Specific port-ই শুধু open করুন

**Mistake 4:** Outbound unrestricted রাখা production-এ
- Compromised server internet-এ data leak করতে পারে
- **Fix:** শুধু প্রয়োজনীয় outbound rule রাখুন

---

## Part 3: IP Addresses — Public, Private, Elastic

### 🌐 প্রথমে IP Address-এর ভিত্তি

**IP Address** = internet-এ প্রতিটা device-এর unique address। যেমন ঠিকানা ছাড়া চিঠি পাঠানো যায় না, IP ছাড়া data পাঠানো যায় না।

**দুই ধরনের IP:**

#### Private IP (Internal)
- শুধু একটা নির্দিষ্ট network-এর ভেতরে ব্যবহার হয়
- Internet-এ route হয় না
- Reserved ranges:
  - `10.0.0.0/8` (10.x.x.x)
  - `172.16.0.0/12` (172.16.x.x - 172.31.x.x)
  - `192.168.0.0/16` (192.168.x.x)

**উদাহরণ:** আপনার বাড়ির WiFi router এই IP দেয় (192.168.1.x সাধারণত)। এই IP দিয়ে বাইরে থেকে connect করা যায় না।

#### Public IP (Internet-routable)
- Unique globally — পৃথিবীতে একই IP আর কারও না
- Internet-এ direct accessible
- ISP-রা allocate করে, AWS-এর নিজস্ব pool আছে

---

### 🖥️ EC2-এর IP Addresses

একটা EC2 instance-এর ৩ ধরনের IP থাকতে পারে:

#### ১. Private IP (সবসময় থাকে)
- VPC-এর CIDR range থেকে allocate
- Instance lifetime-এ change হয় না
- Internal communication-এর জন্য (VPC-এর ভেতরে)
- উদাহরণ: `10.0.1.45`

#### ২. Public IP (Optional, auto-assigned)
- Public subnet-এ launch করলে auto assign হতে পারে
- Instance stop করলে **হারিয়ে যায়**, restart করলে **নতুন IP** পাবে
- Free
- উদাহরণ: `54.203.12.45`

#### ৩. Elastic IP (Optional, manual)
- **আপনার own করা** public IP
- Instance detach করলেও আপনার account-এ থাকে
- Stop/start করলেও **change হয় না**
- Free (যদি একটা instance-এ attach থাকে), **unused থাকলে charge হয়**

---

### 🔄 Private IP vs Public IP — একসাথে কীভাবে কাজ করে

একটা EC2-এর public IP যখন থাকে, তখন আসলে instance-এর শুধু private IP থাকে। AWS-এর router (IGW) **NAT (Network Address Translation)** করে public IP-কে private IP-তে convert করে।

```
Internet
   │
   │ traffic to 54.203.12.45 (public IP)
   │
Internet Gateway (IGW)
   │
   │ NAT translation: 54.203.12.45 → 10.0.1.45
   │
EC2 Instance (private IP: 10.0.1.45)
```

**এজন্য instance-এর OS level-এ `ifconfig` চালালে শুধু private IP দেখবেন, public IP দেখবেন না।**

---

### 🎯 Elastic IP (EIP) — গভীরে

#### কেন Elastic IP দরকার?

**সমস্যা:** Regular public IP stop/start-এ change হয়। কিন্তু আপনার domain name (যেমন `mywebsite.com`) একটা fixed IP-তে point করা থাকে।

**Example scenario:**
- Instance stop করলেন maintenance-এর জন্য
- Public IP: `54.203.12.45` gone
- Start করলেন → নতুন IP: `52.14.88.12`
- আপনার DNS এখনও পুরানো IP-তে point করছে
- Website down!

**Elastic IP-এর সমাধান:**
- একটা static public IP
- Instance-এর সাথে attach/detach করা যায়
- Stop/start করলেও IP থাকে
- DNS সবসময় ঠিক IP-তে point করবে

#### Elastic IP-এর ব্যবহার:

**Use case 1: Production Web Server**
- EIP attach করুন
- Domain DNS এই EIP-তে point করুন
- Instance replace করলেও নতুন instance-এ একই EIP attach করে DNS পরিবর্তন লাগবে না

**Use case 2: Disaster Recovery**
- Primary instance fail করলে
- Quickly EIP detach করে backup instance-এ attach
- User-রা কিছু টের পাবে না (DNS change ছাড়া switchover)

**Use case 3: Third-party Whitelisting**
- কিছু external service আপনার IP whitelist করে রাখে
- EIP থাকলে IP change হবে না, whitelist ভাঙবে না

#### ⚠️ Elastic IP-এর Cost Warning

AWS একটা tricky rule রেখেছে:
- EIP attached to running instance → **Free**
- EIP attached to stopped instance → **Charge হবে**
- EIP **not attached** to anything → **Charge হবে** (~$3.60/month)

**কেন এই rule?** IPv4 address-এর অভাব আছে পৃথিবীতে। AWS চায় না কেউ EIP reserve করে রাখুক unused। তাই unused-এ charge।

**তাই:** ব্যবহার না করলে **release** করুন, শুধু allocate করে রাখবেন না।

#### Elastic IP-এর Limits

- Default: per region-এ **৫টা EIP** allocate করা যায়
- বেশি লাগলে AWS-এর কাছে request করতে হবে (support ticket)
- IPv6-এও Elastic IP সাপোর্ট আছে কিছু region-এ

---

### 📊 Quick Comparison Table

| Feature | Private IP | Public IP (Auto) | Elastic IP |
|---|---|---|---|
| VPC range-এ? | হ্যাঁ | না (AWS pool) | না (AWS pool) |
| Stop-এ থাকে? | হ্যাঁ | না | হ্যাঁ |
| Internet accessible? | না | হ্যাঁ | হ্যাঁ |
| Change হয়? | না | হ্যাঁ | না |
| Cost | Free | Free | Free যদি attached |
| Attach/detach? | না | না | হ্যাঁ |
| Use case | Internal | Temporary public | Production fixed IP |

---

## Part 4: EC2 Launch-এর Full Walkthrough (Conceptual)

এখন সব একসাথে দেখুন। একটা EC2 launch করার পুরো process:

### Launch Wizard Flow:

**১. Name and tags**
- Instance-এর নাম: `web-server-01`
- Tags: Environment=production, Owner=you

**২. Application and OS Images (AMI)**
- Quick start থেকে **Amazon Linux 2023 AMI** select
- বা Ubuntu 22.04

**৩. Instance type**
- **t3.micro** (free tier)

**৪. Key pair (login)**
- আগে বানানো `my-aws-key` select
- না থাকলে নতুন create

**৫. Network settings**
- **VPC:** Default VPC
- **Subnet:** Default-এর একটা public subnet
- **Auto-assign Public IP:** Enable
- **Firewall (Security Group):**
  - Create new OR Select existing
  - Rules:
    - SSH (22) from My IP
    - HTTP (80) from 0.0.0.0/0

**৬. Configure storage**
- **Root volume:** 8 GB gp3
- Free tier-এ 30 GB পর্যন্ত free

**৭. Advanced details (optional)**
- **IAM instance profile:** (later shikhben)
- **User data:** bootstrap script
  ```bash
  #!/bin/bash
  yum update -y
  yum install -y nginx
  systemctl start nginx
  systemctl enable nginx
  ```
  এটা instance boot-এ run হবে, Nginx auto install হবে

**৮. Launch instance**
- Review
- "Launch instance" click
- ১-২ মিনিট পরে running state

### Launch হওয়ার পর AWS কী করে:

1. Physical server-এ space allocate করে
2. AMI থেকে root volume তৈরি করে
3. VPC-তে network interface attach করে
4. Private IP assign করে
5. Public IP assign করে (যদি enable থাকে)
6. Security Group apply করে
7. Public key `~/.ssh/authorized_keys`-এ বসায়
8. User data script run করে
9. Instance "running" state-এ যায়

### Connection Check:

```bash
# Public IP দিয়ে SSH
ssh -i my-aws-key.pem ec2-user@<public-ip>

# Instance-এর ভেতরে
ip addr  # private IP দেখাবে
curl ifconfig.me  # public IP check
```

---

## 🎯 আজকের মূল Takeaways

1. **SSH** = encrypted remote login protocol
2. **Key Pair:** Public key server-এ, Private key আপনার কাছে — private কখনো share করবেন না
3. **Security Group** = instance-level virtual firewall, stateful, deny by default, শুধু allow rule
4. **Inbound:** ভেতরে ঢোকা traffic; **Outbound:** বের হওয়া traffic
5. **Source হিসেবে অন্য SG** use করা best practice
6. **Private IP:** VPC-র ভেতরে, static
7. **Public IP:** Auto-assigned, stop-এ হারায়
8. **Elastic IP:** Static public IP, stop-start-এ থাকে, unused-এ charge

---

## 📝 Self-check Questions

১. SSH-এ Private Key কি network-এ যায়? কেন?
২. একটা database server-এর Security Group কেমন হবে? (Inbound rules বলুন)
৩. Security Group-এ Deny rule লেখা যায়?
৪. `0.0.0.0/0` মানে কী? SSH-এ কি এটা ব্যবহার করা উচিত?
৫. Instance stop করে start করলে public IP-র কী হয়?
৬. Elastic IP-তে কখন charge হয়?
৭. Stateful firewall মানে কী?
৮. একটা instance-এ কয়টা Security Group attach করা যায়?
৯. `.pem` আর `.ppk` file-এর পার্থক্য কী?
১০. Web-App-DB 3-tier design-এ কোন SG কোনটা থেকে traffic নেবে?

---

## 💡 Pro Tips

- **SSH rule-এ কখনো `0.0.0.0/0` না**, শুধু আপনার IP
- **Production-এ Session Manager (SSM)** ব্যবহার করুন SSH-এর বদলে — no key management, full audit log
- **Security Group-এ good description লিখুন** — ৬ মাস পরে ভুলে যাবেন কেন বানিয়েছিলেন
- **EIP release করতে ভুলবেন না** — unused রাখলে প্রতি মাসে charge
- **একটা template SG বানিয়ে রাখুন** — প্রতিবার নতুন বানাতে হবে না

---

## 🚨 Real-world Horror Stories

**Story 1:** এক developer SSH-এ `0.0.0.0/0` দিয়ে weak password রেখেছিলেন। ২ ঘণ্টায় bot login করে crypto mining script চালিয়ে দেয়। মাস শেষে $2,000 bill।

**Story 2:** MongoDB port 27017 `0.0.0.0/0`-তে open ছিল, no authentication। Shodan.io-তে search দিলেই পাওয়া যেত। এক rancomware group পুরো database encrypt করে ransom চায়।

**Moral:** Security Group-এ কখনো careless হবেন না।

---
