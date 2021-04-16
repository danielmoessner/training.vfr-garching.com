chown -R root:www-data /home/training.vfr-garching.com
chmod -R 750 /home/training.vfr-garching.com
find /home/training.vfr-garching.com -type f -print0|xargs -0 chmod 740
chmod -R 770 /home/training.vfr-garching.com/tmp/media
find /home/training.vfr-garching.com/tmp/media -type f -print0|xargs -0 chmod 760
chmod 770 /home/training.vfr-garching.com/tmp/logs
chmod -R 760 /home/training.vfr-garching.com/tmp/logs/*
chmod 770 /home/training.vfr-garching.com/tmp
chmod -R 760 /home/training.vfr-garching.com/tmp/db.sqlite3
