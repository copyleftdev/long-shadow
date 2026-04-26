# Replay — every command in execution order

This document gives the **exact reproducible commands** to verify every claim in the investigation. Each section names the corresponding evidence file (in `data/`) and the article section that depends on it.

> **Pre-requisites:** `gh` CLI authenticated to a GitHub account, `entropyx` (Rust crate, `cargo install entropyx`), `kraken` (`cargo install kraken-cli`), `vajra` (`cargo install vajra`), `jq`, `git`, `curl`, `dig`, `whois`, `sha256sum`. Set `export GITHUB_TOKEN=$(gh auth token)` before running anything that uses `kraken` or hits the GitHub REST API at scale.

> **Rate-limit note:** the GitHub commit-search API trips its secondary rate limit very fast — at ~5 calls per minute even sequentially. Every multi-call script below sleeps 30+ seconds between calls and runs in the background. Do not parallelise.

> **Dataset epoch:** every count in `data/manifests/co_authored_total_counts.json` and the pollution sample was captured **2026-04-25**. Re-running today will return higher counts — the operators have continued to push.

---

## 0 — Foundational: the search that started it

```bash
# Total count of GitHub commits with the Claude trailer (sets context for the whole investigation)
gh api -X GET search/commits -f q='"Co-Authored-By: Claude"' --jq '.total_count'
# → 9,905,060 as of 2026-04-25

# Top repos by author-date-desc — this is the search the farm exploits
gh api -X GET search/commits -f q='"Co-Authored-By: Claude"' \
  -f sort=author-date -f order=desc -f per_page=100 \
  --jq '[.items[].repository.full_name] | group_by(.) | map({repo: .[0], n: length}) | sort_by(-.n) | .[:20]'
# Top 2 results: kyasbalme/Scrapbox + luliguyu/cmbd-book — these are the farm
```

Other AI-tool signature counts captured (`data/manifests/co_authored_total_counts.json`):

```bash
gh api -X GET search/commits -f q='"Co-Authored-By: openhands"' --jq '.total_count'
gh api -X GET search/commits -f q='author:copilot-swe-agent[bot]' --jq '.total_count'
gh api -X GET search/commits -f q='author:devin-ai-integration[bot]' --jq '.total_count'
gh api -X GET search/commits -f q='"Generated with Cursor"' --jq '.total_count'
gh api -X GET search/commits -f q='"aider:"' --jq '.total_count'
```

---

## 1 — Verify the two top farm repos are byte-identical

Article §1, §2.

```bash
mkdir -p /tmp/farm-verify && cd /tmp/farm-verify
git clone --quiet https://github.com/kyasbalme/Scrapbox.git
git clone --quiet https://github.com/luliguyu/cmbd-book.git

# Diff: only README.md should differ
diff -rq --exclude=.git Scrapbox cmbd-book

# File-type histograms — should match exactly
for d in Scrapbox cmbd-book; do
  echo "=== $d ==="
  find $d -type f -not -path '*/\.git/*' | awk -F. '{print $NF}' | sort | uniq -c | sort -rn | head -10
done

# Lockfile size — should match to the byte
ls -la Scrapbox/poetry.lock cmbd-book/poetry.lock
```

Expected: `diff` reports only `README.md` differs. `poetry.lock` is exactly 256,748 bytes in both. `LICENSE` is 35,149 bytes in both. The two repos are byte-identical except for one byte in `README.md`.

**Evidence files**: `evidence/git_tree_sha/all_repos.tsv` shows the HEAD commit SHA and the *root tree SHA* of both repos at capture time — those are immutable Git references; if the repo content changes later, the tree SHA changes too.

---

## 2 — Verify date-fabrication

Article §1, §10.

```bash
cd /tmp/farm-verify/Scrapbox
# Spread: real history range → 2024 to 2037
git log --format='%ai' | sort | sed -n '1p;$p'
# Hour-of-day distribution — should be UNIFORM (no work-day clustering)
git log --format='%ai' | awk '{print substr($2,1,2)}' | sort | uniq -c
# Author timezone — every commit should be +0800 (operator's local clock leaked into fakes)
git log --format='%ai' | awk '{print $3}' | sort -u
# Far-future commits — these are how the farm gets to the top of sort:author-date-desc
git log --format='%H %ai' | awk '$2 > "2027-01-01"' | head -10
```

The `+0800` exclusivity across the entire history is the smoking gun for operator timezone (China / HK / Singapore).

---

## 3 — Cross-account attribution via shared sock-puppet emails

Article §2.

```bash
# Each sock-puppet email's full reach across GitHub
for e in BensonJennifer6145@outlook.com \
         DelacruzDawn1338@outlook.com \
         bmqx9295@163.com \
         naobingdz407945@163.com \
         kuqkz736@yeah.net \
         sbolr9514@yeah.net \
         io64083@yeah.net \
         czmahaixuan@126.com; do
  echo "=== $e ==="
  gh api -X GET search/commits -f q="author-email:$e" -f per_page=100 \
    --jq '{count: .total_count, owners: [.items[].repository.owner.login] | unique, repos: [.items[].repository.full_name] | unique}'
  sleep 33
done
```

**Smoking-gun result**: `bmqx9295@163.com` returns repos owned by *both* `luliguyu` AND `tusmart-grouptt`. Same email, two GitHub accounts. Same operator. Same logic for `naobingdz407945@163.com` linking `luliguyu` and `countneurooman`.

Captured in `data/enumeration/sockpuppet_reach.txt`.

---

## 4 — kraken behavioural fingerprint match

Article §2, §7.

```bash
export GITHUB_TOKEN=$(gh auth token)
mkdir -p /tmp/farm-kraken && cd /tmp/farm-kraken
kraken kyasbalme --depth 2 --max-repos 30 --max-commits 500 --max-users 100 -f json -o kyasbalme.json
kraken luliguyu --depth 2 --max-repos 30 --max-commits 500 --max-users 100 -f json -o luliguyu.json

# Compare the behavioural-fingerprint vectors
jq '.persons[0].fingerprint' kyasbalme.json
jq '.persons[0].fingerprint' luliguyu.json
```

Expected match across both vectors (to four decimals): `rhythm_period: 13.0`, `burst_rate: 0.0`, `star_concentration: 0.0`, `career_hops: 0`. This match is not about the underlying repos — it's a fingerprint of the *automation* doing the laundering.

Also reveals the `blu3mo.com` profile-website impersonation: `jq '.persons[0].profile.website' kyasbalme.json` → `"http://blu3mo.com/"`.

Saved at `data/kraken/{kyasbalme,luliguyu}.json`.

---

## 5 — entropyx forensic scan

Article §1, §7.

```bash
cd /tmp/farm-verify
entropyx scan ./Scrapbox > scrapbox.tq1.json
entropyx scan ./cmbd-book > cmbd-book.tq1.json

# Author entropy across all 156 files — should be 0.0 throughout (single sole author)
jq '[.files[].values[1]] | add / length' scrapbox.tq1.json   # → 0
jq '[.files[].values[1]] | add / length' cmbd-book.tq1.json  # → 0

# Per-metric mean comparison — should match closely between the two "different" repos
for m in 0 1 2 3 4 5 6 7; do
  s=$(jq "[.files[].values[$m]] | add / length" scrapbox.tq1.json)
  c=$(jq "[.files[].values[$m]] | add / length" cmbd-book.tq1.json)
  echo "metric $m: scrapbox=$s cmbd-book=$c"
done
```

Expected: `coupling_stress` mean = 0.2713 in both. `semantic_drift` mean = 0.0958 in both. Same vector across all 8 metrics to 3-4 decimals — entropyx confirms the repos are structurally identical.

Saved at `data/entropyx/{scrapbox,cmbd-book}.tq1.json`.

---

## 6 — Operator B (Anthropic-impersonation) enumeration

Article §3.

```bash
# Total commits with the Anthropic-impersonation forged author
gh api -X GET search/commits -f q='author-email:claude-code@anthropic.local' \
  --jq '{total: .total_count, repos: [.items[].repository.full_name] | unique}'
# → 23 commits across 8 distinct repos

# For each, confirm owner + creation date
for r in CaMaGuee/invest.co.kr \
         esrfdev/ESRF-clean \
         gdhughey/CISTracker \
         jun564/jwcore-review \
         mctils12-arch/voltradeai \
         mearley24/AI-Server \
         rvadapally/PracticeX.App \
         vpneoterra/forge-ecs-platform; do
  echo "=== $r ==="
  gh api repos/$r --jq '{full_name, created_at, pushed_at, fork, owner_type: .owner.type}'
  sleep 33
done

# Owner profile dates — mix of fresh-attacker and 2021/2022/2023 dormant-takeover
for u in CaMaGuee esrfdev gdhughey jun564 mctils12-arch mearley24 rvadapally vpneoterra; do
  gh api users/$u --jq '{login, created_at, public_repos, followers}'
  sleep 33
done
```

Captured in `data/enumeration/farm_b_c.txt`.

---

## 7 — Operator C (DelbyIntelligence) full enumeration

Article §4, §10.

```bash
mkdir -p /tmp/delby
out=/tmp/delby/delby_full.jsonl
: > "$out"
# 32 pages × 100 repos = 3,112 total
for p in $(seq 1 32); do
  gh api "orgs/DelbyIntelligence/repos?per_page=100&page=$p&sort=created&direction=desc" \
    --jq '.[] | {n: .name, c: .created_at, p: .pushed_at, s: .stargazers_count, l: .language, h: .has_pages, d: .description}' >> "$out"
  sleep 1.2
done
wc -l "$out"   # → 3112
```

Per-day creation curve:

```bash
jq -r '.c[:10]' "$out" | sort | uniq -c
```

Hour-of-day distribution (should be uniform across all 24 hours = automation):

```bash
jq -r '.c[11:13]' "$out" | sort | uniq -c
```

Day-of-week distribution (should show human work-week pattern with Sun trough):

```bash
jq -r '.c[:10]' "$out" | while read d; do date -d "$d" +%u; done | sort | uniq -c
```

Showcase repos that name specific targets (Cardinal Health, IIT Bombay, "viral-recruitm[ent]", "ai-lab-seed-agents-challenge-entry"):

```bash
jq -r 'select(.d != null) | "\(.n)\t\(.d[:80])"' "$out"
```

The `delby-ai` operator account (created 92 seconds before the org):

```bash
gh api users/delby-ai --jq '{login, created_at, public_repos, followers}'
gh api orgs/DelbyIntelligence --jq '{login, created_at, public_repos}'
# delby-ai created 2026-04-03T15:18:59Z
# DelbyIntelligence created 2026-04-03T15:20:31Z (92 seconds later)

# Operator's recent activity — confirms night-owl Asian timezone pattern
gh api 'users/delby-ai/events/public?per_page=100' \
  --jq '.[].created_at[11:13]' | sort | uniq -c
```

Captured in `data/enumeration/delby_full.jsonl`, `data/enumeration/delby_analysis.txt`.

---

## 8 — Brand-squat check vs the real Delby company

Article §4, §10.

```bash
# The real company is at delby.ai — separate infrastructure
dig +short delby.ai           # → 34.226.196.35 (AWS US-East-1)
whois delby.ai | grep -E 'Registrar:|Creation Date:|Registrant Org'
# → GoDaddy, Created 2025-09-08, Domains By Proxy

# The phantom canonical URL embedded in DelbyIntelligence's HTML
curl -s -A "Mozilla/5.0" \
  "https://delbyintelligence.github.io/product-choreograph-forge-multi-robot-coordinated-reaching/" | grep canonical
# → <link rel="canonical" href="https://delbyai.github.io/delby-agents/" />

# That canonical URL points to a GitHub user that DOES NOT EXIST
gh api users/delbyai 2>&1 | head -1  # → "Not Found" 404
curl -sI https://delbyai.github.io/                # → HTTP/2 404
curl -sI https://delbyai.github.io/delby-agents/   # → HTTP/2 404

# Wayback Machine confirms it was never archived
curl -s "http://archive.org/wayback/available?url=delbyai.github.io"
curl -s "http://archive.org/wayback/available?url=delbyai.github.io/delby-agents/"
# Both return: archived_snapshots: {}
```

The real Delby's website (`delby.ai`) makes **no mention** of GitHub anywhere. The `DelbyIntelligence` org has no description, no email, no website set. This is brand-squatting, not a corporate-owned account.

---

## 9 — Wallet integrity diff

Article §2 (Operator A) — confirms the laundered wallets are stale snapshots, NOT actively malicious modifications.

```bash
mkdir -p /tmp/wallet-check && cd /tmp/wallet-check
# Real upstreams
git clone --quiet https://github.com/theQRL/zond-web3-wallet.git
git clone --quiet https://github.com/Narwallets/narwallets-extension.git
# Laundered
git clone --quiet https://github.com/luliguyu/dimatura.git
git clone --quiet https://github.com/luliguyu/ssaavedrad.git

# QRL Zond wallet — file-level diff
diff -rq --exclude=.git zond-web3-wallet dimatura | head -30

# Narwallets — manifest version comparison (laundered = 4.0.3, upstream = 4.0.7 — STALE)
diff narwallets-extension/extension/manifest.json ssaavedrad/extension/manifest.json | head -10

# Critical-file content diff: any modified payout addresses or signing logic?
diff narwallets-extension/src/lib/near-api-lite/near-rpc.ts \
     ssaavedrad/src/lib/near-api-lite/near-rpc.ts | head -40
diff narwallets-extension/src/background/background.ts \
     ssaavedrad/src/background/background.ts | head -40
```

Expected: differences between upstream and laundered are time-based snapshots (older versions of the upstream code), NOT modified payout/signing logic. **The wallets are stale, not malicious.** But "stale wallet pretending to be current" is itself a security regression — anyone installing the laundered version misses upstream security fixes.

---

## 10 — Bot-star network mapping

Article §5.

```bash
# The 6 mapped bots — their starred-repo lists reveal customer base
for u in RPaez09l tASDFG12345m 7228735902 superdaysk3wom liiiiiii1i1i1 8888x82; do
  echo "=== $u profile ==="
  gh api users/$u --jq '{login, created_at, public_repos, followers, name, bio}'
  echo "=== $u starred repos (sample 30) ==="
  gh api "users/$u/starred?per_page=30" --jq '[.[] | .full_name]'
  sleep 33
done

# Cross-reference: which repos are starred by 4+ of 6 bots = customer base
# (run starred lists through your own intersection logic)

# Confirm the customer companies are real
for r in iflytek/astron-agent 53AI/53AIHub MemMachine/MemMachine aiflowy/aiflowy; do
  gh api repos/$r --jq '{full_name, stars: .stargazers_count, forks: .forks_count, homepage}'
  sleep 33
done

# Confirm fork inflation accompanies star inflation
for r in tusmart-grouptt/crewrktabletsn countneurooman/ssaavedrad mzbankl/ghaerrb \
         Brusselso/londonapa lenhyluo/xianmin zhoushisheng001b/Aziiizx \
         Galaxy-Dawn/claude-scholar; do
  gh api repos/$r --jq '"\(.full_name)\tstars=\(.stargazers_count)\tforks=\(.forks_count)"'
  sleep 33
done
```

Stargazer-list confirmation that 403/319 stars are bot-driven:

```bash
gh api 'repos/tusmart-grouptt/crewrktabletsn/stargazers?per_page=30' --jq '[.[] | .login]'
gh api 'repos/countneurooman/ssaavedrad/stargazers?per_page=30' --jq '[.[] | .login]'
# Both return random alphanumeric handles like tASDFG12345m, 7228735902, liiiiiii1i1i1, 8888x82
```

Captured in `data/enumeration/star_network.txt`, `star_net_tier2.txt`, `bot_expansion.txt`.

---

## 11 — Quantify pollution rate of the GitHub Claude-trailer search

Article §6.

```bash
out=/tmp/pollution_sample.jsonl
: > "$out"
for p in $(seq 1 10); do
  gh api -X GET search/commits -f q='"Co-Authored-By: Claude"' \
    -f sort=author-date -f order=desc -f per_page=100 -f page=$p \
    --jq '.items[] | {repo: .repository.full_name, owner: .repository.owner.login, sha: .sha, author_email: .commit.author.email, date: .commit.author.date}' >> "$out"
  sleep 5
done
echo "Total commits sampled: $(wc -l < $out)"
echo "Top farm repos:"
jq -r '.repo' "$out" | sort | uniq -c | sort -rn | head -5
```

Expected: 232 commits sampled. **100/232 (43%)** trace to `luliguyu/cmbd-book` (61) + `kyasbalme/Scrapbox` (39). All 30 sampled commits with `author-date > 2027` come from those same two repos.

Saved at `data/enumeration/pollution_sample.jsonl`.

---

## 12 — Verify hashes

```bash
cd /path/to/this/repo
sha256sum --check HASHES.txt
```

Every file in `data/`, `evidence/`, `catalog/`, plus `ARTICLE.md`, `METHODOLOGY.md`, and `CATALOG.md` is hashed. If any check fails, the file has been modified or corrupted since publication.
