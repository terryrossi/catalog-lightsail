# **Linux Server Project.**

 The purpose of this project is to take a baseline installation of a Linux server and prepare it to host a web applications. We will secure our server from a number of attack vectors, install and configure a database server, and deploy one of our existing web applications onto it.

 To complete this project, we'll use a Linux server instance on AWS (Amazon Lightsail).

## **The Script**

The script is written in Python 3.

##### To execute the script, run: `python catalog.py`

## **The Environment**

### Ubuntu Linux server instance on Amazon Lightsail:

  - A new lightsail instance was created on AWS
  - A new User has been created for the grader: `grader`.
          - `sudo adduser grader` From instance terminal.
          - `sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader`
          - `sudo nano /etc/sudoers.d/grader` changed `ubuntus` to `grader`
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



  - Packages have been updated `sudo apt-get update`
  - Packages have been upgraded `sudo apt-get upgrade`
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
            - `sudo ufw allow ssh`
            - `sudo ufw allow www`
            - `sudo ufw allow ntp`
            - `sudo ufw allow 2200/tcp`
            - `sudo nano /etc/ssh/sshd_config` Change port 22 to 2200
            - `sudo service sshd restart`
            - `sudo ufw status`

            `Application	Protocol	Port range
                  SSH	TCP	22
                  HTTP	TCP	80
                  Custom	TCP	2200`
  - Install pip: `sudo apt install python-pip`
  - Install psycopg2: `sudo apt-get install python-psycopg2`
  - Install Python setup tools: `sudo apt-get install python-setuptools`
  - Enable mod_wsgi: `sudo a2enmod wsgi`
  - Restart apache2: `sudo service apache2 restart`
  - Install Git: `apt-get install git`



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

  - Configure Apache to handle requests using WSGI:
        `sudo nano /etc/apache2/sites-enabled/000-default.conf`
        Add `WSGIScriptAlias / /var/www/html/myapp.wsgi` before the closing line `</VirtualHost>`:
            `<VirtualHost *:80>
                  	# The ServerName directive sets the request scheme, hostname and port that
                  	# the server uses to identify itself. This is used when creating
                  	# redirection URLs. In the context of virtual hosts, the ServerName
                  	# specifies what hostname must appear in the request's Host: header to
                  	# match this virtual host. For the default virtual host (this file) this
                  	# value is not decisive as it is used as a last resort host regardless.
                  	# However, you must set it for any further virtual host explicitly.
                  	#ServerName www.example.com

                  	ServerAdmin webmaster@localhost
                  	DocumentRoot /var/www/html

                  	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
                  	# error, crit, alert, emerg.
                  	# It is also possible to configure the loglevel for particular
                  	# modules, e.g.
                  	#LogLevel info ssl:warn

                  	ErrorLog ${APACHE_LOG_DIR}/error.log
                  	CustomLog ${APACHE_LOG_DIR}/access.log combined

                  	# For most configuration files from conf-available/, which are
                  	# enabled or disabled at a global level, it is possible to
                  	# include a line for only one particular virtual host. For example the
                  	# following line enables the CGI configuration for this host only
                  	# after it has been globally disabled with "a2disconf".
                  	#Include conf-available/serve-cgi-bin.conf
                  	WSGIScriptAlias / /var/www/html/myapp.wsgi
</VirtualHost>`
        Restart Apache: `sudo apache2ctl restart`

  - Create the WSGI file:
        `sudo nano /var/www/html/catalog.wsgi`




## Code Quality

The code quality has been validated using The PEP8 style guide. You can do a quick check using the pep8 command-line tool.
