Selleh Lake Restoration
Water Quality Monitoring Dashboard Setup Guide
Prepared for Selleh Lake Restoration team by Rushikesh Sargar

1.	Objective
Selleh lake restoration project focuses on restoring the Selleh Lake in Tempe region with several methods such as Cyano System, Hydroponic Floating Gardens, Robotic Pond Skimmer. The monitoring dashboard project focuses on monitoring the quality of the water to measure the effect of the restoration methods as well as some of the parameters related to the system.

2.	Setup Process
a.	Pre-Requisites: AWS Account, Text Editor, Python 3.x, PuTTY, PuTTYgen, WinSCP
b.	 Technologies Used: AWS IoT Core, DynamoDb, AWS LightSail, Python, Django, HTML, Javascript, CSS
3.	Steps:
a.	Create and AWS account and get an access key and a secret key for the account. (Set your region to us-west-2)
b.	In order to have virtual representation of the sensors which are going to collect the data, create devices in AWS IoT Core
i.	Go to Manage -> Things -> Create a single thing
ii.	Following devices need to be created (keep the name of the device as mentioned as the code is configured accordingly).
1.	D_Oxygen01
2.	D_Turbidity01
3.	D_OutFlow01
4.	D_InFlow01
iii.	Once you enter a device’s name select ‘One Click certification - Create Certificate’ and download ‘certificate for this thing’, ‘public key’ and ‘private key’ and also download and activate the ‘root CA for AWS’
iv.	Click on ‘Attach a Policy’, for the first time there will be no policy. In that case create a new policy.
v.	Give any name to the policy set Action as ‘iot:*’ and resource ARN as ‘*’ and select ‘Allow’ in effect
vi.	Policy has to be created only once you can choose the same one for all the devices.

c.	Once the devices are created, create a database to store the data received from the sensors
i.	Go to ‘DynamoDb’ on AWS console (make sure you create the tables in us-west-2 region)
ii.	Following tables need to be created with mentioned Primary Key and Sort Key

Table Name	Primary Key	Sort Key
Inflow_data	timestamp	deviceId
outflow_data	timestamp	deviceId
turbidity_data	timestamp	deviceId
dissolvedoxygen_data	timestamp	deviceId
Inflow_daily	day	deviceId
outflow_daily	day	deviceId
turbidity_daily	day	deviceId
dissolvedoxygen_daily	day	deviceId
Inflow_hourly	hour	deviceId
outflow_hourly	hour	deviceId
turbidity_hourly	hour	deviceId
dissolvedoxygen_hourly	hour	deviceId
Inflow_weekly	week	deviceId
outflow_weekly	week	deviceId
turbidity_weekly	week	deviceId
dissolvedoxygen_weekly	week	deviceId

d.	Now that the databases are created rules have to be set up to transfer the data to databases as soon as they are received on the devices. Go to AWS IoT Core -> Rules
i.	Click on create a rule and give a name to the rule for e.g StoreTurbidity
ii.	In the Rule Query Statement write 
‘SELECT * FROM '/sensors/devicedata/turbidity'

* The data from the physical sensor has to be pushed on this topic i.e ‘/sensors/devicedata/turbidity’ the rule is selecting everything received on the topic
iii.	In ‘Set one or more Actions’ select ‘Split message into multiple columns of DynamoDB table (DynamoDBv2)’ and select the source name as the table ‘_data’ table from DynamoDb in this example select ‘turbidity_data’ and create a new role and give a name to the role.

Following rules to be created with mentioned queries.

Rule Name	Query
StoreInFlow	SELECT * FROM ‘/sensors/devicedata/inflow’
StoreOutFlow	SELECT * FROM ‘/sensors/devicedata/outflow’
StoreDissolvedOxygen	SELECT * FROM ‘/sensors/devicedata/dissolvedoxygen’
StoreTurbidity	SELECT * FROM ‘/sensors/devicedata/turbidity’


e.	With this the setup of the virtual sensors and the configuration to push the data in db is completed. You may run ‘push_dummy_data.py’ file to test the configuration. Make sure you have entered the file paths of private key and certificate of each sensor as weel as of the root CA certificate correctly in the file. This file will add random data for each sensor in every 5 seconds.
f.	For hosting the dashboard online: The site will be hosted on AWS Lighsail instance , it can be done on EC2 as well, but lightsail is cost efficient.
g.	Go to AWS Console , search AWS LightSail, Click on create instance and select Django under Linux (choose instance location as us-west-2), Download the key in SSH key pair manager (.pem file) we will use this key file to access the instance. Once downloaded create the instance.
h.	Instance will be start running in moments, click on the instance and go to networking.
i.	Create a static ip for the instance and note the static ip.
j.	Under firewall, create rules SSH – TCP – 22 will be there by default. 
k.	Add HTTP – TCP – 80  
l.	You can directly click on ‘Connect using SSH’ to access the instance, it is better to use ‘PuTTY’ app. Make sure you have that on your system or else you need to download it from the internet.
m.	Also download PuTTYgen it be used to convert .pem file to .ppk which will used to log in to lightsail instance.
n.	How to convert.pem to .ppk
i.	Open PuTTYgen
ii.	Click on load and select the .pem file
iii.	Click on save private key
o.	How to access lightsail instance
i.	Open PuTTY
ii.	Add hostname as ‘bitnami@<static_ip>’ put the static ip here.
iii.	Expand on SSH option, click on ‘Auth’, load the .ppk file using browse option.
iv.	Save this session with some name and click on open
p.	Before putting the files on light sail instance we have to make sure, the code in files know about the lightsail instance. 
i.	Open the ‘slr_backend/slr_backend’ folder go to the settings.py file.
ii.	Put your accounts access_key as the value of AWS_ACCESS_KEY_ID and secret key as the value of AWS_SECRET_ACCESS_KEY
iii.	For ALLOWED_HOSTS = [*], put your static ip here in place of  *.
iv.	If you have to change the names of the devices in AWS_IoT core, that can be done but those changes have to be reflected here in this file as the value of the SENSORS variable
SENSORS = {'Site01': {'inflow': 'D_InFlow01', 'outflow': 'D_OutFlow01', 'turbidity': 'D_Turbidity01', 'dissolvedoxygen': 'D_Oxygen01'}}
‘inflow’ is the prefix used for the table names and ‘D_InFlow01’ is the device name, if you wish to modify the table names or device names or add any new device in future make sure that entry is made here in this variable.
v.	Save the file now it is ready to be migrated to lightsail.
 
q.	How to put files on LightSail instance
i.	Open WinSCP (download it if not available)
ii.	Use similar process, put static ip in host name, username will be ‘bitnami’. Click on Advance and Authentication under SSH to add the .ppk file
iii.	Save the config and click on login. Left hand side will show your local directory and right hand side will be the lightsail instance. Make sure you are on the ‘/home/bitnami/apps’ folder of lightsail.
iv.	Create a folder with name ‘django’ in lightsail instance using the new option.
v.	Drag and drop the ‘slr_backend’ folder from your local directory to lightsail’s Django folder.
r.	Deploying the Django app on Lightsail
i.	Go to LightSail instance and navigate to ‘django’ folder
Run following commands one by one
(a)Run this commands one-by-one:
$ sudo apt-get update
$ sudo apt-get upgrade

(b)Next Check the python version :
$ python3 --version

(c)Next install python environment:
$ sudo apt-get install python3-venv
$ python3 -m venv env

(d)Now activate the environment:
$ source env/bin/activate

 (f)Install nginx service:
$ sudo apt-get install -y nginx

(g)Next install gunicorn:
$ pip3 install gunicorn

(h)Install django
$ pip3 install django

(i)Install supervisor
$ sudo apt-get install supervisor

(j)Go-to supervisor location
$ cd /etc/supervisor/conf.d/

(k)Now we can create and edit gunicorn configuration file using this commands with in the $ cd /etc/supervisor/conf.d/
$ sudo touch gunicorn.conf
$ sudo nano gunicorn.conf

(l)Here we can write the gunicorn program (paste as is)

[program:gunicorn]
directory=/home/bitnami/apps/django/slr_backend
command=/home/bitnami/apps/django/env/bin/gunicorn --workers 3 --bind unix:/home/bitnami/apps/django/slr_backend/app.sock slr_backend.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log
[group:guni]
programs:gunicorn


(m)Now create gunicorn file and check status:

$ sudo mkdir /var/log/gunicorn

$ sudo supervisorctl reread
Expected output: guni:avaliable

$ sudo supervisorctl update
Expected output: guni:added process group

$ sudo supervisorctl status
Expected output: guni:gunicorn  Running pid 11219, uptime 0:00:01



(n)Go-to nginx sites location

$ cd /etc/nginx/sites-available/

(o)create django configuration file edit the file

$ sudo touch django.conf
$ sudo nano django.conf

server{
listen 80;
server_name 3.16.31.127;
location / {
include proxy_params;
proxy_pass http://unix:/home/bitnami/apps/django/slr_backend/app.sock;
}
}

Note: Here server_name is STATIC ip address check your instance and copy paste over here in place of 3.16.31.127

(p)Next test the nginx service

$ sudo nginx -t
$ sudo ln django.conf /etc/nginx/sites-enabled/

(q)Finally restart the nginx service:
$ sudo service nginx restart


ii.	This will make sure the service is now running on the static ip. Go to the browser and enter your static ip of lightsail instance you will see the dashboard.
iii.	If there is no data. Run the push_dummy_data.py script to add some dummy data and see the results.

*The AWS cost can be further reduced down by having data for all the sensors stored in one table, but it will require code to be changed.
* Reach out to me @ rsargar@asu.edu in case any assistance in required.


