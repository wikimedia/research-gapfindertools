# gapfindertools
Research apps for Gapfinder

## Deploying to labs instance
1. Clone this repository to /srv/gapfindertools
2. Add a really long secret key to /etc/profile, e.g.:
   echo 'export DJANGO_SECRET_KEY="#)zbti_w!for_jack0xpefbi=&c@tsb2oua4j$e!djyhy&x9g7"'' | sudo tee --append /etc/profile
   source /etc/profile
3. Run /srv/gapfindertools/gapfindertools/labs_setup.sh

