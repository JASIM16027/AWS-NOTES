
# 📚 Day 25 — Event Triggers: S3, SQS, SNS, DynamoDB Streams ও EventBridge

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![SQS vs SNS](../images/14-sqs-vs-sns.png)

![SNS to SQS Fan-out](../images/21-sns-sqs-fanout.png)

**সময়:** ২ ঘণ্টা | **Module:** ৪ (Serverless & Lambda Fundamentals) — Day 4

## 🎯 আজকের লক্ষ্য
- S3 event notification → Lambda (আর recursive loop-এর বিপদ)
- SQS → Lambda: batch, visibility timeout, partial batch failure, DLQ
- SNS → Lambda, আর SNS → SQS → Lambda fan-out
- DynamoDB Streams → Lambda: change data capture
- EventBridge: rule, event pattern, scheduler (cron)
- কোন trigger কখন বাছবেন

---

## Part 1: S3 Event Notification → Lambda (Async)

S3-এ object তৈরি, মুছে ফেলা বা restore হলে Lambda-কে জানানো যায়।

### Setup
S3 bucket → **Properties → Event notifications** → Event type `s3:ObjectCreated:*` → Prefix `uploads/`, Suffix `.jpg` → Destination: Lambda।

### 📥 Event (সংক্ষেপে)
```json
{
  "Records": [{
    "eventName": "ObjectCreated:Put",
    "s3": {
      "bucket": { "name": "my-photos" },
      "object": { "key": "uploads/cat+photo.jpg", "size": 204800 }
    }
  }]
}
```

```python
import urllib.parse, boto3
s3 = boto3.client("s3")

def lambda_handler(event, context):
    for rec in event["Records"]:
        bucket = rec["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(rec["s3"]["object"]["key"])  # space → + হয়ে আসে!
        obj = s3.get_object(Bucket=bucket, Key=key)
        # ... thumbnail বানিয়ে অন্য bucket/prefix-এ রাখুন
```

### ⚠️ Recursive Loop — সবচেয়ে বিপজ্জনক ভুল
```
uploads/cat.jpg তৈরি → Lambda → thumbnail লেখে একই bucket-এ → আবার event → Lambda → ... ♾️
```
একটা loop কয়েক মিনিটে লাখো invocation আর বড় bill বানাতে পারে। (Lambda কিছু loop নিজে ধরে থামাতে পারে, কিন্তু সেটার উপর ভরসা করবেন না।)

**প্রতিরোধ:**
- Output **আলাদা bucket**-এ লিখুন (সবচেয়ে নিরাপদ)
- অথবা input prefix (`uploads/`) আর output prefix (`thumbnails/`) আলাদা, আর event filter-এ শুধু input prefix
- Reserved concurrency দিয়ে সীমা দিন (Day 27)

### অন্যান্য কথা
- S3 → Lambda **async**, তাই ২ বার retry আর on-failure destination প্রযোজ্য
- Event অনেক কম সময়েই delay বা duplicate হতে পারে → idempotent রাখুন
- একাধিক consumer লাগলে S3 → **SNS/EventBridge** → অনেকগুলো target
- S3 bucket-এ **EventBridge notification** চালু করলে আরও advanced filter পাওয়া যায়

---

## Part 2: SQS → Lambda (Poll-based)

Lambda নিজে SQS queue poll করে, message-গুলো **batch**-এ এনে function-এ দেয়।

```
Producer → SQS queue ←(poll)─ Lambda event source mapping → handler(batch of messages)
                   └─ fail হলে message আবার visible → retry → maxReceiveCount পার → DLQ
```

### 📥 Event
```json
{
  "Records": [
    { "messageId": "m1", "body": "{\"orderId\": 101}", "attributes": { "ApproximateReceiveCount": "1" } },
    { "messageId": "m2", "body": "{\"orderId\": 102}" }
  ]
}
```

### ⚙️ গুরুত্বপূর্ণ setting

| Setting | মানে | পরামর্শ |
|---|---|---|
| **Batch size** | এক invocation-এ কতগুলো message (Standard: ১০,০০০ পর্যন্ত; FIFO: ১০) | ১০ দিয়ে শুরু |
| **Batch window** | Batch ভরার জন্য কত সেকেন্ড অপেক্ষা (০–৩০০ s) | খরচ কমাতে কাজে লাগে |
| **Queue visibility timeout** | Message পড়ার পর কতক্ষণ লুকানো থাকবে | **Lambda timeout-এর কমপক্ষে ৬ গুণ** |
| **Redrive policy (DLQ)** | `maxReceiveCount` বার fail করলে DLQ-তে | ৩–৫ |
| **Maximum concurrency** | এই queue-র জন্য সর্বোচ্চ কতগুলো Lambda একসাথে | Downstream DB রক্ষা করতে |

### 🧩 Partial batch failure — খুব গুরুত্বপূর্ণ
Default-এ batch-এর **একটা message fail করলে পুরো batch** আবার আসে, ফলে সফলগুলোও আবার process হয়। সমাধান: event source mapping-এ **`ReportBatchItemFailures`** চালু করে শুধু ব্যর্থগুলো ফেরত দিন:

```python
import json

def lambda_handler(event, context):
    failures = []
    for msg in event["Records"]:
        try:
            order = json.loads(msg["body"])
            process(order)
        except Exception:
            failures.append({"itemIdentifier": msg["messageId"]})
    return {"batchItemFailures": failures}
```

### Standard বনাম FIFO queue-এর সাথে
- **Standard:** সর্বোচ্চ throughput, order নিশ্চিত না, duplicate হতে পারে
- **FIFO:** Message group ID অনুযায়ী ক্রম বজায়; এক group-এর message একসাথে একটাই Lambda process করে

---

## Part 3: SNS → Lambda (Async) ও Fan-out

**SNS** = pub/sub: একটা message সব subscriber-এর কাছে push হয়।

```python
def lambda_handler(event, context):
    for rec in event["Records"]:
        msg = rec["Sns"]["Message"]          # string
        subject = rec["Sns"].get("Subject")
```

### SNS → Lambda সরাসরি বনাম SNS → SQS → Lambda

| | SNS → Lambda | SNS → SQS → Lambda |
|---|---|---|
| Buffering | ❌ | ✅ Spike হলে queue-তে জমা থাকে |
| Lambda বন্ধ বা throttle হলে | SNS কিছুক্ষণ retry, তারপর subscription DLQ (না থাকলে হারায়) | Message ১৪ দিন পর্যন্ত queue-তে |
| Batch processing | ❌ | ✅ |
| সরলতা | সহজ | একটু বেশি setup |

👉 গুরুত্বপূর্ণ কাজে **SNS → SQS → Lambda** (Interview Q109-এর fan-out pattern)। প্রতিটা consumer-এর নিজস্ব queue, নিজস্ব DLQ, নিজস্ব গতি।

**Subscription filter policy** দিয়ে প্রতিটা subscriber শুধু দরকারি message পায়:
```json
{ "eventType": ["order_placed"], "amount": [{ "numeric": [">", 1000] }] }
```

---

## Part 4: DynamoDB Streams → Lambda (Poll-based)

**DynamoDB Streams** table-এর প্রতিটা item পরিবর্তনের (INSERT, MODIFY, REMOVE) ক্রমানুসারী log, ২৪ ঘণ্টা রাখে।

### Setup
Table → **Exports and streams** → DynamoDB stream চালু → View type: `NEW_AND_OLD_IMAGES` → Lambda trigger যোগ।

### 📥 Event
```json
{
  "Records": [{
    "eventName": "MODIFY",
    "dynamodb": {
      "Keys": { "orderId": { "S": "101" } },
      "OldImage": { "status": { "S": "PENDING" } },
      "NewImage": { "status": { "S": "SHIPPED" } }
    }
  }]
}
```
> Value-গুলো DynamoDB-র type format-এ আসে (`{"S": "..."}`, `{"N": "5"}`)। Python-এ `boto3.dynamodb.types.TypeDeserializer` দিয়ে সাধারণ dict বানান।

### Use case
- Order `SHIPPED` হলে customer-কে email (SES/SNS)
- OpenSearch-এ search index sync
- Audit log / history table
- Aggregation (মোট বিক্রি counter update)

### ⚠️ Stream-এর error handling আলাদা!
Stream (Kinesis-এর মতো) **shard অনুযায়ী ক্রমানুসারে** চলে। একটা record fail করলে Lambda **ঐ shard আটকে রেখে** বারবার retry করে, পরের record-গুলো অপেক্ষা করে (**"poison pill"**)। সমাধান, event source mapping-এ:

| Setting | কাজ |
|---|---|
| `MaximumRetryAttempts` | কতবার retry (যেমন ৩) |
| `MaximumRecordAgeInSeconds` | এর চেয়ে পুরনো record বাদ |
| `BisectBatchOnFunctionError` | Batch অর্ধেক করে দোষী record খুঁজে বের করে |
| **On-failure destination** (SQS/SNS/S3) | বাদ দেওয়া record-এর তথ্য রাখে |
| `ReportBatchItemFailures` | কোন record থেকে আবার শুরু করবে |
| **Filter criteria** | শুধু দরকারি event-এ Lambda চলবে (যেমন `eventName = INSERT`), খরচ কমে |

**মনিটর করুন:** `IteratorAge` metric। বাড়তে থাকলে Lambda পিছিয়ে পড়ছে বা আটকে আছে।

---

## Part 5: EventBridge → Lambda (Async)

**Amazon EventBridge** = serverless **event bus**। Event আসে (AWS service, SaaS, আপনার app থেকে), **rule**-এর **event pattern** মিললে target-এ পাঠায়।

### Rule + Event Pattern
উদাহরণ: কোনো EC2 instance `stopped` হলে Lambda চালাও।
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": { "state": ["stopped"] }
}
```

নিজের app থেকে event পাঠানো:
```python
import json, boto3
events = boto3.client("events")
events.put_events(Entries=[{
    "Source": "myapp.orders",
    "DetailType": "OrderPlaced",
    "Detail": json.dumps({"orderId": 101, "amount": 1500}),
    "EventBusName": "default"
}])
```
Rule pattern: `{"source": ["myapp.orders"], "detail": {"amount": [{"numeric": [">", 1000]}]}}`

### ⏰ Scheduled job: EventBridge Scheduler
Cron-এর serverless বিকল্প (Module 3-এ systemd timer/cron ছিল):
```bash
aws scheduler create-schedule --name nightly-report \
  --schedule-expression "cron(0 2 * * ? *)" \
  --schedule-expression-timezone "Asia/Dhaka" \
  --flexible-time-window Mode=OFF \
  --target Arn=arn:aws:lambda:ap-south-1:111122223333:function:report,RoleArn=arn:aws:iam::111122223333:role/scheduler-invoke
```
- `rate(5 minutes)` বা `cron(...)`, **timezone support** সহ
- One-time schedule-ও করা যায় (যেমন "৩ দিন পর reminder")
- পুরনো পদ্ধতি: EventBridge **rule** with schedule (আগে "CloudWatch Events" নামে পরিচিত)

### EventBridge-এর বাড়তি সুবিধা
- ২০+ ধরনের target (Lambda, SQS, Step Functions, API destination...)
- **Archive & replay**: পুরনো event আবার চালানো
- **Schema registry**
- **EventBridge Pipes**: source (SQS, DynamoDB Stream) → filter → enrich → target, code ছাড়াই

---

## Part 6: কোন Trigger কখন? — তুলনা

| প্রয়োজন | বাছুন |
|---|---|
| File upload হলে process | **S3 event** (একাধিক consumer হলে S3 → EventBridge/SNS) |
| Spike সামলানো, buffer, retry, rate নিয়ন্ত্রণ | **SQS** |
| Strict ক্রম + exactly-once processing | **SQS FIFO** |
| এক event → অনেক consumer | **SNS → SQS** fan-out বা **EventBridge** |
| DB-র পরিবর্তনে প্রতিক্রিয়া | **DynamoDB Streams** |
| AWS service event (EC2 stop, CodePipeline fail) | **EventBridge rule** |
| Content-based complex routing, SaaS event | **EventBridge** |
| নির্দিষ্ট সময়ে চালানো (cron) | **EventBridge Scheduler** |
| Real-time বিশাল stream, replay, অনেক consumer | **Kinesis Data Streams** (Module 5) |

| Trigger | Invocation model | ব্যর্থ event |
|---|---|---|
| S3, SNS, EventBridge | Async | Lambda retry ২ বার → DLQ/Destination (SNS/EventBridge-এর নিজেরও retry আছে) |
| SQS | Poll | Queue redrive → DLQ |
| DynamoDB Streams, Kinesis | Poll (ordered) | Retry/age limit → on-failure destination |

---

## Part 7: Hands-on Lab — Order Processing

1. SQS queue `orders` + DLQ `orders-dlq` (maxReceiveCount = 3), visibility timeout 60 s
2. Lambda `process-order` (timeout 10 s), Part 2-এর handler (partial batch response সহ)
3. Execution role-এ `AWSLambdaSQSQueueExecutionRole` managed policy (Day 26)
4. Trigger: SQS `orders`, batch size 10, **Report batch item failures** চালু
5. Test:
```bash
aws sqs send-message --queue-url $Q --message-body '{"orderId": 101}'
aws sqs send-message --queue-url $Q --message-body 'not-json'      # ইচ্ছা করে ভাঙা
```
6. CloudWatch log-এ প্রথমটা সফল দেখুন; দ্বিতীয়টা ৩ বার চেষ্টার পর `orders-dlq`-তে গেছে কিনা দেখুন
7. **বোনাস:** EventBridge Scheduler দিয়ে প্রতি ৫ মিনিটে DLQ-র message সংখ্যা চেক করে SNS-এ alert দেওয়া একটা Lambda

---

## 🎯 আজকের মূল Takeaways

1. **S3 → Lambda** (async): key URL-decode করুন; **recursive loop** এড়াতে output আলাদা bucket/prefix
2. **SQS → Lambda** (poll): visibility timeout ≥ ৬ × Lambda timeout; **ReportBatchItemFailures**; DLQ
3. **SNS → SQS → Lambda** = নির্ভরযোগ্য fan-out
4. **DynamoDB Streams**: ক্রমানুসারী; poison pill ঠেকাতে retry/age limit, bisect, on-failure destination; `IteratorAge` দেখুন
5. **EventBridge**: event pattern-ভিত্তিক routing; **Scheduler** = serverless cron (timezone সহ)
6. সব async/poll consumer **idempotent**

---

## 📝 Self-check Questions

1. S3 trigger-এ Lambda একই bucket-এ output লিখলে কী হতে পারে? কীভাবে ঠেকাবেন?
2. SQS-এর visibility timeout Lambda timeout-এর চেয়ে কম হলে কী হয়?
3. Batch-এর ১০টা message-এর ১টা fail করল। Partial batch response ছাড়া কী হবে?
4. DynamoDB Stream-এ একটা ভাঙা record সব processing আটকে দিচ্ছে। কোন setting-গুলো দিয়ে ঠিক করবেন?
5. প্রতিদিন বাংলাদেশ সময় রাত ২টায় Lambda চালাতে কী ব্যবহার করবেন?
6. একটা "OrderPlaced" event-এ email, inventory আর analytics তিনটা আলাদা service চলবে। কোন pattern?
7. S3 object key `my photo.jpg` Lambda-তে কীভাবে আসে?

<details><summary>▶ উত্তর দেখুন</summary>

1. Recursive loop: output নিজেই আবার event তৈরি করে, অসীম invocation। আলাদা bucket, বা আলাদা prefix + event filter, আর reserved concurrency দিয়ে সীমা।
2. Lambda কাজ করার মাঝেই message আবার visible হয়, অন্য Lambda-ও একই message নেয়; duplicate processing।
3. পুরো batch fail ধরা হয়, সফল ৯টাও আবার process হবে।
4. `MaximumRetryAttempts`, `MaximumRecordAgeInSeconds`, `BisectBatchOnFunctionError`, on-failure destination (আর `ReportBatchItemFailures`)।
5. EventBridge Scheduler, `cron(0 2 * * ? *)` আর timezone `Asia/Dhaka`।
6. SNS → প্রতিটা service-এর নিজস্ব SQS → Lambda (fan-out), অথবা EventBridge rule-এ তিনটা target।
7. URL-encoded: `my+photo.jpg`; `unquote_plus` দিয়ে decode করতে হয়।
</details>

---

## 💡 Pro Tips

- Event source mapping-এ **filter criteria** দিয়ে অদরকারি event-এ Lambda চালানো বন্ধ করুন, খরচ কমে
- DLQ-তে message এলে alarm (`ApproximateNumberOfMessagesVisible > 0`)
- DLQ ঠিক করার পর **redrive** করে message মূল queue-তে ফেরত পাঠানো যায়
- DynamoDB Streams-এর বদলে দরকার হলে **Kinesis Data Streams for DynamoDB** (বেশি retention, বেশি consumer)
- Lambda চেইন করতে (Lambda থেকে Lambda call) না করে **Step Functions** বা **SQS/EventBridge** ব্যবহার করুন (Module 5)

---

## 🎨 Quick Reference

```
S3 ──async──► Lambda          (Records[].s3.bucket.name / object.key [URL-encoded])
SNS ─async──► Lambda          (Records[].Sns.Message)
EventBridge ─async─► Lambda   (detail-type, source, detail)
SQS ──poll──► Lambda          (Records[].body)  → batchItemFailures, DLQ
DDB Stream ─poll(ordered)─► Lambda (Records[].dynamodb.NewImage/OldImage) → IteratorAge
```

```
SQS visibility timeout ≥ 6 × Lambda timeout
Stream: MaximumRetryAttempts + BisectBatchOnFunctionError + on-failure destination
Scheduler: cron(0 2 * * ? *) + timezone
```

---

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** Image resize Lambda একই bucket-এর একই prefix-এ output লিখছিল। রাতের মধ্যে কয়েক লাখ invocation আর বড় bill।
**শিক্ষা:** Output আলাদা bucket-এ, আর reserved concurrency দিয়ে সীমা।

**পরিস্থিতি ২:** DynamoDB Stream-এ একটা ভাঙা record ২৪ ঘণ্টা ধরে retry হলো; সব email notification আটকে থাকল। কেউ টের পায়নি।
**শিক্ষা:** Retry/age সীমা, bisect, on-failure destination, আর `IteratorAge` alarm।

**পরিস্থিতি ৩:** SQS batch-এ একটা খারাপ message-এর কারণে সফল message-গুলোও বারবার process হচ্ছিল; customer একাধিক confirmation email পেল।
**শিক্ষা:** `ReportBatchItemFailures` + idempotency।

---

**⏮ আগের দিন:** [Day 24 — Invocation Models ও API Gateway](./Day-24-Invocation-Models-API-Gateway.md) | **⏭ পরের দিন:** [Day 26 — Permissions ও Security](./Day-26-Permissions-Security-VPC-Secrets.md)
