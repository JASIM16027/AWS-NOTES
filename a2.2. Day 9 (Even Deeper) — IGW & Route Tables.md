
# 📚 Day 9 — Internet Gateway & Route Tables

**সময়:** ১.৫ ঘণ্টা | **Module:** ২ (VPC Design & Network Architecture) — Day 2

## 🎯 আজকের লক্ষ্য
- Internet Gateway (IGW) কী ও কীভাবে কাজ করে গভীরে বুঝবেন
- Route Tables-এর architecture ও routing logic শিখবেন
- Main Route Table vs Custom Route Table পার্থক্য
- Route priority ও longest prefix match
- Subnet association mechanism
- কীভাবে subnet "public" হয় technically
- Real-world routing scenarios

---

## Part 1: Networking Refresher — Routing কী?

VPC-র Internet Gateway ও Route Table বুঝতে হলে general "routing" concept বুঝতে হবে।

### 🛣️ Routing in Real Life

ভাবুন আপনি Dhaka থেকে Chittagong গাড়ি চালাচ্ছেন। প্রতিটা intersection-এ একটা sign post:

```
Intersection 1:
→ Sylhet
→ Comilla
→ Chittagong  (এই দিকে যাব)
```

আপনি destination match করে direction choose করেন।

**Network-এও same logic:**
- প্রতিটা router-এর কাছে একটা "routing table" আছে
- Packet আসলে destination IP দেখে
- Routing table-এ match করে কোন direction-এ পাঠাবে decide করে

### 🌐 Internet-এ Packet Journey

আপনি Dhaka থেকে `google.com` (যে server US-এ) visit করছেন:

```
Your Laptop
    │ (Packet: "send to google.com")
    ▼
Home Router
    │ (Lookup: where to send?)
    ▼
ISP Router (Bangladesh)
    │ 
    ▼
International Gateway
    │
    ▼
Submarine Cable
    │
    ▼
US ISP Router
    │
    ▼
Google's Network
    │
    ▼
google.com Server
```

প্রতিটা hop-এ routing decision হচ্ছে। AWS VPC-তেও same concept।

---

## Part 2: Internet Gateway (IGW)

### 🚪 IGW কী?

**Internet Gateway = VPC-র একটা "gateway" যেটা internet-এর সাথে connection দেয়।**

VPC by default isolated — কেউ ভেতরে আসতে পারে না, ভেতর থেকে কেউ বের হতে পারে না। IGW attach করলেই সেই isolation break হয় (controlled way-তে)।

### 🏛️ Analogy: Office Building Gate

ভাবুন আপনার gated community-র একটাই main gate। সেই gate ছাড়া বাইরে যাওয়া বা ভেতরে আসা অসম্ভব।

- **Gate বন্ধ থাকলে:** কেউ আসা-যাওয়া করতে পারবে না
- **Gate খুলে দিলে:** Authorized লোক ভেতরে-বাইরে যেতে পারবে
- **Gate-এ সবসময় security guard:** কে আসছে check করে

VPC-র IGW সেই gate-এর মতো।

### 🧬 IGW-এর Architecture

**Important characteristics:**

**১. Highly Available**
- AWS internally redundant
- Single point of failure না
- Multi-AZ automatically

**২. Horizontally Scaled**
- Traffic যত বাড়ুক, automatically scale
- Bandwidth bottleneck না

**৩. No Bandwidth Constraint**
- Unlimited throughput
- AWS manages all infrastructure

**৪. Free**
- IGW তৈরি, attach — সব free
- শুধু data transfer-এ charge

**৫. One IGW per VPC**
- একটা VPC-তে একটা IGW attach করা যায়
- চাইলে detach করে অন্যটা attach করতে পারেন

### ⚙️ IGW কীভাবে কাজ করে — Technical Details

IGW একই সাথে দুইটা কাজ করে:

#### Function 1: Route Internet-bound Traffic

VPC-র কোনো instance যখন internet-এ যেতে চায়:
- Packet যায় subnet → route table check
- Route table দেখে: "0.0.0.0/0 → IGW"
- Packet IGW-তে যায়
- IGW সেটা public internet-এ forward করে

#### Function 2: NAT for Public IP-having Instances

IGW আরেকটা magic করে — **NAT (Network Address Translation)**।

**Problem:** EC2 instance-এর শুধু private IP আছে (`10.0.1.5`)। এটা internet-routable না।

**IGW-র Solution:**

```
Outgoing:
EC2 (10.0.1.5) → IGW translates → Public IP (54.203.12.45) → Internet

Incoming:
Internet → Public IP (54.203.12.45) → IGW translates → EC2 (10.0.1.5)
```

**Important:** Private IP-only instance এ NAT কাজ করে না — instance-এ Public IP/EIP থাকতে হবে।

### 🔧 IGW লাগানোর Steps (Conceptual)

**Step 1:** IGW তৈরি করুন
- VPC Console → Internet Gateways → Create
- Name দিন (যেমন `my-vpc-igw`)

**Step 2:** VPC-তে Attach করুন
- IGW select → Actions → Attach to VPC
- VPC select

**Step 3:** Route Table-এ Route যোগ করুন
- 0.0.0.0/0 → IGW
- (Subnet-কে public বানানোর জন্য — পরবর্তী section-এ details)

**Step 4:** Subnet-এ Public IP enable
- Subnet settings → "Auto-assign public IP" enable
- (অথবা launch time-এ instance-এ EIP/Public IP)

এই ৪ step ছাড়া internet access কাজ করবে না।

### 🚨 Common Mistake

**Mistake:** IGW তৈরি করেছি কিন্তু internet access নেই।

**Possible reasons:**
1. IGW VPC-তে attached নেই
2. Route Table-এ 0.0.0.0/0 → IGW route নেই
3. Instance-এ public IP নেই
4. Security Group port block করছে
5. NACL block করছে

সব ৫টা চেক না করলে issue solve হবে না।

---

## Part 3: Route Tables — VPC-র Traffic Director

### 🗺️ Route Table কী?

**Route Table = "rules" এর একটা collection যা VPC-র মধ্যে traffic কোথায় যাবে decide করে।**

প্রতিটা subnet একটা route table-এর সাথে associated থাকে। Subnet-এর instance-গুলো সেই route table follow করে।

### 📋 Route Table-এর Structure

প্রতিটা rule (route)-এ ২টা অংশ:

| Destination | Target |
|---|---|
| Where to go (CIDR) | How to get there |

**Example Route Table:**

```
| Destination     | Target              |
|-----------------|---------------------|
| 10.0.0.0/16     | local               |
| 0.0.0.0/0       | igw-12345           |
| 172.16.0.0/16   | pcx-67890 (peering) |
| 192.168.0.0/16  | vgw-11111 (VPN)     |
```

**Reading this table:**
- VPC-র ভেতরে (10.0.0.0/16) — local routing
- Internet-এ (0.0.0.0/0) — IGW দিয়ে
- 172.16.0.0/16 → peered VPC দিয়ে
- 192.168.0.0/16 → on-premise VPN দিয়ে

### 🏠 Local Route — Always Present

**প্রতিটা route table-এ একটা route automatic add হয়:**

```
Destination: <VPC CIDR>    Target: local
```

**এটা মানে কী:**
- VPC-র ভেতরের communication কোনো IGW/NAT লাগবে না
- VPC-র সব subnet একে অপরের সাথে directly যোগাযোগ করতে পারে
- এই route delete করা যায় না

**Example:**
- VPC: `10.0.0.0/16`
- Subnet A: `10.0.1.0/24`, Subnet B: `10.0.2.0/24`
- Subnet A-র instance `10.0.1.5` → Subnet B-র instance `10.0.2.10` directly যোগাযোগ
- Local route handle করে এটা

### 🎨 Main Route Table vs Custom Route Table

#### Main Route Table

**প্রতিটা VPC-র সাথে একটা "Main Route Table" automatic আসে।**

**Characteristics:**
- VPC create-এ automatic তৈরি
- VPC delete-এ automatic delete
- Default-এ কোনো subnet explicitly associated না (implicitly সবগুলো)
- Initial routes শুধু `local`

**Default behavior:**
- কোনো subnet specifically associate না করলে main route table follow করে
- "Implicit association"

#### Custom Route Table

**আপনি manually তৈরি করেন।**

**Why create:**
- Different subnet-এ different routing
- Public vs private subnet management
- Granular control

**Workflow:**
1. Custom Route Table তৈরি
2. Routes add (যেমন 0.0.0.0/0 → IGW)
3. Specific subnet-এ associate

### 🔗 Subnet-Route Table Association

**একটা subnet** = **একটা route table**

**Rules:**
- প্রতিটা subnet exactly একটা route table-এর সাথে associated
- একই route table multiple subnet-এ associate করা যায়
- Explicit association না থাকলে main route table use হয়

**Example:**

```
VPC: 10.0.0.0/16

Main Route Table (default):
- 10.0.0.0/16 → local

Custom Route Table "Public-RT":
- 10.0.0.0/16 → local
- 0.0.0.0/0 → igw-xxx

Subnets:
- Subnet A (10.0.1.0/24) — associated with Public-RT → INTERNET
- Subnet B (10.0.2.0/24) — associated with Public-RT → INTERNET
- Subnet C (10.0.11.0/24) — no explicit association → Main → NO INTERNET
- Subnet D (10.0.12.0/24) — no explicit association → Main → NO INTERNET
```

এই structure-এ:
- A ও B = Public Subnets
- C ও D = Private Subnets

---

## Part 4: কীভাবে একটা Subnet "Public" হয়?

এই concept critical। অনেকে confuse করে।

### 🤔 "Public Subnet" Defined

**Subnet "public" হয় তখনই যখন:**
1. Route Table-এ `0.0.0.0/0 → IGW` route আছে
2. Instance-এ public IP / EIP attached

**শুধু label না — actual routing।**

### 📐 Step-by-step: Public Subnet Configuration

#### Step 1: VPC তৈরি
```
VPC: my-vpc (10.0.0.0/16)
```

#### Step 2: IGW তৈরি ও Attach
```
IGW: my-vpc-igw
Status: Attached to my-vpc
```

#### Step 3: Subnet তৈরি
```
Subnet: public-1a (10.0.1.0/24, AZ-a)
```

#### Step 4: Custom Route Table তৈরি
```
Name: public-route-table
VPC: my-vpc
Routes (initially): 10.0.0.0/16 → local
```

#### Step 5: Internet Route Add করুন
```
Add: 0.0.0.0/0 → igw-xxxxx
```

এখন route table-এ:
```
| 10.0.0.0/16 | local      |
| 0.0.0.0/0   | igw-xxxxx  |
```

#### Step 6: Subnet-কে Route Table-এ Associate
```
public-1a → public-route-table
```

#### Step 7: Auto-assign Public IP Enable
```
Subnet public-1a → Modify auto-assign IP settings → Enable
```

**এই ৭ steps-এর পরে subnet সত্যিই public।**

---

## Part 5: কীভাবে একটা Subnet "Private" হয়?

### 🔒 "Private Subnet" Defined

**যে subnet-এর route table-এ IGW-র route নেই।**

### 📐 Private Subnet Configuration

#### Step 1: Subnet তৈরি
```
Subnet: private-1a (10.0.11.0/24, AZ-a)
```

#### Step 2: Custom Private Route Table তৈরি
```
Name: private-route-table
VPC: my-vpc
Routes: 10.0.0.0/16 → local
```

**এই table-এ 0.0.0.0/0 → IGW route নেই।**

#### Step 3: Subnet Associate
```
private-1a → private-route-table
```

**Done। Subnet এখন private।**

### 🔁 Private Subnet-এ Internet Access (Outbound only)

ধরুন private subnet-এর EC2 instance-এ Linux update দরকার (yum/apt update)। কিন্তু internet access নেই directly।

**Solution: NAT Gateway** (Day 11-এ details)

```
Private Route Table:
- 10.0.0.0/16 → local
- 0.0.0.0/0 → nat-gateway-xxx
```

NAT Gateway public subnet-এ থাকে। Private instance NAT-এ যায়, NAT IGW-তে।

---

## Part 6: Route Priority — Longest Prefix Match

### 🎯 Multiple Routes-এ কোনটা Win করবে?

Sometimes একটা destination-এর জন্য multiple route থাকতে পারে। কোনটা apply হবে?

**Rule: Longest Prefix Match Wins।**

### 🔢 Longest Prefix Match-এর Logic

**More specific route = higher priority।**

CIDR-এ যত বেশি `/number`, তত specific।

### Example:

```
Route Table:
| Destination       | Target    |
|-------------------|-----------|
| 0.0.0.0/0         | igw-xxx   |
| 172.16.0.0/16     | pcx-yyy   |
| 172.16.5.0/24     | vgw-zzz   |
| 172.16.5.10/32    | nat-www   |
```

Packet-এর destination: `172.16.5.10`

**কোন route match হবে?**

1. `0.0.0.0/0` — matches (everything matches this)
2. `172.16.0.0/16` — matches (within range)
3. `172.16.5.0/24` — matches (within range)
4. `172.16.5.10/32` — matches (exact)

**Longest prefix wins:** `/32` is longest → `nat-www` selected।

### Practical Example:

```
| Destination     | Target  |
|-----------------|---------|
| 10.0.0.0/16     | local   |
| 0.0.0.0/0       | igw-xxx |
| 10.0.1.5/32     | nat-yyy |
```

Traffic to:
- `10.0.1.5` → `/32` match → NAT
- `10.0.1.6` → `/16` (local) match → VPC internal
- `8.8.8.8` → `/0` match → IGW

**Use case:** Specific instance-এর traffic redirect, while VPC-র বাকি সব normal route follow।

---

## Part 7: Implicit vs Explicit Association

### 👥 Subnet Association Types

#### Implicit Association
- Subnet-এ explicit assign করেননি
- Default-এ Main Route Table follow
- "Implicit association with Main"

#### Explicit Association
- আপনি manually subnet → route table assign করেছেন
- Main বা Custom route table-এর সাথে

### 🎨 Example Scenario:

```
VPC: my-vpc

Route Tables:
1. Main RT (auto-created): 
   - 10.0.0.0/16 → local
   
2. Public RT (custom):
   - 10.0.0.0/16 → local
   - 0.0.0.0/0 → igw

3. Private RT (custom):
   - 10.0.0.0/16 → local
   - 0.0.0.0/0 → nat

Subnets:
- public-1a    → explicitly associated with Public RT
- public-1b    → explicitly associated with Public RT
- private-1a   → explicitly associated with Private RT
- private-1b   → explicitly associated with Private RT
- forgotten-1c → NO explicit association → uses Main RT (no internet!)
```

**Important Best Practice:**
**Main Route Table-এ default-এ NO IGW route রাখুন।** এটা safety net। যদি কোনো subnet ভুলে main-এ associate থাকে, accidentally public হবে না।

---

## Part 8: Route Table-এর Routes — Different Targets

Route table-এর `Target` field-এ যেগুলো হতে পারে:

### 🎯 1. local
- VPC-র internal communication
- Auto-added, can't delete
- Always present

### 🎯 2. Internet Gateway (igw-xxxxx)
- Internet access
- For public subnets

### 🎯 3. NAT Gateway (nat-xxxxx)
- Private subnet-এর outbound internet
- Day 11-এ details

### 🎯 4. NAT Instance
- Older NAT solution (EC2-based)
- AWS এখন NAT Gateway recommend করে

### 🎯 5. Virtual Private Gateway (vgw-xxxxx)
- VPN connection-এর gateway
- On-premise network-এ যাওয়ার জন্য
- Module 6-এ আসবে

### 🎯 6. VPC Peering Connection (pcx-xxxxx)
- দুই VPC connect করা
- Module 6-এ details

### 🎯 7. Transit Gateway (tgw-xxxxx)
- Multiple VPC একসাথে connect
- Module 6-এ

### 🎯 8. Network Interface (eni-xxxxx)
- Specific ENI-তে route
- Custom routing scenarios

### 🎯 9. Gateway Endpoint (vpce-xxxxx)
- S3, DynamoDB-এ private connection
- Day 12-এ details

### 🎯 10. Egress-only Internet Gateway (eigw-xxxxx)
- IPv6-এর জন্য, outbound only
- IPv4 NAT-এর IPv6 equivalent

---

## Part 9: Real-world Routing Scenarios

আসুন কিছু practical scenario দেখি।

### Scenario 1: Simple Web Application

**Setup:**
- 1 VPC, 1 IGW
- 2 public subnets (web tier)
- 2 private subnets (database tier)

**Public Route Table:**
```
| 10.0.0.0/16 | local     |
| 0.0.0.0/0   | igw-xxx   |
```
Associated: public-1a, public-1b

**Private Route Table:**
```
| 10.0.0.0/16 | local |
```
Associated: private-1a, private-1b

**Result:**
- Web servers: internet accessible
- Database: VPC-internal only (most secure)

### Scenario 2: 3-Tier with NAT for Private

**Setup:**
- Web (public), App (private), DB (private)
- App needs to update software (apt update)
- DB no internet at all

**Public RT (Web):**
```
| 10.0.0.0/16 | local   |
| 0.0.0.0/0   | igw-xxx |
```

**App-Private RT:**
```
| 10.0.0.0/16 | local   |
| 0.0.0.0/0   | nat-xxx |
```
(NAT Gateway in public subnet)

**DB-Private RT:**
```
| 10.0.0.0/16 | local |
```
(No internet, even outbound)

### Scenario 3: VPC Peering

**Setup:**
- VPC-A: `10.0.0.0/16`
- VPC-B: `10.1.0.0/16`
- Peering connection: pcx-xxx

**VPC-A Route Table (to reach B):**
```
| 10.0.0.0/16 | local   |
| 10.1.0.0/16 | pcx-xxx |
| 0.0.0.0/0   | igw-yyy |
```

**VPC-B Route Table (to reach A):**
```
| 10.1.0.0/16 | local   |
| 10.0.0.0/16 | pcx-xxx |
```

Both VPCs need explicit routes for peering to work।

### Scenario 4: Hybrid (On-Premise + AWS)

**Setup:**
- AWS VPC: `10.0.0.0/16`
- On-premise: `192.168.0.0/16`
- Connected via VPN (vgw-xxx)

**Route Table:**
```
| 10.0.0.0/16     | local    |
| 192.168.0.0/16  | vgw-xxx  |
| 0.0.0.0/0       | igw-yyy  |
```

VPC instances can reach office network।

### Scenario 5: Selective Internet Access

**Setup:**
- Most traffic via NAT
- AWS service-এ direct via Endpoint
- Specific IP via custom route

**Route Table:**
```
| 10.0.0.0/16              | local        |
| pl-xxxxx (S3 prefix list)| vpce-xxx     |
| 8.8.8.8/32               | igw-yyy      |
| 0.0.0.0/0                | nat-zzz      |
```

- S3 traffic: VPC Endpoint (cheap, private)
- Google DNS specifically: IGW
- Other internet: NAT
- VPC: local

---

## Part 10: Route Table Best Practices

### ✅ Do's

**1. Custom Route Tables Always**
- Main RT-এ critical routes না রাখুন
- প্রতি tier-এর জন্য আলাদা RT

**2. Naming Convention**
- `<env>-<tier>-rt` format
- যেমন: `prod-public-rt`, `prod-private-rt`

**3. Tier Separation**
- Public, Private (with NAT), Private (isolated)
- প্রতিটার আলাদা RT

**4. Document Routes**
- প্রতিটা route-এর comment/description
- কেন এই route দরকার

**5. Audit Regularly**
- Unnecessary routes remove করুন
- Old peering connection-এর route clean

### ❌ Don'ts

**1. Main RT-এ IGW Route**
- Accidentally subnet public হয়ে যাবে
- Safety hazard

**2. Overlapping Routes**
- Confusion সৃষ্টি করে
- Longest prefix match-এ unexpected behavior

**3. Too Wide CIDR**
- `0.0.0.0/0` use carefully
- Where possible, specific CIDR

**4. একই RT সব subnet-এ**
- Public + Private mixed
- Security risk

---

## Part 11: VPC Endpoints — Quick Preview

আজ পুরোটা না বলব, কাল-পরশু আসবে। কিন্তু route table-এর সাথে relate করে quick mention:

**VPC Endpoint** = AWS service-এ private connection (internet ছাড়া)।

**দুই type:**
- **Gateway Endpoint** (S3, DynamoDB) — Route table-এ entry add হয়
- **Interface Endpoint** (অন্য services) — ENI-based, route table-এ entry না

**Why this matters now:**
Gateway endpoint create করলে route table automatic update হয়:
```
| pl-S3 (prefix list) | vpce-xxx |
```

S3-এর traffic IGW দিয়ে না, endpoint দিয়ে private route। Cheap + secure।

Day 12-এ details।

---

## Part 12: Common Routing Mistakes & Debugging

### 🔍 Debugging Internet Connectivity

**Problem:** EC2 instance internet-এ যেতে পারছে না।

**Checklist:**

1. **Instance public IP আছে?**
   - Public subnet-এ but no public IP = no internet
   
2. **Subnet public?**
   - Route table check
   - 0.0.0.0/0 → IGW আছে?
   
3. **IGW VPC-তে attached?**
   - Detached থাকলে কাজ করবে না
   
4. **Security Group outbound allow?**
   - Default-এ all outbound allowed
   - Restrictive SG হলে problem
   
5. **NACL allow?**
   - Stateless, both inbound + outbound need explicit allow
   
6. **Instance-এর OS-level firewall?**
   - iptables, firewalld
   
7. **DNS working?**
   - VPC-এ DNS resolution enabled?

### 🔍 Common Errors

**Error 1:** "Connection timed out"
- Usually NACL or SG block
- Or no route to destination

**Error 2:** "Could not resolve hostname"
- DNS issue
- VPC DNS settings disabled

**Error 3:** "Network unreachable"
- Route missing
- IGW not attached

---

## 🎯 আজকের মূল Takeaways

1. **Internet Gateway (IGW)** = VPC-র internet door
2. **One IGW per VPC**, free, highly available
3. **IGW does NAT** for instance with public IP
4. **Route Table** = traffic rules (Destination + Target)
5. **Local route** auto-added, can't delete
6. **Main Route Table** auto-created with VPC
7. **Custom Route Table** for granular control
8. **Subnet "public"** = route table-এ IGW route + public IP
9. **Longest Prefix Match** wins
10. **Explicit > Implicit** association preferred

---

## 📝 Self-check Questions

১. একটা VPC-তে কয়টা IGW attach করা যায়?
২. IGW-তে cost আছে?
৩. `local` route delete করা যায়?
৪. একটা subnet কয়টা route table-এর সাথে associated হতে পারে?
৫. Main RT-এ subnet implicitly বা explicitly associate হয়?
৬. Longest prefix match মানে কী?
৭. কোন subnet "public" — কীভাবে decide?
৮. Public IP ছাড়া কি instance internet-এ যেতে পারে?
৯. IGW কি NAT করে?
১০. Custom RT তৈরি না করলে কী হয়?
১১. একটা RT কয়টা subnet-এ associate করা যায়?
১২. `0.0.0.0/0` route মানে কী?
১৩. VPC Peering-এর জন্য route কেমন হবে?
১৪. Egress-only IGW কীসের জন্য?
১৫. Main RT-এ IGW route রাখা bad practice কেন?

---

## 💡 Pro Tips

- **প্রতিটা VPC-তে at least ৩টা RT রাখুন:** Main (no internet), Public (IGW), Private (NAT)
- **Main RT-এ শুধু local route রাখুন** — safety net
- **RT name-এ environment + tier** include করুন
- **Document each non-local route** — কেন আছে
- **Use VPC Reachability Analyzer** — AWS tool routing debug করতে
- **CloudWatch + VPC Flow Logs** enable করুন troubleshooting-এর জন্য

---

## 🎨 Visual Summary

```
                    Internet
                       │
                       ▼
                ┌──────────────┐
                │   IGW        │
                └──────┬───────┘
                       │
                       │ (VPC attached)
                       │
        ┌──────────────┴──────────────┐
        │           VPC               │
        │      10.0.0.0/16            │
        │                             │
        │  ┌─────────────────────┐   │
        │  │ Public RT:          │   │
        │  │ 10.0.0.0/16 → local │   │
        │  │ 0.0.0.0/0 → IGW     │   │
        │  └──────────┬──────────┘   │
        │             │              │
        │  ┌──────────▼──────────┐   │
        │  │ Public Subnet       │   │
        │  │ 10.0.1.0/24         │   │
        │  │ Web Servers         │   │
        │  └─────────────────────┘   │
        │                             │
        │  ┌─────────────────────┐   │
        │  │ Private RT:         │   │
        │  │ 10.0.0.0/16 → local │   │
        │  └──────────┬──────────┘   │
        │             │              │
        │  ┌──────────▼──────────┐   │
        │  │ Private Subnet      │   │
        │  │ 10.0.11.0/24        │   │
        │  │ Databases           │   │
        │  └─────────────────────┘   │
        │                             │
        └─────────────────────────────┘
```

---

## 🚨 Real-world Story

**Story 1:** Developer একটা new subnet তৈরি করল, ভুলে main route table-এর সাথে associate রইল। Main route table-এ accidentally কেউ আগে IGW route add করেছিল। Database accidentally internet-exposed হয়ে গেল। Hacker discover করে database breach। Million-dollar incident।

**Moral:** Main Route Table-এ IGW route NEVER।

**Story 2:** Two VPC peered, কিন্তু route table-এ peering route add ভুলে গিয়েছিল। Application "VPC peering not working" complaint। ৩ ঘণ্টা debugging-এর পর realize — peering connection-এর সাথে route table-এ entry আলাদা step।

**Moral:** Peering = Connection + Routes (both required)।

---



# 📚 Day 9 (Even Deeper) — IGW & Route Tables

---

## Part 1: একটা Packet-এর জীবন (Packet Journey)

আগে এটা বুঝুন — তাহলে IGW আর Route Table-এর role সব পরিষ্কার হবে।

### 🎬 Scenario: EC2 থেকে google.com ping

আপনার EC2 instance (IP: `10.0.1.5`) থেকে `google.com` (IP: `142.250.190.46`) ping করছেন।

### Step 1: Instance Packet তৈরি করে

```
Packet Header:
├── Source IP: 10.0.1.5 (আপনার EC2)
├── Destination IP: 142.250.190.46 (Google)
└── Data: ICMP ping request
```

### Step 2: Packet Subnet Router-এ পাঠায়

প্রতিটা subnet-এ একটা **invisible router** আছে (AWS-এর internal)। সেটার IP সাধারণত subnet-এর প্রথম usable IP (যেমন `10.0.1.1`)।

```
EC2 (10.0.1.5)
    │
    │ "এই packet 142.250.190.46-এ পাঠাও"
    │
    ▼
Subnet Router (10.0.1.1)
```

### Step 3: Subnet Router Route Table Check করে

Router thinks: "Destination 142.250.190.46। Route Table-এ কোন rule match করে?"

**Route Table:**
```
| Destination     | Target  |
|-----------------|---------|
| 10.0.0.0/16     | local   |
| 0.0.0.0/0       | igw-xxx |
```

**Router-এর checking:**

- Rule 1: `10.0.0.0/16` — does `142.250.190.46` fit? 
  - Binary check: 142.250 starts with `10.0`? **No**
  - Skip
- Rule 2: `0.0.0.0/0` — does `142.250.190.46` fit?
  - `0.0.0.0/0` = "anything"
  - **Yes, match!**

**Selected target:** IGW (igw-xxx)।

### Step 4: Packet IGW-তে যায়

```
Subnet Router
    │
    │ "Target = IGW"
    │
    ▼
Internet Gateway
```

### Step 5: IGW NAT করে

**Important:** Public internet আপনার private IP `10.0.1.5` জানে না। এটা routable না।

IGW magic করে:

```
Original packet:
├── Source: 10.0.1.5 (private)
└── Destination: 142.250.190.46

After NAT translation by IGW:
├── Source: 54.203.12.45 (your instance's public IP)
└── Destination: 142.250.190.46
```

IGW একটা lookup table maintain করে:
```
Public IP            ↔   Private IP
54.203.12.45         ↔   10.0.1.5
```

### Step 6: Packet Internet-এ যায়

```
IGW
    │
    │ "Now packet has public source IP, can travel internet"
    │
    ▼
AWS Backbone Network
    │
    ▼
Public Internet
    │
    ▼
Google Server (142.250.190.46)
```

### Step 7: Google Reply পাঠায়

```
Reply packet:
├── Source: 142.250.190.46 (Google)
└── Destination: 54.203.12.45 (আপনার EC2-র public IP)
```

### Step 8: Reply IGW-তে আসে

IGW lookup করে:
```
"54.203.12.45 → কোন private IP?"
"Found: 10.0.1.5"
```

IGW reverse NAT করে:
```
After reverse NAT:
├── Source: 142.250.190.46
└── Destination: 10.0.1.5 (private IP)
```

### Step 9: Packet Subnet-এ যায়

Route table check (reverse direction):
- "Destination 10.0.1.5"
- Match: `10.0.0.0/16 → local`
- Goes to subnet 10.0.1.0/24
- Reaches EC2 `10.0.1.5`

### Step 10: EC2 Reply পায়

Ping successful!

---

### 🎯 এই Journey-তে কী শিখলেন

1. **প্রতিটা packet route table check করে**
2. **Local routing** = VPC-র ভেতরে কোনো translation নেই
3. **IGW = NAT machine** + Internet door
4. **Public IP** ছাড়া internet impossible (private IP not routable)
5. **Stateful conversation** = AWS connection track করে

---

## Part 2: IGW আরও গভীরে

### 🏗️ IGW Internally কীভাবে কাজ করে

IGW আসলে একটা **logical construct**। AWS-এর data center-এ অসংখ্য redundant network device আছে যেগুলো collectively IGW-র behavior provide করে।

```
আপনার দেখা চিত্র:
[VPC] ─── [IGW] ─── [Internet]

Reality:
[VPC] ─── [Multiple AWS routers, load balancers, NAT translators] ─── [Internet]
              ↑
         আপনি এটাকে "IGW" বলেন
```

**Implications:**
- IGW down হবে না (multiple machines আছে)
- IGW-তে bandwidth limit নেই (scale automatic)
- IGW-এ আপনার configuration কম, AWS-এর internal বেশি

### 🔍 IGW Functions — গভীরে

#### Function 1: Two-way Routing (Internet ↔ VPC)

**Outgoing direction:**
- VPC → IGW → Internet

**Incoming direction:**
- Internet → IGW → VPC (যদি route allow করে)

#### Function 2: Public IP NAT

**Static NAT (1-to-1 mapping):**
- প্রতিটা public IP-র সাথে একটা private IP map
- Persistent mapping যতক্ষণ instance চলে

#### Function 3: Connection Tracking

IGW state maintain করে:
- কোন connection active
- কোন port communication করছে
- Reply packet কোন instance-এ যাবে

### 🚪 IGW vs Other Gateways — Confusion clear করুন

AWS-এ অনেক "gateway" আছে। IGW-র সাথে confuse না:

| Gateway | Purpose |
|---|---|
| **Internet Gateway (IGW)** | VPC ↔ Internet |
| **NAT Gateway** | Private subnet → Internet (outbound only) |
| **Virtual Private Gateway (VGW)** | VPC ↔ On-premise VPN |
| **Customer Gateway (CGW)** | On-premise side of VPN |
| **Transit Gateway (TGW)** | Multiple VPC + on-premise hub |
| **Direct Connect Gateway** | VPC ↔ Direct Connect |
| **Egress-Only IGW** | IPv6 outbound only |

আজ শুধু IGW।

### 🆚 IGW vs NAT Gateway — মূল পার্থক্য

মানুষ এটা সবচেয়ে বেশি confuse করে।

| Feature | IGW | NAT Gateway |
|---|---|---|
| Direction | দুই দিক | শুধু outbound |
| Subnet placement | VPC-level | একটা subnet-এ থাকে (public) |
| For public IP instances | হ্যাঁ | না |
| For private instances | না | হ্যাঁ |
| Cost | Free | Hourly + data |
| Number per VPC | 1 | Multiple (per AZ) |

**কেন দুটোই দরকার:**
- Web server (public subnet) → IGW use
- App server (private subnet) → NAT Gateway use (which then uses IGW)

Day 11-এ NAT details।

---

## Part 3: Route Table Anatomy — Microscope-এ

### 🔬 একটা Route-এর ভেতরের details

প্রতিটা route entry-তে আসলে এই information থাকে:

```
{
  "destination_cidr": "0.0.0.0/0",
  "target_type": "internet_gateway",
  "target_id": "igw-12345abc",
  "state": "active",
  "origin": "CreateRouteTable",
  "propagated": false
}
```

### 🎭 Route Origin Types

প্রতিটা route কীভাবে এসেছে — এটা track হয়:

#### 1. CreateRouteTable
- Route table তৈরির সময় auto-added local route
- যেমন: `10.0.0.0/16 → local`

#### 2. CreateRoute
- আপনি manually add করেছেন
- যেমন: `0.0.0.0/0 → IGW`

#### 3. EnableVgwRoutePropagation
- VPN gateway থেকে auto-propagated
- BGP দিয়ে on-premise network learn

### 🔄 Route Propagation

Advanced concept, কিন্তু জানা ভালো।

**VPN-এ kale auto-route learn হয়:**

```
On-premise network advertises: 192.168.1.0/24
   ↓
VGW receives via BGP
   ↓
Route table-এ auto-add (যদি propagation enable):
192.168.1.0/24 → vgw-xxx
```

**মানে আপনি manually add করেননি, on-premise-এর router বলছে "এই network আমার কাছে আছে"।**

---

### 🏗️ Route Table Lifecycle

#### Creation
- VPC তৈরির সাথে Main RT auto
- আপনি Custom RT manually create
- Route table একটা VPC-এর সাথে bound

#### Modification
- Routes add/edit/delete
- Subnet associations change
- Tags change

#### Deletion
- Custom RT delete করা যায় (যদি কোনো subnet associated না থাকে)
- Main RT delete করা যায় না (VPC delete করতে হবে)

---

## Part 4: Route Table Algorithm — Behind the Scenes

প্রতিটা packet-এর জন্য route table কীভাবে decision নেয়?

### 🧮 The Routing Algorithm

```
function find_route(destination_ip, route_table):
    matching_routes = []
    
    for each route in route_table:
        if destination_ip matches route.cidr:
            matching_routes.append(route)
    
    if matching_routes is empty:
        drop packet (no route)
    
    # Longest prefix match
    best_match = route with highest prefix in matching_routes
    
    return best_match.target
```

### 🔍 Step-by-step Example

**Route Table:**
```
| Route ID | Destination       | Target    | Prefix Length |
|----------|-------------------|-----------|---------------|
| R1       | 10.0.0.0/16       | local     | 16            |
| R2       | 0.0.0.0/0         | igw-xxx   | 0             |
| R3       | 172.16.0.0/16     | pcx-yyy   | 16            |
| R4       | 172.16.5.0/24     | vgw-zzz   | 24            |
| R5       | 172.16.5.10/32    | nat-www   | 32            |
```

**Test 1: Packet destination = `10.0.5.20`**

Step 1: Match against each route
- R1: `10.0.0.0/16` → `10.0.5.20` starts with `10.0`? Yes ✓
- R2: `0.0.0.0/0` → matches everything ✓
- R3: `172.16.0.0/16` → `10.0...` starts with `172.16`? No ✗
- R4: `172.16.5.0/24` → No ✗
- R5: `172.16.5.10/32` → No ✗

Step 2: Matching routes = R1, R2
Step 3: Longest prefix: R1 (/16) wins over R2 (/0)
Step 4: **Target = local**

**Test 2: Packet destination = `172.16.5.10`**

Step 1: Match
- R1: No
- R2: Yes (catches everything)
- R3: `172.16.0.0/16` → `172.16` matches? Yes ✓
- R4: `172.16.5.0/24` → `172.16.5` matches? Yes ✓
- R5: `172.16.5.10/32` → exact match ✓

Step 2: Matching = R2, R3, R4, R5
Step 3: Longest prefix: R5 (/32)
Step 4: **Target = nat-www**

**Test 3: Packet destination = `172.16.5.50`**

Step 1: Match
- R3: Yes ✓
- R4: Yes ✓ (within 172.16.5.0/24)
- R5: No (only matches .10)

Step 2: Matching = R3, R4
Step 3: Longest prefix: R4 (/24)
Step 4: **Target = vgw-zzz**

---

### 🎯 Why Longest Prefix Match Matters

**Real Use Case: Specific Override**

ধরুন আপনার VPC-র সব internet traffic NAT-এ যাচ্ছে। কিন্তু একটা specific server (`10.0.1.50`) directly internet-এ যেতে চান।

```
| 10.0.0.0/16     | local   |
| 0.0.0.0/0       | nat-xxx |  ← সব internet traffic NAT-এ
| 8.8.8.8/32      | igw-yyy |  ← শুধু Google DNS direct IGW-তে
```

`/32` route specific overrides `/0` route। এই pattern advanced routing-এ ব্যবহার হয়।

---

## Part 5: Subnet Public/Private Deep Dive

### 🤔 "Public Subnet" — এটা একটা Setting?

না। AWS কোথাও "Public" বা "Private" toggle নেই subnet-এ।

**Public/Private = behavior, not configuration।**

### 🔬 Technical Reality

একটা subnet "public" তখনই যখন **৩টা condition** সব true:

#### Condition 1: VPC-তে IGW Attached
```
VPC: my-vpc
Internet Gateway: igw-xxx
Status: Attached ✓
```

#### Condition 2: Route Table-এ IGW Route
```
Subnet's Route Table:
| 0.0.0.0/0 | igw-xxx | ← এই route থাকতে হবে
```

#### Condition 3: Instance-এ Public IP
```
EC2: i-xxxxx
Public IP: 54.203.12.45 (assigned)
```

**৩টা একসাথে না হলে subnet "functionally public" না।**

### 🎭 Example: Subnet Variations

#### Variation 1: True Public Subnet
```
VPC: 10.0.0.0/16 (IGW attached)
Subnet: 10.0.1.0/24
RT: 0.0.0.0/0 → IGW ✓
Auto-assign Public IP: ON ✓
Instance: launches with public IP

Result: Internet works
```

#### Variation 2: "Public" but Instance has no Public IP
```
RT: 0.0.0.0/0 → IGW ✓
Auto-assign Public IP: OFF
Instance: no public IP

Result: NO internet (despite "public" subnet)
```

#### Variation 3: "Public" but no IGW in VPC
```
RT: 0.0.0.0/0 → IGW (but IGW detached!)
Result: route exists but doesn't work
```

#### Variation 4: True Private Subnet
```
RT: 10.0.0.0/16 → local (only)
No IGW route

Result: VPC internal only, no internet
```

### 🎨 Subnet "Auto-assign Public IP" Setting

Subnet level-এ একটা setting আছে:

```
Subnet: my-public-1a
Modify auto-assign IP settings:
☑ Enable auto-assign public IPv4 address
☐ Enable auto-assign IPv6 address
```

**Effect:** এই subnet-এ launched সব instance automatically public IP পাবে।

**Override:** Instance launch-এ override করতে পারেন (force public IP বা force private)।

---

## Part 6: Route Tables — Advanced Concepts

### 🎭 Multiple Route Tables Example

বাস্তবে production VPC-তে অনেকগুলো route table থাকে:

```
VPC: production-vpc (10.0.0.0/16)

Route Tables:
1. Main-RT (default, no internet)
   Routes:
   - 10.0.0.0/16 → local
   
2. Public-RT
   Routes:
   - 10.0.0.0/16 → local
   - 0.0.0.0/0 → igw-xxx
   Associated subnets: public-1a, public-1b, public-1c
   
3. Private-NAT-RT (for app tier with internet)
   Routes:
   - 10.0.0.0/16 → local
   - 0.0.0.0/0 → nat-1a
   - pl-S3 → vpce-s3 (S3 endpoint)
   Associated subnets: app-1a
   
4. Private-NAT-RT-1b (NAT in different AZ for HA)
   Routes:
   - 10.0.0.0/16 → local
   - 0.0.0.0/0 → nat-1b
   Associated subnets: app-1b
   
5. Isolated-RT (no internet at all)
   Routes:
   - 10.0.0.0/16 → local
   Associated subnets: db-1a, db-1b, db-1c
```

**কেন এত RT?**
- Different tier-এ different routing logic
- Multi-AZ NAT redundancy
- Security separation (DB no internet ever)
- Cost optimization (S3 endpoint avoids data transfer)

---

### 🔁 Inter-Subnet Communication

**Question:** Subnet-A (`10.0.1.0/24`) থেকে Subnet-B (`10.0.2.0/24`)-এ যেতে route table-এ কোন route লাগবে?

**Answer:** Nothing! Local route automatically handle করে।

**কীভাবে:**
- Both subnets within VPC CIDR `10.0.0.0/16`
- Local route: `10.0.0.0/16 → local`
- Subnet-A থেকে packet → Local routing → Subnet-B
- IGW, NAT কোনোটার দরকার নেই

**Restriction:** Security Group ও NACL allow করতে হবে। Route OK, কিন্তু firewall block করতে পারে।

---

### 🎯 Route Table Quotas & Limits

প্রতিটা VPC-তে limit আছে:

| Item | Default Limit |
|---|---|
| Route tables per VPC | 200 |
| Routes per route table | 50 (can request 1,000) |
| Subnets per route table | Unlimited (but each subnet 1 RT) |
| Route propagation per RT | 50 |

বেশিরভাগ ব্যবহারকারীর জন্য default যথেষ্ট।

---

## Part 7: Subnet Association Mechanics

### 👫 Association Types

#### Explicit Association

আপনি manually link করেছেন:

```
Action: VPC Console → Subnet → Edit Route Table Association → Choose RT

Result:
Subnet "public-1a" → Route Table "Public-RT"
Status: Explicit
```

#### Implicit Association

আপনি কিছু করেননি:

```
Subnet "forgotten-subnet" 
- No explicit RT chosen
- Falls back to Main RT
Status: Implicit (with Main)
```

### 🔁 Changing Association

একটা subnet-এর route table যেকোনো সময় change করা যায়:

**Steps:**
1. Subnet select
2. Route Table tab
3. Edit Route Table Association
4. New RT choose
5. Save

**Effect:** Immediate। Existing connections potentially affected।

**Caveat:** এই change-এ existing connections drop হতে পারে route-এর behavior change হলে।

---

## Part 8: Real-world Architecture — Step-by-step

আসুন একটা production-grade VPC step-by-step build করি (conceptually)।

### 🎯 Goal: Highly Available Web Application

**Requirements:**
- Web tier (public, internet-facing)
- App tier (private, internet via NAT for updates)
- DB tier (private, NO internet ever)
- 3 AZ for HA
- Mumbai region

### 📐 Step 1: VPC

```
Create VPC:
- Name: prod-vpc
- CIDR: 10.0.0.0/16
- Region: ap-south-1
```

### 🚪 Step 2: Internet Gateway

```
Create IGW:
- Name: prod-igw

Attach to VPC:
- prod-igw → prod-vpc
```

### 🏘️ Step 3: Subnets (9 total — 3 tiers × 3 AZ)

**Public Tier (3):**
```
public-1a: 10.0.1.0/24, AZ ap-south-1a
public-1b: 10.0.2.0/24, AZ ap-south-1b
public-1c: 10.0.3.0/24, AZ ap-south-1c
```

**App Tier (3):**
```
app-1a: 10.0.11.0/24, AZ ap-south-1a
app-1b: 10.0.12.0/24, AZ ap-south-1b
app-1c: 10.0.13.0/24, AZ ap-south-1c
```

**DB Tier (3):**
```
db-1a: 10.0.21.0/24, AZ ap-south-1a
db-1b: 10.0.22.0/24, AZ ap-south-1b
db-1c: 10.0.23.0/24, AZ ap-south-1c
```

### 🗺️ Step 4: Route Tables

**Public RT:**
```
Name: prod-public-rt
Routes:
- 10.0.0.0/16 → local
- 0.0.0.0/0 → prod-igw
Associated: public-1a, public-1b, public-1c
```

**App RT (one per AZ for NAT redundancy):**
```
Name: prod-app-rt-1a
Routes:
- 10.0.0.0/16 → local
- 0.0.0.0/0 → nat-1a
Associated: app-1a

Name: prod-app-rt-1b
Routes:
- 10.0.0.0/16 → local
- 0.0.0.0/0 → nat-1b
Associated: app-1b

Name: prod-app-rt-1c
Routes:
- 10.0.0.0/16 → local
- 0.0.0.0/0 → nat-1c
Associated: app-1c
```

**DB RT (no internet at all):**
```
Name: prod-db-rt
Routes:
- 10.0.0.0/16 → local
Associated: db-1a, db-1b, db-1c
```

### 🌐 Step 5: NAT Gateways (one per AZ for HA)

```
NAT Gateway 1a:
- Name: nat-1a
- Subnet: public-1a
- EIP: required

NAT Gateway 1b:
- Subnet: public-1b
NAT Gateway 1c:
- Subnet: public-1c
```

**Why per AZ?** AZ fail করলে NAT-ও fail। Multi-AZ NAT = better HA।

### 📊 Final Architecture

```
                     Internet
                        │
                        ▼
                ┌──────────────┐
                │   IGW        │
                └──────┬───────┘
                       │
     ┌─────────────────┼─────────────────┐
     │ AZ-1a           │ AZ-1b           │ AZ-1c
     │                 │                 │
     │ ┌───────────┐   │ ┌───────────┐   │ ┌───────────┐
     │ │Public-1a  │   │ │Public-1b  │   │ │Public-1c  │
     │ │+ NAT-1a   │   │ │+ NAT-1b   │   │ │+ NAT-1c   │
     │ └─────┬─────┘   │ └─────┬─────┘   │ └─────┬─────┘
     │       │         │       │         │       │
     │ ┌─────▼─────┐   │ ┌─────▼─────┐   │ ┌─────▼─────┐
     │ │App-1a     │   │ │App-1b     │   │ │App-1c     │
     │ └─────┬─────┘   │ └─────┬─────┘   │ └─────┬─────┘
     │       │         │       │         │       │
     │ ┌─────▼─────┐   │ ┌─────▼─────┐   │ ┌─────▼─────┐
     │ │DB-1a      │   │ │DB-1b      │   │ │DB-1c      │
     │ │(isolated) │   │ │(isolated) │   │ │(isolated) │
     │ └───────────┘   │ └───────────┘   │ └───────────┘
     │                 │                 │
     └─────────────────┴─────────────────┘
                  prod-vpc (10.0.0.0/16)
```

এটাই AWS-এ "best practice" 3-tier architecture।

---

## Part 9: Routing Edge Cases

### 🔍 Edge Case 1: Route Conflict

**Question:** যদি দুটা route exact same destination-এর হয়?

```
| 0.0.0.0/0 | igw-xxx |
| 0.0.0.0/0 | nat-yyy |
```

**Answer:** AWS allow করে না। একই destination-এ duplicate route prohibited।

**Workaround:** Different specific destinations use।

### 🔍 Edge Case 2: VPC Connecting to Same CIDR

**Scenario:**
- VPC-A: `10.0.0.0/16`
- VPC-B: `10.0.0.0/16` (same CIDR!)

**Problem:** VPC peering possible না — overlap।

**Solution:** Always different CIDRs use VPC design-এ।

### 🔍 Edge Case 3: Routing Loop

**Bad Configuration:**
```
RT-1: 0.0.0.0/0 → vgw-xxx
RT-2: 0.0.0.0/0 → vgw-xxx
on-premise: 10.0.0.0/16 → AWS
```

Traffic loop করতে পারে। AWS detect করে drop করে।

### 🔍 Edge Case 4: Black Hole Route

**Scenario:** Target deleted but route remains.

```
Route Table:
| 0.0.0.0/0 | igw-xxx (DELETED) |
```

**State:** "blackhole"
**Effect:** All matching traffic dropped silently।

**Fix:** Either re-create target or update route।

---

## Part 10: Troubleshooting Routing — Step by Step

### 🔧 Problem: "EC2 can't access internet"

#### Diagnostic Flow:

**Step 1: Instance basics**
```
Question: Instance-এ public IP আছে?
Check: EC2 console → Instance details → Public IPv4 address

If no: 
- Subnet-এ Auto-assign Public IP enable করুন
- বা Elastic IP attach করুন

If yes: Step 2-এ যান
```

**Step 2: Subnet's Route Table**
```
Question: Subnet-এর RT-এ 0.0.0.0/0 → IGW আছে?
Check: VPC console → Subnet → Route Table tab

If no:
- Add route: 0.0.0.0/0 → igw-xxx

If yes: Step 3-এ যান
```

**Step 3: IGW attached?**
```
Check: VPC console → Internet Gateways → Status

If detached:
- Attach to VPC

If attached: Step 4
```

**Step 4: Security Group**
```
Question: Outbound rule allow internet?
Default SG: All outbound allowed
Custom SG: Check rules

If blocked: Allow outbound 0.0.0.0/0
If allowed: Step 5
```

**Step 5: NACL**
```
Question: Subnet's NACL allow?
Default NACL: All allow
Custom NACL: Both inbound + outbound check (stateless)

If blocked: Allow rules add
If allowed: Step 6
```

**Step 6: OS-level firewall**
```
Linux: iptables, firewalld
Windows: Windows Firewall

Check inside instance.
```

**Step 7: DNS Resolution**
```
Question: VPC DNS settings enabled?
Check: VPC → DNS hostnames, DNS resolution → Enable both

VPC default: enabled
Custom VPC: may need enable
```

**Step 8: Route propagation**
```
For VPN/peering issues:
- Route propagation enabled?
- Routes actually present?
```

**Tool: VPC Reachability Analyzer**
- AWS-এর built-in tool
- Source-destination test
- Step-by-step path show
- Blocking layer identify

---

## Part 11: Special Routes Explained

### 🎯 The Default Route: 0.0.0.0/0

**মানে:** "যেকোনো destination" — catch-all।

**কেন এটা সবচেয়ে কম priority:**
- Prefix length 0 (smallest)
- Longest prefix match-এ অন্য কোনো route-ই win করবে যদি match হয়

**Use cases:**
- Public subnet: `0.0.0.0/0 → IGW`
- Private subnet (with NAT): `0.0.0.0/0 → NAT`
- VPN scenario: `0.0.0.0/0 → VGW`

### 🎯 The Local Route: VPC CIDR → local

**Auto-added, immutable:**
- VPC তৈরির সাথে create
- Modify করা যায় না
- Delete করা যায় না

**Why it matters:**
- VPC-র ভেতরে free communication
- IGW/NAT bypass for internal

### 🎯 The /32 Route: Single IP Override

**Use case:** Specific IP redirect

```
| 10.0.0.0/16    | local   |
| 0.0.0.0/0      | nat-xxx |  ← সাধারণ traffic NAT
| 8.8.8.8/32     | igw-yyy |  ← Google DNS specific direct
```

Traffic to `8.8.8.8` IGW-তে, বাকি সব NAT-এ।

---

## Part 12: VPC Routing Limits ও Performance

### 📊 Performance Considerations

**Route table lookup speed:**
- Hardware accelerated by AWS
- No measurable latency for normal traffic
- Even 50+ routes performant

**Limits to remember:**
- Routes per RT: 50 default (1,000 max)
- RTs per VPC: 200
- Subnets per RT: unlimited

### 💰 Cost Implications of Routing

Route table itself free, but routing decisions affect cost:

**IGW route:**
- Data transfer out: $0.09/GB (Mumbai)
- Free within same region between AZ (subject to recent AWS changes)

**NAT Gateway:**
- $0.045/hour (Mumbai)
- $0.045/GB processed
- Significant cost for high-traffic apps

**VPC Endpoint (preview):**
- Gateway endpoint (S3, DynamoDB): Free
- Interface endpoint: $0.01/hour + data
- Saves NAT/IGW data transfer

**Optimization:** Use VPC Endpoint for AWS service traffic instead of NAT/IGW।

---

## Part 13: Visualizing Real Traffic

### 🎬 Scenario A: User Browses Your Website

```
1. User: browser → www.yoursite.com
2. DNS resolves → 54.203.12.45 (your ALB public IP)
3. Internet → IGW
4. IGW → ALB (in public subnet)
5. ALB → EC2 (in private subnet, via local route)
6. EC2 → Database (in DB subnet, via local route)
7. Database response back
8. EC2 response back
9. ALB response back  
10. ALB → IGW → Internet → User
```

**Routes used:**
- Internet → IGW (no AWS RT, internet routing)
- IGW → public subnet (direct)
- public → private (local route)
- private → DB (local route)
- Reverse for response

### 🎬 Scenario B: App Server Updates Software

```
1. EC2 in app-1a: "yum update" → repository.amazon.com
2. EC2 → app-rt-1a → 0.0.0.0/0 → nat-1a
3. NAT-1a (in public-1a) → public-rt → 0.0.0.0/0 → igw
4. IGW → Internet → repository
5. Response back
6. IGW → NAT-1a (it remembers connection)
7. NAT-1a → app-1a-EC2
```

**Routes used:**
- App tier → NAT (via app-rt)
- NAT → IGW (via public-rt)
- Reverse via stateful tracking

### 🎬 Scenario C: Database Query

```
1. App-1a: query → db-1a
2. App-rt-1a → local route → db-1a (within VPC)
3. Database responds
4. db-rt → local route → app-1a
```

**Routes used:**
- Local route only
- IGW, NAT-এর কোনো involvement নেই

### 🎬 Scenario D: Failed Internet Attempt from DB

```
1. db-1a: someone runs "yum update" by mistake
2. db-rt has only local route
3. No matching route for 0.0.0.0/0
4. Packet dropped
5. Connection times out
```

**Why this is good:** Database isolated by design। Even compromised, can't reach internet.

---

## 🎯 Master Checklist (Today's Topics)

আজকের পর আপনি যা confidently answer করতে পারবেন:

- [ ] Packet-এর VPC-এর ভেতরের journey describe
- [ ] IGW-র internal NAT mechanism
- [ ] Route table lookup algorithm
- [ ] Longest prefix match calculation
- [ ] Public vs Private subnet conditions
- [ ] Multiple route tables design
- [ ] NAT Gateway placement strategy (per AZ)
- [ ] Common routing issues debugging

---

## 📝 Practice Problems

### Problem 1: Route Table Reading

```
RT:
| 10.0.0.0/16  | local   |
| 0.0.0.0/0    | nat-xxx |
| 10.1.0.0/16  | pcx-yyy |
| pl-S3        | vpce-zzz|
```

Where does each go?
- `10.0.5.10` → ?
- `10.1.5.10` → ?
- `8.8.8.8` → ?
- `s3.amazonaws.com IP` → ?

<details>
<summary>Answers</summary>

- `10.0.5.10` → local (within VPC CIDR)
- `10.1.5.10` → pcx-yyy (peered VPC)
- `8.8.8.8` → nat-xxx (catch-all internet)
- `s3.amazonaws.com` → vpce-zzz (S3 endpoint, prefix list match wins)
</details>

### Problem 2: Design from Scratch

Requirement: 
- 1 web server (must be internet accessible)
- 2 app servers (need software updates)
- 1 database (no internet ever)
- 2 AZ minimum

Design:
- VPC CIDR?
- How many subnets?
- How many route tables?
- Where does NAT go?

<details>
<summary>Answer</summary>

**VPC:** `10.0.0.0/16`

**Subnets:**
- Public-1a: `10.0.1.0/24`
- Public-1b: `10.0.2.0/24`
- App-1a: `10.0.11.0/24`
- App-1b: `10.0.12.0/24`
- DB-1a: `10.0.21.0/24`
- DB-1b: `10.0.22.0/24`

**Route Tables:**
- Public RT: 0.0.0.0/0 → IGW (public-1a, public-1b associated)
- App RT 1a: 0.0.0.0/0 → NAT-1a (app-1a)
- App RT 1b: 0.0.0.0/0 → NAT-1b (app-1b)
- DB RT: only local (db-1a, db-1b)

**NAT:** Per public subnet (public-1a, public-1b) for AZ redundancy
</details>

### Problem 3: Debug

User reports: "I can SSH from my office to the EC2 instance, but the EC2 instance can't reach `google.com`."

What could be the issue? List 3 possibilities.

<details>
<summary>Answer</summary>

1. Route table missing 0.0.0.0/0 → IGW (likely if SSH works because instance has public IP)
2. Outbound Security Group blocks port 443/80 (SSH inbound works, outbound separate)
3. NACL outbound rules blocking
4. DNS resolution disabled in VPC
5. OS-level firewall blocking outbound
</details>

---

## 💡 Mental Models

### Model 1: VPC = Apartment Building

- VPC = building
- Subnets = floors
- Instances = apartments
- IGW = main entrance
- Route Table = floor's hallway sign showing where each apartment is and where the exits are
- Local route = "you can walk to any apartment in this building"
- 0.0.0.0/0 → IGW = "exit through main door"

### Model 2: Routing = Postal System

- Packet = letter
- IP address = address
- Route table = post office sorting rules
- Longest prefix match = most specific address wins
- IGW = international mail dispatch
- Local route = "this neighborhood, deliver directly"

### Model 3: NAT = Translator

- Instance speaks "private IP language"
- Internet speaks "public IP language"
- IGW does the translation
- NAT Gateway also translates but only one-way (outbound)

---

## 🎓 Summary: যা আজ শিখলেন

1. **Packet routing journey** — instance থেকে internet পর্যন্ত
2. **IGW = gate + NAT translator** combined
3. **Route table = decision rules** every packet checks
4. **Longest prefix match** — winning algorithm
5. **Public subnet = behavior** (3 conditions), not setting
6. **Multi-RT design** — production-grade VPC pattern
7. **NAT redundancy per AZ** — true HA
8. **Local route always exists** — VPC internal communication
9. **DB tier no internet** — isolation by route table
10. **Routing debug systematic** — checklist approach

---
