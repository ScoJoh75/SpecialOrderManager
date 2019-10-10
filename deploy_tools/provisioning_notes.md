Provisioning a new Special Order Manager site

TL;DR

fab deploy:host=URL-or-IP --set wsgi_app=specialorders * -poof- you are done

System requirements
Any of the following are known to work: Ubuntu 18.04LTS

Required packages:
Python 3.6
virtualenv + pip
Git

sudo apt update
sudo apt install git python3.6 python3.6-venv python3.6-dev


Ningx Web Server
This will be installed automatically if not already in place

Nginx Virtual Host config
see nginx.template.conf
fabfile will install configuration if necessary
fabfile also removes the default Nginx site
Systemd service
see gunicorn-systemd.template.service
fabfile will install and configure service as necessary
Site specific items
intializes transaction log file if not present
ensures that settings.py is setup for deployment
pulls latest commit from git remote as called out in fabfile
sets up virtualenv and installs software from requirements.txt
migrations are completed and static files are copied
finally the required system services are restarted

Folder structure:
Assume we have a user account at /home/USER

/home/USER
└── sites
    └──SITENAME
       ├── database
       ├── source
       ├── static
       └── virtualenv