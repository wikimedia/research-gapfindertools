sudo apt-get -y install nginx uwsgi uwsgi-plugin-python3 mariadb-client python3-dev libmysqlclient-dev
sudo chown -R $USER /srv/gapfindertools/
cd /srv/gapfindertools
virtualenv -p $(which python3) venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=gapfindertools.settings_prod
python manage.py importmappings data/section_mappings.tsv --settings=gapfindertools.settings_prod
mkdir {public,media}
python manage.py collectstatic --settings=gapfindertools.settings_prod
deactivate
#sudo mkdir -p /var/log/uwsgi/app/
#sudo touch /var/log/uwsgi/app/gapfinder.log
#sudo chown www-data:www-data /var/log/uwsgi/app/gapfinder.log
sudo chown -R www-data:www-data /srv/gapfindertools/
sudo cp /srv/gapfindertools/gapfindertools/gapfindertools.service /etc/systemd/system/multi-user.target.wants/
sudo systemctl daemon-reload
sudo systemctl enable gapfindertools.service
sudo systemctl restart gapfindertools.service
sudo unlink /etc/nginx/sites-enabled/gapfindertools.conf
sudo ln -s /srv/gapfindertools/gapfindertools/nginx.conf /etc/nginx/sites-enabled/gapfindertools.conf
sudo systemctl restart nginx
