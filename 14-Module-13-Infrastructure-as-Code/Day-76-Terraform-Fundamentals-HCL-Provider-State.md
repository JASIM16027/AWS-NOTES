# 📚 Day 76 — Terraform Fundamentals: HCL, Provider ও State

> 📊 **Visual Summary** — সহজে বোঝার জন্য diagram:

![Terraform Plan, Apply and State](../images/79-terraform-plan-apply-state.png)

**সময়:** ২ ঘণ্টা | **Module:** ১৩ (Infrastructure as Code) — Day 3

## 🎯 আজকের লক্ষ্য
- Terraform কী, কেন এটা **cloud-agnostic** (CloudFormation-এর থেকে ভিন্ন)
- **HCL** (HashiCorp Configuration Language)-এর মূল syntax: resource, provider, variable, output
- **Terraform State**: কেন এটা এত গুরুত্বপূর্ণ, কী সমস্যা সমাধান করে
- Workflow: `init` → `plan` → `apply` → `destroy`
- **Remote State**: S3 + DynamoDB লক দিয়ে টিম collaboration

---

## Part 1: Terraform কী, কেন Cloud-Agnostic?

**Terraform** (HashiCorp-এর তৈরি) একটা **open-source, cloud-agnostic IaC টুল** — AWS, GCP, Azure, এমনকি Kubernetes, GitHub, Datadog-ও manage করতে পারে একই syntax (HCL) দিয়ে।

```
CloudFormation: শুধু AWS
Terraform: AWS + GCP + Azure + অন্যান্য SaaS/Cloud — একই টুল, একই syntax
```

> Day 61-এর ECS বনাম EKS আলোচনার মতোই দর্শন — CloudFormation "AWS-native, সহজ"; Terraform "multi-cloud/tool-agnostic, বেশি ecosystem"।

---

## Part 2: HCL — HashiCorp Configuration Language

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

variable "environment_name" {
  type    = string
  default = "dev"
}

resource "aws_s3_bucket" "orders_bucket" {
  bucket = "shopbd-orders-${var.environment_name}"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
}

output "bucket_name" {
  value = aws_s3_bucket.orders_bucket.bucket
}

output "web_server_ip" {
  value = aws_instance.web_server.public_ip
}
```

| Block | কাজ |
|---|---|
| `provider` | কোন cloud/service-এর সাথে কথা বলবে (AWS, GCP, ইত্যাদি) |
| `resource` | কোন resource তৈরি হবে (CloudFormation-এর `Resources`-এর মতো) |
| `variable` | Input parameter (CloudFormation-এর `Parameters`-এর মতো) |
| `output` | Deploy শেষে দরকারি মান দেখানো (CloudFormation-এর `Outputs`-এর মতো) |

---

## Part 3: Terraform State — সবচেয়ে গুরুত্বপূর্ণ ধারণা

**সমস্যা:** Terraform কীভাবে জানে আপনার HCL কোডে যা লেখা আছে (**desired state**) আর AWS-এ আসলে কী আছে (**current state**) — এর মধ্যে পার্থক্য কী?

**সমাধান: `terraform.tfstate`** — একটা JSON ফাইল যেখানে Terraform প্রতিটা resource-এর **বর্তমান অবস্থা** track করে রাখে।

```
HCL কোড (desired state) ──┐
                          ├──► terraform plan (তুলনা) ──► "এই ৩টা resource তৈরি হবে, ১টা বদলাবে"
tfstate ফাইল (current state) ┘
```

> **CloudFormation-এর সাথে পার্থক্য:** CloudFormation নিজে AWS-এর ভেতরেই state track করে (আপনাকে কিছু manage করতে হয় না); Terraform-এ state ফাইল **আপনাকে নিজে manage করতে হয়** — এটা Terraform-এর সবচেয়ে বড় দায়িত্ব ও ঝুঁকির জায়গা।

---

## Part 4: Workflow — init → plan → apply → destroy

```bash
terraform init      # provider plugin ডাউনলোড, backend (state storage) সেটআপ
terraform plan       # কী পরিবর্তন হবে তার preview (CloudFormation-এর Change Set-এর মতোই ধারণা)
terraform apply       # প্ল্যান অনুযায়ী AWS-এ পরিবর্তন করা
terraform destroy     # সব resource মুছে ফেলা
```

- `terraform plan` **কখনো** সরাসরি resource বদলায় না — শুধু দেখায়
- `terraform apply` চালানোর সময় confirmation চায় (`yes` টাইপ করতে হয়), CI/CD-তে `-auto-approve` দিয়ে skip করা যায় (সতর্কতার সাথে)

---

## Part 5: Remote State — টিম Collaboration

**সমস্যা:** state ফাইল local মেশিনে থাকলে, দুইজন টিম মেম্বার একসাথে `apply` চালালে conflict/corruption হতে পারে, আর কারো লোকাল মেশিন হারিয়ে গেলে state-ও হারিয়ে যায়।

**সমাধান: Remote State** — state ফাইল S3-তে (Day 5-এর concept) রাখা হয়, আর **DynamoDB** (Day 56-57)-এর একটা টেবিল দিয়ে **state locking** করা হয় (একসাথে দুইজন apply করতে পারবে না)।

```hcl
terraform {
  backend "s3" {
    bucket         = "shopbd-terraform-state"
    key            = "orders-service/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

---

## Part 6: Hands-on Lab

1. একটা `main.tf` লিখুন: AWS provider + একটা S3 bucket + একটা EC2 instance
2. `terraform init`, `terraform plan`, `terraform apply` চালান
3. `terraform.tfstate` ফাইল খুলে দেখুন কী আছে (JSON)
4. একটা resource-এর property বদলে আবার `plan` চালান, পরিবর্তন preview দেখুন
5. S3 + DynamoDB দিয়ে remote backend সেটআপ করুন
6. `terraform destroy` দিয়ে সব মুছুন

---

## 🎯 আজকের মূল Takeaways
- Terraform cloud-agnostic (multi-provider), HCL syntax ব্যবহার করে
- State ফাইল Terraform-এর কেন্দ্রীয় ধারণা — desired বনাম current state তুলনা করতে ব্যবহৃত হয়
- CloudFormation নিজে state manage করে; Terraform-এ আপনাকে state manage করতে হয় (remote backend দিয়ে)
- `plan` সবসময় `apply`-এর আগে চালিয়ে পরিবর্তন preview করুন
- Remote state (S3 + DynamoDB lock) টিম collaboration-এর জন্য প্রায় বাধ্যতামূলক

## 📝 Self-check Questions
1. Terraform কেন "cloud-agnostic" বলা হয়, CloudFormation কেন না?
2. `terraform.tfstate` ফাইল না থাকলে Terraform কী করতে পারবে না?
3. `terraform plan` আর `terraform apply`-এর পার্থক্য কী?
4. DynamoDB লক টেবিল remote state-এ কেন দরকার?

## 💡 Pro Tips
- `terraform.tfstate` ফাইল কখনো Git-এ কমিট করবেন না (sensitive ডেটা থাকতে পারে) — সবসময় remote backend ব্যবহার করুন
- টিমে কাজ করলে Day 1 থেকেই remote state + locking সেটআপ করুন, পরে migrate করা ঝামেলার
- `terraform apply` চালানোর আগে সবসময় `plan` আউটপুট মনোযোগ দিয়ে পড়ুন, বিশেষ করে "will be destroyed" লাইনগুলো
- CI/CD pipeline-এ Terraform চালালে (Module 11-এর ধারণা প্রয়োগ) `plan` একটা stage-এ, manual approval-এর পর `apply` আরেকটা stage-এ রাখুন

## 🎨 Quick Reference
```
Blocks: provider | resource | variable | output
Workflow: init → plan → apply → destroy
State: tfstate ফাইল, desired vs current state tracking
Remote backend: S3 (state storage) + DynamoDB (locking)
plan = preview (কিছু বদলায় না) | apply = কার্যকর করা
```

## 🚨 বাস্তব পরিস্থিতি (যেসব ভুল প্রায়ই হয়)

**পরিস্থিতি ১:** state ফাইল একজনের লোকাল মেশিনে ছিল, সেই ব্যক্তির ল্যাপটপ ক্র্যাশ করল — টিমের কেউ আর জানত না কোন resource Terraform manage করছিল।
**শিক্ষা:** শুরু থেকেই remote state (S3) ব্যবহার করুন।

**পরিস্থিতি ২:** দুইজন ডেভেলপার একই সময়ে `terraform apply` চালাল (locking ছাড়া), state ফাইল corrupt হয়ে গেল।
**শিক্ষা:** DynamoDB state locking ছাড়া কখনো টিমে Terraform ব্যবহার করবেন না।

---

**⏮ আগের দিন:** [Day 75 — CloudFormation Advanced](./Day-75-CloudFormation-Advanced-Nested-Stacks-StackSets-Drift.md) | **⏭ পরের দিন:** [Day 77 — Terraform Modules, Workspaces ও CloudFormation বনাম Terraform](./Day-77-Terraform-Modules-Workspaces-CloudFormation-vs-Terraform.md)
