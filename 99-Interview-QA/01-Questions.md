# ❓ AWS Interview Questions (Q1–Q130)

> উত্তর: [02-Answers-Q1-Q130.md](./02-Answers-Q1-Q130.md)
> 🃏 Flashcard আকারে practice করতে চাইলে: [AWS Recall — Interactive Flashcards](https://claude.ai/artifact/K4VzZgRwxxRuAKPRc7Rb23)


## Core / Foundational

1. What is AWS, and what are the main service categories it offers?
2. Explain the difference between **Availability Zones**, **Regions**, and **Edge Locations**.
3. What is the AWS shared responsibility model?
4. What's the difference between a public and private subnet?
5. What is the difference between scalability and elasticity?
6. What's the difference between vertical and horizontal scaling, and how does AWS support each?

## EC2 & Compute

7. What are the different EC2 pricing models (On-Demand, Reserved, Spot, Savings Plans), and when would you use each?
8. What's the difference between an EC2 instance and a Lambda function? When would you choose one over the other?
9. What is an AMI (Amazon Machine Image)?
10. Explain Auto Scaling Groups — how do they work and what triggers scaling actions?
11. What's the difference between an Application Load Balancer (ALB) and a Network Load Balancer (NLB)?
12. How does AWS Lambda pricing work, and what are cold starts?
13. What are EC2 instance types optimized for (compute, memory, storage), and how do you choose the right one?
14. What's the difference between ECS, EKS, and Fargate?

## Storage

15. What's the difference between S3 storage classes (Standard, IA, One Zone-IA, Glacier, Intelligent-Tiering)?
16. How does S3 achieve durability (11 nines) and what does that actually mean?
17. What's the difference between EBS and instance store volumes?
18. What's the difference between EBS, EFS, and S3 — when would you use each?
19. How do S3 bucket policies differ from IAM policies?
20. What is S3 versioning, and how does it interact with lifecycle policies?
21. Explain S3 pre-signed URLs and a use case for them.

## Networking (VPC)

22. What is a VPC, and what are its core components (subnets, route tables, internet gateway, NAT gateway)?
23. What's the difference between a NAT Gateway and an Internet Gateway?
24. How do Security Groups differ from Network ACLs?
25. What is VPC peering, and what are its limitations (e.g., no transitive peering)?
26. What is a Transit Gateway, and why would you use it over VPC peering at scale?
27. How does Route 53 support different routing policies (latency, weighted, failover, geolocation)?
28. What's the difference between a public and an Elastic IP?

## Databases

29. What's the difference between RDS and DynamoDB, and when would you pick each?
30. What is Multi-AZ deployment in RDS, and how does it differ from Read Replicas?
31. Explain DynamoDB partition keys and sort keys — how do they affect performance?
32. What is read/write capacity in DynamoDB (provisioned vs. on-demand)?
33. What's the difference between Aurora and standard RDS engines (MySQL/PostgreSQL)?
34. What is ElastiCache, and when would you use Redis vs. Memcached?

## Security & IAM

35. What's the difference between an IAM role and an IAM user?
36. How does IAM policy evaluation logic work (explicit deny vs. allow)?
37. What is the principle of least privilege, and how do you implement it in AWS?
38. What's the difference between IAM policies and resource-based policies (e.g., S3 bucket policy)?
39. What is AWS KMS, and how does it integrate with services like S3 and EBS?
40. What is AWS Secrets Manager vs. Systems Manager Parameter Store?
41. How does MFA work with IAM, and how can you enforce it?
42. What is AWS Organizations, and how do Service Control Policies (SCPs) work?
43. What is AWS WAF, and how does it protect applications?

## Serverless & Application Integration

44. What's the difference between SQS and SNS?
45. What is the difference between SQS Standard and FIFO queues?
46. How does API Gateway integrate with Lambda?
47. What is Step Functions used for?
48. What's the difference between EventBridge and SNS?
49. How do you handle retries and dead-letter queues in a serverless architecture?

## Monitoring, DevOps & Architecture

50. What is CloudWatch used for, and what's the difference between metrics, logs, and alarms?
51. What is CloudTrail, and how does it differ from CloudWatch?
52. What is Infrastructure as Code, and how does CloudFormation compare to Terraform?
53. What is a CI/CD pipeline in AWS (CodePipeline, CodeBuild, CodeDeploy)?
54. Explain the concept of a "well-architected framework" and its pillars.
55. How would you design a highly available, fault-tolerant 3-tier web application on AWS?
56. What is a blue/green deployment, and how can it be implemented in AWS?
57. What's the difference between horizontal and vertical scaling in the context of RDS vs. DynamoDB?

## Scenario-Based (common in interviews)

58. How would you reduce costs for a workload running on EC2 24/7 with predictable usage?
59. A website is experiencing latency for global users — how would you architect a fix?
60. How would you secure an S3 bucket that should only be accessible by your application, not the public?
61. Design a disaster recovery strategy for a critical application (RTO/RPO considerations).
62. How would you migrate an on-premises database to AWS with minimal downtime?

---



## Core / Foundational (additional)

63. What's the difference between an AWS account and an AWS Organization?
64. What is the AWS Free Tier, and what are its limitations?
65. What's the difference between the AWS Management Console, CLI, and SDKs?
66. What is an AWS service quota (limit), and how do you request an increase?
67. What's the difference between a managed service and an unmanaged/self-hosted service on AWS?

## EC2 & Compute (additional)

68. What is the difference between EC2 Spot Instances and Spot Fleets?
69. What is a launch template, and how does it differ from a launch configuration?
70. What are EC2 placement groups (cluster, spread, partition), and when would you use each?
71. What is the difference between EBS-backed and instance-store-backed AMIs?
72. What is AWS Elastic Beanstalk, and how does it differ from manually configuring EC2 + ALB + ASG?
73. What is AWS Batch, and when would you use it instead of Lambda or EC2 directly?
74. What's the difference between Lightsail and EC2?
75. How does hibernation differ from stopping an EC2 instance?

## Storage (additional)

76. What's the difference between S3 Object Lock and bucket versioning?
77. What is S3 Transfer Acceleration, and when is it useful?
78. What's the difference between S3 Cross-Region Replication (CRR) and Same-Region Replication (SRR)?
79. What is AWS Storage Gateway, and what problem does it solve for hybrid environments?
80. What's the difference between EBS volume types (gp3, io2, st1, sc1)?
81. How do you back up and restore EBS volumes using snapshots?
82. What is S3 Glacier Vault Lock, and why might a compliance team require it?

## Networking (VPC) (additional)

83. What's the difference between a public IP, a private IP, and an Elastic IP?
84. What is a VPC endpoint, and what's the difference between a Gateway endpoint and an Interface endpoint?
85. How does AWS Direct Connect differ from a VPN connection to AWS?
86. What is a Bastion Host, and what role does it play in securing private subnet access?
87. What's the difference between Route 53 Alias records and standard CNAME records?
88. What is AWS Global Accelerator, and how does it differ from CloudFront?
89. How does CloudFront work with an S3 origin vs. a custom (EC2/ALB) origin?

## Databases (additional)

90. What is Amazon Redshift, and how does it differ from RDS?
91. What is DynamoDB Global Tables, and what problem does it solve?
92. What are DynamoDB Streams, and what are they typically used for?
93. What is RDS Proxy, and what problem does it solve for database connections?
94. What's the difference between a database snapshot and a database backup in RDS?
95. What is Amazon DocumentDB, and when would you choose it over DynamoDB?
96. What is Amazon Neptune used for?

## Security & IAM (additional)

97. What's the difference between AWS Shield Standard and Shield Advanced?
98. What is Amazon GuardDuty, and what kind of threats does it detect?
99. What is AWS Config, and how does it differ from CloudTrail?
100. What is AWS Inspector, and what does it scan for?
101. What's the difference between encryption at rest and encryption in transit, and how does AWS support each?
102. What is a Customer Managed Key (CMK) vs. an AWS Managed Key in KMS?
103. How does cross-account IAM role assumption work (AssumeRole)?
104. What is AWS Certificate Manager (ACM), and how does it integrate with ALB/CloudFront?

## Serverless & Application Integration (additional)

105. What's the difference between synchronous and asynchronous Lambda invocations?
106. What is Lambda concurrency, and what's the difference between reserved and provisioned concurrency?
107. What is AWS AppSync, and how does it relate to GraphQL?
108. What's the difference between an SQS visibility timeout and a message retention period?
109. How would you design a fan-out architecture using SNS and multiple SQS queues?

## Monitoring, DevOps & Architecture (additional)

110. What's the difference between CodePipeline, CodeBuild, and CodeDeploy?
111. What's the difference between a blue/green deployment and a canary deployment?
112. What is AWS X-Ray, and how does it help with debugging distributed applications?
113. What is the AWS Trusted Advisor, and what categories of recommendations does it provide?
114. What is AWS Cost Explorer, and how does it differ from AWS Budgets?
115. What is a Savings Plan, and how does it differ from a Reserved Instance?
116. What's the difference between CloudFormation StackSets and a regular CloudFormation stack?
117. What is drift detection in CloudFormation?

## Migration & Hybrid Cloud

118. What is the AWS Database Migration Service (DMS), and what does it do?
119. What is AWS Schema Conversion Tool (SCT), and how does it relate to DMS?
120. What is AWS Snowball/Snowball Edge, and when would you use it instead of transferring data over the network?
121. What is AWS DataSync, and what use case does it solve?
122. What's the difference between a "lift and shift" and a "re-architecture" migration strategy?
123. What is AWS Application Migration Service (MGN)?

## Scenario-Based (additional)

124. Your application needs to process 10,000 image uploads per minute with unpredictable spikes — how would you architect this serverlessly?
125. A team accidentally exposed AWS access keys in a public GitHub repo — what's your incident response process?
126. How would you set up a multi-account AWS environment for a growing company (dev/staging/prod separation)?
127. Your RDS database is experiencing high read load during business hours — what are your options to fix this without major re-architecture?
128. How would you estimate and control costs before deploying a new workload to AWS?
129. Your company needs to comply with data residency laws in the EU — how does this affect your AWS architecture decisions?
130. How would you design a zero-downtime deployment strategy for a stateful application?

