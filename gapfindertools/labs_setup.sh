sudo apt-get -y install nginx uwsgi
sudo ln -s /srv/gapfindertools/gapfindertools/nginx.conf /etc/nginx/sites-enabled/gapfindertools.conf
cd /srv/gapfindertools
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py importmappings data/section_mappings.tsv
mkdir public
python manage.py collectstatic
deactivate
cp gapfindertools/gapfindertools.service /etc/systemd/system/multi-user.target.wants/
systemctl enable gapfindertools.service
systemctl daemon-reload
systemctl restart gapfindertools.service
systemctl restart nginx
