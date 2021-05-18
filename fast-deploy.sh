git reset --hard HEAD
git pull
tmp/venv/bin/python manage.py migrate
./permissions.sh
systemctl restart apache2
