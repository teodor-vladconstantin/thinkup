#!/bin/sh
# Pull latest main and rebuild containers only if something changed.
# Manual: ./deploy.sh    Force rebuild: ./deploy.sh --force
# Cron (daily 04:00):
#   0 4 * * * /root/thinkup/deploy.sh >> /var/log/thinkup-deploy.log 2>&1
set -e
cd "$(dirname "$0")"

before=$(git rev-parse HEAD)
git pull --ff-only
after=$(git rev-parse HEAD)

if [ "$before" = "$after" ] && [ "$1" != "--force" ]; then
    echo "$(date) no changes ($after)"
    exit 0
fi

echo "$(date) deploying $before -> $after"
cd platform-backend
docker compose up --build -d
# nginx caches container IPs at startup; recreated containers get new ones -> 502 without this
docker compose restart nginx
docker image prune -f
docker builder prune -f --keep-storage 2GB
echo "$(date) done"
