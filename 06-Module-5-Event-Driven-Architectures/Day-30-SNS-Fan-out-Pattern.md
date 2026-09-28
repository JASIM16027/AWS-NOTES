
# 📚 Day 30 — SNS গভীরে ও Fan-out Pattern

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![SQS vs SNS](../images/14-sqs-vs-sns.png)

![SNS to SQS Fan-out](../images/21-sns-sqs-fanout.png)

**সময়:** ১.৫ ঘণ্টা | **Module:** ৫ (Event-Driven Architectures with Lambda) — Day 2

## 🎯 আজকের লক্ষ্য
- SNS-এর মূল ধারণা: topic, publisher, subscription
- Subscriber-এর ধরন (SQS, Lambda, HTTP/S, email, SMS, mobile push, Firehose)
- **Message filtering** (attribute আর body)
- Delivery retry আর subscription DLQ
- SNS FIFO topic
- **Fan-out pattern** (SNS → অনেকগুলো SQS) পুরোটা setup
- কখন SNS, কখন EventBridge

---

## Part 1: SNS কী?

**Amazon SNS (Simple Notification Service)** = managed **pub/sub**। Publisher একটা **topic**-এ message পাঠায়, আর topic সেটা **সব subscriber**-এর কাছে **push** করে।

```
Publisher ──Publish──► Topic "order-events" ──► Subscriber 1 (SQS)
                                            ──► Subscriber 2 (Lambda)
                                            ──► Subscriber 3 (Email)
```

| SQS | SNS |
|---|---|
| Queue: message **জমা থাকে**, consumer **pull** করে | Topic: message সাথে সাথে **push** হয়, জমা থাকে না |
| এক message = **এক** consumer | এক message = **সব** subscriber |
| Buffer, load leveling | Broadcast, notification |

👉 দুটো মিলিয়ে সবচেয়ে শক্তিশালী pattern: **SNS → SQS (fan-out)**।

---

## Part 2: Subscriber-এর ধরন

| Protocol | ব্যবহার | মনে রাখুন |
|---|---|---|
| **SQS** | নির্ভরযোগ্য async processing | Fan-out-এর ভিত্তি; queue policy-তে SNS-কে অনুমতি দিতে হয় |
| **Lambda** | সরাসরি code চালানো | Async invoke (Day 24) |
| **HTTP/HTTPS** | Webhook, অন্য সিস্টেম | Subscription **confirm** করতে হয় (URL-এ confirmation আসে) |
| **Email / Email-JSON** | মানুষকে alert | Subscriber-কে email-এর link-এ confirm করতে হয় |
| **SMS** | Text message | দেশ অনুযায়ী নিয়ম আর খরচ; spending limit আছে |
| **Mobile push** | App notification (APNs, FCM) | Platform application লাগে |
| **Amazon Data Firehose** | S3/Redshift-এ archive | সব event রেখে দিতে |

> 💡 Email subscription শুধু **alert** (যেমন CloudWatch alarm)-এর জন্য ভালো। Customer-কে transactional email পাঠাতে **Amazon SES** ব্যবহার করুন।

---

## Part 3: Publish করা

```python
import boto3, json
sns = boto3.client("sns")
TOPIC = "arn:aws:sns:ap-south-1:111122223333:order-events"

sns.publish(
    TopicArn=TOPIC,
    Message=json.dumps({"orderId": 101, "amount": 1500, "country": "BD"}),
    Subject="OrderPlaced",
    MessageAttributes={
        "eventType": {"DataType": "String", "StringValue": "OrderPlaced"},
        "amount":    {"DataType": "Number", "StringValue": "1500"}
    },
)
```
- **Message attributes** = metadata; filtering-এর জন্য খুব কাজের
- Batch publish: `publish_batch` (একসাথে ১০টা পর্যন্ত), কম খরচ

### Lambda subscriber-এ event
```python
def lambda_handler(event, context):
    for rec in event["Records"]:
        msg = json.loads(rec["Sns"]["Message"])
        attrs = rec["Sns"]["MessageAttributes"]
```

### SQS subscriber-এ কী আসে?
Default-এ SQS message-এর body-তে পুরো **SNS envelope** (JSON: `Type`, `MessageId`, `TopicArn`, `Message`...) আসে, আসল message থাকে `Message` field-এর ভেতরে string হিসেবে। **Raw message delivery** চালু করলে শুধু আসল message আসে, parse করা সহজ হয়।

---

## Part 4: Message Filtering — প্রত্যেকে শুধু যা দরকার

Filter ছাড়া প্রতিটা subscriber **সব** message পায়, তারপর নিজে বাদ দিতে হয় (অপ্রয়োজনীয় খরচ)। **Subscription filter policy** দিলে SNS নিজেই বাছাই করে পাঠায়।

### Attribute-ভিত্তিক (default)
```json
{
  "eventType": ["OrderPlaced", "OrderCancelled"],
  "amount": [{ "numeric": [">=", 1000] }]
}
```
→ শুধু OrderPlaced/OrderCancelled **এবং** amount ≥ 1000।

### Body-ভিত্তিক (`FilterPolicyScope = MessageBody`)
```json
{ "country": ["BD", "IN"], "customer": { "tier": ["gold"] } }
```

### Filter operator (অনেকগুলো)

| Operator | উদাহরণ |
|---|---|
| Exact match | `"eventType": ["OrderPlaced"]` |
| Anything-but | `"status": [{"anything-but": ["TEST"]}]` |
| Prefix / suffix | `"sku": [{"prefix": "ELEC-"}]` |
| Numeric range | `"amount": [{"numeric": [">", 100, "<=", 5000]}]` |
| Exists | `"coupon": [{"exists": true}]` |
| OR (একই key-তে একাধিক মান) | `"country": ["BD", "IN"]` |

- **Key-গুলোর মধ্যে AND**, একই key-এর মানগুলোর মধ্যে **OR**
- Filter policy বদলানোর পর কার্যকর হতে কিছুটা সময় (মিনিটখানেক) লাগতে পারে

---

## Part 5: Delivery Retry ও Subscription DLQ

SNS subscriber-এ পৌঁছাতে না পারলে (Lambda throttle, HTTP endpoint down) **retry** করে:
- **AWS-managed endpoint** (SQS, Lambda): অনেকবার, কয়েক দিন ধরে retry
- **HTTP/S**: retry policy নিজে configure করা যায় (কতবার, কত বিরতিতে, backoff)

সব retry শেষ হলে message **হারিয়ে যায়**, যদি না subscription-এ **DLQ (redrive policy)** দেওয়া থাকে:

```bash
aws sns set-subscription-attributes --subscription-arn $SUB_ARN \
  --attribute-name RedrivePolicy \
  --attribute-value '{"deadLetterTargetArn":"arn:aws:sqs:ap-south-1:111122223333:sns-email-dlq"}'
```
> ⚠️ SNS DLQ **subscription-এ** দেওয়া হয়, topic-এ না। আর DLQ-র queue policy-তে SNS-কে send করার অনুমতি দিতে হয়।

**Filter-এ বাদ পড়া message DLQ-তে যায় না**, সেটা স্বাভাবিকভাবেই পাঠানো হয় না।

---

## Part 6: SNS FIFO Topic

| | Standard topic | **FIFO topic** |
|---|---|---|
| Ordering | Best-effort | Message group অনুযায়ী strict |
| Duplicate | হতে পারে | Dedup (৫ মিনিট) |
| Throughput | প্রায় unlimited | সীমিত (কম) |
| Subscriber | সব ধরনের | মূলত **SQS queue** |
| নাম | যেকোনো | `.fifo` দিয়ে শেষ |

**ব্যবহার:** একই event একাধিক system-এ **ক্রম বজায় রেখে** পাঠাতে হবে। যেমন bank account-এর লেনদেন, একই সাথে ledger service আর notification service-এ।

```
Publisher ──► SNS FIFO topic ──► SQS FIFO (ledger)
                             ──► SQS FIFO (fraud check)
```

---

## Part 7: Fan-out Pattern — পুরো Setup

**লক্ষ্য:** একটা "OrderPlaced" event → email, inventory, analytics, fraud (শুধু বড় order) চারটা আলাদা service।

```
Order API ──► SNS "order-events"
                ├──► SQS email-q      ──► Lambda (email পাঠায়)       + DLQ
                ├──► SQS inventory-q  ──► ECS worker (stock কমায়)     + DLQ
                ├──► SQS analytics-q  ──► Firehose → S3
                └──► SQS fraud-q [filter: amount ≥ 1000] ──► Fraud service + DLQ
```

### ধাপ
1. Topic: `order-events`
2. প্রতিটা consumer-এর জন্য আলাদা **SQS queue + DLQ**
3. প্রতিটা queue-কে topic-এ subscribe করান, **raw message delivery** চালু করুন
4. **Queue access policy**-তে SNS-কে অনুমতি দিন (`aws:SourceArn` দিয়ে শুধু এই topic):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "sns.amazonaws.com" },
    "Action": "sqs:SendMessage",
    "Resource": "arn:aws:sqs:ap-south-1:111122223333:email-q",
    "Condition": { "ArnEquals": { "aws:SourceArn": "arn:aws:sns:ap-south-1:111122223333:order-events" } }
  }]
}
```
5. Fraud queue-র subscription-এ filter policy: `{"amount": [{"numeric": [">=", 1000]}]}`
6. Encryption থাকলে: SQS বা SNS-এ **customer managed KMS key** দিলে key policy-তে SNS-কে `kms:GenerateDataKey` আর `kms:Decrypt` অনুমতি দিতে হবে (AWS managed key `aws/sqs`-এ SNS পাঠাতে পারে না)

### কেন SNS → SQS, সরাসরি SNS → Lambda না?

| সুবিধা | ব্যাখ্যা |
|---|---|
| **Buffer** | Consumer ধীর বা down হলেও message queue-তে ১৪ দিন পর্যন্ত থাকে |
| **স্বাধীন গতি** | প্রতিটা consumer নিজের গতিতে, নিজের scale-এ |
| **আলাদা failure** | Email service ভাঙলে inventory-র কিছু হয় না |
| **আলাদা DLQ ও retry** | প্রতিটার নিজস্ব redrive |
| **Batch** | Lambda একসাথে অনেক message নিতে পারে |
| **নতুন consumer যোগ** | শুধু নতুন queue subscribe, publisher অপরিবর্তিত |

---

## Part 8: SNS বনাম EventBridge (কাল গভীরে)

| | SNS | EventBridge |
|---|---|---|
| Model | Topic → subscriber | Bus → rule (pattern) → target |
| Filtering | Filter policy (attribute/body) | আরও শক্তিশালী event pattern |
| Target | SQS, Lambda, HTTP, email, SMS, mobile push, Firehose | ২০+ AWS service, API destination, অন্য bus |
| AWS service event | নির্দিষ্ট কিছু service SNS-এ পাঠায় | **প্রায় সব AWS service** নিজে পাঠায় |
| SaaS event | ❌ | ✅ Partner event source |
| Archive / replay | ❌ | ✅ |
| Throughput / latency | খুব বেশি, খুব কম latency | বেশি, একটু বেশি latency |
| মানুষকে SMS/email/push | ✅ | ❌ (SNS-কে target দিয়ে) |

👉 সহজ বিশাল fan-out আর মানুষের notification → **SNS**। Event routing, AWS/SaaS event, বেশি filter → **EventBridge**।

---

## Part 9: Hands-on Lab

1. Topic `lab-order-events`
2. তিনটা SQS queue: `lab-email`, `lab-inventory`, `lab-fraud` (প্রতিটার DLQ সহ)
3. তিনটাকে subscribe করান (raw delivery চালু), queue policy-তে SNS-কে অনুমতি
4. `lab-fraud`-এ filter: `{"amount": [{"numeric": [">=", 1000]}]}`
5. Publish:
```bash
aws sns publish --topic-arn $TOPIC --message '{"orderId":1}' \
  --message-attributes '{"amount":{"DataType":"Number","StringValue":"500"}}'
aws sns publish --topic-arn $TOPIC --message '{"orderId":2}' \
  --message-attributes '{"amount":{"DataType":"Number","StringValue":"2500"}}'
```
6. যাচাই: email আর inventory queue-তে ২টা করে, fraud queue-তে শুধু order 2
7. একটা email subscription যোগ করে confirm করুন, আর CloudWatch alarm-এর action হিসেবে এই topic দিন

---

## 🎯 আজকের মূল Takeaways

1. SNS = pub/sub, **push**, এক message সব subscriber-এর কাছে, জমা রাখে না
2. Subscriber: SQS, Lambda, HTTP/S, email, SMS, mobile push, Firehose
3. **Filter policy** (attribute বা body) দিয়ে প্রত্যেকে শুধু দরকারি message পায়
4. সব retry শেষে হারানো ঠেকাতে **subscription-level DLQ**
5. **SNS FIFO** = একাধিক consumer-এ ক্রম + dedup
6. **Fan-out = SNS → প্রতিটা consumer-এর নিজের SQS (+DLQ)**; queue policy-তে `aws:SourceArn`
7. Raw message delivery চালু রাখুন

---

## 📝 Self-check Questions

1. SQS আর SNS-এর মূল পার্থক্য দুটো বলুন।
2. SNS → SQS subscription কাজ করছে না, message আসছে না। প্রথমে কী দেখবেন?
3. Fraud service শুধু ১,০০০ টাকার বেশি order চায়। কীভাবে করবেন?
4. SQS-এ message এলে body-তে অনেক বাড়তি JSON field দেখাচ্ছে। কেন?
5. SNS-এর DLQ কোথায় configure করা হয়?
6. একই bank লেনদেন দুটো service-এ ক্রম বজায় রেখে পাঠাতে কী ব্যবহার করবেন?
7. Customer-কে order confirmation email পাঠাতে SNS email subscription কেন ঠিক না?

<details><summary>▶ উত্তর দেখুন</summary>

1. SQS pull করে আর message জমা রাখে; SNS push করে আর রাখে না। SQS-এ এক message একজন পায়; SNS-এ সবাই পায়।
2. SQS queue access policy-তে SNS topic-কে `sqs:SendMessage` অনুমতি দেওয়া আছে কিনা (আর KMS key policy, যদি encrypted হয়)।
3. Fraud queue-র subscription-এ filter policy: `{"amount": [{"numeric": [">", 1000]}]}` (attribute হিসেবে amount পাঠাতে হবে, বা body scope)।
4. Raw message delivery বন্ধ, তাই পুরো SNS envelope আসছে। চালু করুন বা `Message` field parse করুন।
5. Subscription-এ (redrive policy), topic-এ না।
6. SNS FIFO topic → SQS FIFO queue (message group = account ID)।
7. প্রতিটা email ঠিকানাকে subscribe আর confirm করতে হয়, template/personalization নেই; transactional email-এর জন্য SES।
</details>

---

## 💡 Pro Tips

- Message attribute-এ `eventType`, `version` রাখুন। Filter আর versioning দুটোই সহজ হয়
- প্রতিটা consumer queue-এর নাম দিন `<topic>-<consumer>` ধাঁচে, খুঁজে পেতে সুবিধা
- Topic-এর access policy দিয়ে কে publish করতে পারবে তা সীমিত করুন
- CloudWatch metric `NumberOfNotificationsFailed` আর `NumberOfNotificationsFilteredOut` দেখুন
- Cross-account fan-out: অন্য account-এর SQS-কেও subscribe করানো যায় (দুই পাশের policy লাগে)

---

## 🎨 Quick Reference

```
Topic → Subscriptions (SQS, Lambda, HTTP/S, email, SMS, push, Firehose)
Filter policy: attributes (default) or MessageBody; AND across keys, OR within key
Subscription DLQ: RedrivePolicy on the subscription
Raw message delivery: ON for SQS/HTTP subscribers
FIFO topic (.fifo) → SQS FIFO: ordering by group + dedup
Fan-out: SNS → SQS per consumer (+ DLQ each); queue policy with aws:SourceArn
```

```bash
aws sns create-topic --name order-events
aws sns subscribe --topic-arn $TOPIC --protocol sqs --notification-endpoint $QUEUE_ARN \
  --attributes RawMessageDelivery=true
aws sns publish --topic-arn $TOPIC --message '{"orderId":1}'
```

---

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** SNS → Lambda সরাসরি ছিল। Sale-এর দিন Lambda throttle হলো, আর retry শেষে কয়েক হাজার order-এর email কখনো গেল না।
**শিক্ষা:** গুরুত্বপূর্ণ consumer-এর সামনে SQS রাখুন, আর subscription DLQ দিন।

**পরিস্থিতি ২:** নতুন SQS subscription যোগ করা হলো, কিন্তু কোনো message এলো না। Queue policy-তে SNS-কে অনুমতি দেওয়া হয়নি, আর queue customer KMS key দিয়ে encrypted ছিল।
**শিক্ষা:** Queue policy আর KMS key policy দুটোই চেক করুন।

**পরিস্থিতি ৩:** Filter ছাড়া fraud service সব order পাচ্ছিল, নিজে বাদ দিচ্ছিল। প্রতি মাসে লাখো অপ্রয়োজনীয় Lambda invocation।
**শিক্ষা:** Filter policy দিয়ে উৎসেই বাছাই।

---

**⏮ আগের দিন:** [Day 29 — SQS গভীরে](./Day-29-SQS-Deep-Dive-Standard-FIFO-DLQ.md) | **⏭ পরের দিন:** [Day 31 — EventBridge গভীরে](./Day-31-EventBridge-Buses-Rules-Cross-Account.md)
