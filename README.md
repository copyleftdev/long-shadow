# Operation Long Shadow

> *I went looking for AI-built code on GitHub. I found a farm.*

[![Codename](https://img.shields.io/badge/codename-Long_Shadow-1f1f1f)](ARTICLE.md)
[![Replay](https://img.shields.io/badge/replay-REPLAY.md-blue)](REPLAY.md)
[![Article](https://img.shields.io/badge/article-ARTICLE.md-green)](ARTICLE.md)
[![Methodology](https://img.shields.io/badge/methodology-METHODOLOGY.md-orange)](METHODOLOGY.md)
[![Hashes](https://img.shields.io/badge/integrity-HASHES.txt-red)](HASHES.txt)

**Long Shadow** is the codename for a four-cluster GitHub repo-laundering operation that buries fabricated commits in 2037 to bubble laundered repos to the top of every AI-built-code search. This repository documents the investigation: a 3,112-repo brand-squat of a real Indian AI startup, real-time IP theft of an Allen Institute for AI paper, two republished cryptocurrency wallets, and a paid bot-star service inflating real Chinese AI startups alongside it.

The name comes from the operators' signature trick — every Long Shadow repo casts forward-dated commits into the future, the longest reaching **June 2037**, eleven years past the day this report was written.

**All raw data is in this repository. Every claim has a corresponding command in [REPLAY.md](REPLAY.md) and a hash in [HASHES.txt](HASHES.txt) for verification.**

---

## TL;DR (numbers as of capture date 2026-04-25)

| Metric | Value |
|---|---|
| Distinct operator clusters confirmed | **4** (A, B, C + D paid star service) |
| Confirmed operator GitHub accounts | **17+** (4 + 8 + 1 org + 6 bots, plus the `delby-ai` operator) |
| Laundered repos confirmed | **3,150+** (3,112 from one operator alone) |
| Sock-puppet author emails identified | **9** distinct identities, 5 provider patterns |
| Confirmed real-OSS upstream victims | **9 named projects** + GitHub Classroom student work + Nano-X Window System + 2 crypto wallets |
| Real organizations impersonated | Allen AI, European Synchrotron, Anthropic, Nota Inc., Columbia U, **Delby Intelligence (full brand-squat)** |
| Time-to-launder for fresh academic releases | as little as **4 days** |
| Pollution rate of GitHub `Co-Authored-By: Claude` search top-1000 | **43%** trace to one operator's two repos |
| Bot-star service customers (real Chinese AI startups) | **≥4 startups, ~19,000 inflated stars combined** |

## What you'll find here

```
long-shadow/
├── README.md                            (this file)
├── ARTICLE.md                           publication-ready investigative draft
├── METHODOLOGY.md                       how the investigation actually unfolded
├── REPLAY.md                            every reproduction command, in execution order
├── HASHES.txt                           sha256sum of every artifact
├── docs/index.html                      single-file kinetic data-viz long-read
├── catalog/
│   ├── CATALOG.md                       full evidentiary catalog
│   ├── operators.csv                    every confirmed operator account, one per row
│   ├── farm_repos.csv                   16 farm repos with HEAD SHA + tree SHA + commit count + upstream
│   ├── sock_puppet_emails.csv           9 sock-puppet emails with reach across GitHub
│   ├── upstream_victims.csv             every real OSS / company impersonation victim
│   └── bot_star_customers.csv           paid star-service customer list
├── data/
│   ├── manifests/                       raw count manifests
│   ├── enumeration/                     all GitHub-search enumeration outputs (raw)
│   ├── kraken/                          kraken JSON outputs for both Operator A seeds
│   ├── entropyx/                        entropyx tq1 scans of both top-2 farm repos
│   └── scans/                           entropyx-derived findings
├── evidence/
│   ├── git_tree_sha/all_repos.tsv       immutable HEAD + tree SHAs at capture time
│   └── commit_history/                  per-repo TSV: SHA, dates, author, subject (6,503 commits)
├── disclosures/                         drafted notification emails to affected parties
├── scripts/                             reproduction shell scripts (paced for rate limits)
└── tools/
    └── vet.py                           heuristic detector for repo-laundering signatures
```

## Reproducing the findings

Most reproduction is a single `gh api ...` or `git clone ... && diff -rq ...` away. See [REPLAY.md](REPLAY.md) for the exact commands in execution order.

The forensic tools used:
- **`entropyx`** (Rust) — temporal/structural/authorship dynamics for git history
- **`kraken`** (Rust) — GitHub identity-graph intelligence via GraphQL
- **`vajra`** (Rust) — structural triage of JSON data
- **`gh`** CLI + `git log` + `diff -rq` did most of the load-bearing work

## Verifying integrity

Every file in `data/`, `evidence/`, `catalog/`, `disclosures/`, plus the markdown documents at the root, is hashed in `HASHES.txt`. Verify:

```bash
sha256sum --check HASHES.txt
```

If a file's hash doesn't match, the file has been modified since publication. The TSVs in `evidence/commit_history/` reference *immutable Git commit SHAs* — even if the operators delete their repos, the SHAs in our evidence will match any other clone made before deletion.

## Try the tools

**Detect a single repo** with the seven-heuristic scorer:

```bash
GITHUB_TOKEN=$(gh auth token) python3 tools/vet.py luliguyu/cmbd-book
# Verdict: T0-adversarial  (score 4/7)
```

**Watch the laundered crypto wallets** for malicious modifications (operators control the repos and could push harmful changes any time):

```bash
python3 tools/wallet_watcher.py --workdir /var/lib/farmwatch-wallets
# Diffs current laundered repos against allow-list + current upstream.
# Exit 1 = NEW suspicious findings since previous run.
```

**Watch the operator accounts** for new farm activity:

```bash
GITHUB_TOKEN=$(gh auth token) python3 tools/farm_watcher.py --workdir /var/lib/farmwatch
# Snapshots every operator account's repo list; alerts on new repos and account suspensions.
```

**Watch the bot-star service** for new customers:

```bash
GITHUB_TOKEN=$(gh auth token) python3 tools/star_watcher.py --workdir /var/lib/farmwatch-stars
# Tracks bot-account starring activity + customer-repo star spikes.
```

All four tools are zero-dependency or `pip install requests`-only. Designed for cron deployment with webhook alerts. See [tools/README.md](tools/README.md) for the full operator playbook.

**One-command continuous monitoring** via Docker Compose:

```bash
cp .env.example .env
$EDITOR .env                     # set GITHUB_TOKEN + (optional) WEBHOOK_URL
docker compose up -d
docker compose logs -f farmwatch
```

The container runs all three watchers on the recommended schedule (`docker/crontab`), persists state across restarts, and posts alerts to Slack / Discord / a generic JSON webhook when new findings appear. Full deployment guide in [docker/README.md](docker/README.md).

## Disclosure status

Draft notification emails to all named affected parties live in [disclosures/](disclosures/). They had not been sent at the time this repo was first published — the publication itself is the disclosure. If you are a representative of any of the affected organizations, jump to [disclosures/CONTACTS.md](disclosures/CONTACTS.md) for the recommended action and a short-form summary of what we found about your project.

## Affected parties named in this report

Real-organization impersonations / IP theft (in priority order):

- **Allen Institute for AI** — `allenai/WildDet3D` cloned 4 days after release as `luliguyu/WildDet3D`
- **Anthropic** — `claude-code@anthropic.local` forged author identity across 8 Cluster B repos
- **The Quantum Resistant Ledger** — `theQRL/zond-web3-wallet` republished as `luliguyu/dimatura`
- **Narwallets / NEAR** — `narwallets-extension` republished twice (stale, not actively malicious)
- **yikart** — `AiToEarn` republished by `kyasbalme` and `tusmart-grouptt`
- **Delby Intelligence** (real Indian Physical AI co. at delby.ai) — 3,112-repo brand-squat by `DelbyIntelligence` GitHub org
- **European Synchrotron Research Facility** — `esrfdev` GitHub account name impersonation
- **`blu3mo`** (real Japanese researcher) — profile-website impersonation by `kyasbalme`
- **Real `dimatura`, `ssaavedrad`, `sachinDevloop`** GitHub users — repo-name personal-fork camouflage
- **iflytek, MemMachine, 53AI, aiflowy** — your stars are inflated by a bot service that also serves republishing farms; you may not have known
- **GitHub Trust & Safety** — bulk evidence pack available

## License & ethics

All forensic evidence captured from public GitHub APIs and public Git histories. No private data accessed, no exploits performed against any system. Operator account names and bot account handles are reproduced verbatim because they are themselves public GitHub usernames; we do not name any private individual whose identity we cannot verify.

If you operate one of the named accounts and believe you have been misidentified, contact us with corroborating evidence — corrections will be issued.

This documentation is released **CC-BY-4.0**. The `vet.py` tool is **MIT licensed**.

## Acknowledgements

- The **StarScout** team (Hao He, Haoqin Yang, Philipp Burckhardt, Alexandros Kapravelos, Bogdan Vasilescu, Christian Kästner — CMU + NCSU + Socket) for their ICSE 2026 paper *"Six Million (Suspected) Fake Stars on GitHub"*. Our investigation builds on their methodology and their fake-star-account taxonomy. [github.com/hehao98/StarScout](https://github.com/hehao98/StarScout)
- Anthropic's Claude assistant supported the forensic synthesis. The investigation itself, all command construction, and all forensic interpretation are the author's.
