# docker/ — single-image deployment of the watcher stack

The `Dockerfile` and `docker-compose.yml` at the repository root build and run all three watcher tools (`wallet_watcher.py`, `farm_watcher.py`, `star_watcher.py`) as a single container. State is persisted to a Docker volume so the watchers always have a baseline to diff against between runs.

## Quick start

```bash
# 1. Generate a GitHub PAT (no scopes needed for public-repo monitoring)
#    https://github.com/settings/tokens → Generate new token (classic) → no scopes → Generate
# 2. Optional: set up a webhook
#    Slack:   https://api.slack.com/messaging/webhooks
#    Discord: server settings → Integrations → Webhooks
# 3. Configure
cp .env.example .env
$EDITOR .env       # set GITHUB_TOKEN and (optional) WEBHOOK_URL + WEBHOOK_KIND
# 4. Run
docker compose up -d
# 5. Tail logs (initial baseline takes ~3 minutes — wallet clones are largest)
docker compose logs -f farmwatch
```

## What runs inside

`supercronic` (a cron alternative built for containers — logs to stdout) executes the schedule from `docker/crontab`:

| Schedule | Watcher | Why this cadence |
|---|---|---|
| every 30 min | `wallet_watcher.py` | Highest priority — operators control the laundered crypto-wallet repos and could push malicious code at any time |
| every 15 min | `farm_watcher.py --skip-email-reach` | New farm repos appear within minutes of operator action |
| every 6 hours | `star_watcher.py` | Star spikes accumulate over hours; 6h is enough resolution |
| daily at 04:15 UTC | `farm_watcher.py` (full sock-puppet email sweep) | Slow (~5 min due to GitHub commit-search secondary rate limit), so once daily |

On container start, all three watchers run **once** to establish a baseline state, then supercronic takes over. The first run will not produce any alerts (no previous state to diff against); subsequent runs alert only on NEW findings.

## Webhook payloads

`run-and-alert.sh` posts to `$WEBHOOK_URL` only when a watcher exits with code 1 (= NEW findings since previous run). The payload format depends on `$WEBHOOK_KIND`:

**generic** (default):

```json
{
  "watcher": "wallet",
  "captured_at": "2026-04-26T03:30:00Z",
  "alerts": [
    {
      "repo": "luliguyu/dimatura",
      "head_changed": true,
      "previous_HEAD": "f4cb8d4...",
      "new_HEAD": "abcdef0...",
      "new_suspicious_eth": ["0xabcd...1234"],
      "new_suspicious_near": [],
      "critical_file_diffs": [...]
    }
  ]
}
```

**slack** — formats as a Slack `text` field with the JSON in a code block.

**discord** — formats as a Discord `content` field, capped at 1900 chars.

If you need a different format (PagerDuty, OpsGenie, Microsoft Teams, custom), edit `docker/run-and-alert.sh` — the case statement is one branch per format.

## Resource use

The container is small:
- ~100 MB image
- ~50 MB resident memory
- Outbound network only (GitHub API + git clones + webhook POSTs)
- ~50 MB state volume after a few weeks
- One CPU thread spends most of its time sleeping

The biggest disk consumer is the wallet clones inside `/state/wallets/` — about 30 MB combined for the four wallet repos (laundered + upstream × 2).

## Security model

- Container runs as **non-root** user `farmwatch` (UID 10001)
- No exposed ports — purely outbound
- The PAT in `$GITHUB_TOKEN` only needs read access to public repos (no scopes)
- State volume is owned by the non-root user
- `tini` is the PID 1, so signals (SIGTERM on `docker compose down`) propagate cleanly

## Operating it

**View current state:**

```bash
docker compose exec farmwatch cat /state/wallets/state.json | jq .
docker compose exec farmwatch cat /state/farm/state.json | jq .
docker compose exec farmwatch cat /state/stars/state.json | jq .
```

**Run a watcher manually:**

```bash
docker compose exec farmwatch python3 /opt/farmwatch/tools/wallet_watcher.py --workdir /state/wallets
```

**Reset baseline state (start fresh):**

```bash
docker compose down
docker volume rm public_farmwatch-state    # name may vary by compose-project name; check `docker volume ls`
docker compose up -d
```

**Update to a newer build of farmwatch (e.g. after pulling a new release):**

```bash
git pull
docker compose build --pull
docker compose up -d
```

**Test alert delivery without waiting for a real finding** — manually exit the watcher with code 1:

```bash
docker compose exec farmwatch sh -c '
  WORKDIR=/state/test
  mkdir -p $WORKDIR
  echo "{\"alerts\":[{\"kind\":\"test_alert\",\"detail\":\"this is a test\"}]}" > $WORKDIR/state.json
  WEBHOOK_URL="$WEBHOOK_URL" WEBHOOK_KIND="$WEBHOOK_KIND" \
    /opt/farmwatch/run-and-alert.sh test sh -c "exit 1"
'
```

## Failure modes

**GitHub rate-limit hit.** The container will log the error and the watcher exits with code 2. Supercronic will retry on the next scheduled run. The PAT in `$GITHUB_TOKEN` raises the unauthenticated 60/hour limit to 5,000/hour, which is enough for the 15-minute farm cadence.

**Operator deletes a watched repo.** `wallet_watcher` will fail to clone it (exit 2 from the cloned process); `farm_watcher` will record `"deleted_or_suspended": true` and emit an `account_disappeared` alert.

**Container crashes mid-run.** State files are written atomically (write to a temp file isn't currently implemented — the next iteration should add this). For now: if a watcher is killed mid-write, the state file may be truncated; the next run will treat it as "no previous state" and re-baseline silently. No false alerts.

**Webhook endpoint down.** The `curl` call in `run-and-alert.sh` is `|| true`-suppressed so a webhook failure doesn't kill the watcher run. The state file still records the alert; when the webhook comes back, the next run *won't* re-alert (state already updated). For high-stakes alerting (wallet integrity), pair the webhook with an out-of-band log-tail check.

## Deploying somewhere besides Docker

The watchers are plain Python with one dep (`requests`). Skip the container if you prefer:

```bash
pip install requests
crontab -e   # paste the schedule from docker/crontab, adjust paths
```

The `docker/run-and-alert.sh` wrapper works the same outside a container — just `chmod +x` and `bash run-and-alert.sh wallet python3 tools/wallet_watcher.py --workdir ./state/wallets`.

## Bumping schedules

Edit `docker/crontab`, rebuild, and restart:

```bash
$EDITOR docker/crontab
docker compose build && docker compose up -d
```

Don't go faster than 30 minutes on `wallet_watcher` (the clones take time), and don't skip the daily full-email-sweep on `farm_watcher` — that's the only path that catches *new operator accounts* surfacing for known sock-puppet emails.
