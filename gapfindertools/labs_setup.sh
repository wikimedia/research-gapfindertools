sudo apt-get -y install nginx uwsgi uwsgi-plugin-python3
sudo chown -R www-data:www-data /srv/gapfindertools/
sudo ln -s /srv/gapfindertools/gapfindertools/nginx.conf /etc/nginx/sites-enabled/gapfindertools.conf
sudo su -s /bin/bash www-data
cd /srv/gapfindertools
virtualenv -p $(which python3) venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py importmappings data/section_mappings.tsv
mkdir {public,media}
python manage.py collectstatic
deactivate
exit
sudo mkdir -p /var/log/uwsgi/app/
sudo touch /var/log/uwsgi/app/gapfinder.log
sudo chown www-data:www-data /var/log/uwsgi/app/gapfinder.log
sudo cp /srv/gapfindertools/gapfindertools/gapfindertools.service /etc/systemd/system/multi-user.target.wants/
sudo systemctl daemon-reload
sudo systemctl enable gapfindertools.service
systemctl restart gapfindertools.service
systemctl restart nginx
