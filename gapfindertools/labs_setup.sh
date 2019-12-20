#!/bin/bash

sudo apt-get -y install nginx uwsgi uwsgi-plugin-python3 mariadb-client python3-dev libmariadbclient-dev python3-venv virtualenv python3-virtualenv python3-wheel
sudo chown -R $USER /srv/gapfindertools/
cd /srv/gapfindertools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python manage.py migrate --settings=gapfindertools.settings_prod
# sudo chmod ugo+rxw data/db.sqlite3
# enable this the first time only
#python manage.py importmappings data/section_mappings.xlsx --settings=gapfindertools.settings_prod
mkdir -p {public,media}
python manage.py collectstatic --settings=gapfindertools.settings_prod
deactivate
#sudo mkdir -p /var/log/uwsgi/app/
#sudo touch /var/log/uwsgi/app/gapfinder.log
#sudo chown www-data:www-data /var/log/uwsgi/app/gapfinder.log
sudo chown -R www-data:www-data /srv/gapfindertools/
# sudo chmod gou+rwx /srv/gapfindertools/data/db.sqlite3
sudo cp /srv/gapfindertools/gapfindertools/gapfindertools.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable gapfindertools.service
sudo systemctl restart gapfindertools.service
sudo unlink /etc/nginx/sites-enabled/gapfindertools.conf
sudo ln -s /srv/gapfindertools/gapfindertools/nginx.conf /etc/nginx/sites-enabled/gapfindertools.conf
sudo systemctl restart nginx
