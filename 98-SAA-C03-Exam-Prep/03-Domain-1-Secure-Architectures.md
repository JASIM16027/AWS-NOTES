# 🔐 Domain 1: Design Secure Architectures (30%)

> প্রশ্ন ইংরেজিতে (exam-এর মতো), ব্যাখ্যা বাংলায়। প্রথমে নিজে উত্তর ভাবুন, তারপর **▶ উত্তর দেখুন**-এ click করুন।

**এই domain-এর topic:** IAM user/role/policy, SCP, cross-account access, KMS, S3 security, SG vs NACL, VPC endpoint, WAF/Shield, Secrets Manager, Cognito, GuardDuty/Macie/Inspector।

---

### Q1. EC2 needs S3 access
An application running on Amazon EC2 needs to read objects from an S3 bucket. The security team does not want long-term credentials stored on the instance. What should a solutions architect do?

- A. Create an IAM role with S3 read permissions and attach it to the EC2 instance through an instance profile.
- B. Create an IAM user, generate access keys, and store them in the application config file.
- C. Store access keys in AWS Secrets Manager and retrieve them at startup.
- D. Make the S3 bucket public and restrict access by the EC2 public IP.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

EC2-কে AWS access দেওয়ার সঠিক উপায় **IAM Role (instance profile)**। Role temporary credential দেয়, যা নিজে থেকেই rotate হয়।
- ❌ B: Access key হলো long-term credential, যেটা security team চায় না।
- ❌ C: এটাও long-term access key, শুধু রাখার জায়গা আলাদা।
- ❌ D: Bucket public করা সবচেয়ে বড় security ভুল।
</details>

---

### Q2. Restrict regions for all accounts
A company uses AWS Organizations with 50 accounts. The company must prevent any user, including account root users, from launching resources outside `eu-west-1`. What is the MOST effective solution?

- A. Attach an IAM policy that denies other Regions to every IAM user in each account.
- B. Use AWS Config rules to detect resources in other Regions.
- C. Apply a Service Control Policy (SCP) at the organization root that denies actions when `aws:RequestedRegion` is not `eu-west-1`.
- D. Enable CloudTrail in all Regions and alert on activity.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**SCP** সব member account-এর সবার উপর (**root user সহ**) সীমা বসায়, আর একবার লিখলেই সব account-এ কাজ করে।
- ❌ A: IAM policy root user-এর উপর কাজ করে না, আর ৫০টা account-এ আলাদা আলাদা manage করতে হবে।
- ❌ B, D: এগুলো শুধু **detect** করে, **prevent** করে না।
</details>

---

### Q3. Private S3 access without internet
EC2 instances in a private subnet must upload data to Amazon S3. The traffic must not traverse the internet, and the solution should be cost-effective. What should be used?

- A. NAT gateway
- B. AWS Direct Connect
- C. Internet gateway with a public IP on each instance
- D. S3 Gateway VPC endpoint

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**Gateway endpoint** (S3/DynamoDB-এর জন্য) **free**, আর traffic AWS network-এর ভেতরেই থাকে।
- ❌ A: NAT gateway দিয়ে traffic internet path-এ যায়, আর per-GB processing charge লাগে।
- ❌ B: Direct Connect on-prem-এর জন্য, আর অনেক দামি।
- ❌ C: Instance public হয়ে যায়, traffic internet দিয়ে যায়।
</details>

---

### Q4. Block a malicious IP
A web application behind an ALB is being attacked from a specific set of IP addresses. The team needs to block these IPs quickly. Which TWO options will work? **(Select TWO)**

- A. Add a deny rule in the instances' security group.
- B. Add deny rules for the IPs in the subnet's network ACL.
- C. Create an AWS WAF web ACL with an IP set rule and associate it with the ALB.
- D. Enable Amazon GuardDuty.
- E. Use AWS Shield Standard.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B, C**

- ✅ B: **NACL**-এ **Deny** rule দেওয়া যায় (ALB যে subnet-এ আছে সেখানে)।
- ✅ C: **WAF IP set** rule দিয়ে ALB-এর আগেই block করা যায়।
- ❌ A: **Security Group-এ Deny rule নেই**, শুধু Allow দেওয়া যায়।
- ❌ D: GuardDuty শুধু detect করে, block করে না।
- ❌ E: Shield Standard শুধু DDoS থেকে রক্ষা করে, নির্দিষ্ট IP block করে না।
</details>

---

### Q5. Encrypt S3 with audit trail of key usage
A company must encrypt all objects in S3 at rest. The security team must control the key, rotate it, and audit every use of the key. What should the solutions architect use?

- A. SSE-S3
- B. SSE-KMS with a customer managed key
- C. SSE-C
- D. Client-side encryption with a key stored in the application code

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**SSE-KMS + customer managed key**: key policy দিয়ে control, rotation, আর **CloudTrail-এ প্রতিবার key ব্যবহারের log** পাওয়া যায়।
- ❌ A: SSE-S3-এর key AWS manage করে, আপনার control বা আলাদা audit থাকে না।
- ❌ C: SSE-C-তে প্রতিটা request-এ key আপনাকেই পাঠাতে হয়, manage করা কঠিন।
- ❌ D: Code-এ key রাখা বড় security ঝুঁকি।
</details>

---

### Q6. Database credential rotation
An application uses an Amazon RDS for MySQL database. The company requires the database password to be rotated automatically every 30 days with minimal operational effort. What should be used?

- A. AWS Secrets Manager with automatic rotation enabled
- B. SSM Parameter Store SecureString with a cron job on EC2
- C. Store the password in an encrypted S3 object
- D. IAM database authentication with a static password

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**Secrets Manager**-এ RDS-এর জন্য **built-in automatic rotation** আছে।
- ❌ B: Parameter Store-এ native rotation নেই, নিজে script বানাতে হবে (বেশি ঝামেলা)।
- ❌ C: S3-এ রাখলে rotation হয় না।
- ❌ D: IAM DB authentication token ভিত্তিক, "static password" কথাটাই এখানে ভুল।
</details>

---

### Q7. S3 bucket only through CloudFront
Static website files are stored in an S3 bucket and served through Amazon CloudFront. Users must not be able to access the S3 bucket directly. What should be done?

- A. Make the bucket public and use signed URLs.
- B. Enable S3 Transfer Acceleration.
- C. Configure CloudFront Origin Access Control (OAC) and update the bucket policy to allow only the CloudFront distribution.
- D. Put the bucket in a private subnet.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**OAC** ব্যবহার করলে bucket private থাকে, আর bucket policy-তে শুধু CloudFront distribution-কে allow করা হয়।
- ❌ A: Bucket public করলে user সরাসরি S3-এ ঢুকে যাবে।
- ❌ B: Transfer Acceleration শুধু upload-এর speed বাড়ায়, security-র সাথে সম্পর্ক নেই।
- ❌ D: S3 কোনো VPC subnet-এ থাকে না।
</details>

---

### Q8. Mobile app user sign-in
A mobile application needs user sign-up and sign-in with social identity providers (Google, Facebook), and authenticated users must upload photos directly to S3. What should be used?

- A. IAM users for each mobile user
- B. AWS Directory Service
- C. AWS IAM Identity Center
- D. Amazon Cognito user pool for authentication and identity pool for temporary AWS credentials

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**Cognito User Pool** sign-up, sign-in আর social login সামলায়। **Identity Pool** user-কে S3-এ upload করার জন্য **temporary AWS credential** দেয়।
- ❌ A: লাখো app user-এর জন্য IAM user বানানো যায় না (limit আছে, practice-ও ভুল)।
- ❌ B: Directory Service হলো Active Directory, mobile app login-এর জন্য নয়।
- ❌ C: Identity Center নিজের কর্মীদের (workforce) SSO-র জন্য, app-এর customer-দের জন্য নয়।
</details>

---

### Q9. Cross-account access for an auditor
A third-party auditing company needs read-only access to resources in your AWS account. You want to avoid sharing long-term credentials and prevent the "confused deputy" problem. What should you do?

- A. Create an IAM user with ReadOnlyAccess and share the access keys.
- B. Create an IAM role with ReadOnlyAccess that trusts the auditor's AWS account and requires an external ID.
- C. Share the root user credentials with MFA.
- D. Create a resource-based policy on every resource.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

**Cross-account role + External ID** হলো 3rd-party access দেওয়ার standard উপায়। Temporary credential দেয়, আর external ID confused deputy সমস্যা ঠেকায়।
- ❌ A: Access key long-term credential।
- ❌ C: Root credential কখনো কাউকে দেবেন না।
- ❌ D: সব service resource-based policy support করে না, আর manage করাও কঠিন।
</details>

---

### Q10. Detect sensitive data in S3
A company stores millions of documents in S3 and must identify which objects contain personally identifiable information (PII) such as credit card numbers. What service should be used?

- A. Amazon Macie
- B. Amazon GuardDuty
- C. Amazon Inspector
- D. AWS Config

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

**Macie** ML দিয়ে S3-এর ভেতরে **PII/sensitive data** খুঁজে বের করে।
- ❌ B: GuardDuty threat detection করে (যেমন malicious activity)।
- ❌ C: Inspector software vulnerability (CVE) খোঁজে।
- ❌ D: Config resource-এর configuration compliance দেখে, file-এর ভেতরের data না।
</details>

---

### Q11. Protect against SQL injection
A public web application on an ALB is receiving SQL injection and cross-site scripting attempts. What is the MOST operationally efficient way to protect it?

- A. Write input validation code in every microservice.
- B. Use security groups to block port 80.
- C. Deploy AWS WAF on the ALB with AWS Managed Rules (core rule set and SQL database rule set).
- D. Enable VPC Flow Logs.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**WAF + Managed Rules** দিয়ে SQLi আর XSS ready-made rule পাওয়া যায়, নিজে কিছু লিখতে হয় না।
- ❌ A: প্রতিটা service-এ code লেখা অনেক বেশি পরিশ্রম (operational overhead)।
- ❌ B: Port বন্ধ করলে website-টাই বন্ধ হয়ে যাবে।
- ❌ D: Flow Logs শুধু traffic log করে, কিছু block করে না।
</details>

---

### Q12. Encrypt an existing unencrypted EBS volume
A company has an unencrypted EBS volume attached to a production EC2 instance. The volume must be encrypted. What should the solutions architect do?

- A. Enable encryption directly on the existing volume.
- B. Enable encryption on the EC2 instance.
- C. Use SSE-S3 on the volume.
- D. Create a snapshot, copy the snapshot with encryption enabled, create a new volume from the encrypted snapshot, and replace the volume.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

চালু থাকা unencrypted volume-কে **সরাসরি encrypt করা যায় না**। উপায় হলো: snapshot নেওয়া → encryption চালু করে snapshot copy → সেই copy থেকে নতুন volume বানানো → পুরনোটার জায়গায় বসানো।
- ❌ A, B: এমন কোনো option নেই।
- ❌ C: SSE-S3 শুধু S3-এর জন্য।
- 💡 ভবিষ্যতের জন্য account-এ **"EBS encryption by default"** চালু করে রাখুন।
</details>

---

### Q13. Least-privilege for a Lambda
A Lambda function writes items to a single DynamoDB table named `Orders`. What IAM configuration follows the principle of least privilege?

- A. Attach `AmazonDynamoDBFullAccess` to the Lambda execution role.
- B. Allow `dynamodb:PutItem` on the `Orders` table ARN in the Lambda execution role.
- C. Allow `dynamodb:*` on `*`.
- D. Use the root user access keys in the function.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: B**

Least privilege মানে **নির্দিষ্ট action (PutItem) + নির্দিষ্ট resource ARN**।
- ❌ A, C: দরকারের চেয়ে অনেক বেশি permission।
- ❌ D: Root key কখনো ব্যবহার করা উচিত না।
</details>

---

### Q14. Enforce HTTPS for S3
A compliance requirement states that all access to an S3 bucket must use encryption in transit. What should be done?

- A. Add a bucket policy that denies requests where `aws:SecureTransport` is `false`.
- B. Enable default encryption with SSE-S3.
- C. Enable S3 Versioning.
- D. Enable Object Lock.

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: A**

"In transit" মানে HTTPS। **`aws:SecureTransport=false` হলে Deny** করলে HTTP request আর ঢুকতে পারবে না।
- ❌ B: এটা **at rest** encryption, in transit না।
- ❌ C, D: এগুলো data protection feature, encryption-এর সাথে সম্পর্ক নেই।
</details>

---

### Q15. Private subnet administration without SSH
Administrators need shell access to EC2 instances in private subnets. The security team does not allow inbound port 22 or bastion hosts, and all sessions must be logged. What should be used?

- A. EC2 Instance Connect with a public IP
- B. A NAT gateway
- C. AWS Systems Manager Session Manager
- D. Site-to-Site VPN

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: C**

**Session Manager**-এ কোনো inbound port, SSH key বা bastion লাগে না। Access IAM দিয়ে control হয়, আর প্রতিটা session S3/CloudWatch-এ log হয়।
- ❌ A: Public IP আর port 22 খোলা লাগে।
- ❌ B: NAT শুধু outbound internet দেয়, shell access না।
- ❌ D: VPN দিয়ে ঢুকলেও port 22 খোলা রাখতে হবে।
</details>

---

### Q16. Centralized threat detection
A company wants to continuously monitor all AWS accounts for malicious activity such as compromised EC2 instances communicating with known command-and-control servers, with minimal setup. What should be used?

- A. Amazon Inspector
- B. VPC Flow Logs with a custom Lambda analyzer
- C. AWS Trusted Advisor
- D. Amazon GuardDuty with a delegated administrator in AWS Organizations

<details><summary>▶ উত্তর দেখুন</summary>

**✅ উত্তর: D**

**GuardDuty** CloudTrail, VPC Flow Logs আর DNS log বিশ্লেষণ করে threat (C2 communication, crypto-mining) ধরে। Organization-এ delegated admin থাকলে সব account একসাথে দেখা যায়।
- ❌ A: Inspector শুধু vulnerability খোঁজে।
- ❌ B: নিজে analyzer বানানো অনেক বেশি পরিশ্রম।
- ❌ C: Trusted Advisor শুধু best practice check করে।
</details>

---

## 📌 Domain 1 Quick Revision

- **Security Group** = stateful, শুধু Allow → **NACL** = stateless, Allow + Deny
- EC2/Lambda-কে access দিতে সবসময় **Role**, কখনো **access key না**
- Organization-wide guardrail → **SCP** (root-কেও আটকায়, management account-কে না)
- Private way-তে S3/DynamoDB → **Gateway Endpoint** (free); অন্য service → **Interface Endpoint**
- Key-এর control + audit → **KMS customer managed key**; single-tenant HSM → **CloudHSM**
- Password rotation → **Secrets Manager**
- Layer 7 attack → **WAF**; DDoS → **Shield**
- PII → **Macie**; Threat → **GuardDuty**; CVE → **Inspector**; Config compliance → **Config**; API audit → **CloudTrail**
