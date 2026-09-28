# 🗂 Module 8 Cheat Sheet — Network Security & Monitoring

> **এক পাতায় পুরো module।** বিস্তারিত লাগলে Day 49–53-এ যান।

📚 বিস্তারিত নোট: [Day 49](../09-Module-8-Network-Security-Monitoring/Day-49-WAF-Shield-Network-Firewall-Deep-Dive.md) → [Day 53](../09-Module-8-Network-Security-Monitoring/Day-53-Module-8-Revision-Complete-Secure-Architecture-Project.md)

---

## 🖼 Visual Summary

![Network Monitoring Pipeline](../images/55-network-monitoring-pipeline.png)

![Security Services Together](../images/56-security-services-together.png)

![Compliance and Audit Pipeline](../images/57-compliance-audit-pipeline.png)

---

## ⚡ Service at a Glance

| Service | কী | মূল পয়েন্ট |
|---|---|---|
| **WAF** | L7 web application firewall | SQLi/XSS block, rate-based rules |
| **Shield** | DDoS protection | Standard (free, সবার জন্য) vs Advanced (paid, 24/7 DRT) |
| **Network Firewall** | VPC-level L3-L7 firewall | Stateless + stateful rule groups, Suricata rules |
| **VPC Flow Logs** | নেটওয়ার্ক traffic record | CloudWatch/S3/Firehose-এ পাঠানো যায় |
| **GuardDuty** | Threat detection (ML-based) | DNS, traffic pattern analysis |
| **Security Hub** | Findings aggregator | নিজে scan করে না, ASFF format-এ একত্র করে |
| **CloudTrail** | API audit log | Management vs data events, organization trail |
| **Secrets Manager** | Auto-rotating secret store | create→set→test→finish rotation cycle |

---

## 🔀 WAF vs Shield vs Network Firewall vs Security Group

| | WAF | Shield | Network Firewall | Security Group |
|---|---|---|---|---|
| Layer | L7 | L3/L4 (DDoS) | L3-L7 | L4 (instance) |
| কী থামায় | SQLi, XSS, bot | Volumetric DDoS | Custom traffic filtering rule | নির্দিষ্ট port/IP |
| Scope | CloudFront/ALB/API GW | সব AWS resource | পুরো VPC | Instance/ENI |

---

## 💻 Practical Commands

```bash
# Secret rotation চালু করা
aws secretsmanager rotate-secret --secret-id prod/db/password \
  --rotation-lambda-arn arn:aws:lambda:...:function:SecretsManagerRDSRotation \
  --rotation-rules AutomaticallyAfterDays=30
```

---

## ⚠️ Top Gotchas

1. **Security Group-এ Deny rule নেই** — block করতে NACL, WAF, বা Network Firewall লাগবে।
2. **Security Hub নিজে কিছু scan করে না** — এটা GuardDuty/Inspector/Config-এর finding aggregate করে।
3. **VPC Flow Logs default-এ off** — turn on না করলে network troubleshoot/audit-এর সময় কোনো data থাকবে না।
4. **CloudTrail data events আলাদা চালু করতে হয়** (default শুধু management events) — S3 object-level access log করতে হলে মনে রাখুন।
5. **Secrets rotation Lambda-তে app যদি secret cache করে**, rotation-এর পরও পুরনো password দিয়ে connect করার চেষ্টা করে fail করতে পারে।

---

## 🔢 মনে রাখার সংখ্যা

- CloudTrail default event history: **90 দিন**
- GuardDuty finding severity: **Low (0.1-3.9) / Medium (4-6.9) / High (7-8.9) / Critical (9-10)**
- Secrets Manager rotation cycle: **create → set → test → finish**
- WAF rate-based rule: min threshold **100 requests/5 মিনিট**

---

**⏮ পূর্ববর্তী:** [Module 7 Cheat Sheet](./07-Module-7-Edge-DNS-LB-Cheat-Sheet.md) | **⏭ পরবর্তী:** [Module 9 Cheat Sheet](./09-Module-9-Databases-Cheat-Sheet.md)
