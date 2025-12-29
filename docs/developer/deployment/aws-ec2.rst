==================
AWS EC2 Deployment
==================

Complete guide to deploying Construbot on Amazon Web Services EC2 instances.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
========

This guide covers deploying Construbot to AWS EC2 using Docker Compose. This setup is suitable for small to medium deployments (up to several thousand users).

**What you'll build:**

- EC2 instance running Ubuntu 22.04
- Docker Compose orchestrating all services
- RDS PostgreSQL database (recommended) or self-hosted
- ElastiCache Redis (optional) or self-hosted
- S3 for media file storage
- Route 53 for DNS (optional)
- SSL certificate from Let's Encrypt

**Estimated cost:** $20-80/month depending on instance sizes

Prerequisites
=============

AWS Account Setup
-----------------

.. code-block:: bash

   ✓ AWS account with billing enabled
   ✓ AWS CLI installed and configured
   ✓ SSH key pair for EC2 access
   ✓ Domain name (for HTTPS)

**Install AWS CLI:**

.. code-block:: bash

   # macOS
   brew install awscli

   # Linux
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install

   # Configure
   aws configure

Local Requirements
------------------

.. code-block:: bash

   ✓ SSH client
   ✓ Git
   ✓ Basic Linux administration knowledge

Step 1: Launch EC2 Instance
============================

Instance Selection
------------------

**Recommended specs:**

- **Instance Type:** t3.small (2 vCPU, 2 GB RAM) minimum, t3.medium (2 vCPU, 4 GB RAM) recommended
- **OS:** Ubuntu Server 22.04 LTS
- **Storage:** 30 GB gp3 SSD minimum
- **Region:** Choose closest to your users

**Via AWS Console:**

1. Navigate to EC2 Dashboard
2. Click "Launch Instance"
3. Choose "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type"
4. Select instance type (t3.small or larger)
5. Configure storage (30 GB minimum)
6. Add tags: Name=construbot-production
7. Configure Security Group (see below)
8. Review and Launch

**Via AWS CLI:**

.. code-block:: bash

   aws ec2 run-instances \\
     --image-id ami-0557a15b87f6559cf \\ # Ubuntu 22.04 (us-east-1)
     --instance-type t3.small \\
     --key-name your-key-pair \\
     --security-group-ids sg-xxxxx \\
     --subnet-id subnet-xxxxx \\
     --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":30,"VolumeType":"gp3"}}]' \\
     --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=construbot-production}]'

Security Group Configuration
-----------------------------

**Required rules:**

.. code-block:: text

   Type        Protocol    Port Range    Source          Description
   SSH         TCP         22            Your IP         SSH access
   HTTP        TCP         80            0.0.0.0/0       HTTP traffic
   HTTPS       TCP         443           0.0.0.0/0       HTTPS traffic

**Via AWS Console:**

1. EC2 Dashboard → Security Groups → Create Security Group
2. Add inbound rules as above
3. Name: construbot-sg

**Via AWS CLI:**

.. code-block:: bash

   # Create security group
   aws ec2 create-security-group \\
     --group-name construbot-sg \\
     --description "Construbot security group"

   # Add rules
   aws ec2 authorize-security-group-ingress \\
     --group-name construbot-sg \\
     --protocol tcp --port 22 --cidr your-ip/32

   aws ec2 authorize-security-group-ingress \\
     --group-name construbot-sg \\
     --protocol tcp --port 80 --cidr 0.0.0.0/0

   aws ec2 authorize-security-group-ingress \\
     --group-name construbot-sg \\
     --protocol tcp --port 443 --cidr 0.0.0.0/0

Elastic IP
----------

**Assign static IP:**

.. code-block:: bash

   # Allocate Elastic IP
   aws ec2 allocate-address

   # Associate with instance
   aws ec2 associate-address \\
     --instance-id i-xxxxx \\
     --allocation-id eipalloc-xxxxx

.. warning::
   **Elastic IP charges:** You are charged when the IP is allocated but the instance is stopped. Release unused Elastic IPs to avoid charges.

Step 2: Connect to Instance
============================

SSH Connection
--------------

.. code-block:: bash

   # Get instance public IP
   aws ec2 describe-instances \\
     --instance-ids i-xxxxx \\
     --query 'Reservations[0].Instances[0].PublicIpAddress'

   # Connect via SSH
   ssh -i ~/.ssh/your-key.pem ubuntu@<public-ip>

**First time connection:**

You'll see a message about host authenticity. Type ``yes`` to continue.

Step 3: Server Setup
=====================

System Updates
--------------

.. code-block:: bash

   # Update package list
   sudo apt update

   # Upgrade packages
   sudo apt upgrade -y

   # Install basic tools
   sudo apt install -y git curl wget vim

Install Docker
--------------

.. code-block:: bash

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Add ubuntu user to docker group
   sudo usermod -aG docker ubuntu

   # Install Docker Compose
   sudo apt install -y docker-compose-plugin

   # Verify installation
   docker --version
   docker compose version

   # Log out and back in for group changes to take effect
   exit

Configure Firewall
------------------

.. code-block:: bash

   # Enable UFW
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # HTTP
   sudo ufw allow 443/tcp   # HTTPS
   sudo ufw --force enable

   # Check status
   sudo ufw status

Step 4: Deploy Application
===========================

Clone Repository
----------------

.. code-block:: bash

   # Create application directory
   sudo mkdir -p /opt/construbot
   sudo chown ubuntu:ubuntu /opt/construbot

   # Clone repository
   cd /opt/construbot
   git clone https://github.com/javier-llamas/construbot.git .

Configure Environment
---------------------

.. code-block:: bash

   # Copy environment template
   cp .env.example .env

   # Edit environment file
   nano .env

**Minimal production .env:**

.. code-block:: bash

   # Django
   DJANGO_SETTINGS_MODULE=construbot.config.settings.production
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<generate-with-openssl-rand-base64-50>
   DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

   # Database (self-hosted)
   DATABASE_URL=postgresql://construbot:strong-password@postgres:5432/construbot

   # Redis
   REDIS_URL=redis://redis:6379/0

   # Email (example with Mailgun)
   DJANGO_EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
   MAILGUN_API_KEY=your-api-key
   MAILGUN_SENDER_DOMAIN=mg.your-domain.com
   DEFAULT_FROM_EMAIL=noreply@your-domain.com

   # Static/Media
   USE_S3=True
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_STORAGE_BUCKET_NAME=construbot-media
   AWS_S3_REGION_NAME=us-east-1

   # Security
   DJANGO_SECURE_SSL_REDIRECT=True
   DJANGO_SECURE_HSTS_SECONDS=31536000

   # Monitoring
   SENTRY_DSN=your-sentry-dsn

Build and Start
---------------

.. code-block:: bash

   # Build production images
   docker compose build

   # Start services
   docker compose up -d

   # Check status
   docker compose ps

Initialize Database
-------------------

.. code-block:: bash

   # Run migrations
   docker compose run --rm django python manage.py migrate

   # Create superuser
   docker compose run --rm django python manage.py createsuperuser

   # Collect static files
   docker compose run --rm django python manage.py collectstatic --no-input

Step 5: Configure Domain and SSL
=================================

DNS Configuration
-----------------

**Using Route 53:**

.. code-block:: bash

   # Create hosted zone (if not exists)
   aws route53 create-hosted-zone --name your-domain.com --caller-reference $(date +%s)

   # Get hosted zone ID
   aws route53 list-hosted-zones

   # Create A record
   aws route53 change-resource-record-sets \\
     --hosted-zone-id Z1234567890ABC \\
     --change-batch '{
       "Changes": [{
         "Action": "CREATE",
         "ResourceRecordSet": {
           "Name": "your-domain.com",
           "Type": "A",
           "TTL": 300,
           "ResourceRecords": [{"Value": "your-elastic-ip"}]
         }
       }]
     }'

**Using other DNS providers:**

Add A record pointing to your Elastic IP:

.. code-block:: text

   Type: A
   Name: @
   Value: <your-elastic-ip>
   TTL: 3600

SSL Certificate (Let's Encrypt)
--------------------------------

.. code-block:: bash

   # Install certbot
   sudo apt install -y certbot python3-certbot-nginx

   # Stop nginx in Docker (if running)
   docker compose stop nginx

   # Obtain certificate
   sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

   # Certificates saved to:
   # /etc/letsencrypt/live/your-domain.com/fullchain.pem
   # /etc/letsencrypt/live/your-domain.com/privkey.pem

   # Set up auto-renewal
   sudo systemctl enable certbot.timer
   sudo systemctl start certbot.timer

**Update docker-compose.yml to mount certificates:**

.. code-block:: yaml

   nginx:
     volumes:
       - /etc/letsencrypt:/etc/letsencrypt:ro

**Restart nginx:**

.. code-block:: bash

   docker compose up -d nginx

Step 6: Configure AWS Services
===============================

RDS PostgreSQL (Recommended)
-----------------------------

**Benefits:**

- Automated backups
- High availability (Multi-AZ)
- Automatic failover
- Managed updates

**Create RDS instance:**

.. code-block:: bash

   aws rds create-db-instance \\
     --db-instance-identifier construbot-db \\
     --db-instance-class db.t3.micro \\
     --engine postgres \\
     --engine-version 14.7 \\
     --master-username construbot \\
     --master-user-password strong-password \\
     --allocated-storage 20 \\
     --backup-retention-period 7 \\
     --vpc-security-group-ids sg-xxxxx \\
     --publicly-accessible

**Update .env:**

.. code-block:: bash

   DATABASE_URL=postgresql://construbot:password@construbot-db.abc123.us-east-1.rds.amazonaws.com:5432/construbot

**Remove postgres from docker-compose.yml.**

ElastiCache Redis (Optional)
-----------------------------

.. code-block:: bash

   aws elasticache create-cache-cluster \\
     --cache-cluster-id construbot-redis \\
     --engine redis \\
     --cache-node-type cache.t3.micro \\
     --num-cache-nodes 1 \\
     --security-group-ids sg-xxxxx

**Update .env:**

.. code-block:: bash

   REDIS_URL=redis://construbot-redis.abc123.cache.amazonaws.com:6379/0

S3 for Media Files
------------------

.. code-block:: bash

   # Create S3 bucket
   aws s3 mb s3://construbot-media-your-domain

   # Block public access (use signed URLs)
   aws s3api put-public-access-block \\
     --bucket construbot-media-your-domain \\
     --public-access-block-configuration \\
       "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

   # Create IAM user for S3 access
   aws iam create-user --user-name construbot-s3-user

   # Attach S3 policy
   aws iam put-user-policy \\
     --user-name construbot-s3-user \\
     --policy-name S3Access \\
     --policy-document '{
       "Version": "2012-10-17",
       "Statement": [{
         "Effect": "Allow",
         "Action": ["s3:*"],
         "Resource": ["arn:aws:s3:::construbot-media-your-domain/*"]
       }]
     }'

   # Create access keys
   aws iam create-access-key --user-name construbot-s3-user

**Update .env:**

.. code-block:: bash

   USE_S3=True
   AWS_ACCESS_KEY_ID=<access-key>
   AWS_SECRET_ACCESS_KEY=<secret-key>
   AWS_STORAGE_BUCKET_NAME=construbot-media-your-domain

Step 7: Automate Startup
=========================

Systemd Service
---------------

Create ``/etc/systemd/system/construbot.service``:

.. code-block:: ini

   [Unit]
   Description=Construbot Docker Compose
   Requires=docker.service
   After=docker.service

   [Service]
   Type=oneshot
   RemainAfterExit=yes
   WorkingDirectory=/opt/construbot
   ExecStart=/usr/bin/docker compose up -d
   ExecStop=/usr/bin/docker compose down

   [Install]
   WantedBy=multi-user.target

**Enable service:**

.. code-block:: bash

   sudo systemctl enable construbot
   sudo systemctl start construbot

**Application now starts automatically on boot.**

Step 8: Monitoring and Maintenance
===================================

CloudWatch Monitoring
---------------------

**Enable detailed monitoring:**

.. code-block:: bash

   aws ec2 monitor-instances --instance-ids i-xxxxx

**Create CloudWatch alarms:**

.. code-block:: bash

   # CPU alarm
   aws cloudwatch put-metric-alarm \\
     --alarm-name construbot-high-cpu \\
     --alarm-description "Alert when CPU > 80%" \\
     --metric-name CPUUtilization \\
     --namespace AWS/EC2 \\
     --statistic Average \\
     --period 300 \\
     --evaluation-periods 2 \\
     --threshold 80 \\
     --comparison-operator GreaterThanThreshold \\
     --dimensions Name=InstanceId,Value=i-xxxxx

Automated Backups
-----------------

**Create backup script** ``/opt/construbot/scripts/backup.sh``:

.. code-block:: bash

   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   BUCKET="s3://construbot-backups"

   # Database backup (if using self-hosted)
   docker compose exec -T postgres pg_dump -U construbot construbot | \\
     gzip > /tmp/db_backup_$DATE.sql.gz

   # Upload to S3
   aws s3 cp /tmp/db_backup_$DATE.sql.gz $BUCKET/database/

   # Cleanup
   rm /tmp/db_backup_$DATE.sql.gz

**Schedule with cron:**

.. code-block:: bash

   # crontab -e
   0 2 * * * /opt/construbot/scripts/backup.sh

Log Management
--------------

**Ship logs to CloudWatch:**

.. code-block:: bash

   # Install CloudWatch agent
   wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
   sudo dpkg -i amazon-cloudwatch-agent.deb

   # Configure agent
   sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

Step 9: Scaling
===============

Vertical Scaling
----------------

.. code-block:: bash

   # Stop instance
   aws ec2 stop-instances --instance-ids i-xxxxx

   # Wait for stopped state
   aws ec2 wait instance-stopped --instance-ids i-xxxxx

   # Change instance type
   aws ec2 modify-instance-attribute \\
     --instance-id i-xxxxx \\
     --instance-type "{\"Value\": \"t3.medium\"}"

   # Start instance
   aws ec2 start-instances --instance-ids i-xxxxx

Horizontal Scaling
------------------

For multi-instance deployment:

1. Use Application Load Balancer (ALB)
2. Create Auto Scaling Group
3. Use RDS for database (required)
4. Use ElastiCache for Redis (required)
5. Use S3 for media files (required)

**This is beyond single-server scope** - consider using ECS or EKS for container orchestration.

Troubleshooting
===============

Instance Not Accessible
-----------------------

.. code-block:: bash

   # Check instance status
   aws ec2 describe-instance-status --instance-ids i-xxxxx

   # Check security group
   aws ec2 describe-security-groups --group-ids sg-xxxxx

   # Verify Elastic IP association
   aws ec2 describe-addresses

Application Not Starting
-------------------------

.. code-block:: bash

   # SSH into instance
   ssh -i ~/.ssh/your-key.pem ubuntu@<elastic-ip>

   # Check Docker logs
   cd /opt/construbot
   docker compose logs

   # Check service status
   docker compose ps

Out of Disk Space
-----------------

.. code-block:: bash

   # Check disk usage
   df -h

   # Clean Docker
   docker system prune -a -f

   # Resize volume (AWS Console or CLI)
   aws ec2 modify-volume --volume-id vol-xxxxx --size 50

Cost Optimization
=================

Reduce Costs
------------

1. **Use Reserved Instances** - Save up to 75% for 1-3 year commitment
2. **Right-size instances** - Monitor and adjust based on actual usage
3. **Use Spot Instances** - Save up to 90% (for non-critical workloads)
4. **Enable S3 Intelligent Tiering** - Automatic cost optimization
5. **Set up Budget Alerts** - Monitor spending

**Estimated monthly costs (us-east-1):**

.. code-block:: text

   t3.small EC2 instance:      $15-20
   30 GB gp3 storage:          $3
   RDS db.t3.micro:            $15
   50 GB S3 storage:           $1
   Data transfer (100 GB):     $9
   --------------------------------
   Total:                      $43-48/month

See Also
========

- :doc:`production-checklist` - Pre-deployment checklist
- :doc:`docker-compose` - Docker Compose configuration
- :doc:`environment-variables` - Environment setup
- :doc:`static-media-files` - S3 configuration
- `AWS EC2 Documentation <https://docs.aws.amazon.com/ec2/>`_
