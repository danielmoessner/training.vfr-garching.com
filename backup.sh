TODAY=`date +'%Y-%m-%d'`
FILENAME="/home/vfrgarching/tmp/backup/${TODAY}.sqlite3"
cp /home/vfrgarching/tmp/db.sqlite3 ${FILENAME}
echo $FILENAME
