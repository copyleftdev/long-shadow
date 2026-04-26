# Disclosure contacts and short-form summaries

If you are a representative of one of these organizations, this page is for you. The full forensic case is in [../ARTICLE.md](../ARTICLE.md) and [../catalog/CATALOG.md](../catalog/CATALOG.md). The reproducible commands are in [../REPLAY.md](../REPLAY.md).

This documentation was published as the disclosure. The author has not separately notified you in advance — if that is preferred for any future investigation involving your project, please reach out via the public contact in this repo's main README.

## Allen Institute for AI — `allenai/WildDet3D`

**Short summary:** Your `WildDet3D` repository (created 2026-04-03, 505 stars) was cloned and republished as `luliguyu/WildDet3D` on **2026-04-07** — four days after your release. The fake repo preserves your researcher Weikai Huang's commits and `weikaih@allenai.org` author identity. The owner account `luliguyu` is part of a multi-account republishing farm based in China (Operator Cluster A in our taxonomy).

**Recommended action:**
1. Report the fake repo via [github.com/contact/dmca](https://github.com/contact/dmca) as a trademark / IP complaint, citing your authorship and the 4-day lag from official release.
2. Consider whether `Weikai Huang <weikaih@allenai.org>` would like Anthropic-style language posted to your README about provenance verification.

See: `data/enumeration/evidence_pack.txt`, `evidence/commit_history/luliguyu_WildDet3D.tsv`.

## Anthropic — `claude-code@anthropic.local` impersonation

**Short summary:** A separate operator cluster (Cluster B) is forging the author identity `Claude Code <claude-code@anthropic.local>` on commits across at least 8 GitHub repos. `anthropic.local` is not a real domain. The forge appears designed to make republished/laundered code appear as if Anthropic's Claude Code authored it. 23 commits identified; the actual reach is likely larger.

**Recommended action:**
1. Notify GitHub Trust & Safety with the `claude-code@anthropic.local` email pattern as an Anthropic impersonation signal.
2. Consider publishing guidance that Claude Code never sets `*.anthropic.local` as an author email — anyone seeing that pattern is observing a forge.

Affected repos identified: `CaMaGuee/invest.co.kr`, `esrfdev/ESRF-clean`, `gdhughey/CISTracker`, `jun564/jwcore-review`, `mctils12-arch/voltradeai`, `mearley24/AI-Server`, `rvadapally/PracticeX.App`, `vpneoterra/forge-ecs-platform`.

See: `data/enumeration/farm_b_c.txt`.

## Delby Intelligence (`delby.ai`, India) — full GitHub-org brand squat

**Short summary:** A GitHub organization named `DelbyIntelligence` (created 2026-04-03) has published **3,112 fake AI-product landing pages** under your brand, growing at ~140 repos per day. Each repo description begins "Delby AI Product:" and serves a static landing page on `delbyintelligence.github.io/{repo}/`. Your real company website (`delby.ai`) does not link to this org. The HTML's canonical URL points to a non-existent `delbyai.github.io/delby-agents/` GitHub Pages site that has never been indexed by Wayback Machine.

The operator account `delby-ai` was created **92 seconds before** the org. Operator activity hours and day-of-week pattern suggest a Chinese (or possibly Indian) night-owl operator, not your real team.

**Recommended action (high priority):**
1. **Trademark complaint** at [github.com/contact/dmca](https://github.com/contact/dmca) — citing 3,112-repo bulk impersonation. The naming pattern `Delby AI Product: …` and brand reference is unambiguous.
2. **Coordinate with GitHub Trust & Safety** for bulk org-level removal. The StarScout precedent (CMU/NCSU/Socket, ICSE 2026) achieved 90.4% removal of flagged repos.
3. **Check for related impersonations** — operators that scale to 3,112 repos in 22 days commonly run multiple squats in parallel.

See: `data/enumeration/delby_full.jsonl` (full list), `catalog/CATALOG.md` (Operator C section).

## The Quantum Resistant Ledger — `theQRL/zond-web3-wallet`

**Short summary:** Your wallet code was cloned and republished as `luliguyu/dimatura` (named after a real GitHub user `dimatura` for personal-fork camouflage). The laundered version is a snapshot from before your `Qrl* → Zond*` rename completed. We diffed the laundered repo against your upstream and **found no malicious modifications** — no payout-address tampering, no signing-logic changes. **However**, anyone who installs `luliguyu/dimatura` rather than `theQRL/zond-web3-wallet` runs a stale wallet missing your subsequent security fixes.

**Recommended action:**
1. DMCA complaint to [github.com/contact/dmca](https://github.com/contact/dmca) for the brand impersonation and personal-fork misrepresentation.
2. Consider publishing canonical-installation guidance pointing users at your verified releases.

See: `evidence/commit_history/luliguyu_dimatura.tsv`.

## Narwallets / NEAR Protocol — `Narwallets/narwallets-extension`

**Short summary:** Your extension was cloned **twice** — as `luliguyu/ssaavedrad` and `countneurooman/ssaavedrad`. Both repo names use the GitHub handle of one of your real contributors as personal-fork camouflage. The laundered manifests are at **version 4.0.3**; your upstream is at **4.0.7**. Same as the QRL Zond wallet finding: **no actively malicious modifications detected**, but the laundered versions are 4 minor versions behind your security fixes.

**Recommended action:**
1. DMCA complaint to GitHub for both fake forks.
2. Notify the real `ssaavedrad` user that their handle is being used as camouflage.

See: `evidence/commit_history/luliguyu_ssaavedrad.tsv`.

## yikart — `yikart/AiToEarn`

**Short summary:** Your `AiToEarn` content-monetization platform (9,765 stars) was republished as `kyasbalme/AiToEarn` (3,004 commits, preserving your contributor identities) and `tusmart-grouptt/AiToEarn`. Both fake repos are owned by accounts in our identified Operator A republishing farm.

**Recommended action:**
1. DMCA complaint to GitHub.
2. Note that the operator's own activity demonstrates familiarity with content-monetization automation as a revenue model — this is potentially a competitive-intelligence concern as well as a brand one.

## European Synchrotron Research Facility — `esrfdev` impersonation

**Short summary:** A user account named `esrfdev` (created 2026-04-12, same day as its first repo) published `esrfdev/ESRF-clean`. Your real `esrfdev` developer presence is potentially confusable with this fresh impersonation. The same operator forges `claude-code@anthropic.local` as the author identity (Cluster B).

**Recommended action:**
1. Trademark complaint to GitHub citing your prior use of `esrfdev` as an institutional account name.

## `blu3mo` (real Japanese researcher) — profile-website impersonation

**Short summary:** The `kyasbalme` GitHub account (created 2025-10-25, sock-puppet) lists `http://blu3mo.com/` as its profile website and claims bio "CS & Philosophy @ Columbia". This is the same account hosting the laundered Japanese Shogi-AI project at `kyasbalme/Scrapbox` — likely intentional misdirection toward your real identity.

**Recommended action:**
1. If you wish your identity removed from this account's profile, GitHub's impersonation policy applies: report at [github.com/contact/report-abuse](https://github.com/contact/report-abuse) → "Impersonation".

## iflytek, MemMachine, 53AI, aiflowy — your stars are inflated by the same bot service that promotes republishing farms

**Short summary:** A pool of at least 6 GitHub accounts that we identified as bot-stargazers has been starring your repositories alongside republishing-farm repos. The same accounts that starred `tusmart-grouptt/crewrktabletsn` (our identified Operator A farm) have also starred your highest-star repos — `iflytek/astron-agent` (8,780★), `53AI/53AIHub` (5,681★), `MemMachine/MemMachine` (3,534★), `aiflowy/aiflowy` (1,049★). At least one bot account (`8888x82`) has *forked* both `tusmart-grouptt/crewrktabletsn` (a farm repo) and `53AI/53AIHub` (your repo), giving direct evidence the same vendor serves both customer types.

**Recommended action (advisory):**
1. You may not have known. If you purchased the stars, the FTC 2024 final rule on fake social-influence indicators technically applies in US jurisdiction with penalties exceeding $50,000 per violation.
2. If you did *not* purchase the stars (and someone else is inflating your repo to make it look successful for some other reason), this is also worth knowing.
3. Consider publishing real engagement metrics (issue throughput, PR contributors, package downloads) instead of stars to anchor real growth.

See the bot stargazer enumeration in `data/enumeration/star_network.txt` and `data/enumeration/star_net_tier2.txt`.

## GitHub Trust & Safety — bulk evidence pack

**Bulk-removal request payload, ready to ship:**

| Cluster | Owner accounts | Repos | Suggested action |
|---|---|---|---|
| A | `kyasbalme`, `luliguyu`, `tusmart-grouptt`, `countneurooman` | 16 known farm repos | Suspension of fresh accounts; investigation of dormant ones |
| B | `CaMaGuee`, `esrfdev`, `gdhughey`, `jun564`, `mctils12-arch`, `mearley24`, `rvadapally`, `vpneoterra` | 8 farm repos | Action on Anthropic + ESRF impersonation; original-owner notification on dormant takeover |
| C | `delby-ai` (operator), `DelbyIntelligence` (org) | **3,112 fake brand-squat repos** | Bulk org removal as impersonation of `delby.ai` |
| D | `RPaez09l`, `tASDFG12345m`, `7228735902`, `superdaysk3wom`, `liiiiiii1i1i1`, `8888x82` (mapped subset; real pool larger) | n/a (these are starrers, not repo owners) | Account suspension for inauthentic activity |

**Reporting paths:**
- General abuse / impersonation: [github.com/contact/report-abuse](https://github.com/contact/report-abuse)
- Trademark / brand: [github.com/contact/dmca](https://github.com/contact/dmca)
- Bulk evidence: this entire repository

The full enumeration is in `catalog/operators.csv`, `catalog/farm_repos.csv`, `catalog/sock_puppet_emails.csv`.
