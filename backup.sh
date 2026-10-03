#!/bin/sh
# Daily backup: database (typed JSON, via the backend container) + uploaded files.
# Cron (daily 03:30, before the 04:00 deploy):
#   30 3 * * * /root/thinkup/backup.sh >> /var/log/thinkup-backup.log 2>&1
# Restore DB:    gunzip -c db-<stamp>.json.gz | docker exec -i thinkup-app python scripts/backup_db.py restore
#   (add --suffix -restored to restore into copies of the tables and inspect them first)
# Restore files: tar xzf files-<stamp>.tar.gz -C /root/thinkup/platform-backend
set -e
DIR=${BACKUP_DIR:-/root/thinkup-backups}
DB_KEEP_DAYS=${DB_KEEP_DAYS:-30}
FILES_KEEP_DAYS=${FILES_KEEP_DAYS:-7}
stamp=$(date +%F-%H%M)
mkdir -p "$DIR"
cd "$(dirname "$0")/platform-backend"

# Write to a temp file first so a failed dump never replaces a good backup
docker exec thinkup-app python scripts/backup_db.py dump > "$DIR/db-$stamp.json.tmp"
gzip "$DIR/db-$stamp.json.tmp"
mv "$DIR/db-$stamp.json.tmp.gz" "$DIR/db-$stamp.json.gz"

tar czf "$DIR/files-$stamp.tar.gz.tmp" local_storage
mv "$DIR/files-$stamp.tar.gz.tmp" "$DIR/files-$stamp.tar.gz"

find "$DIR" -name 'db-*.json.gz' -mtime +"$DB_KEEP_DAYS" -delete
find "$DIR" -name 'files-*.tar.gz' -mtime +"$FILES_KEEP_DAYS" -delete
find "$DIR" -name '*.tmp*' -mtime +1 -delete
echo "$(date) backup ok: $(du -sh "$DIR" | cut -f1) in $DIR"
