
# 📚 Day 46 — Route 53 Routing Policies, Health Checks ও DNS Failover

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![Route 53 Latency and Failover Routing](../images/52-route53-failover-latency.png)

**সময়:** ২ ঘণ্টা | **Module:** ৭ (Edge Services, DNS & Load Balancing) — Day 4

## 🎯 আজকের লক্ষ্য
- সব routing policy: Simple, Weighted, Latency, Failover, Geolocation, Geoproximity, Multivalue, IP-based
- **Health check**-এর তিন ধরন: endpoint, calculated, CloudWatch alarm
- **DNS failover** (active-passive, active-active)
- Evaluate target health (Alias)
- Policy মিলিয়ে ব্যবহার (nested records / Traffic Flow)
- DNS failover-এর সীমা আর Application Recovery Controller

> 📖 Interview Q27-এ policy-গুলোর সংক্ষিপ্ত টেবিল আছে। আজ প্রতিটার কাজ, setup আর ফাঁদ।

---

## Part 1: Routing Policy কেন?

একটা নামের (`api.shopbd.com`) জন্য একাধিক record থাকতে পারে। **Routing policy** ঠিক করে কোন query-তে কোন উত্তর যাবে: কে কাছে, কে healthy, কত % traffic।

> ⚠️ মনে রাখুন: DNS শুধু **ঠিকানা দেয়**, traffic নিজে Route 53 দিয়ে যায় না। আর উত্তর TTL পর্যন্ত **cache** থাকে, তাই DNS-ভিত্তিক পরিবর্তন সাথে সাথে সবার কাছে পৌঁছায় না।

---

## Part 2: সব Routing Policy

### 1️⃣ Simple
- একটা record, এক বা একাধিক মান; একাধিক হলে **সবগুলো** ফেরত দেয়, client নিজে একটা বেছে নেয় (random)
- **Health check নেই**
- একটা server বা একটা ALB-এর জন্য

### 2️⃣ Weighted
```
api.shopbd.com  A  ALB-v1   weight 90   (SetIdentifier: v1)
api.shopbd.com  A  ALB-v2   weight 10   (SetIdentifier: v2)
```
- Traffic ভাগ: weight ÷ মোট weight
- **Canary / blue-green release**, নতুন region-এ ধীরে traffic, A/B test
- Weight **0** = কোনো traffic না (বন্ধ); সব ০ হলে সবগুলোতে সমান ভাগ
- Health check দিলে unhealthy record বাদ পড়ে

### 3️⃣ Latency-based
- User-এর resolver থেকে **সবচেয়ে কম latency-র AWS region**-এর record
- AWS-এর মাপা latency data অনুযায়ী (ভৌগোলিক দূরত্ব না)
- **Multi-region active-active** app: Mumbai + Frankfurt + Virginia
- Health check দিলে unhealthy region বাদ দিয়ে পরের কাছের region

### 4️⃣ Failover (active-passive)
```
api.shopbd.com  Alias → ALB Mumbai     Failover: PRIMARY    + health check
api.shopbd.com  Alias → ALB Singapore  Failover: SECONDARY  (বা S3 maintenance page)
```
- Primary healthy থাকলে সবসময় primary; unhealthy হলে secondary
- **Primary-তে health check বাধ্যতামূলক** (বা Alias-এ evaluate target health)
- DR (Interview Q61) আর "sorry page"

### 5️⃣ Geolocation
- User **কোথা থেকে** (দেশ, মহাদেশ, US state) query করছে তা দেখে
- **Localization**: বাংলাদেশের user → বাংলা site; EU user → EU region (**data residency**)
- **Content licensing**: নির্দিষ্ট দেশে সীমাবদ্ধ
- ⚠️ **Default record অবশ্যই দিন**, নাহলে কোনো নিয়মে না পড়া দেশের user কোনো উত্তরই পাবে না (NODATA)
- সবচেয়ে নির্দিষ্ট মিল জেতে (দেশ > মহাদেশ > default)

### 6️⃣ Geoproximity
- User আর resource-এর **ভৌগোলিক দূরত্ব** অনুযায়ী, সাথে **bias** (−৯৯ থেকে +৯৯)
- Bias বাড়ালে ঐ resource-এর "এলাকা" বড় হয়, বেশি traffic টানে; কমালে ছোট
- Resource: AWS region, বা non-AWS resource-এর latitude/longitude
- ব্যবহার: একটা region-এ ধীরে ধীরে বেশি traffic সরানো, নতুন data center-এর এলাকা বাড়ানো
- (আগে শুধু **Traffic Flow** দিয়ে; এখন সাধারণ record হিসেবেও দেওয়া যায়)

### 7️⃣ Multivalue Answer
- **৮টা পর্যন্ত healthy** record-এর মান ফেরত দেয় (random)
- প্রতিটা record-এ health check দেওয়া যায়, unhealthy বাদ
- Simple-এর মতো, কিন্তু health check সহ; **ELB-এর বিকল্প না**, সহজ client-side load balancing

### 8️⃣ IP-based
- User-এর resolver-এর **IP range (CIDR collection)** অনুযায়ী
- ISP-নির্দিষ্ট routing, নির্দিষ্ট network-এর user-কে নির্দিষ্ট endpoint-এ
- Geolocation-এর চেয়ে বেশি নিয়ন্ত্রিত (আপনি জানেন কোন ISP কোন IP range)

### 📋 সারসংক্ষেপ
| প্রয়োজন | Policy |
|---|---|
| একটাই resource | Simple |
| % অনুযায়ী ভাগ, canary | **Weighted** |
| দ্রুততম region | **Latency** |
| Primary বন্ধ হলে backup | **Failover** |
| দেশ অনুযায়ী আলাদা content / compliance | **Geolocation** |
| দূরত্ব + bias দিয়ে এলাকা বাড়ানো-কমানো | **Geoproximity** |
| কয়েকটা healthy IP random | Multivalue |
| নির্দিষ্ট ISP/network | IP-based |

---

## Part 3: Health Checks

Route 53-এর health checker-গুলো **বিশ্বের বিভিন্ন জায়গা** থেকে endpoint পরীক্ষা করে। যথেষ্ট সংখ্যক checker (default ~১৮%-এর বেশি) healthy বললে endpoint healthy।

### তিন ধরন

| ধরন | কী পরীক্ষা করে | কখন |
|---|---|---|
| **Endpoint** | IP বা domain-এর HTTP/HTTPS/TCP; HTTP হলে status 2xx/3xx, চাইলে response body-তে নির্দিষ্ট text (**string matching**, প্রথম ৫১২০ byte) | Public endpoint (ALB, EC2 EIP, on-prem server) |
| **Calculated** | অন্য কয়েকটা health check মিলিয়ে: "৩টার মধ্যে কমপক্ষে ২টা healthy হলে healthy" | অনেক component-এর সম্মিলিত অবস্থা |
| **CloudWatch alarm** | একটা CloudWatch alarm-এর অবস্থা (ALARM = unhealthy) | **Private resource** (Route 53 checker private IP-তে পৌঁছাতে পারে না), বা যেকোনো metric (যেমন error rate, queue depth) |

### Setting
- **Request interval**: ৩০ সেকেন্ড (standard) বা ১০ সেকেন্ড (fast, বেশি খরচ)
- **Failure threshold**: কতবার পরপর fail হলে unhealthy (default ৩)
- Health check-এর নিজের **CloudWatch metric** আর alarm → SNS
- Firewall/SG-তে **Route 53 health checker-দের IP range** allow করতে হবে (AWS-এর published IP range থেকে)

### ⚠️ ভালো health endpoint
```
GET /health  → 200 OK  (শুধু app চলছে কিনা)                       ← খুব সহজ, dependency ধরে না
GET /health/deep → DB, cache, দরকারি dependency চেক করে 200/503    ← বেশি অর্থবহ
```
Deep check-এ সাবধান: shared dependency (যেমন DB) একটু ধীর হলে **সব region একসাথে unhealthy** দেখাতে পারে, তখন Route 53 সব বাদ দিয়ে দেয় (বা fail-open করে)। ভারসাম্য রাখুন।

---

## Part 4: Evaluate Target Health (Alias)

Alias record (ALB, CloudFront ইত্যাদি)-এ **"Evaluate target health = Yes"** দিলে আলাদা health check ছাড়াই:
- **ALB/NLB**: target group-এ কোনো healthy target না থাকলে record unhealthy
- অন্য Alias record: সেই record-এর health

Failover/latency/weighted-এ ALB-এর জন্য এটাই সবচেয়ে সহজ উপায়।

---

## Part 5: DNS Failover Pattern

### Active-Passive
```
Failover PRIMARY:   Alias → ALB Mumbai        (evaluate target health)
Failover SECONDARY: Alias → ALB Singapore     (warm standby)
                    বা Alias → S3/CloudFront "We'll be back" page
```

### Active-Active (latency + health)
```
Latency (ap-south-1):     Alias → ALB Mumbai      + health
Latency (eu-central-1):   Alias → ALB Frankfurt   + health
Latency (us-east-1):      Alias → ALB Virginia    + health
```
একটা region বন্ধ হলে সেই এলাকার user পরের কাছের healthy region-এ।

### Nested: policy মিলিয়ে
Latency-র ভেতরে প্রতিটা region-এ weighted বা failover:
```
api.shopbd.com (Latency)
 ├── ap-south-1 → Alias → mumbai.api.shopbd.com (Failover: primary Mumbai ALB, secondary static page)
 └── eu-central-1 → Alias → frankfurt.api.shopbd.com (Weighted: v1 90%, v2 10%)
```
**Traffic Flow** (visual editor + traffic policy) দিয়ে এমন জটিল tree সহজে বানানো ও version করা যায় (policy record-এর খরচ আলাদা)।

---

## Part 6: DNS Failover-এর সীমা ও Application Recovery Controller

### সীমা
- **TTL + client cache**: resolver বা app পুরনো উত্তর TTL (বা তার বেশি) ধরে রাখে; কিছু client (যেমন পুরনো JVM) DNS অনেকক্ষণ cache করে
- Health check detect করতে কিছু সময় (interval × threshold)
- মোট failover সময় সাধারণত **মিনিটের ঘরে**, সেকেন্ডে না

**দ্রুত failover লাগলে:** **Global Accelerator** (Day 48; static IP, DNS cache-এর উপর নির্ভর না, সাধারণত এক মিনিটের কম)।

### Route 53 Application Recovery Controller (ARC)
- **Readiness check**: DR region আসলে তৈরি কিনা (capacity, config মিলছে কিনা) আগে থেকে যাচাই
- **Routing control**: health check-এর উপর নির্ভর না করে **মানুষ বা automation নিজে on/off switch** দিয়ে region-এর traffic সরায়; switch-গুলো highly available data plane-এ (৫টা region-এ cluster)
- **Zonal shift**: একটা **AZ**-এর সমস্যায় ALB/NLB-এর traffic সেই AZ থেকে সাময়িক সরিয়ে নেওয়া
- ব্যবহার: mission-critical system, যেখানে "কখন failover" সিদ্ধান্ত নিয়ন্ত্রিত হতে হবে

---

## Part 7: Hands-on Lab — Failover

1. দুটো region-এ দুটো সহজ web server বা ALB (বা একটা ALB আর একটা S3 static "maintenance" site)
2. Health check: primary-র `/health` (HTTP, 30 s, threshold 3)
3. Records (`app.yourdomain.com`):
   - Failover **PRIMARY** → primary ALB (Alias, evaluate target health) বা EIP (A + health check)
   - Failover **SECONDARY** → S3 website / দ্বিতীয় region
4. ```bash
   watch -n 10 "dig +short app.yourdomain.com"
   ```
5. Primary-র app বন্ধ করুন (বা SG থেকে health checker-দের বাদ দিন) → কয়েক মিনিটে উত্তর secondary-তে বদলায় ✅
6. Primary আবার চালু → ফিরে আসে
7. **বোনাস:** Weighted record দিয়ে ৯০/১০ ভাগ করে ২০ বার `dig` চালিয়ে ভাগ দেখুন (low TTL সহ)
8. Health check মুছে ফেলুন (খরচ আছে)

---

## 🎯 আজকের মূল Takeaways

1. DNS ঠিকানা দেয়, traffic বহন করে না; TTL-এর কারণে পরিবর্তন ধীরে ছড়ায়
2. **Weighted** (canary), **Latency** (দ্রুততম region), **Failover** (primary/secondary), **Geolocation** (দেশ, **default record দিন**), **Geoproximity** (দূরত্ব + bias), Multivalue (৮টা healthy), IP-based (CIDR)
3. Health check: **endpoint** (string match), **calculated**, **CloudWatch alarm** (private resource-এর জন্য)
4. Alias-এ **evaluate target health** = ALB-এর সহজ health
5. Active-passive (failover) বনাম active-active (latency + health); nested / Traffic Flow
6. DNS failover মিনিটের ঘরে; দ্রুত চাইলে Global Accelerator; নিয়ন্ত্রিত failover-এ **ARC**

---

## 📝 Self-check Questions

1. নতুন version-এ ৫% traffic পাঠাতে কোন policy?
2. Geolocation-এ শুধু বাংলাদেশ আর ভারতের record দিলেন। আমেরিকার user কী পাবে?
3. Private subnet-এর database-এর health দেখে DNS failover করতে কী ধরনের health check?
4. Latency আর Geolocation-এর পার্থক্য কী?
5. Health check-এর সব checker endpoint-এ পৌঁছাতে পারছে না, অথচ app ঠিক আছে। কী দেখবেন?
6. DNS failover-এ ১ মিনিটের কম সময় লাগবে, এমন নিশ্চয়তা কি দেওয়া যায়? বিকল্প কী?
7. Multivalue answer কি ELB-এর বদলে ব্যবহার করা উচিত?

<details><summary>▶ উত্তর দেখুন</summary>

1. Weighted (যেমন ৯৫/৫)।
2. কোনো উত্তর না (NODATA), যদি default location record না থাকে; তাই default record দিতে হবে।
3. CloudWatch alarm-ভিত্তিক health check (Route 53 checker private IP-তে পৌঁছায় না)।
4. Latency = সবচেয়ে কম network latency-র region; Geolocation = user কোন দেশ/মহাদেশ থেকে (দূরত্ব বা গতি না)।
5. SG/NACL/firewall-এ Route 53 health checker-দের IP range allow করা আছে কিনা (আর path, port, protocol ঠিক কিনা)।
6. না; TTL আর client cache-এর কারণে মিনিটের ঘরে। Global Accelerator (static anycast IP, দ্রুত failover) বিবেচনা করুন।
7. না; এটা health সহ সহজ client-side ভাগ। আসল load balancing, TLS, routing-এর জন্য ELB।
</details>

---

## 💡 Pro Tips

- Failover record-এর TTL কম রাখুন (৬০ সেকেন্ড); Alias-এ target-এর TTL নেয়
- Health check-এর CloudWatch metric-এ alarm দিন, failover হলে জানতে পারবেন
- Geolocation-এ **default** সবসময়; আর মহাদেশ-level record দিয়ে ফাঁক পূরণ
- Weighted-এ **SetIdentifier** আর health check সহ; weight ০ দিয়ে কোনো endpoint maintenance-এ সরানো যায়
- DR drill: নিয়মিত primary বন্ধ করে দেখুন সত্যিই secondary-তে যায় কিনা

---

## 🎨 Quick Reference

```
Simple (no health) | Weighted (%; 0 = off) | Latency (fastest region) | Failover (PRIMARY+health / SECONDARY)
Geolocation (country/continent; ALWAYS add Default) | Geoproximity (distance + bias −99..+99)
Multivalue (up to 8 healthy) | IP-based (CIDR collections)
Health checks: endpoint (HTTP/HTTPS/TCP, string match) | calculated | CloudWatch alarm (private resources)
Interval 30 s / 10 s fast; failure threshold 3; allow Route 53 checker IPs
Alias: Evaluate target health = Yes
Nested records / Traffic Flow for combos | ARC: readiness, routing control, zonal shift
```

---

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** Geolocation-এ শুধু এশিয়ার দেশগুলোর record ছিল, default ছিল না। Europe-এ launch-এর দিন সেখানকার কোনো user site খুলতে পারল না।
**শিক্ষা:** Default location record।

**পরিস্থিতি ২:** Failover সেট করা ছিল, কিন্তু primary-র health check-এর path ছিল `/` যেটা CloudFront cache থেকে সবসময় 200 দিত। Server বন্ধ হলেও failover হলো না।
**শিক্ষা:** Health check সরাসরি আসল origin-এর অর্থবহ `/health` path-এ।

**পরিস্থিতি ৩:** Deep health check shared database চেক করত। DB সামান্য ধীর হতেই সব region একসাথে "unhealthy" দেখাল।
**শিক্ষা:** Health check-এ শুধু region-নির্দিষ্ট জিনিস; shared dependency-র জন্য আলাদা monitoring।

---

**⏮ আগের দিন:** [Day 45 — Route 53 Hosted Zones ও Records](./Day-45-Route53-Hosted-Zones-Records.md) | **⏭ পরের দিন:** [Day 47 — ALB, NLB ও GWLB](./Day-47-Load-Balancers-ALB-NLB-GWLB-Deep-Dive.md)
