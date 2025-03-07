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







