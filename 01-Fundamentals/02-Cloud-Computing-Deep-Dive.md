# ☁️ Cloud Computing — Technical Deep Dive

---

## 1. Virtualization — Cloud এর Core Technology

Cloud এর পুরো concept দাঁড়িয়ে আছে **Virtualization** এর উপর।

### Physical Reality:

```
One Physical Server (AWS Data Center)
├── 32 CPU Cores
├── 256 GB RAM
└── 10 TB Storage
```

এই একটা physical machine কে AWS ভাগ করে দেয় অনেক গুলো **Virtual Machine (VM)** এ:

```
Physical Server
├── VM 1 → তোমার EC2 (2 CPU, 8GB RAM)
├── VM 2 → অন্য কারো EC2 (4 CPU, 16GB RAM)
├── VM 3 → আরেকজনের EC2 (1 CPU, 4GB RAM)
└── ...আরো অনেক
```

এটা possible হয় **Hypervisor** দিয়ে। AWS নিজস্ব hypervisor use করে যার নাম **Nitro System**।

---

## 2. Service Models — Technical পার্থক্য

### IaaS (EC2):

```
You manage:
├── Application Code
├── Runtime (Node.js, Python)
├── OS (Ubuntu, Amazon Linux)
└── Middleware

AWS manages:
├── Virtualization (Hypervisor)
├── Physical Servers
├── Network Hardware
└── Data Center
```

### PaaS (Elastic Beanstalk):

```
You manage:
└── Application Code only

AWS manages:
├── OS patching
├── Runtime installation
├── Load balancing
├── Auto scaling
└── Everything below
```

### SaaS (Gmail):

```
You manage:
└── Your data/usage only

AWS/Provider manages:
└── Literally everything
```

---

## 3. AWS Global Infrastructure — Technical Architecture

### Region এর ভিতরে আসলে কী আছে?

```
ap-south-1 (Mumbai Region)
├── AZ: ap-south-1a
│   ├── Data Center 1
│   └── Data Center 2
├── AZ: ap-south-1b
│   ├── Data Center 3
│   └── Data Center 4
└── AZ: ap-south-1c
    ├── Data Center 5
    └── Data Center 6
```

**AZ গুলো physically:**
- একে অপর থেকে কয়েক km দূরে
- আলাদা power grid
- আলাদা internet connection
- Underground fiber দিয়ে connected (low latency ~1ms)

### Latency Comparison:

```
Same AZ:          < 1ms
Different AZ:     1-2ms
Different Region: 50-200ms
Edge Location:    < 10ms (cached content)
```

---

## 4. Network — Packet আসলে কোথায় যায়?

তুমি Bangladesh থেকে request করলে technically কী হয়?

```
তোমার Browser (Dhaka)
      ↓ DNS Lookup
Route 53 (AWS DNS)
      ↓ Returns nearest IP
CloudFront Edge (Singapore/Mumbai)
      ↓ Cache miss হলে
Origin Server (EC2 - Mumbai)
      ↓
Your NestJS App
      ↓
Response same path এ ফিরে আসে
```

### Cache Hit vs Miss:

```
Cache HIT:
User → Edge Location → Response (fast, ~10ms)

Cache MISS:
User → Edge → Origin EC2 → Edge (store) → Response (~100ms)
```

---

## 5. Scalability — Technical Mechanism

### Vertical Scaling (Scale Up):

```
Before: t3.micro  (1 CPU, 1GB RAM)
After:  t3.xlarge (4 CPU, 16GB RAM)

Problem: Downtime লাগে, limit আছে
```

### Horizontal Scaling (Scale Out):

```
Normal traffic:
Load Balancer → [EC2-1]

High traffic:
Load Balancer → [EC2-1]
             → [EC2-2]  ← auto added
             → [EC2-3]  ← auto added

Traffic কমলে:
Load Balancer → [EC2-1]  ← others terminated
```

এটা করে **Auto Scaling Group (ASG)**:

```
ASG Config:
├── Min instances: 1
├── Max instances: 10
├── Scale out when: CPU > 70%
└── Scale in when:  CPU < 30%
```

---

## 6. Shared Responsibility — Technical Breakdown

```
┌─────────────────────────────────────┐
│         YOUR RESPONSIBILITY         │
├─────────────────────────────────────┤
│  Application Code & Logic           │
│  Data Encryption (at rest/transit)  │
│  IAM Users, Roles, Policies         │
│  OS Updates (EC2 তে)               │
│  Security Groups (Firewall rules)   │
│  Network ACLs                       │
├─────────────────────────────────────┤
│         AWS RESPONSIBILITY          │
├─────────────────────────────────────┤
│  Hypervisor & Virtualization        │
│  Physical Hardware                  │
│  Data Center Physical Security      │
│  Managed Service OS (RDS, Lambda)   │
│  Global Network Infrastructure      │
└─────────────────────────────────────┘
```

---

## 7. Data Flow — Full Technical Picture

একটা NestJS app এর real request flow:

```
Client Request (HTTP)
      ↓
Internet Gateway
      ↓
CloudFront (CDN + DDoS protection)
      ↓
Application Load Balancer (Layer 7)
      ↓ Route by path (/api → backend)
EC2 Instance (NestJS running)
      ↓           ↓
    RDS        S3 Bucket
 (PostgreSQL)  (File Storage)
      ↓
Response back to client
```

### Security Layers এই flow এ:

```
CloudFront    → WAF (Web Application Firewall)
Load Balancer → SSL Termination (HTTPS)
EC2           → Security Group (port rules)
RDS           → Private Subnet (no internet access)
All           → IAM (who can do what)
```

---

## 8. Pricing Model — Technical Reality

```
EC2 Pricing:
├── On-Demand:  per second billing
├── Reserved:   1-3 year commitment (60-70% cheaper)
├── Spot:       unused capacity (~90% cheaper, can be terminated)
└── Savings Plan: flexible commitment

S3 Pricing:
├── Storage:    per GB/month
├── Requests:   per GET/PUT request
└── Transfer:   data out to internet (data in = free)
```

---

## 9. High Availability Architecture

Production এ কেমন দেখতে হয়:

```
                    Route 53 (DNS Failover)
                         ↓
              CloudFront (Global CDN)
                         ↓
         Application Load Balancer (Multi-AZ)
              ↙                    ↘
    AZ-1 (ap-south-1a)      AZ-2 (ap-south-1b)
    EC2 Instance 1           EC2 Instance 2
         ↓                         ↓
    RDS Primary ←──────────→ RDS Standby
    (ap-south-1a)  sync      (ap-south-1b)
```

Primary RDS fail করলে automatically Standby promote হয়। এটাই **Multi-AZ Deployment**।

---

## Key Technical Terms Summary

| Term | Technical Meaning |
|------|------------------|
| Hypervisor | Physical server কে VM এ ভাগ করে |
| AMI | EC2 এর OS + software template |
| EBS | EC2 এর attached block storage |
| VPC CIDR | Network IP range (e.g. 10.0.0.0/16) |
| IGW | Internet Gateway — VPC কে internet এ connect করে |
| NAT Gateway | Private subnet কে outbound internet দেয় |
| Security Group | Instance level stateful firewall |
| NACL | Subnet level stateless firewall |

---
