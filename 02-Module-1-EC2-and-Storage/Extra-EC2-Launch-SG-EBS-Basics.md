# 📝 EC2 Basics Notes — Instance Types, Launch, Security Group, EBS

## **EC2 Instance Type Attributes Explained**

When selecting an **EC2 instance type**, several key attributes determine its performance, capacity, and use case. Below is a detailed explanation of each attribute with examples:

---

### **1. Instance Type**
- Represents the category and size of the instance, combining compute, memory, and networking capabilities.  
- AWS offers various instance families such as:  
  - **General Purpose** (e.g., `t3.medium`)  
  - **Compute Optimized** (e.g., `c5.large`)  
  - **Memory Optimized** (e.g., `r5.large`)  
  - **Storage Optimized** (e.g., `i3.large`)  

**Example:**  
| Instance Type | Description |
|:---------------|:------------|
| `t3.medium`     | General purpose instance for balanced CPU and memory |
| `c5.large`       | Ideal for compute-intensive workloads like web servers |
| `r5.large`       | Suitable for applications requiring high memory like databases |

---

### **2. vCPUs (Virtual CPUs)**
- vCPUs determine the **processing power** of the instance.  
- Each vCPU is a **hyper-thread** of an Intel/AMD CPU core.  
- More vCPUs = Better parallel processing capability.  

**Example:**  
| Instance Type | vCPUs |
|:---------------|:-------|
| `t3.medium`     | 2 vCPUs |
| `c5.large`       | 2 vCPUs |
| `m5.2xlarge`     | 8 vCPUs |

---

### **3. Architecture**
- Refers to the **CPU architecture** supported by the instance.  
- Common architectures include:  
  - **x86_64** (Intel/AMD)  
  - **ARM64** (AWS Graviton processors for cost-efficiency)  

**Example:**  
| Instance Type | Architecture |
|:---------------|:-------------|
| `t3.medium`     | x86_64 |
| `m6g.large`     | ARM64 (Graviton) |
| `c5.large`       | x86_64 |

---

### **4. Memory (GiB)**
- Determines the **RAM** capacity of the instance.  
- Larger memory is crucial for applications that require high data processing like databases, caching servers, etc.  

**Example:**  
| Instance Type | Memory (GiB) |
|:---------------|:--------------|
| `t3.medium`     | 4 GiB |
| `r5.large`       | 16 GiB |
| `m5.2xlarge`     | 32 GiB |

---

### **5. Storage (GB)**
- Refers to the **instance storage capacity**.  
- Some instances provide **instance store** (temporary local storage) while others require **EBS volumes** (Elastic Block Storage) for persistent data.  

**Example:**  
| Instance Type | Storage (GB) | Storage Type |
|:---------------|:--------------|:----------------|
| `t3.medium`     | EBS only       | Persistent (Flexible) |
| `i3.large`         | 475 GB NVMe  | Local SSD (Fast & Temporary) |
| `m5.large`         | EBS only       | Persistent (Flexible) |

---

### **6. Storage Type**
- Defines how the storage behaves:  
  - **EBS (Elastic Block Store):** Persistent storage that exists separately from the instance.  
  - **Instance Store:** Temporary storage that’s directly attached to the instance (data is lost if the instance is stopped).  

**Example Use Cases:**  
- Use **EBS** for databases, applications, or persistent data.  
- Use **Instance Store** for caching or temporary data that doesn’t need to be retained.

---

### **7. Network Performance**
- Describes the **network bandwidth** available to the instance.  
- Performance is categorized as:  
  - **Low**, **Moderate**, **High**, or **Up to 25 Gbps**  
- Higher bandwidth is important for applications like media streaming, gaming servers, or data-intensive workloads.

**Example:**  
| Instance Type | Network Performance |
|:---------------|:----------------------|
| `t3.medium`     | Up to 5 Gbps |
| `c5.4xlarge`      | Up to 10 Gbps |
| `m5.8xlarge`      | Up to 25 Gbps |

---

### **Example Comparison Table for EC2 Instances**
| **Instance Type** | **vCPUs** | **Architecture** | **Memory (GiB)** | **Storage (GB)** | **Storage Type** | **Network Performance** |
|:------------------|:------------|:--------------------|:-------------------|:---------------------|:-----------------------|:----------------------------|
| `t3.medium`         | 2               | x86_64                  | 4                             | EBS only                   | Persistent (Flexible)       | Up to 5 Gbps                      |
| `c5.large`            | 2               | x86_64                  | 4                             | EBS only                   | Persistent (Flexible)       | Up to 10 Gbps                    |
| `r5.large`             | 2               | x86_64                  | 16                           | EBS only                   | Persistent (Flexible)       | Up to 10 Gbps                    |
| `i3.large`              | 2               | x86_64                  | 15.25                       | 475 GB NVMe             | Local SSD (Temporary)    | Up to 10 Gbps                    |

---

### **Choosing the Right Instance Type**
✅ Use **General Purpose** instances like `t3.medium` for websites, APIs, or small applications.  
✅ Use **Compute Optimized** instances like `c5.large` for heavy processing tasks.  
✅ Use **Memory Optimized** instances like `r5.large` for large in-memory databases.  
✅ Use **Storage Optimized** instances like `i3.large` for big data applications or analytics.



This image shows the **"Launch an EC2 Instance"** configuration page in the **AWS Management Console**. Let's break down each section in detail to understand its purpose and options.

---

## **1. Name and Tags**
- **Name:**  
   - This is where you assign a **name** to your instance for easier identification.  
   - Example: `MyWebServer`, `Database-Server`, etc.  
- **Tags (Optional):**  
   - Tags are key-value pairs that help you organize, track, and manage your AWS resources.  
   - Example:  
     - **Key:** `Environment` → **Value:** `Production`  
     - **Key:** `Department` → **Value:** `IT`  

✅ **Best Practice:** Use consistent naming conventions and meaningful tags for better resource management.

---

## **2. Application and OS Images (Amazon Machine Image - AMI)**
- The **Amazon Machine Image (AMI)** defines the **OS**, **applications**, and **configuration** for your instance.  
- Options include:  
  - **Amazon Linux 2** (optimized for AWS)  
  - **Ubuntu**, **Windows Server**, **RHEL**, etc.  
- AMIs can be customized to include pre-installed software, which simplifies deployment.

✅ **Best Practice:** Select an AMI that suits your workload and security needs.

---

## **3. Instance Type**
- The **instance type** defines the hardware resources for your instance, such as:  
  - **vCPU** (Virtual CPU)  
  - **RAM (Memory)**  
  - **Network Performance**  
- Common instance types include:  
  - **t2.micro** – Free Tier eligible, suitable for low-traffic web servers.  
  - **m5.large** – Ideal for general-purpose workloads.  
  - **c5.2xlarge** – Optimized for compute-heavy applications.  

✅ **Best Practice:** Choose the right instance type to balance cost and performance.

---

## **4. Key Pair (Login)**
- A **key pair** is essential for securely connecting to your instance via **SSH** (for Linux) or **RDP** (for Windows).  
- Options include:  
  - **Create a new key pair** (recommended if you haven’t generated one).  
  - **Use an existing key pair** if you’ve already created one.  

✅ **Important:** Download your `.pem` file securely and run `chmod 400 <filename>.pem` before connecting.

---

## **5. Network Settings**
- This section configures the networking environment for your instance.  
- Key options include:  
  - **VPC (Virtual Private Cloud):** Defines the network your instance will reside in.  
  - **Subnet:** Controls the IP range your instance will use.  
  - **Auto-assign public IP:** Determines whether the instance gets a public IP (required for SSH access).  
  - **Security Group:** Acts as a firewall to control inbound and outbound traffic.  
    - Example:  
      - **Inbound Rule:** Port `22` (SSH) from your IP.  
      - **Outbound Rule:** Typically allows **all traffic** by default.

✅ **Best Practice:** Always restrict SSH access to trusted IPs for better security.

---

## **6. Configure Storage**
- Here you define the **EBS (Elastic Block Store)** volumes attached to your instance.  
- Common storage types include:  
  - **gp3 (General Purpose SSD):** Balanced performance for most workloads.  
  - **io2 (Provisioned IOPS SSD):** Best for I/O-intensive applications.  
- You can adjust:  
  - **Size (GB)**  
  - **Volume Type**  
  - **Delete on termination** (deletes the volume when the instance is terminated).  

✅ **Best Practice:** Select appropriate storage based on performance needs.

---

## **7. Advanced Details**
This section allows you to configure additional settings, such as:

- **IAM Role:** Assign an IAM role to manage AWS resources securely.  
- **User Data:** Enter custom scripts that run during instance launch.  
- **Shutdown Behavior:** Choose whether the instance stops or terminates when shut down.  
- **Monitoring:** Enable **CloudWatch** for detailed performance insights.  
- **Elastic Fabric Adapter (EFA):** Optimizes performance for high-performance computing (HPC).

✅ **Best Practice:** Use **User Data** scripts for automation (e.g., installing updates, configuring services).

---

## **Recommended Steps for Launching an EC2 Instance**
1. **Name your instance** (e.g., `WebServer-Prod`).  
2. Select a **suitable AMI** (e.g., Amazon Linux 2 for general workloads).  
3. Choose an **instance type** (e.g., `t2.micro` for Free Tier).  
4. Select a **key pair** for secure SSH access.  
5. Configure **network settings** to restrict access only to your IP.  
6. Set appropriate **storage** size and type.  
7. Review all settings and click **Launch**.  

---

If you'd like guidance on specific configurations like setting up security groups, adding user data scripts, or automating deployment, let me know! 🚀


### **AWS EC2 Instance Details Explained**

When managing Amazon EC2 instances, you'll encounter various key attributes that describe the instance's identity, state, and network configuration. Below is a detailed explanation of each attribute with examples.

---

### **1. Name**
- The **Name** is a user-defined tag for easier identification of your EC2 instance.
- While optional, it’s highly recommended for tracking purposes.

**Example:**  
- `WebServer-01`  
- `Database-Production`  

💡 **Tip:** Use meaningful names for clarity, especially in environments with multiple instances.

---

### **2. Instance ID**
- A **unique identifier** automatically assigned by AWS to each instance.  
- Used to reference the instance in CLI commands, SDKs, or APIs.

**Format Example:**  
```
i-0abcdef1234567890
```

💡 **Tip:** The instance ID is immutable and cannot be changed.

---

### **3. Instance State**
Indicates the **current status** of the instance. Common states include:

- **`pending`** – The instance is launching.  
- **`running`** – The instance is active and ready for use.  
- **`stopping`** – The instance is in the process of shutting down.  
- **`stopped`** – The instance is halted but retains data in its EBS volumes.  
- **`terminated`** – The instance is permanently deleted.

**Example:**  
`running` (active and operational)

---

### **4. Instance Type**
- Defines the **hardware specifications** for the instance.  
- Includes vCPU count, memory (RAM), storage capacity, and network performance.

**Example Types:**  
- `t3.medium` (General purpose)  
- `c5.large` (Compute optimized)  
- `r5.large` (Memory optimized)  

---

### **5. Status Check**
AWS performs **health checks** to ensure the instance is operational. There are two types:

- **System Status Check:** Monitors AWS infrastructure issues (e.g., hardware failures).  
- **Instance Status Check:** Monitors software and network issues within the instance.

✅ **2/2 checks passed** = Healthy  
❌ **1/2 checks failed** = Investigate instance issues  

---

### **6. Alarm Status**
- Displays the state of **CloudWatch Alarms** configured for the instance.  
- Possible states:  
  - **OK** – The instance is functioning as expected.  
  - **ALARM** – A metric has breached the set threshold.  
  - **INSUFFICIENT DATA** – Data for the metric is unavailable.

**Example:**  
✅ **OK** — CPU utilization is within the expected range.  
⚠️ **ALARM** — CPU utilization exceeded 80%.

---

### **7. Availability Zone (AZ)**
- Specifies the **data center location** within an AWS Region where the instance runs.  
- Each region has multiple AZs for fault tolerance.

**Example:**  
- `us-east-1a` (First AZ in the `us-east-1` region)  
- `ap-south-1b` (Second AZ in the `ap-south-1` region)  

💡 **Tip:** Distributing instances across multiple AZs enhances high availability.

---

### **8. Public IPv4 DNS**
- A **domain name** automatically assigned to your instance for public access.  
- Changes every time the instance stops and starts unless an **Elastic IP** is associated.

**Example:**  
```
ec2-54-183-22-45.compute-1.amazonaws.com
```

---

### **9. Public IPv4 Address**
- A dynamically assigned **IP address** for public internet access.  
- Changes every time the instance stops and starts (unless linked to an Elastic IP).

**Example:**  
```
54.183.22.45
```

💡 **Tip:** If you need a **static IP**, use an **Elastic IP**.

---

### **10. Elastic IP**
- A **static IPv4 address** that remains constant even if the instance is stopped and restarted.  
- Ideal for scenarios where a **fixed IP** is required (e.g., DNS records or remote server connections).

**Example Elastic IP:**  
```
54.200.33.100
```

💡 **Tip:** Elastic IPs are **free** while associated with a running instance, but AWS charges if it's reserved without being in use.

---

### **Example Overview Table**
| **Attribute**           | **Example Value**                        | **Description**                          |
|-------------------------|------------------------------------------|-------------------------------------------|
| **Name**                  | `WebServer-01`                          | User-defined name for instance            |
| **Instance ID**           | `i-0abcdef1234567890`                   | Unique identifier for the instance        |
| **Instance State**        | `running`                                | Instance is active and operational         |
| **Instance Type**         | `t3.medium`                             | General purpose instance                  |
| **Status Check**          | `2/2 checks passed`                     | Both system and instance checks passed     |
| **Alarm Status**          | `OK`                                     | No issues detected by CloudWatch alarms    |
| **Availability Zone**     | `us-east-1a`                             | Data center location within the AWS region |
| **Public IPv4 DNS**       | `ec2-54-183-22-45.compute-1.amazonaws.com` | Public domain name for external access     |
| **Public IPv4 Address**   | `54.183.22.45`                          | Dynamic IP for public internet access       |
| **Elastic IP**            | `54.200.33.100`                         | Static IP address (remains constant)       |

---

### **Best Practices**
✅ Assign **meaningful names** to your instances for easy identification.  
✅ Monitor **Status Checks** and **Alarm Status** for proactive issue detection.  
✅ Use **Elastic IPs** for instances requiring static IP addresses.  
✅ Distribute instances across **multiple AZs** for high availability.  


### **Creating a Security Group in AWS EC2**
A **Security Group** in AWS acts as a **virtual firewall** for your EC2 instance, controlling both **inbound** (incoming) and **outbound** (outgoing) traffic. This is crucial for ensuring that only authorized connections can access your instance.

---

### **Steps to Create a Security Group**
The form shown in the image breaks down the creation process into several sections:

---

### **1. Basic Details**
This section defines the fundamental details of the security group:

- **Security Group Name**  
   - The name uniquely identifies your security group.  
   - Once created, the **name cannot be edited**.  
   - Example: `WebServer-SG`, `Database-SG`, or `AppServer-SG`.

- **Description**  
   - Provides a meaningful description to explain the purpose of the security group.  
   - Example: `"Allows SSH, HTTP, and HTTPS traffic for web servers"`

- **VPC (Virtual Private Cloud)**  
   - Select the **VPC** where this security group will reside.  
   - A VPC defines your AWS network environment.  
   - Example: Select your **default VPC** or a custom one you created.

✅ **Best Practice:** Use descriptive names and clear descriptions for better resource management.

---

### **2. Inbound Rules**
**Inbound rules** define what kind of incoming traffic is allowed to reach your instance.

- **By default**, no inbound rules are added, meaning **all incoming traffic is denied**.
- Click **"Add rule"** to specify allowed connections.

**Example Inbound Rules for a Web Server:**

| **Type** | **Protocol** | **Port Range** | **Source** |
|:-----------|:---------------|:------------------|:---------------|
| **SSH**      | TCP             | **22**               | `My IP` (Recommended) |
| **HTTP**     | TCP             | **80**               | `0.0.0.0/0` (Public Access) |
| **HTTPS**    | TCP             | **443**              | `0.0.0.0/0` (Public Access) |

✅ **Best Practice:** Restrict SSH access to your IP only for security purposes.

---

### **3. Outbound Rules**
**Outbound rules** control the outgoing traffic from your instance.

- **By default**, AWS allows **all outbound traffic** unless restricted.
- Click **"Add rule"** if you need to limit outbound connections.

**Example Outbound Rule:**

| **Type** | **Protocol** | **Port Range** | **Destination** |
|:-----------|:---------------|:------------------|:-------------------|
| **All Traffic** | All               | All                         | `0.0.0.0/0` (Allow all outgoing connections) |

✅ **Best Practice:** Outbound rules are often left unrestricted unless you need stricter control.

---

### **4. Tags (Optional)**
Tags are **key-value pairs** that help you organize and manage AWS resources.

- **Key:** Identifies the tag. Example: `Environment`, `Project`, or `Owner`.
- **Value:** Describes the key. Example: `Production`, `WebApp`, or `TeamA`.

**Example Tags for a Web Server Security Group:**

| **Key**       | **Value**   |
|:-----------------|:--------------|
| `Environment`  | `Production` |
| `Owner`         | `DevOps Team` |

✅ **Best Practice:** Use consistent tagging to simplify cost tracking and resource identification.

---

### **5. Final Steps**
1. After configuring the details, click **"Create security group"**.
2. Attach the security group to your EC2 instance during the instance creation process.

---

### **Key Tips for Best Practices**
✅ Follow the **principle of least privilege** — allow only the minimum access required.  
✅ Regularly **review and update rules** to ensure security.  
✅ Avoid using `0.0.0.0/0` for SSH unless absolutely necessary.  
✅ Use meaningful **names** and **tags** for better organization.



### **AWS EBS Overview**  

AWS Elastic Block Store (EBS) is a cloud-based storage service designed to deliver durable, high-performance block storage for Amazon EC2 instances.  

It functions like a virtual hard drive, enabling data storage and access even if your EC2 instances are stopped or terminated.



