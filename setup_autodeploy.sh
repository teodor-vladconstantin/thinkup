#!/bin/sh
# One-time VPS setup for automatic deploys. Run on the server from the repo root:
#   sh setup_autodeploy.sh
# - creates an SSH key GitHub Actions uses to log in and run deploy.sh
# - adds a daily cron fallback (04:00)
# - prints the values to put in GitHub repo secrets
set -e
cd "$(dirname "$0")"
REPO=$(pwd)
KEY="$HOME/.ssh/thinkup_deploy"

chmod +x deploy.sh

# git pull must work without a password prompt
git pull --ff-only || { echo "git pull failed: set up a token (git config credential.helper store) or a deploy key first"; exit 1; }

mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"
[ -f "$KEY" ] || ssh-keygen -t ed25519 -N "" -C "github-actions-deploy" -f "$KEY"
grep -qF "$(cat "$KEY.pub")" "$HOME/.ssh/authorized_keys" 2>/dev/null || cat "$KEY.pub" >> "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"

CRON="0 4 * * * $REPO/deploy.sh >> /var/log/thinkup-deploy.log 2>&1"
( crontab -l 2>/dev/null | grep -vF "$REPO/deploy.sh"; echo "$CRON" ) | crontab -

echo
echo "=== GitHub > Settings > Secrets and variables > Actions ==="
echo "VPS_HOST    = $(curl -s https://api.ipify.org || hostname -I | cut -d' ' -f1)"
echo "VPS_USER    = $(whoami)"
echo "VPS_PATH    = $REPO"
echo "VPS_SSH_KEY = (everything below, including BEGIN/END lines)"
cat "$KEY"
