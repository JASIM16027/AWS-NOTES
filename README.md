# AWS-NOTES

---

### **What is Cloud Computing?**  
- Cloud computing is the **on-demand delivery** of compute power, database storage, applications, and other IT resources.
  
- Cloud computing is a way of using computing resources like servers, storage, and databases over the internet instead of having them physically in your office or home. Think of it like renting a computer instead of buying one—you can access the resources whenever you need them, and you only pay for what you use.


---

### **Key Features of Cloud Computing**  

1. **On-Demand Access:**  
   - You can get computing resources whenever you need them, just like streaming a movie on Netflix instead of buying a DVD.  
   
2. **Access from Anywhere:**  
   - You can use cloud services from any device with an internet connection, whether you're at home, in the office, or traveling.

3. **Shared Resources (Resource Pooling):**  
   - The cloud provider (like Amazon Web Services or Google Cloud) manages a large number of servers and shares them among users. It’s like a power grid where multiple houses use electricity from the same source.

4. **Scalability (Grow or Shrink as Needed):**  
   - If you need more storage or computing power, you can increase it easily, just like upgrading your internet plan.

5. **Pay-as-You-Go (Measured Service):**  
   - You only pay for what you use. If you store more data or use more processing power, your bill increases, just like an electricity bill.

---

### **Types of Cloud Services (What Can You Use in the Cloud?)**  

1. **Infrastructure as a Service (IaaS)** – Like Renting a Virtual Computer  
   - Cloud providers give you access to virtual servers, storage, and networks.  
   - Example: Amazon EC2, Google Compute Engine (Think of renting a powerful computer online).  

2. **Platform as a Service (PaaS)** – Ready-to-Use Development Platform  
   - Provides tools and environments to build applications without managing the underlying infrastructure.  
   - Example: Google App Engine, AWS Elastic Beanstalk (Think of it as a pre-configured kitchen where you can just cook without worrying about the setup).  

3. **Software as a Service (SaaS)** – Fully Managed Software  
   - Provides applications that you can use directly without installing them.  
   - Example: Google Workspace (Gmail, Docs), Microsoft 365, Netflix (Think of it as using Uber instead of owning a car).  

---

### **Types of Cloud Deployment (Where is the Cloud Hosted?)**  

1. **Public Cloud** – Services are shared among multiple users and managed by a third-party provider.  
   - Example: Gmail, Google Drive, AWS, Microsoft Azure.  

2. **Private Cloud** – Dedicated cloud infrastructure for a single organization.  
   - Example: A company setting up its own private cloud for better security.  

3. **Hybrid Cloud** – A mix of public and private clouds to balance cost and security.  
   - Example: A bank using a public cloud for customer apps but a private cloud for sensitive transactions.  

4. **Multi-Cloud** – Using multiple cloud providers for redundancy and flexibility.  
   - Example: A company using AWS for databases and Google Cloud for analytics.  

---

### **Benefits of Cloud Computing (Why Use It?)**  

✅ **Cost Savings** – No need to buy expensive hardware, just rent what you need.  
✅ **Flexibility** – Access your data from anywhere.  
✅ **Scalability** – Increase or decrease resources based on demand.  
✅ **Security** – Cloud providers use encryption, backups, and security measures to protect data.  
✅ **Automatic Updates** – No need to manually update software, it happens automatically in the cloud.  

---

### **Real-Life Examples of Cloud Computing**  

- **Netflix** uses cloud servers to stream videos to millions of users without owning all the hardware.  
- **Google Drive** lets you store and share files online.  
- **Zoom** provides online meetings without needing special hardware.  
- **E-commerce Websites** like Amazon run on the cloud to handle millions of customers at once.





---


## Who Manage What?


![image](https://github.com/user-attachments/assets/e7630b02-eded-448b-b6ef-189b2fb65542)


This image explains the differences between **On-Premises**, **Infrastructure as a Service (IaaS)**, **Platform as a Service (PaaS)**, and **Software as a Service (SaaS)** in terms of management responsibilities.

### **Key Understanding**:
- The **blue boxes** represent components that **you manage**.
- The **orange boxes** represent components that are **managed by others (cloud providers)**.

---

### **1. On-Premises (Traditional IT)**
- **Fully managed by you**.
- You control everything, including hardware, software, networking, and security.
- Requires purchasing and maintaining physical servers, storage, and networking infrastructure.
- **Example:** Running a data center in your own office.

---

### **2. Infrastructure as a Service (IaaS)**
- The cloud provider **manages the physical infrastructure** (Networking, Storage, Servers, and Virtualization).
- You manage the **operating system, middleware, runtime, data, and applications**.
- Offers flexibility as you can install any software and configure it as needed.
- **Example:** Amazon EC2, Google Compute Engine, Microsoft Azure Virtual Machines.

---

### **3. Platform as a Service (PaaS)**
- The cloud provider **manages everything except your applications and data**.
- Developers only focus on coding and deploying applications without worrying about managing servers or operating systems.
- **Example:** AWS Elastic Beanstalk, Google App Engine, Microsoft Azure App Services.

---

### **4. Software as a Service (SaaS)**
- The cloud provider **manages everything**, and you only use the application.
- No need for installation, maintenance, or management of any underlying infrastructure.
- **Example:** Gmail, Microsoft 365, Google Drive, Dropbox, Zoom.

---

### **Comparison Summary**  
| Model | Who Manages What? | Example |
|--------|----------------|---------|
| **On-Premises** | You manage everything | Your own data center |
| **IaaS** | Cloud provider manages hardware; you manage OS, apps, and data | AWS EC2, Google Compute Engine |
| **PaaS** | Cloud provider manages most things; you manage apps and data | Google App Engine, AWS Elastic Beanstalk |
| **SaaS** | Cloud provider manages everything; you just use the software | Gmail, Google Drive, Zoom |

#### **Key Takeaway**  
- **IaaS** gives more control but requires management effort.  
- **PaaS** simplifies development but limits customization.  
- **SaaS** is the easiest but least flexible.  


---



## **AWS Cloud Pricing **  

![image](https://github.com/user-attachments/assets/bb4f5c7a-92d2-48ab-a53c-f6f721faec69)


This slide provides an overview of **AWS (Amazon Web Services) pricing**, which follows a **pay-as-you-go** model. This means you only pay for the resources you use, without upfront costs.

---

### **1. AWS Pricing Fundamentals**  
AWS pricing is based on three main factors:  

#### **1. Compute (Processing Power)**  
- You **pay for compute time**, which means you are charged based on the time your virtual servers (EC2 instances), containers, or serverless functions are running.  
- **Example Services:**  
  - **Amazon EC2** – Virtual machines (charged per second/minute).  
  - **AWS Lambda** – Serverless compute (charged per execution).  
  - **Amazon ECS/EKS** – Containerized workloads.  

💡 **Analogy:** Think of it like paying for a taxi ride—you are charged for the duration you use the service.  

---

#### **2. Storage (Data Stored in AWS)**  
- You are charged for the amount of data stored in AWS storage services.  
- **Example Services:**  
  - **Amazon S3** – Object storage (pay per GB stored).  
  - **Amazon EBS** – Block storage for EC2 instances.  
  - **Amazon Glacier** – Low-cost long-term backup storage.  

💡 **Analogy:** Think of it like renting a storage unit—the larger the space you use, the more you pay.  

---

#### **3. Data Transfer (Inbound is Free, Outbound is Charged)**  
- **Data transfer INTO AWS (uploads) is free.**  
- **Data transfer OUT OF AWS (downloads) is charged.**  
- Costs vary based on the destination and AWS region.  

💡 **Analogy:** Similar to a hotel minibar—bringing in food is free, but taking food out (or consuming minibar items) costs extra.  

---

### **2. Why AWS Pricing is Cost-Effective**  
Compared to traditional IT infrastructure, AWS eliminates:  
✔ **Upfront hardware costs** – No need to buy expensive servers.  
✔ **Maintenance costs** – AWS manages the infrastructure.  
✔ **Overprovisioning** – Scale up or down as needed.  

---

### **Conclusion:**  
AWS follows a **pay-as-you-go** model where you are billed based on:  
- **Compute:** Charged for processing power used.  
- **Storage:** Charged for data stored.  
- **Data Transfer:** Charged for data leaving AWS.  

💡 **Overall Benefit:** AWS helps businesses reduce costs and scale efficiently without investing in physical infrastructure.  



###  **Tour of the AWS Console**  


- **AWS has Global Services:**  
  - Identity and Access Management (IAM)  
  - Route 53 (DNS service)  
  - CloudFront (Content Delivery Network)  
  - WAF (Web Application Firewall)  

- **Most AWS services are Region-scoped:**  
  - Amazon EC2 (Infrastructure as a Service)  
  - Elastic Beanstalk (Platform as a Service)  
  - Lambda (Function as a Service)  
  - Rekognition (Software as a Service)
 
    

### **Detailed Explanation of the AWS Console and Services**  

Amazon Web Services (AWS) provides a broad range of cloud-based services, which can be categorized into **Global Services** and **Region-Scoped Services**. Understanding these distinctions is essential for effectively managing AWS resources and optimizing performance.

---

## **1. Global Services in AWS 🌍**  
Global services are **not tied to a specific AWS region**. These services operate across all AWS data centers worldwide and provide **centralized** management, making them accessible from anywhere.

### **Key AWS Global Services:**
#### **A. Identity and Access Management (IAM) 🔐**
- IAM is a security and access control service that helps manage user authentication and authorization in AWS.
- It allows organizations to **create users, roles, and policies** to define who can access AWS resources and what actions they can perform.
- Example: You can create an IAM role that grants **read-only** access to S3 buckets across all AWS regions.

#### **B. Amazon Route 53 🌐 (DNS Service)**
- Route 53 is a **scalable Domain Name System (DNS) web service** that helps route user traffic to applications.
- It supports domain registration, DNS health checks, and traffic flow management.
- Example: If you host a website on AWS, Route 53 can direct users to the correct web server based on their location.

#### **C. Amazon CloudFront 🚀 (Content Delivery Network - CDN)**
- CloudFront is AWS's **content delivery network** (CDN) that speeds up the distribution of web content by caching data in edge locations worldwide.
- It reduces latency and improves the performance of websites, videos, and applications.
- Example: A streaming service can use CloudFront to serve videos efficiently to users globally.

#### **D. AWS Web Application Firewall (WAF) 🛡️**
- WAF helps **protect web applications** from attacks such as **SQL injection, cross-site scripting (XSS), and DDoS attacks**.
- It filters and monitors HTTP/HTTPS requests based on security rules.
- Example: An eCommerce website can use WAF to block malicious requests from attackers.

---

## **2. Region-Scoped AWS Services 🌎**
Region-scoped services operate within a **specific AWS region**. This means that each region has its own isolated resources, and services **must be explicitly deployed in a chosen region**.

### **Key AWS Region-Scoped Services:**
#### **A. Amazon EC2 🖥️ (Infrastructure as a Service - IaaS)**
- EC2 provides **virtual servers (instances)** that run applications in the cloud.
- Users can choose **different instance types** based on CPU, memory, and storage needs.
- Example: A company hosting a web application can deploy **EC2 instances in the US East (Virginia) region** for faster access to North American users.

#### **B. AWS Elastic Beanstalk 🌱 (Platform as a Service - PaaS)**
- Elastic Beanstalk helps developers deploy and manage applications **without managing infrastructure**.
- It supports popular programming languages like **Node.js, Python, Java, and PHP**.
- Example: A startup can use **Elastic Beanstalk** to quickly deploy a website without worrying about server configurations.

#### **C. AWS Lambda ⚡ (Function as a Service - FaaS)**
- Lambda lets you run **serverless functions** in response to events **without provisioning or managing servers**.
- It automatically scales based on demand, making it cost-efficient.
- Example: A mobile app can trigger a Lambda function to **process user data every time a form is submitted**.

#### **D. Amazon Rekognition 📸 (Software as a Service - SaaS)**
- Rekognition is an **AI-powered image and video analysis service**.
- It can **detect faces, recognize text, and identify objects** in images or videos.
- Example: A security system can use **Rekognition** to verify identities based on facial recognition.

---

### **Summary: Key Differences**
| **Service Type** | **Global Services** | **Region-Scoped Services** |
|-----------------|---------------------|---------------------------|
| **Availability** | Available worldwide | Limited to specific AWS regions |
| **Examples** | IAM, Route 53, CloudFront, WAF | EC2, Elastic Beanstalk, Lambda, Rekognition |
| **Usage** | Used for security, networking, and global content delivery | Used for computing, development, and AI |

### **Final Thoughts**
- **Global Services** provide centralized management across AWS.
- **Region-Scoped Services** ensure **data locality, compliance, and reduced latency**.
- Understanding **which service is global vs. regional** helps optimize AWS usage for performance and cost-efficiency.



---

## AWS Shared Responsibility Model


![image](https://github.com/user-attachments/assets/85e32133-5df8-4d51-bacc-65521702b540)


### Security and Compliance: A Shared Responsibility
Security and Compliance is a shared responsibility between AWS and the customer. This shared model helps relieve the customer’s operational burden, as AWS:
- Operates, manages, and controls components from the host operating system and virtualization layer down to the physical security of the facilities.
- Provides infrastructure security, while customers assume responsibility for managing their guest operating system, application software, and firewall configurations.

Customers should carefully consider their chosen AWS services, as their responsibilities vary depending on:
- Services used.
- Integration into their IT environment.
- Applicable laws and regulations.

This differentiation is commonly referred to as **Security “of” the Cloud** versus **Security “in” the Cloud**.

### AWS Responsibility: "Security of the Cloud"
AWS is responsible for protecting the infrastructure that runs AWS Cloud services, which includes:
- Hardware
- Software
- Networking
- Facilities

### Customer Responsibility: "Security in the Cloud"
Customer responsibility depends on the AWS services selected. 
- **For IaaS services (e.g., Amazon EC2):** Customers must manage:
  - Guest operating system updates and security patches.
  - Application software or utilities installed.
  - AWS-provided firewall (security group) configuration.
- **For abstracted services (e.g., Amazon S3, DynamoDB):** AWS manages infrastructure, OS, and platforms, while customers must:
  - Manage and encrypt their data.
  - Classify assets.
  - Use IAM tools to set appropriate permissions.

### IT Control Shared Responsibility Model
AWS and customers share the management, operation, and verification of IT controls.

#### Control Categories:
1. **Inherited Controls:** Fully managed by AWS, such as:
   - Physical and environmental controls.

2. **Shared Controls:** Responsibilities are split between AWS and customers:
   - **Patch Management:**
     - AWS patches the infrastructure.
     - Customers patch their guest OS and applications.
   - **Configuration Management:**
     - AWS maintains infrastructure configuration.
     - Customers configure their OS, databases, and applications.
   - **Awareness & Training:**
     - AWS trains AWS employees.
     - Customers train their employees.

3. **Customer-Specific Controls:** Fully managed by customers, including:
   - Service and Communications Protection or Zone Security.
   - Routing or zoning data within specific security environments.

### Applying the AWS Shared Responsibility Model in Practice
To apply the AWS Shared Responsibility Model effectively, customers must consider factors such as chosen AWS services, Regions, integrations, and legal requirements.

#### Recommended Exercises:
1. **Determine Security & Compliance Requirements**
   - Consider frameworks like NIST Cybersecurity Framework (CSF) and ISO.
2. **Review AWS Service Capabilities for Privacy Considerations**
   - Utilize the AWS Cloud Adoption Framework (CAF) and Well-Architected best practices.
3. **Evaluate AWS Security Services**
   - Review security functionalities and configurations in AWS service documentation.
4. **Leverage AWS Compliance Documentation**
   - Analyze third-party audit attestation documents for inherited controls.
5. **Train Internal and External Audit Teams**
   - Use Cloud Audit Academy programs for cloud-specific learning.
6. **Perform a Well-Architected Review**
   - Assess security, reliability, and performance best practices.
7. **Explore AWS Marketplace Solutions**
   - Find and deploy security solutions from independent vendors.
8. **Leverage AWS Security Competency Partners**
   - Get expert assistance for cloud security and compliance management.



## AWS Acceptable Use Policy (Last Updated: July 1, 2021)

### **General Rules**
- By using AWS services or visiting the AWS website, you agree to follow this policy.
- AWS may update this policy at any time.

### **Prohibited Uses**
You **must not** use AWS services or the AWS website for:
1. **Illegal or fraudulent activities**
2. **Violating others' rights**
3. **Encouraging harm**, including violence or terrorism
4. **Child exploitation or abuse**
5. **Compromising security**, such as hacking or disrupting networks
6. **Sending spam**, including mass unsolicited emails or advertisements

### **Investigation & Enforcement**
- AWS may **investigate** any suspected violations.
- AWS can **remove or block access** to content that breaks this policy.
- You must **cooperate** if AWS asks you to fix a violation.

### **Policy Compliance Considerations**
- AWS may assess how well you follow this policy, including:
  - Your **ability** to comply
  - Your **efforts** to prevent or remove prohibited content





### **Identity and Access Management (IAM)**

AWS **Identity and Access Management (IAM)** is a **global** service that allows administrators to control access to AWS resources securely. The image provides key details about IAM **users** and **groups** within an organization.

---

### **Key Concepts:**
1. **IAM (Identity and Access Management) = Global Service**
   - IAM is not limited to a specific AWS region; it applies across all AWS services and accounts globally.

2. **Root Account**
   - The AWS **root account** is the first account created when signing up for AWS.
   - It has **full control** over all AWS services and should **not** be used for daily operations.
   - Sharing the root account **is not recommended** due to security risks.

3. **Users**
   - **IAM Users** represent individuals within an organization who require access to AWS services.
   - Each user gets a unique identity and **can be assigned permissions** based on their role.

4. **Groups**
   - **Groups are collections of IAM users** with similar permissions.
   - Groups help manage permissions efficiently rather than assigning them to users individually.
   - **Important Rule:** Groups **cannot** contain other groups, only individual users.

5. **Users & Group Membership**
   - A user **is not required** to belong to a group.
   - A user **can be part of multiple groups** at the same time.

---

![image](https://github.com/user-attachments/assets/d762fe27-4c49-47c3-9a76-fa69fbb1f1a6)


### **Understanding the Image**
The image displays different **IAM groups** and their **associated users**:

#### **Group: Developers (Blue Box)**
- **Users:** Alice, Bob, Charles
- **Purpose:** Likely given access to AWS services needed for software development (e.g., EC2, Lambda, S3).
- **Charles is also part of another group (Audit Team).**

#### **Group: Audit Team (Green Box)**
- **Users:** Charles, David
- **Purpose:** Likely focused on security auditing and compliance.
- **Charles and David are also part of other groups.**

#### **Group: Operations (Orange Box)**
- **Users:** David, Edward
- **Purpose:** Likely responsible for infrastructure management and system maintenance.
- **David is also part of the Audit Team.**

#### **User Outside Groups**
- **Fred** is not part of any group, meaning his permissions must be assigned directly.

---

### **Best Practices for IAM Users & Groups**
- **Use Groups for Role-Based Access Control:** Assign permissions to groups instead of individual users.
- **Follow the Principle of Least Privilege:** Users should only have the minimum permissions required for their tasks.
- **Avoid Using the Root Account:** Create admin users instead of using the root account.
- **Regularly Review IAM Permissions:** Ensure that users and groups have appropriate permissions and remove unused access.


