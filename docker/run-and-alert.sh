#!/usr/bin/env bash
# run-and-alert.sh — wraps a watcher invocation, captures its output, and posts
# an alert to $WEBHOOK_URL when the watcher exits with code 1 (= NEW findings
# since previous run).
#
# Usage:  run-and-alert.sh <watcher-tag> <command...>
# Example: run-and-alert.sh wallet python3 tools/wallet_watcher.py --workdir /state/wallets
#
# Recognised webhook formats via $WEBHOOK_KIND:
#   generic  POST raw JSON body (default)
#   slack    POST {"text": "..."} to a Slack incoming-webhook URL
#   discord  POST {"content": "..."} to a Discord webhook URL

set -uo pipefail

WATCHER_TAG="${1:?watcher tag required (e.g. wallet|farm|stars|email)}"
shift

ts() { date -u +%FT%TZ; }

# Resolve the workdir from the args (--workdir /path)
WORKDIR=""
prev=""
for a in "$@"; do
  if [ "$prev" = "--workdir" ]; then WORKDIR="$a"; fi
  prev="$a"
done

echo
echo "[$(ts)] [$WATCHER_TAG] starting: $*"

# Run the watcher; capture its full stdout
LOG=$(mktemp)
"$@" >"$LOG" 2>&1
RC=$?

# Always echo the watcher's output to container stdout
cat "$LOG"
echo "[$(ts)] [$WATCHER_TAG] exit=$RC"

if [ $RC -eq 1 ] && [ -n "${WEBHOOK_URL:-}" ] && [ -n "$WORKDIR" ] && [ -f "$WORKDIR/state.json" ]; then
  ALERTS=$(python3 -c '
import json, sys
try:
    s = json.load(open(sys.argv[1]))
    print(json.dumps(s.get("alerts", []), indent=2))
except Exception as e:
    print("[]")
' "$WORKDIR/state.json")

  case "${WEBHOOK_KIND:-generic}" in
    slack)
      MSG=$(printf '%s' "$ALERTS" | head -c 3500)
      curl -sS -X POST -H "content-type: application/json" \
        -d "$(jq -nc --arg t "*[farmwatch:$WATCHER_TAG]* alerts at $(ts)" --arg b "$MSG" '{text: ("\($t)\n```\n\($b)\n```")}')" \
        "$WEBHOOK_URL" || true
      ;;
    discord)
      MSG=$(printf '%s' "$ALERTS" | head -c 1900)
      curl -sS -X POST -H "content-type: application/json" \
        -d "$(jq -nc --arg t "**[farmwatch:$WATCHER_TAG]** alerts at $(ts)" --arg b "$MSG" '{content: ("\($t)\n```json\n\($b)\n```")}')" \
        "$WEBHOOK_URL" || true
      ;;
    generic|*)
      curl -sS -X POST -H "content-type: application/json" \
        -d "$(jq -nc --arg watcher "$WATCHER_TAG" --arg captured_at "$(ts)" --argjson alerts "$ALERTS" '{watcher: $watcher, captured_at: $captured_at, alerts: $alerts}')" \
        "$WEBHOOK_URL" || true
      ;;
  esac
fi

rm -f "$LOG"
exit 0
