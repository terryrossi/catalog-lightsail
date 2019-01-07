# **Linux Server Project**

 The purpose of this project is to take a baseline installation of a Linux server and prepare it to host a web applications.

 We will do the following tasks:

      1. Create an AWS account.
      2. Create a new Lightsail instance.
      3. Create a new `grader` user with `sudo` priviledges.
      4. Remove login access through passwords (allow access through private key)
      5. Remove `root` login access.
      6. Secure our server from a number of attack vectors.
      7. Install, Update and Upgrade all packages.
      8. Install and configure a database server.
      9. Deploy one of our existing web applications onto it.

(See more details below under **The Environment**)

## **SSH Login access for grader user from client**

`ssh -i /Users/username/Downloads/Keypair-file.pem grader@34.220.60.51 -p 2200`

## **The Script**

The script is written in Python 3.

##### To execute the script, run: `python3 catalog.py`

## **The Environment**

### Ubuntu Linux server instance on Amazon Lightsail:

      3. Create a new `grader` user with `sudo` priviledges.

          - `sudo adduser grader` From instance terminal.
          - `sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader`
          - `sudo nano /etc/sudoers.d/grader` changed `ubuntus` to `grader`

      4. Remove login access through passwords (allow access through private key only)

          - `sudo su - grader` to create files with right owner.
          - download key pairs file from AWS account
          - `cd grader`
          - `mkdir .ssh`
          - `chmod 700 .ssh`
          - `cd .ssh`
          - `touch authorized.keys`
          - `chmod 600 authorized.keys`
          - Retrieve public key for the key pair:
                Open new tab and Set permission to 400 on the downloaded key files: `chmod 400 keypair-file.pem`
          - `ssh-keygen -y` + enter keypair-file path
          - copy the public key displayed. paste it to authorized_keys file on grader account
          - SSH login from client:
          `ssh -i /Users/username/Downloads/Keypair-file.pem grader@34.220.60.51.xip.io -p 2200`

          - Video on how to access the server on a client app using key pairs:[AWS SSH Access](https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/)

      5. Remove `root` login access:
          - `sudo nano /etc/ssh/sshd_config`
          - change `PermitRootLogin prohibit-password` to `PermitRootLogin no`
          - Restart SSHD: `sudo service sshd restart `

      6. Secure our server from a number of attack vectors:
           Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123):
              - `sudo ufw default deny incoming`
              - `sudo ufw default allow outgoing`
              - `sudo ufw allow www`
              - `sudo ufw allow ntp`
              - `sudo ufw allow 2200/tcp`

              - `sudo nano /etc/ssh/sshd_config` Change port 22 to 2200
              - `sudo service sshd restart`
              - `sudo ufw status verbose`
              `ubuntu@ip-172-26-8-28:~$ sudo ufw status verbose
                Status: active
                Logging: on (low)
                Default: deny (incoming), allow (outgoing), disabled (routed)
                New profiles: skip

                To                         Action      From
                --                         ------      ----
                80/tcp                     ALLOW IN    Anywhere
                123                        ALLOW IN    Anywhere
                2200/tcp                   ALLOW IN    Anywhere
                80/tcp (v6)                ALLOW IN    Anywhere (v6)
                123 (v6)                   ALLOW IN    Anywhere (v6)
                2200/tcp (v6)              ALLOW IN    Anywhere (v6)`


  - Packages have been updated `sudo apt-get update`
  - Packages have been upgraded `sudo apt-get dist-upgrade` (Trying to run just sudo apt-get update && sudo apt-get upgrade wont install packages kept back because apt-get upgrade by default does not try to install new packages (such as new kernel versions); from the man page: under no circumstances are currently installed packages removed, or packages not already installed retrieved and installed.[Reference](https://serverfault.com/questions/265410/ubuntu-server-message-says-packages-can-be-updated-but-apt-get-does-not-update)
  - finger installed `sudo apt-get install finger`
  - Python3 installed `sudo apt-get python python3`
  - Apache2 installed `sudo apt-get install apache2`
  - Apache2 for wsgi python3 installed `sudo apt-get install libapache2-mod-wsgi-py3`
  - PostgreSql installed `sudo apt-get install postgresql`
  - Set Server time to UTC:
          1. `sudo apt install chrony`
          2. make sure `server 169.254.169.123 prefer iburst` is present in `/etc/chrony/chrony.conf`
          3. Restart the chrony service: `sudo /etc/init.d/chrony restart`
          4. Verify that chrony is using the 169.254.169.123 IP address to synchronize the time: `chronyc sources -v`
          5. Verify the time synchronization metrics: `chronyc tracking`
          `ubuntu@ip-172-26-8-28:~$ chronyc tracking
            Reference ID    : 169.254.169.123 (169.254.169.123)
            Stratum         : 4
            Ref time (UTC)  : Tue Dec 25 19:20:50 2018
            System time     : 0.000000006 seconds slow of NTP time
            Last offset     : +0.000044166 seconds
            RMS offset      : 0.000041572 seconds
            Frequency       : 12.203 ppm slow
            Residual freq   : +0.093 ppm
            Skew            : 0.154 ppm
            Root delay      : 0.000470 seconds
            Root dispersion : 0.000418 seconds
            Update interval : 260.3 seconds
            Leap status     : Normal`
  - I found that second option much easier (`sudo dpkg-reconfigure tzdata`)
  - Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123):
            - `sudo ufw default deny incoming`
            - `sudo ufw default allow outgoing`
            - `sudo ufw allow www`
            - `sudo ufw allow ntp`
            - `sudo ufw allow 2200/tcp`
            - `sudo nano /etc/ssh/sshd_config` Change port 22 to 2200
            - `sudo service sshd restart`
            - `sudo ufw status`


  - Install pip: `sudo apt install python-pip`
  - Install psycopg2: `sudo apt-get install python-psycopg2`
  - Install Flask `sudo apt-get install python-flask`
  - Install Python setup tools: `sudo apt-get install python-setuptools`
  - Enable mod_wsgi: `sudo a2enmod wsgi`
  - Restart apache2: `sudo service apache2 restart`
  - Install Git: `sudo apt-get install git`


### PostgreSQL Database

  - Do not allow remote connections: `sudo nano /etc/postgresql/9.5/main/pg_hba.conf`
      ... comment: `#host    all             all             ::1/128                 md5`
  - Access psql: `sudo su - postgres`
  - create Database: `CREATE DATABASE catalog;`
  - create user: `CREATE USER catalog;`
  - create password: `ALTER ROLE catalog WITH PASSWORD 'catalog'`
  - Grant priviledge to user on DB: `GRANT ALL ON DATABASE catalog TO catalog;`


## Deployment:

  - Creating the Flask App:
        `cd /var/www `
        `sudo mkdir catalog`
        `cd catalog`
        `sudo mkdir catalog`
        `cd catalog`
        `sudo git clone https://github.com/terryrossi/catalog-new.git`

  - Configure and Enable a New Virtual Host:
      Create catalog.conf to edit: sudo nano /etc/apache2/sites-available/catalog.conf
        `<VirtualHost *:80>
                ServerName 34.220.60.51.xip.io
                ServerAdmin terryrossi1@gmail.com
                WSGIScriptAlias / /var/www/catalog/catalog.wsgi
                <Directory /var/www/catalog/catalog/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/catalog/catalog/static
                <Directory /var/www/catalog/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
          </VirtualHost>`

      Create WSGI file
        `sudo nano /var/www/catalog/catalog.wsgi`
        `#!/usr/bin/python
          import sys
          import logging
          logging.basicConfig(stream=sys.stderr)
          sys.path.insert(0,"/var/www/catalog/")

          from catalog import catalog as application
          application.secret_key = '**************************.apps.googleusercontent.com'`

  - Configure Apache to handle requests using WSGI:

        sudo a2dissite 000-default.conf
        sudo a2ensite catalog.cong
              Restart Apache: `sudo apache2ctl restart`



        If there were errors, I used the command, as per the book:

        sudo tail -f /var/log/apach2/error.log




## Code Quality

The code quality has been validated using The PEP8 style guide. You can do a quick check using the pep8 command-line tool.
