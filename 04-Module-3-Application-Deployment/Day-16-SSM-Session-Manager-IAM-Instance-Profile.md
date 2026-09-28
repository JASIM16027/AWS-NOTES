

# 📚 Day 16 — SSM Session Manager & IAM Instance Profile

**সময়:** ১.৫ ঘণ্টা | **Module:** ৩ (Application Deployment on EC2) — Day 2

## 🎯 আজকের লক্ষ্য
- IAM basics (User vs Role) refresh
- IAM Instance Profile কীভাবে কাজ করে
- AWS SDK credential chain
- SSM Session Manager গভীরে
- Session logging ও audit
- Port forwarding via SSM
- Run Command, Patch Manager preview

---

## Part 1: IAM Refresher

আগে IAM-এর basics দেখি, তারপর Instance Profile।

### 🔑 IAM = Identity and Access Management

**৩টা core concepts:**

#### 1. User
- কোনো ব্যক্তি বা application
- Long-term credentials
- Access keys, password
- যেমন: developer, admin

#### 2. Group
- Multiple users-এর collection
- Policy attach group-এ
- যেমন: "Developers", "Admins"

#### 3. Role
- **Temporary credentials**
- Assume করতে হয়
- AWS service বা cross-account use করে
- কোনো permanent credentials নেই

### 🆚 User vs Role

| Aspect | User | Role |
|---|---|---|
| **Credentials** | Long-term (access keys) | Temporary (auto-rotated) |
| **Who uses** | Person/Application | AWS service or assumed by user |
| **Password** | Yes | No |
| **MFA** | Possible | Possible |
| **Best for** | Human access | Service access |

### 🎭 Why Roles Matter for EC2

**Problem:** EC2 instance-এ application AWS service call করতে চায় (S3 upload, DynamoDB read)।

**Bad approach:** Hardcode access keys
```python
import boto3
s3 = boto3.client('s3',
    aws_access_key_id='AKIA...',  # BAD!
    aws_secret_access_key='...'
)
```

**Problems:**
- Keys in code/config = security risk
- Keys leak to Git/logs
- Manual rotation needed
- If compromised, manual revoke

**Good approach:** IAM Role
```python
import boto3
s3 = boto3.client('s3')  # No credentials!
# Boto3 automatically gets temp credentials from instance metadata
```

---

## Part 2: IAM Instance Profile

### 🎯 Instance Profile কী?

**Instance Profile = একটা container যা একটা IAM Role-কে EC2 instance-এর সাথে attach করে।**

### 🤔 কেন এই Extra Layer?

Historical reason: IAM Roles প্রথমে human/cross-account use-এর জন্য ছিল। EC2-তে attach করার জন্য আলাদা wrapper concept তৈরি হয়েছিল।

**Practical reality:**
- IAM Console-এ Role create করলে Instance Profile automatic তৈরি হয়
- দুটোর same name থাকে
- আপনি Role attach করেন, AWS Instance Profile use করে behind the scenes

### 🏗️ Architecture

```
EC2 Instance
     │
     │ "I need to access S3"
     ▼
Instance Profile (attached)
     │
     │ Wraps the Role
     ▼
IAM Role
     │
     │ Has policies attached
     ▼
IAM Policies
     │
     ▼
Permissions: S3:GetObject, S3:PutObject, etc.
```

### 🔄 How Credentials Flow

```
1. Application makes AWS API call
       │
       ▼
2. AWS SDK looks for credentials
       │
       ▼
3. Checks credential chain (next section)
       │
       ▼
4. Finds Instance Metadata Service (IMDS)
       │
       ▼
5. Requests temp credentials from IMDS
       │
       ▼
6. IMDS returns:
   - Access Key (temporary)
   - Secret Key (temporary)
   - Session Token
   - Expiration time
       │
       ▼
7. SDK uses these for API call
       │
       ▼
8. Credentials auto-refresh before expiry
```

### 🛠️ Setup Instance Profile

#### Step 1: Create IAM Role

```
IAM Console → Roles → Create Role
- Trusted entity: AWS service
- Service: EC2
- Permissions: attach policies (e.g., AmazonS3ReadOnlyAccess)
- Name: my-app-role
```

**Behind the scenes:** AWS auto-creates Instance Profile with same name।

#### Step 2: Attach to EC2

**At launch:**
```
EC2 Launch Wizard → Advanced details → IAM instance profile → Select my-app-role
```

**Existing instance:**
```
EC2 Console → Select instance → Actions → Security → Modify IAM role → Select role
```

#### Step 3: Test from Instance

```bash
# Get current role
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Get credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/my-app-role
```

Response:
```json
{
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "...",
  "Token": "...",
  "Expiration": "2026-04-25T18:00:00Z"
}
```

These are **temporary credentials**, auto-rotated every few hours।

#### Step 4: Application Uses Credentials

**Python (boto3):**
```python
import boto3

# No credentials specified - SDK finds them automatically
s3 = boto3.client('s3')
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')
```

**AWS CLI:**
```bash
aws s3 ls
# Works without `aws configure`
```

---

## Part 3: AWS SDK Credential Chain

### 🔗 কীভাবে SDK Credentials খুঁজে?

**Order of precedence (top to bottom):**

#### 1. Explicit credentials in code
```python
boto3.client('s3', aws_access_key_id='...', aws_secret_access_key='...')
```

#### 2. Environment variables
```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

#### 3. AWS credentials file
```
~/.aws/credentials
[default]
aws_access_key_id = ...
aws_secret_access_key = ...
```

#### 4. Container credentials (ECS task role)
```
ECS_CONTAINER_METADATA_URI
```

#### 5. **Instance Profile (IMDS)** ← EC2 default
```
http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

### 🎯 Best Practice: Use Instance Profile (Option 5)

- No credentials in code
- No credentials on disk
- Auto-rotation
- Per-instance audit
- Easy to revoke (detach role)

**একটা EC2 application-এর AWS access সাধারণত Instance Profile দিয়েই হয়।**

---

## Part 4: Common Instance Profile Policies

### 📋 AWS Managed Policies (Common Use)

#### 1. AmazonSSMManagedInstanceCore
**Purpose:** Session Manager + Patch Manager + Run Command

**Use:** Almost every production EC2 (for management)

#### 2. AmazonS3ReadOnlyAccess
**Purpose:** Read S3 buckets

**Use:** App needs to download configs/assets

#### 3. CloudWatchAgentServerPolicy
**Purpose:** Send metrics/logs to CloudWatch

**Use:** Monitoring agent

#### 4. AmazonEC2ContainerRegistryReadOnly
**Purpose:** Pull Docker images from ECR

**Use:** Container workloads

### 📝 Custom Policy Example: App-Specific S3

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-data/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-data"
      ]
    }
  ]
}
```

**Effect:** Only this specific bucket, only specific actions। Least privilege।

### 🛡️ Least Privilege Principle

**Rule:** Only the **minimum permissions needed** to function।

**Bad:**
```
Policy: AdministratorAccess (full AWS access!)
```

**Good:**
```
Policy: Custom policy with only S3 read on specific bucket
```

**Benefits:**
- Compromised instance = limited damage
- Audit-friendly
- Easier to reason about

---

## Part 5: SSM Session Manager — Deep Dive

Day 11-এ basic শিখেছেন। আজ গভীরে।

### 🔧 SSM Architecture

```
You (IAM User)
     │
     │ AWS Console / CLI
     ▼
AWS Systems Manager Service
     │
     │ (over secure HTTPS)
     ▼
SSM Agent on EC2
     │
     │ (initiated FROM instance, outbound)
     ▼
Session Established
     │
     ▼
Interactive Shell
```

### 🎬 Connection Flow

#### Step 1: User Initiates
```bash
aws ssm start-session --target i-1234567890
```

#### Step 2: AWS Authentication
- Your IAM user/role checked
- Permission `ssm:StartSession` required
- Target instance permission also checked

#### Step 3: SSM Agent Polls
- SSM Agent on instance constantly polls AWS
- Discovers pending session
- Establishes WebSocket connection

#### Step 4: Tunnel Created
- Encrypted tunnel between you and instance
- Through SSM service (not direct)
- No port 22, no public IP needed

#### Step 5: Session Live
- Interactive shell
- Commands logged (if configured)
- Idle timeout applies

### 🔑 SSM Agent Requirements

**On Instance:**

#### 1. SSM Agent Installed
- Pre-installed in:
  - Amazon Linux 2/2023
  - Ubuntu 16.04+
  - Windows 2008+
  - RHEL/CentOS (newer versions)
- Manual install for older AMIs

#### 2. Outbound HTTPS to SSM Endpoints
Required endpoints:
```
ssm.region.amazonaws.com
ssmmessages.region.amazonaws.com
ec2messages.region.amazonaws.com
```

**Options:**
- Public internet (via IGW + public IP, or NAT Gateway)
- VPC Endpoints (recommended — no internet needed)

#### 3. IAM Instance Profile
- Policy: `AmazonSSMManagedInstanceCore`
- Allows SSM Agent to communicate with AWS

### 🔐 IAM for User (Initiator)

**Required permissions:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:StartSession",
        "ssm:DescribeInstanceProperties",
        "ssm:DescribeInstanceInformation"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:TerminateSession",
        "ssm:ResumeSession"
      ],
      "Resource": "arn:aws:ssm:*:*:session/${aws:username}-*"
    }
  ]
}
```

---

## Part 6: Session Manager Logging & Audit

### 📊 Why Logging Critical

**Compliance requirements:**
- SOC2, HIPAA, PCI-DSS
- All admin activities logged
- Immutable audit trail
- Who did what, when

**Security investigation:**
- Breach analysis
- User accountability
- Anomaly detection

### 🎯 Logging Setup

#### Option 1: CloudWatch Logs
```
SSM Console → Session Manager → Preferences → Edit
- Enable CloudWatch logging
- Log group: /aws/ssm/sessions
- KMS encryption: optional
```

#### Option 2: S3 Bucket
```
- Enable S3 logging
- Bucket: ssm-session-logs
- Bucket prefix: production/
- Encryption: SSE-S3 or KMS
```

#### Option 3: Both
- Real-time monitoring (CloudWatch)
- Long-term archive (S3)
- Common production setup

### 📋 What's Logged

```json
{
  "session_id": "user-abc123",
  "user": "alice@company.com",
  "instance_id": "i-xyz",
  "start_time": "2026-04-25T10:00:00Z",
  "end_time": "2026-04-25T10:30:00Z",
  "commands": [
    "ls /opt",
    "cat /etc/nginx/nginx.conf",
    "systemctl restart nginx"
  ]
}
```

**প্রতিটা command, output, timestamp।**

### 🔍 Logging Best Practices

#### 1. Always Enable in Production
- Never run without audit trail
- Compliance + security

#### 2. Centralized Storage
- Single account for logs
- Cross-account log shipping

#### 3. Log Retention
- Compliance-driven
- Typically 1-7 years

#### 4. Encryption
- KMS-managed keys
- At rest + in transit

#### 5. Access Control
- Logs read-only for most
- Tampering prevention

#### 6. Monitoring/Alerts
- Unusual session patterns
- Off-hours access
- Privileged commands

---

## Part 7: SSM Run Command

### 🎬 Run Command কী?

**Without SSH, run commands on multiple instances simultaneously।**

### Use Cases:
- Patch all servers at once
- Check status across fleet
- Configuration update
- Emergency response

### Example:

```bash
# Run command on multiple instances
aws ssm send-command \
  --document-name "AWS-RunShellScript" \
  --targets "Key=tag:Environment,Values=production" \
  --parameters 'commands=["systemctl status nginx"]' \
  --output text
```

**Effect:** Every production-tagged instance runs `systemctl status nginx`। Output collected centrally।

### 🎯 SSM Documents

**Document = pre-defined script template।**

#### AWS-managed documents:
- `AWS-RunShellScript` — generic shell
- `AWS-RunPowerShellScript` — Windows
- `AWS-UpdateSSMAgent` — update agent
- `AWS-ConfigureAWSPackage` — install software

#### Custom documents:
You create reusable templates:

```yaml
schemaVersion: "2.2"
description: "Restart application service"
parameters:
  serviceName:
    type: String
    default: myapp
mainSteps:
  - action: aws:runShellScript
    name: restartService
    inputs:
      runCommand:
        - "systemctl restart {{ serviceName }}"
        - "systemctl status {{ serviceName }}"
```

### Use Run Command:
```bash
aws ssm send-command \
  --document-name "RestartApp" \
  --targets "Key=tag:App,Values=myapp" \
  --parameters "serviceName=myapp"
```

---

## Part 8: SSM Port Forwarding

### 🌐 Port Forwarding via SSM

Need to access private database from your laptop?

**Without SSM:** Bastion host, SSH tunnel।

**With SSM:** Port forward through Session Manager।

### Example: Database Access

```bash
# Forward local 3306 to private database through SSM
aws ssm start-session \
  --target i-bastion-instance \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters host="db.cluster.amazonaws.com",portNumber="3306",localPortNumber="3306"
```

**Effect:**
- Local port 3306 → SSM tunnel → bastion → DB
- `mysql -h localhost -P 3306` works locally
- No bastion SSH, no public DB

### 🎯 Use Cases

**1. Database access for development**
**2. RDP to Windows servers**
**3. Web admin panels (port 8080)**
**4. Internal APIs**
**5. Secure remote debugging**

### 🆚 vs SSH Tunneling

| Feature | SSH Tunnel | SSM Port Forwarding |
|---|---|---|
| SSH key needed | Yes | No |
| Public IP needed | Yes | No |
| Bastion needed | Yes | Optional |
| Audit logging | Limited | Full |
| Setup complexity | Medium | Low |

---

## Part 9: SSM Patch Manager (Preview)

### 🛠️ Patch Manager কী?

**Automated patching for EC2 instances।**

Module 8-এ details আসবে। আজ overview:

### Features:
- Automated security patches
- Scheduled maintenance windows
- Patch baselines (which patches to apply)
- Multi-instance, multi-OS
- Compliance reporting

### Workflow:
```
1. Define patch baseline (e.g., critical security patches)
2. Tag instances for patch group
3. Schedule maintenance window
4. SSM auto-patches during window
5. Compliance report generated
```

**Benefit:** No manual patching, consistent fleet, compliance-ready।

---

## Part 10: SSM Parameter Store

### 📦 Parameter Store কী?

**Centralized configuration management।**

Application config, secrets, parameters store করুন।

### Use Cases:

#### 1. Database Endpoints
```
/myapp/prod/db/host = db.example.com
/myapp/prod/db/port = 3306
```

#### 2. Application Settings
```
/myapp/prod/feature/dark-mode = enabled
/myapp/prod/api/timeout = 30
```

#### 3. Secrets (basic)
```
/myapp/prod/api-key = SecureString  (encrypted)
```

### Parameter Types:
- **String** — plain text
- **StringList** — comma-separated
- **SecureString** — encrypted (KMS)

### Example:

#### Store:
```bash
aws ssm put-parameter \
  --name /myapp/prod/db/host \
  --value db.internal.com \
  --type String

aws ssm put-parameter \
  --name /myapp/prod/api-key \
  --value "secret123" \
  --type SecureString \
  --key-id alias/aws/ssm
```

#### Retrieve from EC2:
```bash
aws ssm get-parameter \
  --name /myapp/prod/db/host \
  --query Parameter.Value \
  --output text
```

#### In Application (Python):
```python
import boto3

ssm = boto3.client('ssm')
db_host = ssm.get_parameter(Name='/myapp/prod/db/host')['Parameter']['Value']

# For secrets (decrypt automatically)
api_key = ssm.get_parameter(
    Name='/myapp/prod/api-key',
    WithDecryption=True
)['Parameter']['Value']
```

### 🎯 vs Secrets Manager

| Feature | Parameter Store | Secrets Manager |
|---|---|---|
| **Cost** | Free (Standard) | $0.40/secret/month |
| **Auto rotation** | No | Yes |
| **Versioning** | Yes | Yes |
| **Cross-account** | Limited | Yes |
| **API rate limits** | Lower | Higher |
| **Use case** | Config, low-sensitivity | Critical secrets, RDS rotation |

**Rule of thumb:**
- Configuration → Parameter Store
- Database passwords → Secrets Manager (auto-rotation)
- API keys → Either (depends on rotation needs)

---

## Part 11: Real-world Production Setup

### 🏗️ Complete EC2 Application Architecture

```
EC2 Instance
├── IAM Instance Profile: app-instance-profile
│   └── Role: app-role
│       └── Policies:
│           ├── AmazonSSMManagedInstanceCore (SSM access)
│           ├── CloudWatchAgentServerPolicy (monitoring)
│           └── Custom: app-s3-access
├── SSM Agent (running)
├── CloudWatch Agent (running)
├── Application
│   ├── Reads config from Parameter Store
│   ├── Reads secrets from Secrets Manager
│   ├── Uses temp credentials from IMDS
│   ├── Logs to CloudWatch Logs
│   └── Backs up to S3
└── No SSH (Session Manager only)
```

### 🎯 Setup Checklist

```
☐ IAM Role created (app-role)
☐ Instance Profile attached (app-instance-profile)
☐ Policies attached:
  ☐ AmazonSSMManagedInstanceCore
  ☐ CloudWatchAgentServerPolicy
  ☐ Custom least-privilege policies
☐ SSM Agent running
☐ Outbound HTTPS to SSM endpoints (or VPC endpoints)
☐ CloudWatch Logs group exists
☐ Parameter Store hierarchy set up
☐ Secrets Manager secrets created
☐ Session Manager logging enabled
☐ Patch Manager configured
☐ No SSH keys deployed (Session Manager only)
☐ MFA on IAM users for SSM access
```

### 🔐 Security Hardening

```
✓ IMDSv2 enforced
✓ Public IP avoided where possible
✓ SSM via VPC Endpoints
✓ Session logging to S3 + CloudWatch
✓ KMS encryption for sensitive data
✓ Least privilege IAM policies
✓ MFA enforced for users
✓ Regular audit of attached policies
✓ Tag-based access control where possible
```

---

## Part 12: Troubleshooting

### 🔧 Issue 1: SSM Session Won't Start

**Diagnostic:**
```bash
# From your local
aws ssm describe-instance-information

# Check if instance shows up
```

**If instance not listed:**

1. **SSM Agent not running:**
```bash
# Connect to instance via console (if possible)
sudo systemctl status amazon-ssm-agent
sudo systemctl restart amazon-ssm-agent
```

2. **No IAM Instance Profile:**
```bash
# Check from instance
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
# Should return role name, not empty
```

3. **No outbound HTTPS:**
```bash
# Test from instance
curl -v https://ssm.ap-south-1.amazonaws.com
```

4. **Missing endpoints (private subnet):**
- Need: ssm, ssmmessages, ec2messages endpoints
- Or NAT Gateway for outbound

### 🔧 Issue 2: Permission Denied

**Symptom:** `User is not authorized to perform: ssm:StartSession`

**Fix:** Add IAM permission to user/role:
```json
{
  "Effect": "Allow",
  "Action": "ssm:StartSession",
  "Resource": "arn:aws:ec2:*:*:instance/*"
}
```

### 🔧 Issue 3: Session Logging Not Working

**Check:**
- IAM role has CloudWatch Logs permissions?
- S3 bucket policy allows SSM service?
- KMS key permissions configured?

**Permissions for S3 logging:**
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:PutObject",
    "s3:GetEncryptionConfiguration"
  ],
  "Resource": "arn:aws:s3:::ssm-session-logs/*"
}
```

### 🔧 Issue 4: Application Can't Access AWS

**Symptom:** `boto3.exceptions.NoCredentialsError`

**Diagnostic:**
```bash
# From instance
aws sts get-caller-identity
# Should return role ARN
```

**If fails:**
- Instance Profile attached?
- Role has trust policy for EC2?
- Policy attached to role?

---

## 🎯 আজকের মূল Takeaways

1. **IAM Instance Profile** = wraps Role for EC2 attachment
2. **Auto credential rotation** via IMDS (every few hours)
3. **AWS SDK** auto-detects credentials from instance metadata
4. **SSM Agent** + IAM permissions = Session Manager works
5. **Required policy:** `AmazonSSMManagedInstanceCore`
6. **Session logging** to CloudWatch + S3 for audit
7. **Run Command** = batch operations on multiple instances
8. **Port Forwarding** via SSM = secure database access
9. **Parameter Store** = config + low-sensitivity secrets
10. **Secrets Manager** = critical secrets with rotation

---

## 📝 Self-check Questions

১. IAM User vs Role — মূল পার্থক্য কী?
২. Instance Profile কেন দরকার Role-এর সাথে?
৩. Credentials কোথা থেকে আসে EC2-এ application-এ?
৪. AWS SDK credential chain-এর order কী?
৫. SSM Agent running না থাকলে Session Manager কাজ করে?
৬. SSM-এর জন্য কোন IAM policy দরকার instance-এ?
৭. SSM private subnet-এ কাজ করতে কী লাগে?
৮. Session Manager log কোথায় store হতে পারে?
৯. Run Command-এ targets কীভাবে select?
১০. Port Forwarding-এ local + remote port specify হয় কীভাবে?
১১. Parameter Store vs Secrets Manager — কোনটা কখন?
১২. Least privilege principle কী?
১৩. SecureString parameter কীভাবে decrypt হয়?
১৪. Access keys hardcode না করার benefit কী?
১৫. SSM via VPC Endpoint vs NAT — কোনটা better?

---

## 💡 Pro Tips

- **Always use Instance Profile**, never hardcode credentials
- **`AmazonSSMManagedInstanceCore`** = baseline policy for all production EC2
- **Session Manager > SSH** for production
- **Enable session logging** organization-wide
- **Use Parameter Store hierarchy** (`/app/env/component/key`)
- **Tag-based access control** powerful (e.g., team can access only their tagged instances)
- **VPC Endpoints for SSM** = no internet needed
- **MFA for IAM users** mandatory production
- **Rotate access keys** if you must use them
- **Audit unused IAM policies** quarterly

---

## 🎨 Quick Reference

### Credential Flow:
```
EC2 Instance → IMDS → Temp Credentials → AWS API
        ↑
  Instance Profile
        ↑
   IAM Role
        ↑
  Policies (permissions)
```

### Session Manager Flow:
```
You → AWS SSM → SSM Agent on EC2 → Shell
       (HTTPS,         (outbound,
        IAM-auth)       no inbound port)
```

### Parameter Store Path:
```
/myapp/prod/db/host
/myapp/prod/db/password (SecureString)
/myapp/staging/api/key
/shared/cache/endpoint
```

---

## 🚨 Real-world Stories

**Story 1:** Company hardcoded AWS keys in code, code went public on GitHub. Bot scanned, found keys in 3 minutes. Mining cryptocurrency 10 minutes later. $30,000 bill in hours।

**Moral:** Instance Profile, never hardcode।

**Story 2:** Developer used SSH bastion, leaked SSH key. Migrated to Session Manager + IAM. Realized eliminating SSH = eliminating entire class of attacks।

**Moral:** Modern auth > legacy SSH।

**Story 3:** Production EC2 had `AdministratorAccess` policy "for convenience"। Compromised via app vulnerability, attacker accessed everything। Should have been least-privilege scoped role।

**Moral:** Least privilege saves blast radius।

**Story 4:** Session Manager logged all admin activity to S3. Compliance audit passed easily. Without logging, would have failed audit, lost contract।

**Moral:** Audit logs = compliance + accountability।

---

---

**⏭ পরের দিন:** [Day 17 — CloudWatch Agent](./Day-17-CloudWatch-Agent-Setup.md)
