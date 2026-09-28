
# 📚 Day 14 — Network Design Patterns + Module 2 Revision

**সময়:** ১.৫ ঘণ্টা | **Module:** ২ (VPC Design & Network Architecture) — শেষ দিন

## 🎯 আজকের লক্ষ্য
- 3-Tier Architecture pattern গভীরে
- Hub-and-Spoke design
- Multi-VPC strategies
- High Availability principles
- Disaster Recovery network design
- Module 2-এর পুরো revision
- Real-world architecture decisions

---

## Part 1: Architecture Patterns — কেন Pattern?

### 🤔 Pattern কেন?

**Software development-এ design patterns আছে।** Networking-এও।

Pattern = proven solution to common problems।

প্রতিবার নতুন করে চিন্তা না করে established patterns follow করলে:
- Faster design
- Fewer mistakes
- Industry standard
- Easier collaboration

---

## Part 2: 3-Tier Architecture — Classic Pattern

### 🏛️ Concept

**Application কে ৩ layer-এ ভাগ:**

1. **Presentation Tier (Web)** — User interaction
2. **Application Tier (App)** — Business logic
3. **Data Tier (DB)** — Storage

প্রতিটা tier আলাদা subnet-এ। নিরাপত্তা ও scalability-র জন্য।

### 🏗️ Network Layout

```
                    Internet
                       │
                       ▼
                ┌──────────┐
                │   IGW    │
                └─────┬────┘
                      │
        ┌─────────────┼─────────────┐
        │ Public Subnet (per AZ)    │
        │  - Application Load       │
        │    Balancer (ALB)         │
        │  - NAT Gateway            │
        └─────────────┬─────────────┘
                      │
        ┌─────────────┼─────────────┐
        │ Private Subnet - App Tier │
        │  - EC2/ECS application    │
        │  - Auto Scaling Group     │
        └─────────────┬─────────────┘
                      │
        ┌─────────────┼─────────────┐
        │ Private Subnet - DB Tier  │
        │  - RDS / Aurora           │
        │  - ElastiCache            │
        │  - Multi-AZ replica       │
        └───────────────────────────┘
```

### 🛡️ Security Layers

প্রতিটা tier আলাদা SG:

#### Web Tier (Public Subnet):
```
sg-alb (Application Load Balancer):
Inbound:
- HTTP (80) from 0.0.0.0/0
- HTTPS (443) from 0.0.0.0/0

Outbound:
- TCP 8080 to sg-app
```

#### App Tier (Private Subnet):
```
sg-app:
Inbound:
- TCP 8080 from sg-alb (only ALB)

Outbound:
- TCP 3306 to sg-db
- HTTPS to 0.0.0.0/0 (via NAT for updates)
```

#### Data Tier (Private Subnet):
```
sg-db:
Inbound:
- TCP 3306 from sg-app

Outbound:
- (nothing or restricted)
```

### 🎯 Why This Pattern Works

**1. Separation of Concerns:**
- Each tier focused on one responsibility
- Independent scaling
- Independent deployment

**2. Defense in Depth:**
- Public users only reach ALB
- ALB only talks to App
- App only talks to DB
- Multiple firewalls breach

**3. High Availability:**
- Multi-AZ deployment
- Auto Scaling per tier
- Failover mechanism

**4. Cost Optimization:**
- Different instance types per tier
- Database might use RI (long-term)
- App tier might use Spot

### 📋 Implementation Checklist

```
☐ VPC with /16 CIDR
☐ 3 AZs minimum
☐ 9 subnets (3 tiers × 3 AZs)
☐ IGW attached
☐ NAT Gateway per AZ (HA)
☐ Route tables per tier
☐ Security Groups per role
☐ ALB in public subnets
☐ Auto Scaling for App tier
☐ RDS Multi-AZ for DB tier
☐ VPC Endpoints (S3, etc.)
☐ Session Manager (no bastion)
```

---

## Part 3: Hub-and-Spoke Architecture

### 🌟 Concept

**একটা central VPC (Hub) যা multiple VPCs (Spokes)-এর সাথে connect।**

ভাবুন একটা চাকা — center-এ hub, চারপাশে spokes।

### 🏗️ Architecture

```
                    Hub VPC
                  (Central)
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    ┌───▼───┐      ┌──▼──┐        ┌──▼──┐
    │Spoke 1│      │Spoke│        │Spoke│
    │ VPC   │      │  2  │        │  3  │
    │       │      │     │        │     │
    └───────┘      └─────┘        └─────┘
   Application   Application   Application
```

### 🎯 Use Cases

**Scenario 1: Multi-Account Organization**

```
Hub VPC (Networking Account):
- Shared services
- Active Directory
- Logging
- Security tools
- Centralized firewall

Spoke VPCs (Application Accounts):
- Production app
- Dev/Staging
- Data analytics
- Each isolated, but accesses shared services
```

**Scenario 2: Multi-Environment**

```
Hub VPC:
- VPN/Direct Connect to on-premise
- DNS resolver
- Monitoring infrastructure

Spokes:
- Production VPC
- Staging VPC
- Development VPC
```

### 🔗 Connection Methods

**Option 1: VPC Peering**
- Direct VPC-to-VPC connection
- Non-transitive (Spoke-to-Spoke needs peering)
- Mesh complexity grows

**Option 2: Transit Gateway** (better for hub-spoke)
- Single point connecting all VPCs
- Transitive routing
- Module 6-এ details

### 🆚 Hub-Spoke vs Mesh

#### Mesh (Direct All-to-All)

```
VPC-A ←→ VPC-B
  ↑↓      ↑↓
VPC-D ←→ VPC-C
```

**Connections needed:** N(N-1)/2
- 3 VPCs: 3 connections
- 4 VPCs: 6 connections
- 10 VPCs: 45 connections

**Problem:** Doesn't scale।

#### Hub-Spoke

```
VPC-A          VPC-B
   ↘          ↙
      Hub VPC
   ↗          ↖
VPC-D          VPC-C
```

**Connections needed:** N (one per spoke)
- 10 VPCs: 10 connections (linear)

**Better at scale।**

### 📊 Hub-Spoke Benefits

**1. Centralized Management**
- One firewall in hub
- One DNS resolver
- One monitoring point

**2. Cost Efficient**
- Shared services not duplicated
- Single Direct Connect
- Centralized NAT

**3. Compliance**
- All traffic through hub for inspection
- Audit centralized

**4. Security**
- Hub enforces policies
- Spokes isolated from each other (default)

---

## Part 4: Multi-AZ Architecture for HA

### 🎯 Why Multi-AZ?

**AZ Failure Scenarios:**
- Power outage
- Natural disaster
- AWS infrastructure issue

**Single AZ:** Single point of failure.

### 🏗️ Multi-AZ Pattern

```
       Region: ap-south-1 (Mumbai)
       │
       ├── AZ-1a
       │   ├── Web (subnet)
       │   ├── App (subnet)
       │   └── DB (subnet)
       │
       ├── AZ-1b
       │   ├── Web (subnet)
       │   ├── App (subnet)
       │   └── DB (subnet)
       │
       └── AZ-1c
           ├── Web (subnet)
           ├── App (subnet)
           └── DB (subnet)
```

### 📋 HA Components

#### Load Balancer (ALB)
- Multi-AZ by default
- Routes to healthy targets
- AZ fail = automatic failover

#### Auto Scaling Group
- Multi-AZ subnets
- AZ fail = launches in healthy AZ
- Maintains desired capacity

#### RDS Database
- Multi-AZ deployment
- Synchronous replication to standby AZ
- Auto failover on primary failure
- ~60-120 seconds switchover

#### NAT Gateway
- Per-AZ (best practice)
- AZ fail = only that AZ affected
- Other AZs use their own NAT

### ⚖️ Trade-offs

**More AZs = More HA, More Cost**

| Setup | Cost | HA Level |
|---|---|---|
| 1 AZ | Lowest | None (AZ fail = all down) |
| 2 AZs | Moderate | Good (AZ fail = 50% impact) |
| 3 AZs | Higher | Excellent (AZ fail = 33% impact) |

**Production:** 3 AZs recommended।

---

## Part 5: Multi-Region Architecture

### 🌍 Why Multi-Region?

**Use cases:**
1. **Global users** — low latency from multiple regions
2. **Disaster Recovery** — entire region failure
3. **Compliance** — data residency requirements
4. **High Availability** — beyond AZ level

### 🏗️ Multi-Region Patterns

#### Pattern 1: Active-Passive (Disaster Recovery)

```
Primary Region (Mumbai)
├── Production traffic
└── All users

Backup Region (Singapore)
├── Standby infrastructure
├── Data replication from Mumbai
└── Activated if Mumbai fails
```

**Setup:**
- Primary: full setup, takes traffic
- Backup: minimal infrastructure, ready to scale
- Data: cross-region replication
- DNS: failover routing

**RTO/RPO:**
- RTO (Recovery Time Objective): minutes to hours
- RPO (Recovery Point Objective): seconds to minutes

#### Pattern 2: Active-Active

```
Mumbai Region
├── Asian users
└── 50% traffic

US East Region
├── American users
└── 50% traffic

Both regions serve traffic simultaneously
```

**Setup:**
- Both regions full deployment
- Geo-routing via Route 53
- Cross-region database sync
- More expensive but better UX

#### Pattern 3: Pilot Light

```
Primary Region: full setup
Backup Region: 
- Minimal compute (just enough for restore)
- Database replication ongoing
- Quick scale-up on disaster
```

Cheaper than active-passive, slower recovery।

#### Pattern 4: Warm Standby

```
Primary: full
Backup: scaled-down version (reduced capacity)
On disaster: scale up
```

Middle ground।

### 🔄 Cross-Region Connectivity

**Option 1: VPC Peering**
- Cross-region peering supported
- Encrypted traffic
- Use private IPs

**Option 2: Transit Gateway Peering**
- Hub-spoke across regions
- Better for complex setups

**Option 3: PrivateLink + VPN**
- Specific service sharing

### 💰 Multi-Region Cost

**Significantly higher:**
- Duplicate infrastructure
- Cross-region data transfer ($0.02/GB)
- Database replication cost
- Multiple managed services

**Worth it for:** Critical workloads, global business।

---

## Part 6: Disaster Recovery Strategies

### 🚨 4 DR Strategies (AWS Defined)

#### 1. Backup & Restore
- **RTO:** Hours to days
- **RPO:** Hours
- **Cost:** Lowest
- **How:** Backups in S3/Glacier, manual restore in DR region

**Use:** Non-critical workloads।

#### 2. Pilot Light
- **RTO:** Tens of minutes
- **RPO:** Minutes
- **Cost:** Low
- **How:** Critical components running in DR, scale up on disaster

**Use:** Important but not critical।

#### 3. Warm Standby
- **RTO:** Minutes
- **RPO:** Seconds
- **Cost:** Medium-high
- **How:** Scaled-down full version in DR, scale up

**Use:** Important business apps।

#### 4. Multi-Site Active-Active
- **RTO:** Real-time/zero
- **RPO:** Real-time/zero
- **Cost:** Highest
- **How:** Both regions live, serving traffic

**Use:** Mission-critical, financial, healthcare।

### 📊 DR Strategy Comparison

| Strategy | RTO | RPO | Cost | Use Case |
|---|---|---|---|---|
| Backup/Restore | Hours-days | Hours | $ | Non-critical |
| Pilot Light | Tens of min | Min | $$ | Important |
| Warm Standby | Min | Sec | $$$ | Business critical |
| Active-Active | 0 | 0 | $$$$ | Mission critical |

---

## Part 7: Common VPC Patterns Summary

### Pattern 1: Single VPC, Multi-AZ

**Best for:**
- Small to medium apps
- Single team/project
- Simple architecture

**Components:**
- 1 VPC, 3 AZs
- 3-tier subnets
- ALB, ASG, RDS Multi-AZ

### Pattern 2: Multiple VPCs (Per Environment)

**Best for:**
- Complete isolation
- Compliance requirements
- Different teams

**Components:**
- Prod VPC, Staging VPC, Dev VPC
- Each fully independent
- Optional peering for shared services

### Pattern 3: Hub-and-Spoke

**Best for:**
- Multi-account organization
- Centralized services
- Large enterprise

**Components:**
- Hub VPC (shared services)
- Multiple spoke VPCs
- Transit Gateway for connectivity

### Pattern 4: Hybrid Cloud

**Best for:**
- Migration scenarios
- Legacy + cloud workloads
- Compliance/data residency

**Components:**
- AWS VPC
- VPN/Direct Connect to on-premise
- Resolver endpoints for DNS

### Pattern 5: Multi-Region

**Best for:**
- Global users
- High availability beyond AZ
- Regional compliance

**Components:**
- Primary + DR regions
- Cross-region replication
- Route 53 failover

---

## Part 8: Module 2 Complete Revision

আজ পর্যন্ত যা শিখেছেন:

### Day 8: VPC Foundations
- VPC = isolated virtual network
- Region-bound, multi-AZ span
- CIDR notation: `IP/prefix`
- Total IPs = 2^(32-prefix)
- Private IP ranges (RFC 1918)
- AWS reserves 5 IPs per subnet
- Public vs Private subnet
- Default vs Custom VPC

### Day 9: IGW & Route Tables
- IGW = VPC's internet door
- One IGW per VPC, free, HA
- Route Table = traffic rules
- Local route always (VPC CIDR → local)
- Longest prefix match
- Subnet "public" = IGW route + public IP
- Multiple route tables per VPC
- Implicit vs explicit association

### Day 10: SG vs NACL
- SG = instance level, stateful, allow-only
- NACL = subnet level, stateless, allow + deny
- Default SG: deny inbound, allow outbound
- Default NACL: allow all
- Custom NACL: deny all initially
- NACL rules numbered, evaluated in order
- Ephemeral ports critical (NACL stateless)
- SG as source = powerful

### Day 11: NAT, Bastion, SSM
- NAT = private subnet outbound, inbound block
- NAT Gateway = managed, HA per AZ
- NAT Instance = legacy, EC2-based
- Bastion Host = traditional SSH gateway
- Session Manager = modern, no SSH/keys
- Egress-Only IGW = IPv6 outbound

### Day 12: VPC Endpoints
- Gateway Endpoint = S3, DynamoDB, free
- Interface Endpoint = most services, $0.01/hr/AZ
- PrivateLink = underlying tech
- Endpoint Policy = access control
- Private DNS = transparent integration
- Cost savings on NAT data transfer

### Day 13: DNS & IP Management
- Route 53 Resolver = VPC's DNS
- Resolver IP = VPC CIDR + 2
- Inbound endpoint = on-prem → AWS DNS
- Outbound endpoint = AWS → on-prem DNS
- Private Hosted Zone = internal DNS
- DHCP Option Set = VPC DNS/NTP config
- EIP = static public IPv4 ($3.65/month if unattached)
- IPv6 = free, vast addresses
- Public IPv4 charged since 2025

### Day 14: Architecture Patterns (Today)
- 3-Tier = Web/App/DB separation
- Hub-and-Spoke = central + peripherals
- Multi-AZ = AZ-level HA
- Multi-Region = region-level HA
- DR strategies = 4 types

---

## Part 9: Architecture Decision Framework

আপনার application-এর জন্য কী choose করবেন?

### 🎯 Decision Tree

```
Application Size?
├── Small (< 10 users) → Single VPC, single AZ (POC only)
├── Medium → Single VPC, multi-AZ (3-tier)
└── Large → Multi-VPC (Hub-Spoke)

Geographic Distribution?
├── Single country → Single region, multi-AZ
├── Continental → Multi-AZ, optional 2nd region for DR
└── Global → Multi-region active-active

Compliance Requirements?
├── None → Standard architecture
├── Data residency → Multi-region with restrictions
└── Regulated industry → Hub-spoke with central inspection

Budget?
├── Tight → Single AZ, On-Demand, no DR
├── Moderate → Multi-AZ, mixed pricing, basic DR
└── Generous → Multi-region, active-active, full DR

Existing Infrastructure?
├── All cloud → Pure VPC architecture
├── Hybrid → VPN/Direct Connect, Resolver endpoints
└── Migration → Phased hybrid approach
```

### 📋 Standard Production Setup

**Recommended for most apps:**

```
✓ Single Region (with DR planning)
✓ 3 AZs
✓ Custom VPC (10.0.0.0/16)
✓ 9 subnets (3 tiers × 3 AZs)
✓ IGW + NAT Gateway per AZ
✓ ALB for traffic distribution
✓ Auto Scaling Groups
✓ RDS Multi-AZ
✓ S3 Gateway Endpoint
✓ Interface Endpoints (SSM, KMS, etc.)
✓ Session Manager (no bastion)
✓ Security Groups per role
✓ NACLs default (or custom for compliance)
✓ VPC Flow Logs enabled
✓ CloudWatch monitoring
```

---

## Part 10: Cost Optimization Summary

### 💰 Network Costs (Mumbai region approx.)

| Component | Cost |
|---|---|
| VPC | Free |
| Subnets | Free |
| IGW | Free (data transfer charged) |
| NAT Gateway | $0.045/hr + $0.045/GB |
| NAT Instance | EC2 cost only |
| EIP (unattached) | $0.005/hr |
| EIP (attached, since 2025) | $0.005/hr |
| Public IPv4 (auto-assigned) | $0.005/hr |
| Gateway Endpoint | Free |
| Interface Endpoint | $0.01/hr/AZ + $0.01/GB |
| Route 53 query | $0.40/million |
| Data transfer (cross-AZ) | $0.01/GB |
| Data transfer (cross-region) | $0.02/GB |
| Data transfer (out internet) | $0.09/GB (after free tier) |

### 🎯 Optimization Strategies

**1. Use Gateway Endpoints**
- S3, DynamoDB free
- Avoid NAT data charges
- Significant savings

**2. Right-size NAT Gateways**
- Per-AZ HA worth it for prod
- Single NAT for dev/test
- Schedule down off-hours

**3. Reduce Public IPv4 Usage**
- Use IPv6 where possible
- Audit unused EIPs
- Use private endpoints

**4. Optimize Cross-AZ Traffic**
- Keep tiers within same AZ when possible
- Use VPC Endpoints for AWS services

**5. Monitor Data Transfer**
- VPC Flow Logs analysis
- CloudWatch metrics
- Cost Explorer regular review

---

## Part 11: Security Best Practices Summary

### 🛡️ Defense in Depth Checklist

```
☐ VPC level: 
  - Custom VPC (not default)
  - Specific CIDR planning
  - Document IP allocation

☐ Subnet level:
  - Public/private separation
  - Multiple AZs
  - NACL rules where needed

☐ Network level:
  - Security Groups per role
  - Least privilege rules
  - SG as source (not IP)
  - SSH restricted to specific IPs

☐ Service level:
  - Block Public Access (S3)
  - Encryption at rest/transit
  - VPC Endpoint policies
  - IAM least privilege

☐ Access level:
  - Session Manager (no bastion)
  - MFA enforced
  - Rotate credentials
  - Audit logs

☐ Monitoring:
  - VPC Flow Logs enabled
  - CloudWatch alarms
  - GuardDuty for threats
  - Config for compliance
```

---

## 📝 Module 2 Final Self-check (২০টা প্রশ্ন)

১. VPC কোন level-এ scope করে — Region, AZ, Account?
২. একটা subnet multiple AZ-এ থাকতে পারে?
৩. AWS প্রতি subnet-এ কয়টা IP reserve করে?
৪. `10.0.0.0/16`-এ কতগুলো IP?
৫. Public Subnet-এর ৩টা condition কী?
৬. IGW per VPC কয়টা attach হয়?
৭. Local route delete করা যায়?
৮. Longest prefix match কী?
৯. SG stateful বলতে কী বোঝায়?
১০. NACL stateless মানে কী?
১১. SG-এ deny rule সম্ভব?
১২. NAT Gateway কোন subnet-এ থাকে?
১৩. Per-AZ NAT কেন important?
১৪. Session Manager কীভাবে SSH-এর চেয়ে secure?
১৫. Gateway vs Interface Endpoint — মূল পার্থক্য?
১৬. S3 Gateway Endpoint কত cost?
১৭. Private Hosted Zone কী?
১৮. Outbound Resolver Endpoint কখন দরকার?
১৯. EIP unattached থাকলে কী হয়?
২০. Hub-and-Spoke vs Mesh — কোনটা scalable?

---

## 🏆 Module 2 Completion Checklist

```
☐ VPC concept clear (region, AZ, isolation)
☐ CIDR notation comfortable (subnet math)
☐ IGW & Route Tables understand
☐ Public/Private subnet difference clear
☐ Security Group rules can write
☐ NACL vs SG difference clear
☐ NAT Gateway HA design know
☐ Bastion vs Session Manager comparison
☐ VPC Endpoints can choose right type
☐ DNS resolution flow understand
☐ DHCP options purpose know
☐ EIP cost implications clear
☐ IPv6 basics understand
☐ 3-tier architecture can design
☐ Hub-spoke pattern know
☐ DR strategies aware
☐ Cost optimization techniques
☐ Security best practices internalized
```

---

## 🎉 Congratulations!

**Module 2 Complete!**

৭ দিনে আপনি শিখেছেন:
- Virtual Private Cloud foundation
- Subnet design ও routing
- Network security (SG + NACL)
- NAT, Bastion, Session Manager
- VPC Endpoints + PrivateLink
- DNS ও IP management
- Architecture patterns

এখন আপনি একটা **production-grade VPC design** করতে পারবেন।

---

## 🚀 সামনে কী?

**Module 3: Application Deployment on EC2 with systemd** (Day 15-21)

- User Data scripts ও cloud-init
- SSM Session Manager (more depth)
- IAM Instance Profile
- CloudWatch Agent
- systemd service management
- Nginx reverse proxy
- Application stack deployment
- CodeDeploy ও CI/CD

Module 1, 2 = **infrastructure foundation**
Module 3 = **practical deployment**

---

## 💪 Optional Project (Practice)

আপনার শেখা একসাথে apply করতে চান?

**Mini Project: Build a 3-tier VPC**

```
1. VPC: 10.0.0.0/16, Mumbai
2. 6 subnets: 2 public, 2 app, 2 db (in 2 AZs)
3. IGW attached
4. NAT Gateway in 1 public subnet
5. Route Tables: public-rt, private-rt
6. Security Groups: sg-alb, sg-app, sg-db
7. Launch a t3.micro in app subnet
8. Verify: from app instance, can `curl google.com`? (via NAT)
9. Use Session Manager to access (no SSH)
10. Add S3 Gateway Endpoint, verify route
11. **Cleanup**: delete everything to avoid charges!
```

এই project-এ Day 8-14 সব concept practical experience হবে।

---

## 🎓 Module 2 Architecture Diagram (Final Reference)

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
       AZ-1a              AZ-1b           AZ-1c
       │                    │               │
   ┌───▼────────┐    ┌─────▼─────┐    ┌────▼─────┐
   │ Public-1a  │    │ Public-1b │    │Public-1c │
   │ (10.0.1/24)│    │(10.0.2/24)│    │(10.0.3/24)│
   │            │    │           │    │          │
   │ ALB        │    │ ALB       │    │ ALB      │
   │ NAT-1a     │    │ NAT-1b    │    │ NAT-1c   │
   └─────┬──────┘    └─────┬─────┘    └─────┬────┘
         │                 │                 │
   ┌─────▼──────┐    ┌─────▼─────┐    ┌─────▼────┐
   │ App-1a     │    │ App-1b    │    │ App-1c   │
   │(10.0.11/24)│    │(10.0.12/24)│   │(10.0.13/24)│
   │            │    │           │    │          │
   │ EC2 (ASG)  │    │ EC2 (ASG) │    │ EC2 (ASG)│
   └─────┬──────┘    └─────┬─────┘    └─────┬────┘
         │                 │                 │
   ┌─────▼──────┐    ┌─────▼─────┐    ┌─────▼────┐
   │ DB-1a      │    │ DB-1b     │    │ DB-1c    │
   │(10.0.21/24)│    │(10.0.22/24)│   │(10.0.23/24)│
   │            │    │           │    │          │
   │ RDS Master │    │RDS Standby│    │  Replica │
   └────────────┘    └───────────┘    └──────────┘
   
   VPC: prod-vpc (10.0.0.0/16)
   Endpoints: S3 (Gateway), SSM (Interface), KMS (Interface)
   Session Manager: enabled (no bastion)
   VPC Flow Logs: enabled to CloudWatch
```

এটা production-grade reference architecture। মনে রাখুন।

---

## 💡 Final Pro Tips for Module 2

- **VPC design first**, then app deployment
- **3 AZs always** for production
- **Separate tiers** with Security Groups
- **No public IP** unless absolutely needed
- **Endpoints over NAT** for AWS services
- **Session Manager** instead of bastion
- **Document everything** — IP allocation, SG rules, route tables
- **Monitor with Flow Logs** — invaluable for security
- **Cost review monthly** — surprises avoid
- **Tag religiously** — cost allocation, ownership

---

## 🚨 Remember These Stories

1. **Story:** Small `/24` VPC, ran out of IPs in 6 months → migration nightmare
   **Lesson:** Start with `/16`

2. **Story:** Single NAT Gateway, AZ failure → all apps internet-less
   **Lesson:** Per-AZ NAT for production

3. **Story:** Default SG outbound all-allow → compromised instance exfiltrated data
   **Lesson:** Restrict outbound

4. **Story:** SSH 0.0.0.0/0 with weak password → crypto mining bot
   **Lesson:** Restrict SSH to specific IPs

5. **Story:** S3 traffic via NAT, $2,500/month → added Gateway Endpoint, free
   **Lesson:** Endpoints save money

6. **Story:** Bastion Host SSH key leaked → security breach
   **Lesson:** Session Manager + IAM safer

7. **Story:** Custom DHCP only on-prem DNS → AWS service DNS broken
   **Lesson:** Don't replace, supplement

---
