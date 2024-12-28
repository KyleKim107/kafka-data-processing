# kafka-data-processing

 **Create EC2** 
![](images/ec2-console.png)
 **Connect to EC2**
   ```bash
   $ ssh -i "dataEng-seoul.pem" ec2-user@<your-ec2-public-ip>.ap-northeast-1.compute.amazonaws.com
   ```

## Kafka Setup on EC2

### Create 3 EC2 Instances for Kafka
- Use medium-type instances.

### Install Kafka

1. **Download and Extract Kafka**
   ```bash
   $ wget https://downloads.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz
   $ tar xvf kafka_2.13-3.6.1.tgz
   $ ln -s kafka_2.13-3.6.1 kafka
   ```

2. **Start Kafka Services**
   ```bash
   $ cd kafka
   $ ./bin/zookeeper-server-start.sh config/zookeeper.properties &
   $ ./bin/kafka-server-start.sh config/server.properties &
   ```

3. **Verify Services**
   ```bash
   $ sudo netstat -anp | egrep "9092|2181"
   ```

4. **Create a Kafka Topic**
   ```bash
   $ bin/kafka-topics.sh --create --topic apartinfo --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092 &
   ```

5. **List Topics**
   ```bash
   $ bin/kafka-topics.sh --list --bootstrap-server localhost:9092
   ```

6. **Consume Messages**
   ```bash
   $ ./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic apartinfo --from-beginning
   ```

---

## Kafka Producer and Consumer Setup

### Install Logstash (Producer)
1. **Add Logstash Repository**
   ```bash
   $ sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
   $ sudo vi /etc/yum.repos.d/logstash.repo
   ```

   Add the following:
   ```
   [logstash-8.x]
   name=Elastic repository for 8.x packages
   baseurl=https://artifacts.elastic.co/packages/8.x/yum
   gpgcheck=1
   gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
   enabled=1
   autorefresh=1
   type=rpm-md
   ```

2. **Install and Configure Logstash**
   ```bash
   $ sudo yum install logstash -y
   $ logstash --version
   ```

3. **Create Logstash Config File**
   ```bash
   $ vi apartinfo_test.conf
   ```

   Example configuration:
   ```plaintext
   input {
         s3 {
           access_key_id => "accesskey"
           secret_access_key => "security_key"
           region => "ap-northeast-2"
           prefix => "ods/danji_master.json/"
           bucket => "fc-storydata"
           additional_settings => {
             force_path_style => true
             follow_redirects => false
           }
         }
       }

   output {
     stdout { }
   }
   ```

4. **Run Logstash**
   ```bash
   $ logstash -f apartinfo_test.conf
   ```

---