# tools/

Standalone Python tools. All zero-dependency or `pip install requests`-only. All MIT-licensed. Each is designed to run standalone or via cron.

## vet.py — heuristic detector for any GitHub repo

Runs the seven T0-adversarial heuristics on a single `owner/repo`. Returns score 0-7 + verdict (clean / suspect / T0-adversarial).

```bash
GITHUB_TOKEN=$(gh auth token) python3 vet.py owner/repo
GITHUB_TOKEN=$(gh auth token) python3 vet.py luliguyu/cmbd-book   # → 4/7 T0-adversarial
```

Add `--json` for machine-readable output.

The seven heuristics are the same ones described in `catalog/CATALOG.md` (T0 vetting). They were derived inductively from the Cluster A / B / C cases. A 4/7 score on `luliguyu/cmbd-book` was the validation.

False-positive risk: real maintainers who push from a single account, with imported history, will trigger 1-2 heuristics. The 3+ threshold is calibrated to exclude these. False-negative risk: an operator who fixes the obvious tells (rotates emails per repo, doesn't fabricate timestamps, opens PRs to themselves to defeat the no-PR heuristic) could pass the screen.

## wallet_watcher.py — periodic integrity check on the laundered crypto wallets

Operators (`luliguyu`, `countneurooman`) control `luliguyu/dimatura` (theQRL/zond-web3-wallet clone) and `luliguyu/ssaavedrad` (Narwallets/narwallets-extension clone). Today's snapshot is benign — but the operators could push malicious code at any time.

This watcher re-clones the laundered + upstream repos, extracts every ETH `0x...` and NEAR `*.near` address, and compares against:

1. The address allow-list at `evidence/wallet_addresses/baseline.txt` (captured 2026-04-25, all upstream-original test fixtures + well-known token contracts).
2. The current upstream version (re-cloned each run).

Any address in the laundered repo that is *not* in the allow-list AND *not* in the current upstream is flagged. Critical-file changes (manifest, signing/RPC/transaction code) are also reported.

```bash
python3 wallet_watcher.py --workdir /var/lib/farmwatch-wallets
python3 wallet_watcher.py --workdir /var/lib/farmwatch-wallets --json
python3 wallet_watcher.py --workdir /var/lib/farmwatch-wallets --webhook https://hooks.slack.com/...
```

State file: `<workdir>/state.json`. On second-and-subsequent runs, the script computes diffs against the previous state — only NEW suspicious findings are alerted.

Cron deployment (every 30 minutes, alert on diff via Slack):

```cron
*/30 * * * * /usr/bin/python3 /opt/farmwatch/tools/wallet_watcher.py \
  --workdir /var/lib/farmwatch-wallets \
  --webhook https://hooks.slack.com/services/XXX/YYY/ZZZ
```

Exit 0 = clean, 1 = NEW suspicious findings (alert), 2 = setup error.

## farm_watcher.py — periodic monitor for new farm activity

Watches every account in `catalog/operators.csv`:
- New repos appearing on a known operator account
- Account suspension/deletion (404 or list returns empty after being non-empty)
- DelbyIntelligence repo count growth (currently +140/day)

Optionally re-queries each sock-puppet email (from `catalog/sock_puppet_emails.csv`) against GitHub commit search. New owner accounts ever-appearing for a known sock-puppet email = a NEW operator account discovered.

```bash
GITHUB_TOKEN=$(gh auth token) python3 farm_watcher.py --workdir /var/lib/farmwatch
GITHUB_TOKEN=$(gh auth token) python3 farm_watcher.py --workdir /var/lib/farmwatch --skip-email-reach
GITHUB_TOKEN=$(gh auth token) python3 farm_watcher.py --workdir /var/lib/farmwatch --webhook https://...
```

The `--skip-email-reach` flag is important — the email-reach lookups are slow (35s sleep between queries to respect GitHub commit-search secondary rate limit). Skip them on frequent (e.g. every 15 min) runs and reserve them for daily ones.

## star_watcher.py — periodic monitor for the bot-star service

Watches every bot account in `catalog/operators.csv` (cluster D):
- New repos newly-starred by a known bot = candidate new customer of the star-buying service OR a new farm repo
- Bot account suspension/deletion

Watches every customer repo in `catalog/bot_star_customers.csv`:
- Star-count growth above `--star-spike-threshold` (default +50) between runs = fresh purchase signal

```bash
GITHUB_TOKEN=$(gh auth token) python3 star_watcher.py --workdir /var/lib/farmwatch-stars
GITHUB_TOKEN=$(gh auth token) python3 star_watcher.py --workdir /var/lib/farmwatch-stars --star-spike-threshold 100
```

## Suggested combined deployment

A single watcher host running all three monitors as cron jobs, posting to a single webhook:

```cron
# Wallet integrity (HIGHEST PRIORITY — operators control crypto wallet code)
*/30 *  * * * cd /opt/farmwatch && python3 tools/wallet_watcher.py --workdir state/wallets --webhook $WEBHOOK

# Operator-account changes (new repos, suspensions)
*/15 *  * * * cd /opt/farmwatch && GITHUB_TOKEN=$(cat /etc/gh-token) python3 tools/farm_watcher.py --workdir state/farm --skip-email-reach --webhook $WEBHOOK

# Bot-star activity + customer-star spikes
0 */6   * * * cd /opt/farmwatch && GITHUB_TOKEN=$(cat /etc/gh-token) python3 tools/star_watcher.py --workdir state/stars --webhook $WEBHOOK

# Full sock-puppet email reach (slow, daily)
15 4    * * * cd /opt/farmwatch && GITHUB_TOKEN=$(cat /etc/gh-token) python3 tools/farm_watcher.py --workdir state/farm --webhook $WEBHOOK
```

## License

All tools MIT-licensed.
