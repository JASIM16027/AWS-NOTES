# 🔐 AWS IAM — Technical Deep Dive

---

## 1. IAM কী — Core Concept

IAM = **Identity and Access Management**

সহজ কথায়: AWS এ **কে** (Who) **কী** (What) করতে পারবে সেটা control করার system।

```
Question IAM answer করে:
├── কে request করছে?     → Authentication
├── তার permission আছে?  → Authorization
└── কোন resource এ?      → Policy Evaluation
```

---

## 2. IAM এর 4টা Core Component

### 2.1 User

```
IAM User = একজন মানুষ বা application এর identity

Properties:
├── Username
├── Password (Console access)
├── Access Key ID + Secret (CLI/API access)
└── Attached Policies (permissions)

Example:
├── developer-john  → S3 read, EC2 start/stop
├── developer-jane  → only S3 read
└── ci-cd-bot       → ECR push, ECS deploy
```

### 2.2 Group

```
Group = Users এর collection

কেন দরকার?
├── 50 জন developer কে একে একে permission দেওয়া ঝামেলা
└── Group এ policy দাও → সব member পাবে

Example:
Group: "Backend-Developers"
├── Policy: EC2-ReadOnly
├── Policy: S3-FullAccess
└── Members: john, jane, rahim, karim
```

### 2.3 Role

```
Role = Service বা User এর temporary identity

User থেকে পার্থক্য:
├── User → specific person এর permanent identity
└── Role → যে কেউ assume করতে পারে (temporarily)

Use cases:
├── EC2 → S3 access করবে (EC2 Role)
├── Lambda → DynamoDB write করবে (Lambda Role)
└── GitHub Actions → AWS deploy করবে (CI/CD Role)
```

### 2.4 Policy

```
Policy = JSON document যা define করে permissions

Structure:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow" or "Deny",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::my-bucket/*"]
    }
  ]
}
```

---

## 3. Policy — Technical Deep Dive

### Policy এর Anatomy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3Read",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "ap-south-1"
        }
      }
    }
  ]
}
```

প্রতিটা field মানে:

```
Sid        → Statement ID (optional label)
Effect     → Allow বা Deny
Action     → কোন AWS operation
Resource   → কোন specific resource এ
Condition  → extra conditions (optional)
```

### ARN Format:

```
arn:aws:s3:::my-bucket
 │   │   │   │   └── Resource name
 │   │   │   └────── Account ID (blank = any)
 │   │   └────────── Service name
 │   └────────────── AWS partition
 └────────────────── "arn" prefix

More examples:
arn:aws:ec2:ap-south-1:123456789:instance/i-1234567890
arn:aws:iam::123456789:user/john
arn:aws:rds:ap-south-1:123456789:db:my-database
```

---

## 4. Policy Types — কোনটা কখন

```
┌─────────────────────────────────────────────┐
│           AWS Managed Policy                │
│  AWS নিজে বানায়, maintain করে             │
│  Example: AmazonS3FullAccess               │
│  Use: Quick setup এ                        │
├─────────────────────────────────────────────┤
│           Customer Managed Policy           │
│  তুমি নিজে বানাও                          │
│  Reusable across users/roles               │
│  Use: Production এ (precise control)       │
├─────────────────────────────────────────────┤
│           Inline Policy                     │
│  Specific user/role এ directly attach      │
│  Not reusable                              │
│  Use: One-off special cases এ             │
└─────────────────────────────────────────────┘
```

---

## 5. Policy Evaluation Logic

এটা সবচেয়ে important — AWS কীভাবে decide করে Allow বা Deny:

```
Request আসলে AWS এই order এ check করে:

Step 1: Explicit DENY আছে?
        ↓ YES → DENY (end)
        ↓ NO  → next

Step 2: Explicit ALLOW আছে?
        ↓ YES → ALLOW (end)
        ↓ NO  → next

Step 3: Default → DENY
```

Visual flow:

```
API Request
     ↓
Explicit Deny? ──YES──→ ❌ DENY
     ↓ NO
Explicit Allow? ──YES──→ ✅ ALLOW  
     ↓ NO
Default ──────────────→ ❌ DENY
```

**গুরুত্বপূর্ণ নিয়ম:**
> Explicit DENY সবসময় ALLOW কে override করে।

---

## 6. IAM Role — Technical Flow

### EC2 থেকে S3 access করার real flow:

```
Step 1: EC2 তে Role attach করো
        Role: "EC2-S3-Upload-Role"
        Policy: Allow s3:PutObject on my-bucket

Step 2: EC2 boot হলে automatically
        Instance Metadata Service (IMDS) থেকে
        temporary credentials নেয়

Step 3: তোমার NestJS app এ:
        AWS SDK automatically এই credentials use করে

Step 4: S3 API call যায়
        AWS verify করে → Allow → Success
```

### Temporary Credentials কেমন দেখতে:

```json
{
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "wJalr...",
  "SessionToken": "AQoDYXdzE...",
  "Expiration": "2024-01-01T12:00:00Z"
}
```

এগুলো automatically rotate হয় — তোমাকে কিছু করতে হয় না।

---

## 7. Real Project IAM Setup

### NestJS App এর জন্য proper IAM:

```
Production Setup:
├── IAM Role: "nestjs-app-role"
│   ├── Policy: S3 upload (specific bucket only)
│   ├── Policy: RDS connect
│   └── Policy: SES send email
│
├── IAM User: "ci-cd-deploy"
│   ├── Policy: ECR push image
│   └── Policy: ECS update service
│
└── IAM Group: "backend-team"
    ├── Policy: EC2 read/start/stop
    ├── Policy: S3 read (logs bucket)
    └── Policy: CloudWatch logs view
```

### S3 Upload Policy (Minimal):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-app-bucket"
    }
  ]
}
```

---

## 8. Security Best Practices — Technical

### ❌ যা কখনো করবে না:

```
# NEVER do this in code:
const s3 = new S3Client({
  accessKeyId: "AKIAIOSFODNN7EXAMPLE",      // hardcoded!
  secretAccessKey: "wJalrXUtnFEMI/K7MDENG" // danger!
});

# NEVER commit .env with AWS keys to GitHub
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

### ✅ যা করবে:

```javascript
// EC2 তে Role থাকলে SDK automatically নেয়
const s3 = new S3Client({ 
  region: "ap-south-1" 
  // No credentials needed! Role handles it
});

// Local dev এ:
// ~/.aws/credentials file use করো
// বা environment variable (short-lived)
```

### MFA Setup করো Root Account এ:

```
Root Account
├── ❌ Daily use করো না
├── ✅ MFA enable করো
├── ✅ Access key delete করো
└── ✅ শুধু billing/emergency তে use করো
```

---

## 9. IAM এর Golden Rules

```
Rule 1: Least Privilege
        → শুধু যতটুকু দরকার ততটুকুই দাও

Rule 2: Never use Root
        → Root = god mode, daily use বিপজ্জনক

Rule 3: Roles > Users for Services
        → EC2/Lambda তে কখনো Access Key দিও না

Rule 4: Rotate Credentials
        → Access Key পুরনো হলে rotate করো

Rule 5: Explicit Deny for Critical Resources
        → Production DB delete করা block করে রাখো

Rule 6: Enable CloudTrail
        → কে কী করলো সব log রাখো
```

---

## 10. Full Picture

```
┌─────────────────────────────────────┐
│              AWS Account            │
│                                     │
│  ┌─────────┐    ┌───────────────┐  │
│  │  Users  │    │    Groups     │  │
│  │  john   │───▶│ backend-team  │  │
│  │  jane   │    │               │  │
│  └─────────┘    └───────┬───────┘  │
│                         │          │
│  ┌─────────┐            │ Policy   │
│  │  Roles  │            ▼          │
│  │ ec2-role│    ┌───────────────┐  │
│  │ lambda  │───▶│   Policies    │  │
│  └────┬────┘    │ S3:PutObject  │  │
│       │         │ EC2:Describe  │  │
│       │ assume  └───────┬───────┘  │
│       ▼                 │ applied  │
│  ┌─────────┐            ▼          │
│  │   EC2   │    ┌───────────────┐  │
│  │ NestJS  │───▶│  AWS Resources│  │
│  └─────────┘    │  S3, RDS, etc │  │
│                 └───────────────┘  │
└─────────────────────────────────────┘
```

---

এখন বলো — **EC2 + VPC technical setup** দেখবো নাকি **S3 + IAM Role দিয়ে file upload** implement করবো? 🔥
