chown -R root:www-data /home/vfrgarching
chmod -R 750 /home/vfrgarching
find /home/vfrgarching -type f -print0|xargs -0 chmod 740
chmod -R 770 /home/vfrgarching/tmp/media
find /home/vfrgarching/tmp/media -type f -print0|xargs -0 chmod 760
chmod 770 /home/vfrgarching/tmp/logs
chmod -R 760 /home/vfrgarching/tmp/logs/*
chmod 770 /home/vfrgarching/tmp
chmod -R 760 /home/vfrgarching/tmp/db.sqlite3
