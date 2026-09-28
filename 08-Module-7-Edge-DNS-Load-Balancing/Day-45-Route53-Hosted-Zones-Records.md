
# 📚 Day 45 — Route 53: Hosted Zones, Record Types, Alias ও Domain Delegation

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![Region, AZ and Edge Location](../images/01-region-az-edge.png)

**সময়:** ১.৫ ঘণ্টা | **Module:** ৭ (Edge Services, DNS & Load Balancing) — Day 3

## 🎯 আজকের লক্ষ্য
- DNS resolution কীভাবে ঘটে (দ্রুত revision)
- Route 53-এর তিন কাজ: domain registration, DNS hosting, health checking
- **Public বনাম private hosted zone**
- Record type: A, AAAA, CNAME, **Alias**, MX, TXT, NS, SOA, CAA, SRV
- **Alias বনাম CNAME** (zone apex)
- TTL-এর প্রভাব
- Domain অন্য registrar থেকে Route 53-এ আনা, subdomain delegation
- DNSSEC (সংক্ষেপে)

> 📖 Day 13-এ Route 53 Resolver, private hosted zone আর hybrid DNS দেখেছি। আজ public DNS আর record-এর দিকে গভীরে।

---

## Part 1: DNS Resolution — দ্রুত Revision

User browser-এ `www.shopbd.com` লিখলে:
```
Browser → OS cache → Recursive resolver (ISP / 8.8.8.8)
            │ cache-এ না থাকলে
            ├─► Root server (.)        : ".com কোথায়?" → .com-এর NS
            ├─► .com TLD server        : "shopbd.com কোথায়?" → Route 53-এর NS (ns-123.awsdns-45.com ...)
            └─► Route 53 name server   : "www.shopbd.com?" → 203.0.113.10 (বা CloudFront-এর IP)
          → উত্তর TTL পর্যন্ত cache → browser connect করে
```
- **Authoritative name server** = যে server আসল উত্তর জানে। Route 53 আপনার domain-এর authoritative server
- **TTL** = উত্তর কতক্ষণ cache থাকবে

---

## Part 2: Route 53-এর তিন কাজ

| কাজ | কী |
|---|---|
| **Domain registration** | নতুন domain কেনা (`.com`, `.net`, `.io`... অনেক TLD; কিছু দেশীয় TLD যেমন `.com.bd` Route 53-এ পাওয়া যায় না) |
| **DNS hosting** | Hosted zone-এ record রেখে DNS query-র উত্তর দেওয়া (**100% availability SLA**, anycast name server) |
| **Health checking** | Endpoint ঠিক আছে কিনা পরীক্ষা, failover (Day 46) |

> নাম "Route 53" কারণ DNS port **53**।

---

## Part 3: Hosted Zone — Public বনাম Private

**Hosted zone** = একটা domain-এর সব DNS record-এর container।

| | **Public hosted zone** | **Private hosted zone** |
|---|---|---|
| কে query করতে পারে | **Internet-এর যে কেউ** | শুধু **associated VPC**-র ভেতর থেকে |
| ব্যবহার | Website, API, email (`shopbd.com`) | Internal নাম (`db.internal.shopbd.com`) |
| Name server | ৪টা AWS name server পায় (registrar-এ বসাতে হয়) | লাগে না |
| VPC setting | — | `enableDnsHostnames` + `enableDnsSupport` চালু |

### Split-view (split-horizon) DNS
একই নাম (`api.shopbd.com`) দুটো zone-এ: public zone-এ public ALB-এর ঠিকানা, private zone-এ internal ALB-এর ঠিকানা। VPC-র ভেতর থেকে private উত্তর, বাইরে থেকে public উত্তর।

**খরচ:** প্রতি hosted zone মাসে একটা ছোট fee + প্রতি লাখ/কোটি query-র দাম। **Alias query AWS resource-এ free**।

---

## Part 4: Record Type

| Type | কী রাখে | উদাহরণ |
|---|---|---|
| **A** | IPv4 address | `www → 203.0.113.10` |
| **AAAA** | IPv6 address | `www → 2001:db8::10` |
| **CNAME** | অন্য নাম (alias নাম) | `blog → shopbd.ghost.io` |
| **Alias** (Route 53-এর নিজস্ব) | AWS resource-এর দিকে pointer, A/AAAA হিসেবে উত্তর | `shopbd.com → d111.cloudfront.net` |
| **MX** | Mail server (priority সহ) | `10 mail1.shopbd.com` |
| **TXT** | যেকোনো text: SPF, DKIM, domain verification | `"v=spf1 include:amazonses.com ~all"` |
| **NS** | Zone-এর name server | Delegation |
| **SOA** | Zone-এর মূল তথ্য (primary NS, serial, negative cache TTL) | নিজে থেকে তৈরি |
| **CAA** | কোন Certificate Authority certificate দিতে পারবে | `0 issue "amazon.com"` |
| **SRV** | Service-এর host আর port | VoIP, কিছু protocol |
| **PTR** | Reverse DNS (IP → নাম) | Mail server reputation |

---

## Part 5: Alias বনাম CNAME — Exam-এর প্রিয় বিষয়

| | **CNAME** | **Alias** |
|---|---|---|
| Target | **যেকোনো** DNS নাম | শুধু AWS resource: **CloudFront, ALB/NLB, API Gateway, S3 website, Elastic Beanstalk, Global Accelerator, VPC interface endpoint**, একই zone-এর অন্য record |
| **Zone apex** (`shopbd.com`) | ❌ **দেওয়া যায় না** (DNS standard) | ✅ **দেওয়া যায়** |
| Query খরচ | চার্জ হয় | AWS resource-এ **free** |
| Resolution | Client-কে আরেকটা lookup করতে হয় | Route 53 নিজে IP ফেরত দেয় (A/AAAA) |
| Target-এর IP বদলালে | Target-এর DNS নিজে সামলায় | Route 53 নিজে track করে |
| TTL | আপনি দেন | Target-এর থেকে নেয় |
| Health | — | **Evaluate target health** (Day 46) |

```
shopbd.com       Alias A  → dxxxx.cloudfront.net          ✅ (apex, CNAME সম্ভব না)
www.shopbd.com   Alias A  → dxxxx.cloudfront.net          ✅ (Alias ভালো, free)
blog.shopbd.com  CNAME    → shopbd.ghost.io               ✅ (বাইরের service)
api.shopbd.com   Alias A  → my-alb-123.ap-south-1.elb.amazonaws.com
```

> ⚠️ **EC2 instance-এর DNS নাম-এ Alias দেওয়া যায় না**; EC2-র জন্য A record (Elastic IP) দিন, অথবা সামনে ALB রাখুন।

---

## Part 6: TTL-এর প্রভাব

| TTL | সুবিধা | অসুবিধা |
|---|---|---|
| **বেশি** (যেমন ২৪ ঘণ্টা) | কম query, কম খরচ, দ্রুত (cache) | পরিবর্তন ছড়াতে অনেক সময় |
| **কম** (যেমন ৬০ সেকেন্ড) | পরিবর্তন দ্রুত কার্যকর, failover দ্রুত | বেশি query, বেশি খরচ |

### Migration-এর কৌশল
```
১-২ দিন আগে: TTL 86400 → 300 (কমিয়ে রাখুন)
পুরনো TTL শেষ হওয়া পর্যন্ত অপেক্ষা
Migration: record-এর মান বদলান (৫ মিনিটে সবখানে)
সব ঠিক থাকলে: TTL আবার বাড়ান
```
> Alias record-এ TTL আপনি দেন না, target-এর (যেমন ALB-এর ৬০ সেকেন্ড) নেওয়া হয়।

---

## Part 7: Domain Registrar ও Delegation

### ক্ষেত্র ১: Domain Route 53-এ কেনা
Hosted zone নিজে থেকে তৈরি হয়, name server নিজে থেকে বসানো থাকে। কিছু করতে হয় না।

### ক্ষেত্র ২: Domain অন্য registrar-এ (GoDaddy, Namecheap, দেশীয় registrar), DNS Route 53-এ চান
1. Route 53-এ **public hosted zone** বানান `shopbd.com`
2. Zone-এর **৪টা NS record** দেখুন (`ns-123.awsdns-45.com`, `.net`, `.org`, `.co.uk`)
3. Registrar-এর panel-এ **name server** এই ৪টা দিয়ে বদলান
4. পুরনো NS-এর TTL (প্রায়ই ২৪–৪৮ ঘণ্টা) শেষ হলে Route 53 authoritative
> আগে সব record (বিশেষ করে **MX**, নইলে email বন্ধ!) Route 53-এ copy করে নিন।

(চাইলে domain registration-ও Route 53-এ **transfer** করা যায়।)

### ক্ষেত্র ৩: Subdomain delegation (multi-account)
`shopbd.com` main account-এ; `dev.shopbd.com` dev team নিজের account-এ manage করবে:
1. Dev account-এ hosted zone `dev.shopbd.com` → ৪টা NS পায়
2. Main account-এর `shopbd.com` zone-এ **NS record**: `dev` → ঐ ৪টা name server
3. এখন `*.dev.shopbd.com`-এর সব record dev team নিজে বদলাতে পারে, main zone-এ হাত না দিয়ে

---

## Part 8: DNSSEC (সংক্ষেপে)

**DNS spoofing/cache poisoning** আক্রমণে attacker ভুল IP ফেরত দিতে পারে। **DNSSEC** DNS উত্তরকে **digital signature** দিয়ে sign করে, resolver যাচাই করতে পারে উত্তরটা আসল।
- Route 53-এ public hosted zone-এ **DNSSEC signing** চালু করা যায় (KMS key দিয়ে, `us-east-1`-এ asymmetric key)
- Parent zone (registrar/TLD)-এ **DS record** বসাতে হয়
- VPC-র ভেতরে **Route 53 Resolver DNSSEC validation** চালু করা যায়
- ভুল configure করলে পুরো domain resolve বন্ধ হতে পারে, তাই সাবধানে, আগে test

---

## Part 9: Hands-on Lab

> একটা domain লাগবে (Route 53-এ কেনা, বা অন্য জায়গা থেকে)। না থাকলে private hosted zone দিয়ে record-এর অনুশীলন করুন।

1. Public hosted zone `yourdomain.com` (registrar-এ NS বসান যদি বাইরে কেনা)
2. Records:
   - `yourdomain.com` **Alias** → Day 43-এর CloudFront distribution
   - `www` **Alias** → একই distribution
   - `blog` **CNAME** → অন্য কোনো hostname
   - `TXT` → `"hello-from-route53"`
3. যাচাই:
```bash
dig +short yourdomain.com
dig +short www.yourdomain.com
dig TXT yourdomain.com +short
dig NS yourdomain.com +short                # Route 53-এর ৪টা NS
dig @8.8.8.8 www.yourdomain.com +noall +answer   # TTL দেখুন
```
4. Apex-এ CNAME দেওয়ার চেষ্টা করুন → Route 53 আটকাবে
5. **বোনাস:** Private hosted zone `internal.yourdomain.com` বানিয়ে একটা VPC-র সাথে associate; VPC-র instance থেকে resolve হয়, বাইরে থেকে হয় না

---

## 🎯 আজকের মূল Takeaways

1. DNS: resolver → root → TLD → **authoritative (Route 53)**; উত্তর TTL পর্যন্ত cache
2. Route 53 = registration + DNS hosting (100% SLA) + health check
3. **Public** zone = internet; **private** zone = associated VPC; split-view সম্ভব
4. Record: A, AAAA, CNAME, MX, TXT, NS, SOA, CAA...; Route 53-এর বিশেষ **Alias**
5. **Alias**: apex-এ চলে, AWS target-এ free, target health; **CNAME** apex-এ চলে না
6. TTL: কম = দ্রুত পরিবর্তন/বেশি খরচ; migration-এর আগে TTL কমান
7. বাইরের registrar → registrar-এ Route 53-এর ৪টা NS; subdomain delegation = parent zone-এ NS record
8. DNSSEC = DNS উত্তরের signature

---

## 📝 Self-check Questions

1. `shopbd.com` (apex)-কে ALB-এর দিকে কীভাবে point করবেন? কেন CNAME না?
2. Public আর private hosted zone-এর পার্থক্য কী?
3. Domain GoDaddy-তে কেনা, DNS Route 53-এ আনতে কী করবেন? কোন record ভুলে গেলে email বন্ধ হবে?
4. Server migration-এর আগের দিন কী করবেন DNS-এ?
5. `dev.shopbd.com` আলাদা account-এর team manage করবে। কীভাবে?
6. EC2 instance-এর public DNS নাম-এ Alias দেওয়া যায়?
7. CAA record কী কাজে লাগে?

<details><summary>▶ উত্তর দেখুন</summary>

1. Alias A record → ALB; DNS standard অনুযায়ী zone apex-এ CNAME দেওয়া যায় না।
2. Public zone internet থেকে query করা যায়; private zone শুধু associated VPC থেকে।
3. Route 53-এ public hosted zone, সব record copy, তারপর GoDaddy-তে name server Route 53-এর ৪টা NS দিয়ে বদলানো। MX record।
4. TTL কমিয়ে দিন (যেমন ৩০০ সেকেন্ড), পুরনো TTL শেষ হওয়া পর্যন্ত অপেক্ষা করুন।
5. Dev account-এ `dev.shopbd.com` hosted zone, আর parent `shopbd.com` zone-এ `dev` নামে NS record (dev zone-এর ৪টা name server)।
6. না; Elastic IP দিয়ে A record, বা সামনে ALB।
7. কোন Certificate Authority আপনার domain-এর জন্য certificate দিতে পারবে তা সীমিত করে।
</details>

---

## 💡 Pro Tips

- সব DNS record **IaC**-তে রাখুন (Terraform/CloudFormation), হাতে বদলানো record পরে কেউ বোঝে না
- **Route 53 query logging** চালু রাখুন (public zone-এর log `us-east-1`-এর CloudWatch Logs-এ যায়)
- Email-এর জন্য **SPF, DKIM, DMARC** TXT record ঠিকমতো দিন, নাহলে mail spam-এ যায়
- Domain-এর **auto-renew** চালু রাখুন আর registrar-এ **transfer lock**; domain expire হওয়া ভয়ংকর বিপদ
- `dig +trace` দিয়ে পুরো resolution-এর পথ দেখা যায়, delegation সমস্যায় কাজে লাগে

---

## 🎨 Quick Reference

```
Resolution: resolver → root → TLD → authoritative (Route 53 NS ×4) → cached for TTL
Public zone: internet | Private zone: associated VPCs (DNS hostnames+support on)
Records: A, AAAA, CNAME, Alias, MX, TXT, NS, SOA, CAA, SRV, PTR
Alias: apex OK, AWS targets (CloudFront, ELB, API GW, S3 website, GA, VPCE), free queries, evaluate target health
CNAME: any hostname, NOT at apex
TTL: lower before migration, raise after
External registrar: set its name servers to Route 53's 4 NS
Subdomain delegation: NS record in parent zone → child zone NS
```

```bash
dig +short example.com
dig NS example.com +short
dig +trace www.example.com
```

---

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** DNS Route 53-এ সরানো হলো, কিন্তু MX record copy করা হয়নি। দুই দিন company-র কোনো email আসেনি।
**শিক্ষা:** NS বদলানোর আগে সব record (MX, TXT, SPF, DKIM) copy।

**পরিস্থিতি ২:** Migration-এর দিন record বদলানো হলো, কিন্তু TTL ছিল ২৪ ঘণ্টা। অর্ধেক user পুরো এক দিন পুরনো (বন্ধ) server-এ যেতে থাকল।
**শিক্ষা:** Migration-এর আগে TTL কমান।

**পরিস্থিতি ৩:** Domain-এর credit card expire হয়ে গিয়েছিল, auto-renew fail করল। Domain expire হয়ে website আর email দুটোই বন্ধ।
**শিক্ষা:** Auto-renew, সঠিক billing, আর expiry reminder।

---

**⏮ আগের দিন:** [Day 44 — CloudFront Caching ও Security](./Day-44-CloudFront-Caching-Security-Edge-Functions.md) | **⏭ পরের দিন:** [Day 46 — Route 53 Routing Policies ও Health Checks](./Day-46-Route53-Routing-Policies-Health-Checks-Failover.md)
