#!/usr/bin/env bash
# Container entrypoint: run all three watchers ONCE on startup (so we have a
# baseline state before the cron schedule kicks in), then hand control to
# supercronic for the recurring schedule.
set -euo pipefail

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "ERROR: GITHUB_TOKEN env var is not set. farm_watcher and star_watcher require it."
  exit 2
fi
export GITHUB_TOKEN

if [ -z "${WEBHOOK_URL:-}" ]; then
  echo "WARN: WEBHOOK_URL env var is not set. Alerts will print to stdout only."
fi

WEBHOOK_KIND="${WEBHOOK_KIND:-generic}"
echo "farmwatch starting at $(date -u +%FT%TZ)"
echo "  WEBHOOK_KIND  = $WEBHOOK_KIND   (generic | slack | discord)"
echo "  WEBHOOK_URL   = $([ -n "${WEBHOOK_URL:-}" ] && echo set || echo unset)"
echo "  state volume  = /state"
echo

# Initial baseline pass — exit codes from initial runs are intentionally ignored;
# they will always be exit 0 (no previous state to diff against, so nothing alerts).
echo "== initial baseline pass =="
/opt/farmwatch/run-and-alert.sh wallet python3 /opt/farmwatch/tools/wallet_watcher.py --workdir /state/wallets || true
/opt/farmwatch/run-and-alert.sh farm   python3 /opt/farmwatch/tools/farm_watcher.py   --workdir /state/farm   --skip-email-reach || true
/opt/farmwatch/run-and-alert.sh stars  python3 /opt/farmwatch/tools/star_watcher.py   --workdir /state/stars  || true
echo
echo "== initial baseline complete; entering supercronic schedule =="

exec /usr/local/bin/supercronic /opt/farmwatch/crontab
