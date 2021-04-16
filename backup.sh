TODAY=`date +'%Y-%m-%d'`
FILENAME="/home/training.vfr-garching.com/tmp/backup/${TODAY}.sqlite3"
cp /home/training.vfr-garching.com/tmp/db.sqlite3 ${FILENAME}
echo $FILENAME
