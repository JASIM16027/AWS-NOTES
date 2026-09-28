
# 📚 Day 32 — Step Functions Basics: State Machine, States, Standard বনাম Express

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![Step Functions Order Workflow](../images/40-step-functions-order-workflow.png)

**সময়:** ১.৫ ঘণ্টা | **Module:** ৫ (Event-Driven Architectures with Lambda) — Day 4

## 🎯 আজকের লক্ষ্য
- Step Functions কী, কেন Lambda দিয়ে Lambda call করা খারাপ
- State machine আর Amazon States Language (ASL)
- সব state type: Task, Choice, Wait, Parallel, Map, Pass, Succeed, Fail
- State-এর মধ্যে data কীভাবে চলে (InputPath, Parameters, ResultPath, OutputPath)
- **Standard বনাম Express** workflow
- Direct SDK integration (Lambda ছাড়াই DynamoDB, SQS, SNS)

---

## Part 1: সমস্যা — Lambda দিয়ে Lambda চেইন

একটা order process করতে কয়েকটা ধাপ:
```
Validate → Reserve inventory → Charge payment → Ship → Notify
```

### ❌ খারাপ উপায়: এক Lambda আরেকটাকে call করে
```
ValidateFn ──invoke──► InventoryFn ──invoke──► PaymentFn ──invoke──► ...
```
- প্রতিটা Lambda অপেক্ষা করে বসে থাকে → **দুবার টাকা** (caller + callee)
- কোথায় fail করল, কতটা হয়েছে, বোঝা কঠিন
- Retry, timeout, rollback সব নিজে code-এ লিখতে হয়
- ১৫ মিনিটের সীমা পুরো চেইনের উপর

### ✅ ভালো উপায়: Step Functions
**AWS Step Functions** = serverless **workflow orchestration**। ধাপগুলো একটা **state machine**-এ define করেন, আর Step Functions:
- প্রতিটা ধাপ ক্রমানুসারে বা parallel-এ চালায়
- **Retry, catch, timeout** declarative ভাবে (code ছাড়া)
- প্রতিটা execution-এর **visual history**: কোন ধাপ, কী input/output, কোথায় fail
- Standard workflow **১ বছর** পর্যন্ত চলতে পারে (মানুষের approval-এর অপেক্ষা সহ)

---

## Part 2: State Machine ও ASL

State machine লেখা হয় **Amazon States Language (ASL)**, একটা JSON format-এ (console-এ **Workflow Studio** দিয়ে drag-and-drop-ও করা যায়)।

```json
{
  "Comment": "Simple order workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:ap-south-1:111122223333:function:validate-order",
        "Payload.$": "$"
      },
      "OutputPath": "$.Payload",
      "Next": "IsHighValue"
    },
    "IsHighValue": {
      "Type": "Choice",
      "Choices": [
        { "Variable": "$.amount", "NumericGreaterThan": 10000, "Next": "ManualReview" }
      ],
      "Default": "ChargePayment"
    },
    "ManualReview": {
      "Type": "Pass",
      "Result": "sent for review",
      "End": true
    },
    "ChargePayment": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": { "FunctionName": "charge-payment", "Payload.$": "$" },
      "OutputPath": "$.Payload",
      "Next": "Done"
    },
    "Done": { "Type": "Succeed" }
  }
}
```

| অংশ | মানে |
|---|---|
| `StartAt` | প্রথম state |
| `States` | সব state-এর map |
| `Type` | State-এর ধরন |
| `Next` / `End: true` | পরের state / শেষ |
| `$` | বর্তমান input (JSONPath) |
| `"Payload.$": "$"` | `.$` দিয়ে শেষ হলে মানটা JSONPath হিসেবে পড়া হয় |

> 💡 Step Functions-এ এখন **JSONata** query language-ও ব্যবহার করা যায় (`"QueryLanguage": "JSONata"`), data transform সহজ হয়। এখানে পরিচিত JSONPath দিয়ে দেখাচ্ছি।

---

## Part 3: সব State Type

### 1️⃣ Task: কাজ করা
Lambda, বা সরাসরি AWS service (DynamoDB, SQS, SNS, ECS, Glue, Bedrock...)।
```json
"SaveOrder": {
  "Type": "Task",
  "Resource": "arn:aws:states:::dynamodb:putItem",
  "Parameters": {
    "TableName": "orders",
    "Item": { "orderId": { "S.$": "$.orderId" }, "status": { "S": "PAID" } }
  },
  "ResultPath": null,
  "Next": "Notify"
}
```
👆 Lambda ছাড়াই DynamoDB-তে লেখা: **direct SDK integration** (কম code, কম খরচ, কম latency)।

### 2️⃣ Choice: if/else
```json
"CheckStock": {
  "Type": "Choice",
  "Choices": [
    { "Variable": "$.inStock", "BooleanEquals": false, "Next": "OutOfStock" },
    { "And": [
        { "Variable": "$.amount", "NumericGreaterThanEquals": 1000 },
        { "Variable": "$.country", "StringEquals": "BD" }
      ], "Next": "FreeShipping" }
  ],
  "Default": "NormalShipping"
}
```
Comparison: `StringEquals`, `NumericGreaterThan`, `BooleanEquals`, `IsPresent`, `StringMatches` (wildcard), `TimestampLessThan`... আর `And`, `Or`, `Not`।

### 3️⃣ Wait: অপেক্ষা
```json
"WaitForCooling": { "Type": "Wait", "Seconds": 600, "Next": "SendReminder" }
```
বা `"Timestamp": "2026-10-01T09:00:00Z"`, বা `"SecondsPath": "$.delay"`। অপেক্ষার সময় **Lambda চলে না, খরচ হয় না** (Standard-এ state transition-এর দাম শুধু)।

### 4️⃣ Parallel: একসাথে কয়েকটা শাখা
```json
"ProcessInParallel": {
  "Type": "Parallel",
  "Branches": [
    { "StartAt": "ReserveInventory", "States": { "ReserveInventory": { "Type": "Task", "Resource": "arn:aws:states:::lambda:invoke", "Parameters": { "FunctionName": "reserve", "Payload.$": "$" }, "End": true } } },
    { "StartAt": "FraudCheck", "States": { "FraudCheck": { "Type": "Task", "Resource": "arn:aws:states:::lambda:invoke", "Parameters": { "FunctionName": "fraud", "Payload.$": "$" }, "End": true } } }
  ],
  "Next": "Merge"
}
```
- সব শাখা শেষ হলে output হয় **array** (প্রতিটা শাখার ফল)
- একটা শাখা fail করলে পুরো Parallel fail

### 5️⃣ Map: প্রতিটা item-এর জন্য একই কাজ (loop)
```json
"ProcessEachItem": {
  "Type": "Map",
  "ItemsPath": "$.items",
  "MaxConcurrency": 10,
  "ItemProcessor": {
    "ProcessorConfig": { "Mode": "INLINE" },
    "StartAt": "PriceItem",
    "States": {
      "PriceItem": { "Type": "Task", "Resource": "arn:aws:states:::lambda:invoke",
                     "Parameters": { "FunctionName": "price-item", "Payload.$": "$" }, "End": true }
    }
  },
  "Next": "Total"
}
```
- **Inline map**: execution-এর ভেতরে, ছোট list
- **Distributed map**: বিশাল dataset (S3-এর লাখো object/CSV row), সর্বোচ্চ ১০,০০০ parallel child execution (Day 33)

### 6️⃣ Pass: data সাজানো বা placeholder
```json
"SetDefaults": { "Type": "Pass", "Result": { "currency": "BDT" }, "ResultPath": "$.meta", "Next": "Charge" }
```

### 7️⃣ Succeed / 8️⃣ Fail
```json
"OrderRejected": { "Type": "Fail", "Error": "OrderRejected", "Cause": "Fraud check failed" }
```

---

## Part 4: State-এর মধ্যে Data Flow (JSONPath)

প্রতিটা state input নেয় আর output দেয়। চারটা filter দিয়ে নিয়ন্ত্রণ করা যায়:

```
State input
  → InputPath     (input-এর কোন অংশ নেবে)
  → Parameters    (task-কে কী পাঠাবে, নতুন JSON বানিয়ে)
  → [task চলে] → task result
  → ResultSelector (result-এর কোন অংশ রাখবে)
  → ResultPath    (result মূল input-এর কোথায় বসাবে)
  → OutputPath    (শেষে কোন অংশ পরের state-এ যাবে)
State output
```

| Filter | Default | সবচেয়ে common ব্যবহার |
|---|---|---|
| `InputPath` | `$` | কম ব্যবহার হয় |
| `Parameters` | — | `"Payload.$": "$"` দিয়ে Lambda-কে input দেওয়া |
| `ResultSelector` | — | Lambda response থেকে শুধু `Payload` নেওয়া |
| **`ResultPath`** | `$` (result পুরো input-কে **প্রতিস্থাপন** করে) | `"$.payment"` = মূল input রেখে result যোগ করা; `null` = result ফেলে দেওয়া |
| `OutputPath` | `$` | `"$.Payload"` |

### ResultPath-এর উদাহরণ
Input: `{"orderId": "101", "amount": 1500}`, Lambda result: `{"txnId": "T9"}`

| ResultPath | Output |
|---|---|
| (default `$`) | `{"txnId": "T9"}` ← orderId হারিয়ে গেল! |
| `"$.payment"` | `{"orderId": "101", "amount": 1500, "payment": {"txnId": "T9"}}` ✅ |
| `null` | `{"orderId": "101", "amount": 1500}` |

> ⚠️ State-এর মধ্যে data-র সীমা **২৫৬ KB**। বড় data S3-এ রেখে শুধু key পাঠান।

---

## Part 5: Standard বনাম Express Workflow

| | **Standard** | **Express** |
|---|---|---|
| সর্বোচ্চ সময় | **১ বছর** | **৫ মিনিট** |
| Execution semantics | **Exactly-once** (প্রতিটা ধাপ একবার) | **At-least-once** (async) / at-most-once (sync) |
| খরচ | প্রতি **state transition** | প্রতি execution + duration + memory (অনেক সস্তা, বেশি volume-এ) |
| Throughput | মাঝারি (প্রতি সেকেন্ডে হাজারের ঘরে execution শুরু) | বিশাল (প্রতি সেকেন্ডে লাখের ঘরে) |
| Execution history | Console-এ ৯০ দিন, visual | CloudWatch Logs-এ (চালু করতে হয়) |
| Callback (`.waitForTaskToken`), `.sync` job | ✅ | ❌ |
| কখন | Order processing, approval, ETL, long job, **payment** (exactly-once জরুরি) | IoT/stream processing, high-volume API backend, ছোট data transform |

**Express-এর দুই ধরন:**
- **Synchronous**: caller ফল পর্যন্ত অপেক্ষা করে (API Gateway → Express sync → response)
- **Asynchronous**: শুরু করে চলে যায়

> 💡 মিশ্রণও চলে: Standard workflow-এর ভেতরে high-volume অংশ Express child workflow হিসেবে।

---

## Part 6: Execution শুরু করা

| কীভাবে | উদাহরণ |
|---|---|
| SDK/CLI | `aws stepfunctions start-execution --state-machine-arn $SM --input '{"orderId":"101"}'` |
| **EventBridge rule** target | `OrderPlaced` event এলে workflow শুরু |
| API Gateway | REST/HTTP API integration (Express sync দিয়ে সরাসরি response) |
| Scheduler | নির্দিষ্ট সময়ে |
| অন্য state machine | Nested workflow (`states:startExecution.sync`) |

Execution name unique হতে হয় (Standard-এ ৯০ দিন), তাই `orderId` দিয়ে নাম দিলে একই order দুবার শুরু হওয়া ঠেকানো যায় (**idempotency**)।

### Permission
State machine-এর একটা **execution role** থাকে: এটাই Lambda invoke, DynamoDB write ইত্যাদির অনুমতি দেয় (least privilege, Day 26-এর মতো)।

---

## Part 7: Hands-on Lab — প্রথম Workflow

1. দুটো Lambda: `validate-order` (amount না থাকলে error ছোঁড়ে, না হলে input ফেরত দেয়) আর `charge-payment` (`{"txnId": "T-" + orderId}` ফেরত দেয়)
2. Step Functions → **Create state machine** → Standard → Workflow Studio-তে:
   - Validate (Lambda) → Choice (amount > 10000?) → হ্যাঁ: Pass "ManualReview" / না: Charge (Lambda, **ResultPath `$.payment`**) → DynamoDB PutItem (direct integration) → Succeed
3. Execution চালান:
```json
{"orderId": "101", "amount": 1500}
```
4. **Graph view**-এ প্রতিটা ধাপে click করে input/output দেখুন; ResultPath-এর প্রভাব খেয়াল করুন
5. `{"orderId": "102", "amount": 50000}` দিয়ে Choice-এর অন্য শাখা দেখুন
6. `{"orderId": "103"}` (amount নেই) দিয়ে fail দেখুন। কাল এটা Retry/Catch দিয়ে সামলাব

---

## 🎯 আজকের মূল Takeaways

1. Lambda থেকে Lambda call না, **orchestration-এর জন্য Step Functions**
2. ASL (JSON): `StartAt`, `States`, `Type`, `Next`/`End`; `.$` = JSONPath মান
3. State: **Task, Choice, Wait, Parallel, Map, Pass, Succeed, Fail**
4. **Direct SDK integration**: DynamoDB/SQS/SNS ইত্যাদি Lambda ছাড়াই
5. Data flow: InputPath → Parameters → ResultSelector → **ResultPath** → OutputPath; ২৫৬ KB সীমা
6. **Standard** (১ বছর, exactly-once, প্রতি transition) বনাম **Express** (৫ মিনিট, at-least-once, বিশাল volume, সস্তা)
7. Wait state-এ কোনো compute খরচ নেই

---

## 📝 Self-check Questions

1. Lambda থেকে সরাসরি আরেকটা Lambda synchronous-ভাবে call করার দুটো সমস্যা বলুন।
2. Payment workflow-এর জন্য Standard না Express? কেন?
3. প্রতি সেকেন্ডে ৫০,০০০ IoT event ছোট transform করে DynamoDB-তে লিখতে কোন workflow?
4. Lambda task-এর পর মূল input হারিয়ে যাচ্ছে। কী বদলাবেন?
5. তিনটা কাজ একসাথে চালিয়ে সবগুলো শেষ হলে এগোতে কোন state?
6. ২০০টা item-এর প্রতিটার দাম হিসাব করতে কোন state?
7. DynamoDB-তে শুধু একটা item লিখতে Lambda লাগবে?

<details><summary>▶ উত্তর দেখুন</summary>

1. Caller অপেক্ষা করে বসে থাকে (দুবার টাকা), error/retry/rollback আর visibility নিজে সামলাতে হয়, পুরো চেইন ১৫ মিনিটে আটকে থাকে।
2. Standard: exactly-once execution, লম্বা সময়, visual history আর audit।
3. Express (বিশাল volume, ছোট সময়, সস্তা)।
4. `ResultPath` দিন (যেমন `"$.payment"`), যাতে result মূল input-এর সাথে যোগ হয়।
5. Parallel।
6. Map (খুব বড় dataset হলে Distributed Map)।
7. না; `arn:aws:states:::dynamodb:putItem` direct integration।
</details>

---

## 💡 Pro Tips

- Workflow Studio দিয়ে শুরু করুন, তারপর ASL JSON SAM/CDK-তে রাখুন
- Lambda-কে ছোট আর একটা কাজের রাখুন; সিদ্ধান্ত (if/else) Choice state-এ
- Direct integration যত বেশি, তত কম Lambda আর কম খরচ
- State-এর নাম পরিষ্কার দিন (`ChargePayment`), graph view-তে পড়া সহজ হয়
- Standard-এ state transition গোনা হয়। বিশাল loop হলে Express child বা Distributed Map বিবেচনা করুন

---

## 🎨 Quick Reference

```
States: Task | Choice | Wait | Parallel | Map | Pass | Succeed | Fail
Lambda task: "Resource": "arn:aws:states:::lambda:invoke",
             "Parameters": {"FunctionName": "...", "Payload.$": "$"}, "OutputPath": "$.Payload"
Direct SDK: arn:aws:states:::dynamodb:putItem | sqs:sendMessage | sns:publish ...
ResultPath: "$" (replace) | "$.x" (add) | null (discard)
Payload between states: 256 KB
Standard: 1 year, exactly-once, per transition | Express: 5 min, at-least-once, per request+duration
```

```bash
aws stepfunctions start-execution --state-machine-arn $SM --name order-101 --input '{"orderId":"101"}'
aws stepfunctions describe-execution --execution-arn $EXEC
```

---

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** "Orchestrator" Lambda ১০টা Lambda-কে ক্রমানুসারে call করত। একটা ধীর হলে পুরোটা ১৫ মিনিটে timeout, আর কোন ধাপ পর্যন্ত হয়েছিল কেউ জানত না।
**শিক্ষা:** Orchestration-এ Step Functions, visual history সহ।

**পরিস্থিতি ২:** Payment Lambda-র পর ResultPath দেওয়া হয়নি, তাই পরের ধাপে orderId হারিয়ে গেল, আর order "PAID" update হলো না।
**শিক্ষা:** Default ResultPath পুরো input মুছে দেয়; `$.payment` ধাঁচে দিন।

**পরিস্থিতি ৩:** প্রতি সেকেন্ডে হাজারো ছোট event-এর জন্য Standard workflow ব্যবহার করা হলো। State transition-এর bill অপ্রত্যাশিতভাবে বড়।
**শিক্ষা:** High-volume, ছোট কাজে Express।

---

**⏮ আগের দিন:** [Day 31 — EventBridge](./Day-31-EventBridge-Buses-Rules-Cross-Account.md) | **⏭ পরের দিন:** [Day 33 — Step Functions Error Handling ও Orchestration](./Day-33-Step-Functions-Error-Handling-Orchestration.md)
