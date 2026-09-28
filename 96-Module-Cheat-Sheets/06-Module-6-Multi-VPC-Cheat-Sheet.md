# 🗂 Module 6 Cheat Sheet — Multi-VPC & Private Connectivity

> **এক পাতায় পুরো module।** বিস্তারিত লাগলে Day 36–42-এ যান।

📚 বিস্তারিত নোট: [Day 36](../07-Module-6-Multi-VPC-Private-Connectivity/Day-36-VPC-Peering-Deep-Dive-IP-Planning.md) → [Day 42](../07-Module-6-Multi-VPC-Private-Connectivity/Day-42-Module-6-Revision-Multi-Account-Network-Design.md)

---

## 🖼 Visual Summary

![VPC Peering vs Transit Gateway](../images/10-peering-vs-tgw.png)

![Multi-account OU](../images/23-multi-account-ou.png)

![Shared VPC via RAM](../images/47-shared-vpc-ram.png)

---

## ⚡ Service at a Glance

| Service | কী | মূল পয়েন্ট |
|---|---|---|
| **VPC Peering** | দুই VPC-এর direct connection | Non-transitive, অল্প VPC-তে ভালো |
| **Transit Gateway** | Hub-and-spoke network | Transitive, অনেক VPC/VPN/DX-এর জন্য |
| **Site-to-Site VPN** | On-prem ↔ AWS, encrypted | ইন্টারনেটের উপর দিয়ে, দ্রুত সেটআপ |
| **Direct Connect** | Private dedicated link | Consistent speed, সপ্তাহ লাগে সেটআপে |
| **RAM (Resource Access Manager)** | Cross-account resource share | Shared VPC subnet, TGW share |
| **PrivateLink** | Service-কে private-ভাবে expose | ENI-based, VPC peering-এর বিকল্প |

---

## 🔀 Peering vs Transit Gateway

| | VPC Peering | Transit Gateway |
|---|---|---|
| Transitive? | না (A-B, B-C থাকলেও A-C নেই) | হ্যাঁ |
| Scale | ~kilometer-এ ভালো, বেশি VPC-তে messy | শত শত VPC/account-এ ভালো |
| খরচ | Data transfer only | Attachment + data processing চার্জ |

---

## 💻 Practical Commands

```bash
# VPC Peering accept করা
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id pcx-1a2b3c

# Route table-এ peering/TGW-এর route যোগ করা
aws ec2 create-route --route-table-id rtb-aaaa \
  --destination-cidr-block 10.1.0.0/16 --vpc-peering-connection-id pcx-1a2b3c

# Transit Gateway route table associate করা
aws ec2 associate-transit-gateway-route-table --transit-gateway-attachment-id tgw-attach-xxx \
  --transit-gateway-route-table-id tgw-rtb-xxx

# Customer Gateway + VPN তৈরি (Site-to-Site VPN)
aws ec2 create-customer-gateway --type ipsec.1 --public-ip 203.0.113.10 --bgp-asn 65010
aws ec2 attach-vpn-gateway --vpn-gateway-id vgw-0abc --vpc-id vpc-app
```

---

## ⚠️ Top Gotchas

1. **VPC Peering non-transitive** — A↔B, B↔C থাকলে A↔C automatically কাজ করবে না, TGW লাগবে।
2. **CIDR overlap থাকলে peering/TGW route কাজ করবে না** — planning-এর সময় non-overlapping CIDR নিশ্চিত করুন।
3. **TGW route table প্রতিটা attachment-এ association+propagation আলাদা** — ভুলে একসাথে সব VPC access দিয়ে দিলে segmentation ভেঙে যায়।
4. **VPN over internet latency অনিশ্চিত** — production-critical হলে Direct Connect (+ backup VPN) বিবেচনা করুন।
5. **RAM দিয়ে shared subnet-এ owner account ছাড়া participant account resource delete করতে পারে না** (শুধু নিজের resource manage করতে পারে)।

---

## 🔢 মনে রাখার সংখ্যা

- TGW max attachments: **৫,০০০ per TGW**
- VPC Peering: max **125 active peering per VPC** (soft limit)
- Site-to-Site VPN tunnel: প্রতি connection-এ **২টা tunnel** (HA-এর জন্য)
- Direct Connect port speed: **50 Mbps – 100 Gbps**

---

**⏮ পূর্ববর্তী:** [Module 5 Cheat Sheet](./05-Module-5-Event-Driven-Cheat-Sheet.md) | **⏭ পরবর্তী:** [Module 7 Cheat Sheet](./07-Module-7-Edge-DNS-LB-Cheat-Sheet.md)
