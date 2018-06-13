# gapfindertools
Research apps for Gapfinder

## Deploying to labs instance
1. Clone this repository to /srv/gapfindertools
2. Add a really long secret key to /etc/profile, e.g.:
   echo 'export DJANGO_SECRET_KEY="#)zbti_w!for_jack0xpefbi=&c@tsb2oua4j$e!djyhy&x9g7"'' | sudo tee --append /etc/profile
   source /etc/profile
3. Run /srv/gapfindertools/gapfindertools/labs_setup.sh
4. After each update you may want to collect static files depending on
   whether you've changed CSS and JS files:
   - cd /srv/gapfindertools
   - sudo venv/bin/python manage.py collectstatic --settings=gapfindertools.settings_prod

## How to create translations
1. cd sectionalignment
2. django-admin makemessages -l fr  # or some other language code
3. Edit sectionalignment/locale/fr/LC_MESSAGES/django.po
4. django-admin compilemessages

## How to edit translations
0. Edit files in sectionalignment/locale/...
1. cd sectionalignment
2. django-admin compilemessages

## TODO
1. Auto reload UWSGI after pulling new changes to the production server.
