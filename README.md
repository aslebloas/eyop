# EYOP


## Deployment on UBUNTU

```
sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo apt-get install -y nginx
sudo pip3 install virtualenv
```

Install a firewall
```
sudo apt-get install ufw
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 8000
```

Download Repo
```
wget -P ~/ https://github.com/aslebloas/eyop/archive/master.zip
sudo apt-get install unzip
unzip ~/master.zip
mv ~/*-master ~/eyop
```

Install Dependencies
```
. venv/bin/activate
pip3 install -r eyop/requirements.txt 
```

Production configuration
In the settings.py file, change: 
`sed -i "s/DEBUG = True/DEBUG = False/" ~/eyop/referral_mate/referral_mate/settings.py`
`sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = ['35.199.23.20']/" ~/eyop/referral_mate/referral_mate/settings.py`
`sed -i "\$aSTATIC_ROOT = os.path.join(BASE_DIR, 'static')\n" ~/eyop/referral_mate/referral_mate/settings.py`


Install postgres
```
sudo apt-get install -y postgresql
sudo apt-get install -y postgresql-contrib
```