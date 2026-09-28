# 📚 Day 11 — NAT Gateway, NAT Instance & Bastion Host

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![NAT Gateway vs Internet Gateway](../images/25-nat-vs-igw.png)


**সময়:** ১.৫ ঘণ্টা | **Module:** ২ (VPC Design & Network Architecture) — Day 4

## 🎯 আজকের লক্ষ্য
- NAT কী এবং কেন দরকার গভীরে বুঝবেন
- NAT Gateway vs NAT Instance — পুরো comparison
- Bastion Host (Jump Server) architecture
- AWS Systems Manager Session Manager — modern alternative
- High availability NAT design
- Cost optimization strategies
- Real-world hybrid setup

---

## Part 1: Private Subnet-এর Internet Problem

### 🤔 The Problem

Day 9-এ আপনি শিখেছেন private subnet-এ IGW route নেই। এটা security-এর জন্য ভালো। কিন্তু একটা practical issue:

### 🏥 Real-life Scenario

আপনার application server private subnet-এ:
- `yum update` দরকার security patches-এর জন্য
- `npm install` package download করতে হবে
- External API call করতে হবে (`api.stripe.com`)
- Time sync NTP server থেকে
- Logs পাঠাতে হবে external monitoring service-এ

**Private subnet-এ:** কোনোটাই possible না, কারণ internet route নেই।

### 💡 Conflicting Requirements

```
Security চাই:
- Database internet-এ exposed না
- App server-এ direct hack না
- Inbound traffic block

কিন্তু application functionality-র জন্য:
- Outbound internet access (updates, APIs)
- Software dependencies download
```

**Solution:** NAT — outbound allow, inbound block।

---

## Part 2: NAT — The Concept

### 🔄 NAT = Network Address Translation

**Idea:** Private IP-কে public IP-তে translate করা যাতে internet-এ যেতে পারে, কিন্তু internet থেকে directly আসতে পারবে না।

### 🎭 Analogy: Hotel Concierge

ভাবুন একটা hotel:

- **Guests (private instances)** room number আছে (private IP)
- কেউ outside থেকে directly room number-এ phone করতে পারে না
- কিন্তু guest concierge (NAT) দিয়ে outside-এ call করতে পারে
- Concierge call route করে, আবার reply guest-কে দেয়
- Outside থেকে guest-কে call করতে হলে concierge-এর number, তারপর guest's room ask

**NAT এমনই কাজ করে।** Private instance থেকে outbound OK, কিন্তু external কেউ initiate করতে পারে না।

### 🔧 NAT-এর Technical Mechanism

#### Outbound Flow (Instance → Internet):

```
EC2 Private (10.0.11.5)
    │
    │ Source: 10.0.11.5:54321
    │ Dest: api.example.com:443
    ▼
NAT Gateway (10.0.1.10 in public subnet, EIP: 54.X.Y.Z)
    │
    │ NAT translates source:
    │ Source: 54.X.Y.Z:NEW_PORT  (NAT's public IP)
    │ Dest: api.example.com:443
    │
    │ Records mapping:
    │ NEW_PORT ↔ (10.0.11.5:54321)
    ▼
IGW
    │
    ▼
Internet → api.example.com
```

#### Inbound Flow (Reply):

```
api.example.com → Internet
    │
    │ Source: api.example.com:443
    │ Dest: 54.X.Y.Z:NEW_PORT
    ▼
IGW
    │
    ▼
NAT Gateway
    │
    │ NAT looks up mapping:
    │ NEW_PORT → 10.0.11.5:54321
    │
    │ Translates back:
    │ Source: api.example.com:443
    │ Dest: 10.0.11.5:54321
    ▼
EC2 Private (10.0.11.5)
```

**Key insight:** NAT maintains a "port mapping table" — outbound connection → unique port number → reply route back।

### 🚫 কেন Inbound Initiate Possible না?

External attacker `54.X.Y.Z`-এ random port-এ packet পাঠালে:
- NAT-এর mapping table-এ এই port নেই
- কোন instance-এ পাঠাবে জানে না
- Packet drops

**এজন্যই NAT secure** — outbound only, inbound (initiated externally) blocked by design।

---

## Part 3: NAT Gateway (AWS Managed)

### 🌐 NAT Gateway কী?

**NAT Gateway = AWS-এর fully managed NAT service।**

আপনি বানালেন, AWS সব manage করে — high availability, scaling, patching।

### ⭐ Key Characteristics

#### 1. Managed Service
- AWS handles infrastructure
- Automatic patching
- No OS to manage
- Pay-per-hour pricing

#### 2. High Availability (within AZ)
- AZ-redundant within that AZ
- কিন্তু single AZ-bound (এই AZ fail করলে এই NAT GW down)

#### 3. Scalable
- 5 Gbps starting bandwidth
- Burst up to 100 Gbps
- No tuning needed

#### 4. Public IP Required
- Always uses Elastic IP (EIP)
- Public subnet-এ deploy

#### 5. Stateful
- Connection tracking automatic
- Reply traffic auto-allowed

### 🏗️ NAT Gateway Architecture

```
                    Internet
                       │
                       ▼
                ┌─────────────┐
                │     IGW     │
                └──────┬──────┘
                       │
    ┌──────────────────┴──────────────────┐
    │                                      │
┌───▼─────────────┐              ┌────────▼────────┐
│ Public Subnet   │              │ Private Subnet  │
│ 10.0.1.0/24     │              │ 10.0.11.0/24    │
│                 │              │                 │
│  ┌────────────┐ │              │  ┌────────────┐│
│  │ NAT Gateway│◄────────────────┤Private EC2 ││
│  │ + EIP      │ │   outbound   │  │            ││
│  └────────────┘ │   internet   │  └────────────┘│
└─────────────────┘              └─────────────────┘
```

**Important:**
- NAT Gateway **public subnet-এ** থাকে (so it can reach IGW)
- Private subnet-এর route table NAT Gateway-তে point করে

### 🛠️ NAT Gateway Setup Steps

#### Step 1: Allocate Elastic IP
```
EC2 Console → Elastic IPs → Allocate Elastic IP
```

#### Step 2: Create NAT Gateway
```
VPC Console → NAT Gateways → Create
- Name: prod-nat-1a
- Subnet: public-1a (must be public!)
- Connectivity type: Public
- Elastic IP: [select allocated EIP]
- Create
```

#### Step 3: Update Private Route Table
```
VPC Console → Route Tables → private-rt-1a
Edit routes:
- Add: 0.0.0.0/0 → nat-1a
```

#### Step 4: Test
```
Private EC2: 
$ curl https://google.com
Should work now!
```

### 💰 NAT Gateway Pricing (Mumbai region)

**Two charges:**

#### 1. Hourly charge
- $0.045/hour
- ~$32/month per NAT Gateway (24x7)

#### 2. Data processing charge
- $0.045/GB processed
- Both inbound AND outbound traffic counted

#### Cost Example:

**Small workload (10 GB/day outbound):**
- Hours: $32/month
- Data: 300 GB × $0.045 = $13.50/month
- **Total: ~$45.50/month**

**Heavy workload (1 TB/day):**
- Hours: $32/month
- Data: 30,000 GB × $0.045 = $1,350/month
- **Total: ~$1,382/month**

**সতর্কতা:** Heavy data transfer applications-এ NAT Gateway expensive। VPC Endpoint use করে cost কমাতে পারেন (Day 12)।

### 🔥 High Availability Design

#### Single NAT Gateway Problem

```
   AZ-1a              AZ-1b              AZ-1c
   ┌────────┐         ┌────────┐         ┌────────┐
   │ NAT-1a │         │        │         │        │
   └───┬────┘         └────────┘         └────────┘
       │
   App-1a            App-1b              App-1c
   (works)         (uses NAT-1a)      (uses NAT-1a)
```

**Problem:**
- AZ-1a fail করলে NAT-1a down
- All AZs use NAT-1a
- App-1b, App-1c-এর internet bandhа

#### HA Solution: NAT per AZ

```
   AZ-1a              AZ-1b              AZ-1c
   ┌────────┐         ┌────────┐         ┌────────┐
   │ NAT-1a │         │ NAT-1b │         │ NAT-1c │
   └───┬────┘         └───┬────┘         └───┬────┘
       │                  │                  │
   App-1a            App-1b              App-1c
```

**Setup:**
- প্রতি public subnet-এ একটা NAT
- Private RT (per AZ) → own AZ-এর NAT
- AZ fail = শুধু সেই AZ's apps affected
- Other AZs unaffected

**Cost:** 3x NAT Gateway = ~$96/month + data

**Trade-off:** 
- 1 NAT: $32/month, no HA
- 3 NAT: $96/month, full HA

Production-এ ৩ NAT recommended।

---

## Part 4: NAT Instance (Legacy/DIY)

### 📜 NAT Instance কী?

**NAT Instance = একটা EC2 instance যেটা NAT software চালায়।**

NAT Gateway আসার আগে এটাই ছিল primary option।

### 🏗️ Architecture

```
NAT Instance:
- Regular EC2 (Amazon Linux NAT AMI)
- iptables/NAT software configured
- Public IP/EIP attached
- Source/Destination check disabled
- IP forwarding enabled in OS
```

### 🆚 NAT Instance vs NAT Gateway

| Feature | NAT Instance | NAT Gateway |
|---|---|---|
| **Type** | EC2-based | Managed service |
| **HA** | DIY (need scripting) | Per-AZ AWS managed |
| **Bandwidth** | Instance-dependent | 5-100 Gbps |
| **Maintenance** | You patch OS | AWS handles |
| **Setup complexity** | High | Low |
| **Source/Dest check** | Must disable | N/A |
| **Cost** | Instance + EIP | Hourly + data |
| **Use as Bastion** | Yes (one instance, dual purpose) | No |
| **Customization** | Full control | Limited |
| **AWS recommendation** | Legacy | **Use this** |

### 🛠️ NAT Instance Setup (Conceptual)

```bash
# Launch EC2 with NAT-eligible AMI
# (Amazon NAT AMI or custom configured)

# Disable Source/Destination check (CRITICAL)
EC2 → Actions → Networking → Change source/destination check → Disable

# Enable IP forwarding (in OS)
sudo sysctl -w net.ipv4.ip_forward=1

# Configure iptables for NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
```

**Update Private Route Table:**
```
0.0.0.0/0 → eni-of-nat-instance (instead of NAT Gateway)
```

### ⚠️ Source/Destination Check

**একটা important EC2 setting:**

By default, EC2 instance only sends/receives traffic for itself (its own IP)। NAT instance has to forward traffic for others।

**Solution:** Disable source/dest check।

```
Instance → Actions → Networking → Change source/destination check → Disable
```

**ভুললে:** NAT কাজ করবে না, traffic drop হবে।

### 💰 Cost Comparison

**Small NAT Instance (t3.small):**
- Instance: $15/month
- EIP: free if attached
- Data transfer: same as IGW pricing
- **Total: ~$15-20/month**

**vs NAT Gateway:** ~$32/month base

**বাচ্চা workload-এ NAT Instance সস্তা।**

### 🎯 কখন NAT Instance Use করবেন

**✅ Use NAT Instance:**
- Very small workload (cost critical)
- Dual purpose (NAT + Bastion)
- Custom firewall rules needed
- Educational/learning environment
- Specific NAT software requirement

**❌ Don't Use NAT Instance:**
- Production critical
- High traffic
- Don't want maintenance overhead
- HA needed

**AWS recommends:** NAT Gateway for production.

---

## Part 5: Bastion Host (Jump Server)

### 🤔 Problem: SSH-ing to Private Instances

**Setup:**
- Database in private subnet
- No public IP
- IGW route absent
- How do you SSH to it?

**Direct SSH:** Impossible (no public IP, no route)।

**Solutions:**
1. Bastion Host (traditional)
2. AWS Systems Manager Session Manager (modern)
3. VPN to VPC (corporate setup)

### 🏰 Bastion Host কী?

**Bastion Host = একটা hardened public EC2 instance যেটার মাধ্যমে আপনি private instances-এ SSH করেন।**

**"Jump server" / "Jump box"** also called।

### 🏗️ Architecture

```
                     Internet
                        │
                        ▼
                  ┌──────────┐
                  │   IGW    │
                  └─────┬────┘
                        │
         ┌──────────────┴───────────────┐
         │                              │
   Public Subnet                  Private Subnet
   ┌─────────────┐                 ┌─────────────┐
   │   Bastion   │                 │  Private    │
   │   Host      │ ───SSH──────►   │  Instance   │
   │  (public IP)│                 │             │
   └─────▲───────┘                 └─────────────┘
         │
         │ SSH from your office
         │
   Your Laptop
```

**Flow:**
1. SSH from laptop to Bastion (public IP)
2. From Bastion, SSH to private instance (private IP)
3. Two-hop SSH

### 🛠️ Bastion Host Setup

#### Step 1: Launch Bastion EC2

```
Name: bastion-host
AMI: Amazon Linux 2023
Instance type: t3.micro
Subnet: public subnet
Auto-assign public IP: enable
Key pair: my-bastion-key
Security Group: sg-bastion
```

#### Step 2: Bastion Security Group

```
sg-bastion:
Inbound:
- SSH (22) from your-office-IP/32 (ONLY)

Outbound:
- All (or restrict to internal SSH ports)
```

**Critical:** SSH source restricted to office IP, NOT 0.0.0.0/0।

#### Step 3: Private Instance Security Group

```
sg-private:
Inbound:
- SSH (22) from sg-bastion (Source = SG, not IP)

Outbound:
- As needed
```

#### Step 4: SSH Workflow

**Method 1: Two-step**

```bash
# Step 1: SSH to bastion
ssh -i bastion-key.pem ec2-user@<bastion-public-ip>

# Step 2: From bastion, SSH to private
ssh -i private-key.pem ec2-user@10.0.11.5
```

**Problem:** Private key bastion-এ থাকতে হবে — security risk।

**Method 2: SSH Agent Forwarding (better)**

Local-এ:
```bash
# Add key to SSH agent
ssh-add private-key.pem

# SSH to bastion with agent forwarding
ssh -A -i bastion-key.pem ec2-user@<bastion-public-ip>

# Now from bastion, SSH to private (uses key from your laptop)
ssh ec2-user@10.0.11.5
```

**Benefit:** Private key never on bastion।

**Method 3: ProxyJump (best)**

`~/.ssh/config`-এ:
```
Host bastion
    HostName <bastion-public-ip>
    User ec2-user
    IdentityFile ~/.ssh/bastion-key.pem

Host private-server
    HostName 10.0.11.5
    User ec2-user
    IdentityFile ~/.ssh/private-key.pem
    ProxyJump bastion
```

Then:
```bash
ssh private-server
```

Direct, automatic two-hop। SSH config handles complexity।

---

### 🛡️ Bastion Best Practices

#### 1. Hardening

```
✓ Latest security patches
✓ Disable password authentication (key only)
✓ Fail2ban for brute force protection
✓ Strong key pair (RSA 4096 or ED25519)
✓ Audit logging enabled (CloudWatch)
✓ Time-based SSH access (only business hours)
```

#### 2. Limited Privileges

```
- Bastion-এ minimal software
- No production data
- No application code
- Just SSH gateway
- Read-only access if possible
```

#### 3. Multi-AZ Bastions

```
- 2 bastions, one per AZ
- Round-robin DNS
- AZ failure tolerance
```

#### 4. Audit Everything

```
- SSH login logs to CloudWatch
- All commands logged (auditd)
- Access reviews monthly
```

#### 5. Strict Security Group

```
✓ Source: specific office IPs only
✗ Never 0.0.0.0/0 for SSH
```

#### 6. Just-in-Time Access

```
Advanced: Open SSH only when needed
- Lambda function modifies SG
- Open port 22 → user → close after work
- Reduces attack surface
```

#### 7. MFA

```
- SSH + MFA (Google Authenticator)
- 2-factor authentication
- Even if key stolen, MFA stops
```

### 📊 Bastion Disadvantages

❌ Always-on cost (instance charges)
❌ Maintenance overhead (patches, updates)
❌ Single point of compromise (if bastion hacked, private network at risk)
❌ Key management complexity
❌ Audit logging setup needed
❌ Public IP exposed (target for attacks)

---

## Part 6: AWS Systems Manager Session Manager (Modern Alternative)

### 💡 Session Manager কী?

**SSH-এর modern, secure replacement।** Bastion ছাড়াই private instance-এ access।

**Key benefit:** No SSH, no public IP, no key management।

### 🏗️ How It Works

```
Your Laptop
    │
    │ AWS Console / CLI
    ▼
AWS Systems Manager
    │
    │ (over secure HTTPS)
    ▼
SSM Agent (running on EC2)
    │
    │ (initiated FROM instance, outbound)
    ▼
Connection Established
```

**Magic:**
- SSM Agent on EC2 outbound connects to AWS SSM
- AWS SSM acts as proxy
- No inbound SSH port needed
- No public IP needed
- No bastion needed

### ✨ Benefits

#### 1. No Open Ports
- Inbound port 22 NOT needed
- Reduce attack surface

#### 2. No Public IP
- Private instances accessible
- No bastion infrastructure

#### 3. No SSH Keys
- IAM-based authentication
- No key management

#### 4. Full Audit Trail
- Every session logged
- Commands recorded
- CloudTrail integration
- S3 log archival

#### 5. Permission Granular
- IAM policies control access
- Per-instance, per-user permissions
- Time-based access

#### 6. Cross-platform
- Linux, Windows
- Web console or CLI

### 🛠️ Session Manager Setup

#### Prerequisites

**On EC2 Instance:**
1. SSM Agent installed (most AMIs have it)
2. IAM Role attached with `AmazonSSMManagedInstanceCore` policy
3. Outbound HTTPS (port 443) to SSM endpoints

**On Your Local:**
1. AWS CLI installed
2. Session Manager plugin (for CLI sessions)
3. IAM permissions for `ssm:StartSession`

#### Step 1: IAM Role for EC2

```
Role: SSM-EC2-Role
Policy: AmazonSSMManagedInstanceCore
Attach to: All EC2 instances
```

#### Step 2: Connect via Console

```
EC2 Console → Select Instance → Connect → Session Manager → Connect
```

Browser-based shell opens। No SSH client needed।

#### Step 3: Connect via CLI

```bash
aws ssm start-session --target i-1234567890abcdef0
```

Direct shell access, no SSH।

#### Step 4: Optional Logging

```
Configure session logging:
- S3 bucket for logs
- CloudWatch Logs
- KMS encryption
- Automatic retention
```

### 🆚 Session Manager vs Bastion

| Feature | Bastion Host | Session Manager |
|---|---|---|
| **Inbound port** | SSH 22 | None |
| **Public IP** | Yes | Not needed |
| **SSH keys** | Manage | Not needed |
| **Setup complexity** | High | Low |
| **Audit logging** | DIY | Built-in |
| **Access control** | SG + IAM + OS | IAM + tagging |
| **Cost** | Instance + EIP | Free (SSM included) |
| **Scalability** | Manual | Automatic |
| **OS support** | Linux/Windows | Linux/Windows/Mac |
| **Just-in-time access** | Custom scripts | Built-in (IAM) |

### 🎯 Modern Recommendation

**Use Session Manager unless:**
- Port forwarding needed (specific cases)
- Legacy systems require SSH
- Specific compliance need

**For most use cases:** Session Manager > Bastion Host।

### 🔌 Port Forwarding via SSM

Need to access private DB locally?

```bash
# Forward local 3306 to private DB through SSM
aws ssm start-session \
  --target i-bastion-instance \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters host="private-db-endpoint.amazonaws.com",portNumber="3306",localPortNumber="3306"
```

Then `mysql -h localhost -P 3306` works locally।

---

## Part 7: Comparison — All Three

### 📊 Use Cases Matrix

| Use Case | NAT Gateway | NAT Instance | Bastion Host | Session Manager |
|---|---|---|---|---|
| **Outbound internet from private subnet** | ✅ Best | ✅ Cheaper | ❌ | ❌ |
| **SSH to private instances** | ❌ | ❌ | ✅ Traditional | ✅ Modern |
| **Custom firewall rules** | ❌ | ✅ | ✅ | ✅ |
| **Audit logging** | Basic | Custom | DIY | ✅ Built-in |
| **High availability** | ✅ Per AZ | DIY | DIY | ✅ Managed |
| **Production recommended** | ✅ | ❌ | ⚠️ Use Session Mgr | ✅ |

### 🎯 Decision Matrix

**Need internet from private subnet:**
→ **NAT Gateway** (managed, HA)

**Cost-critical small workload:**
→ NAT Instance (with caveat: maintenance overhead)

**SSH to private instance:**
→ **Session Manager** (modern, secure)

**Legacy SSH workflow needed:**
→ Bastion Host (with strict security)

**Both NAT + Bastion combined (cost-saving):**
→ NAT Instance acting as Bastion (small environment only)

---

## Part 8: Real-world Architecture

আজ Day 9-এ design করা VPC-তে এই components যোগ করুন।

### 🏗️ Complete Architecture

```
                        Internet
                           │
                           ▼
                     ┌──────────┐
                     │   IGW    │
                     └─────┬────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼─────┐   ┌─────▼──────┐  ┌────▼──────┐
    │  AZ-1a     │   │  AZ-1b     │  │  AZ-1c    │
    │            │   │            │  │           │
    │  Public    │   │  Public    │  │  Public   │
    │  Subnet    │   │  Subnet    │  │  Subnet   │
    │            │   │            │  │           │
    │  ┌──────┐  │   │  ┌──────┐  │  │  ┌──────┐ │
    │  │ NAT  │  │   │  │ NAT  │  │  │  │ NAT  │ │
    │  │  GW  │  │   │  │  GW  │  │  │  │  GW  │ │
    │  └──┬───┘  │   │  └──┬───┘  │  │  └──┬───┘ │
    │     │      │   │     │      │  │     │     │
    │  ┌──┴───┐  │   │     │      │  │     │     │
    │  │  ALB │  │   │     │      │  │     │     │
    │  └──────┘  │   │     │      │  │     │     │
    │            │   │     │      │  │     │     │
    └────────────┘   └─────┼──────┘  └─────┼─────┘
                           │                │
    ┌────────────┐   ┌─────▼──────┐  ┌────▼──────┐
    │  App-1a    │   │  App-1b    │  │  App-1c   │
    │  Subnet    │   │  Subnet    │  │  Subnet   │
    │            │   │            │  │           │
    │ EC2 with   │   │ EC2 with   │  │ EC2 with  │
    │ SSM Agent  │   │ SSM Agent  │  │ SSM Agent │
    │ (no public │   │ (no public │  │ (no public│
    │  IP)       │   │  IP)       │  │  IP)      │
    └────────────┘   └────────────┘  └───────────┘
    
    ┌────────────┐   ┌────────────┐  ┌───────────┐
    │  DB-1a     │   │  DB-1b     │  │  DB-1c    │
    │  Subnet    │   │  Subnet    │  │  Subnet   │
    │ (isolated) │   │ (isolated) │  │ (isolated)│
    └────────────┘   └────────────┘  └───────────┘
```

### 🎯 Design Decisions

**1. NAT Gateway per AZ (3 total):**
- HA at AZ level
- ~$96/month + data
- Worth it for production

**2. Session Manager for SSH:**
- No bastion host
- IAM-based access
- Full audit log
- Cost: free

**3. App tier internet via NAT:**
- yum/npm updates
- External APIs (Stripe, Twilio)
- Logging services

**4. DB tier truly isolated:**
- No NAT route
- No internet access
- Only VPC internal communication

### 🛡️ Security Configuration

**SG-NAT (NAT Gateway-এর জন্য না, by AWS managed):**
- N/A, AWS handles

**SG-App:**
```
Inbound: Port 8080 from sg-alb
Outbound: 443 to 0.0.0.0/0 (via NAT for updates)
         3306 to sg-db
```

**SG-DB:**
```
Inbound: 3306 from sg-app
Outbound: nothing
```

**For SSM:**
```
SG-App outbound also needs:
- 443 to AWS service endpoints (for SSM)
```

---

## Part 9: Cost Optimization Strategies

NAT Gateway expensive হতে পারে। কিছু savings strategies:

### 💰 Strategy 1: Use VPC Endpoints

**Problem:** S3-এ data পাঠাতে NAT Gateway use → data transfer charge।

**Solution:** S3 Gateway Endpoint (free)।

**Savings:**
- Without endpoint: NAT charges full data
- With endpoint: zero data transfer cost for S3 traffic

Day 12-এ details।

### 💰 Strategy 2: Reduce Outbound Calls

**Audit:** আপনার app-এর outbound traffic কী?

**Common culprits:**
- Logging to external services (CloudWatch internal — free)
- API calls (cache responses)
- Large file downloads (CDN-এ)
- Repeated DNS lookups (cache TTL)

### 💰 Strategy 3: Single NAT for Dev/Staging

**Production:** Per-AZ NAT (3x cost)
**Dev/Staging:** Single NAT (1x cost, no HA)

Dev environment HA matter করে না — accept downtime risk for cost saving।

### 💰 Strategy 4: NAT Instance for Tiny Workloads

**Use case:** Personal projects, small startups
- t3.nano NAT instance
- $5/month vs $32/month NAT Gateway
- Trade-off: maintenance, no HA

### 💰 Strategy 5: Schedule NAT Down

**Dev environment:**
- Office hours only (8 AM - 6 PM)
- Lambda automation
- 50% cost reduction

### 💰 Strategy 6: Monitor & Alert

```
CloudWatch Metric: NAT Gateway data processed
Alert if > expected baseline
Investigate spikes
```

Often surprise spikes = misconfigured app, infinite loops, etc.

---

## Part 10: Troubleshooting

### 🔧 Problem: Private Instance Can't Access Internet

**Checklist:**

#### 1. Route Table
```
Private RT has 0.0.0.0/0 → nat-xxx?
Verify NAT Gateway ID matches.
```

#### 2. NAT Gateway State
```
VPC Console → NAT Gateways → State = "Available"?
If "Failed" or "Deleting", recreate.
```

#### 3. NAT Gateway Subnet
```
NAT Gateway in PUBLIC subnet?
(must have IGW route)
```

#### 4. NAT Gateway EIP
```
EIP attached?
EIP not used elsewhere?
```

#### 5. Security Groups
```
Private instance SG: outbound allow?
Default SG: outbound all allowed.
```

#### 6. NACL
```
Private subnet NACL: 
- Outbound allow to internet
- Inbound allow ephemeral ports for replies
```

#### 7. DNS
```
VPC DNS resolution enabled?
DNS hostnames enabled?
```

### 🔧 Problem: Can't SSH to Bastion

**Checklist:**

```
✓ Public IP on bastion?
✓ SG inbound: SSH 22 from your IP?
✓ NACL allow inbound 22?
✓ NACL allow outbound ephemeral (return SSH traffic)?
✓ Subnet has IGW route?
✓ SSH key correct? (chmod 400)
✓ Username correct? (ec2-user, ubuntu, admin)
```

### 🔧 Problem: Bastion-from-Private SSH Fails

```
✓ Private instance SG inbound: SSH from sg-bastion?
✓ Both subnets within VPC (local route)?
✓ Username and key correct?
✓ Private SG outbound allows reply?
```

### 🔧 Problem: SSM Session Manager Won't Connect

**Checklist:**

```
✓ EC2 has IAM Role with SSM permissions?
✓ SSM Agent running? (systemctl status amazon-ssm-agent)
✓ Outbound 443 to SSM endpoints?
   - ssm.region.amazonaws.com
   - ssmmessages.region.amazonaws.com
   - ec2messages.region.amazonaws.com
✓ Instance state running?
✓ Your IAM user has ssm:StartSession permission?
```

---

## Part 11: Egress-Only Internet Gateway (IPv6)

### 🤔 IPv6-এর Special Case

IPv6 এ NAT-এর concept different — সব IPv6 addresses globally unique। তাই traditional NAT-এর দরকার নেই।

**Problem:** তবু আমি চাই IPv6 instance internet-এ outbound যাক, কিন্তু inbound block।

**Solution:** **Egress-Only Internet Gateway (EIGW)**।

### 🚪 EIGW Characteristics

- IPv6 only
- Outbound traffic allowed
- Inbound traffic blocked (stateful)
- Equivalent to NAT for IPv6
- Free (unlike NAT Gateway)

### 🛠️ Setup

```
1. Create Egress-Only Internet Gateway
2. Attach to VPC
3. Route table: ::/0 → eigw-xxx (IPv6 only)
```

**Use case:** Modern IPv6-enabled VPCs।

---

## 🎯 আজকের মূল Takeaways

1. **NAT** = private instance-কে internet outbound, inbound block
2. **NAT Gateway** = AWS managed, HA per AZ, recommended
3. **NAT Instance** = legacy, EC2-based, cost-cheap but maintenance-heavy
4. **Bastion Host** = SSH gateway to private instances (traditional)
5. **Session Manager** = modern SSH replacement, no public IP needed
6. **Multi-AZ NAT** = production HA (per public subnet)
7. **NAT cost = hourly + data** (data transfer expensive)
8. **VPC Endpoints** save NAT cost for AWS services
9. **Source/Dest check** must be disabled for NAT Instance
10. **Bastion best practices:** restricted SG, MFA, audit, hardening

---

## 📝 Self-check Questions

১. NAT কেন দরকার?
২. NAT Gateway public subnet-এ থাকে কেন?
৩. NAT Gateway-এর HA কীভাবে design করবেন?
৪. NAT Instance-এ source/destination check কেন disable?
৫. Bastion Host-এর primary purpose কী?
৬. Session Manager-এ SSH key লাগে কি?
৭. Bastion vs Session Manager — কোনটা preferred এখন?
৮. NAT Gateway-এ data transfer-এ charge হয়?
৯. Single NAT vs Multi-AZ NAT — pros/cons?
১০. Egress-Only IGW কীসের জন্য?
১১. Bastion SG-এ SSH source কী হওয়া উচিত?
১২. Private instance থেকে S3-এ পাঠাতে NAT use cost কেন?
১৩. SSM Agent কীভাবে কাজ করে (inbound vs outbound)?
১৪. Bastion-এ private key রাখা bad practice কেন?
১৫. SG vs NACL — bastion-এ কোনটা use?

---

## 💡 Pro Tips

- **Production-এ NAT Gateway**, NAT Instance avoid
- **Per-AZ NAT** for true HA
- **Session Manager > Bastion** modern setups-এ
- **VPC Endpoints** + NAT = optimal cost
- **Bastion strict SG** — source = office IP only
- **Audit logs** SSM-এ enable, S3-এ archive
- **MFA on bastion** mandatory production-এ
- **NAT Gateway monitoring** — data transfer alerts
- **Source/dest check** NAT Instance-এ disable, ভুলবেন না
- **Schedule dev environment NAT** off-hours

---

## 🎨 Quick Decision Guide

```
Need outbound internet from private subnet?
└── Production? → NAT Gateway (HA per AZ)
└── Dev/Test? → Single NAT Gateway or NAT Instance

Need to SSH to private instances?
└── Modern setup? → Session Manager
└── Legacy/specific need? → Bastion Host

Cost optimization for NAT?
└── Use VPC Endpoints (S3, DynamoDB)
└── Schedule dev NAT off-hours
└── Monitor data transfer
```

---

## 🚨 Real-world Stories

**Story 1:** Startup used single NAT Gateway, AZ-1a went down. All apps in 3 AZs lost internet for 4 hours. After incident, moved to per-AZ NAT। Cost increased $64/month, but never had outage again।

**Moral:** HA is worth the cost.

**Story 2:** Developer used Bastion Host, SSH key leaked via developer's laptop being stolen। Attacker used key to access private network। Fortunately, MFA caught the access। Switched to Session Manager next week।

**Moral:** SSH keys are vulnerability. Session Manager + IAM safer।

**Story 3:** App was downloading 5 TB/month from public APIs through NAT Gateway। NAT data transfer bill: $225/month। Just for NAT! Switched to VPC Endpoint where possible, cached responses। Bill dropped to $40/month।

**Moral:** Monitor NAT data, optimize traffic patterns।

**Story 4:** NAT Instance used as both NAT and Bastion (cost saving)। Single point of failure — when patched, both NAT and Bastion went down। Production app couldn't update software, support couldn't SSH।

**Moral:** Don't combine critical services in production।

---
