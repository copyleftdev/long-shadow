# Methodology — how the investigation actually unfolded

This is the chronological account of how the investigation moved from *"build a small AI/human classifier corpus"* to *"three-cluster repo-laundering economy with a paid bot-star service serving real Chinese AI startups"*. Including the wrong turns.

## Phase 0 — the original (never-completed) experiment

**Hypothesis:** Three forensic tools (`entropyx` for git-history dynamics, `kraken` for GitHub identity-graph intelligence, `vajra` for structural triage) could distinguish AI-authored code from human-authored code on real GitHub repositories.

**Plan:**
1. Build a tier-stratified corpus from GitHub commit-search.
2. Tier 1 = SWE-bench paired AI-attempt + human-merged-fix datasets.
3. Tier 2 = repos with verifiable `Co-Authored-By:` trailers (Claude, OpenHands, Aider, Copilot Workspace).
4. Tier 3 = repos by GitHub-attested AI bot identities (`copilot-swe-agent[bot]`, `devin-ai-integration[bot]`).
5. Tier 4 = pre-2021-06 repos as pure-human control.
6. Run the three tools on each tier, look for distinguishing signatures.

Initial corpus assembly succeeded (`data/manifests/initial_corpus_manifest.jsonl` — 73 repos across 4 tiers). The trouble started when I picked the top two T2 candidates by commit count.

## Phase 1 — the smoking gun

**Top two `Co-Authored-By: Claude` repos by commit count, sorted by author-date-desc:**
- `kyasbalme/Scrapbox` (101 trailer commits)
- `luliguyu/cmbd-book` (101 trailer commits)

Both extend committer dates to **June 2037**. I was sceptical but cloned both anyway:

```bash
diff -rq --exclude=.git Scrapbox cmbd-book
# → only README.md differs
```

Of 156 files in each repo, only `README.md` differed by 1 byte. Same `poetry.lock` (256,748 bytes), same `LICENSE` (35,149 bytes), same everything. The two "different" repos by two "different" sock-puppet authors were the same Japanese Shogi-AI source, republished twice.

That's when the investigation pivoted from "build a corpus" to "trace this farm".

## Phase 2 — sock-puppet enumeration

The two visible authors (`BensonJennifer6145@outlook.com` and `DelacruzDawn1338@outlook.com`) followed the same generator pattern: `[A-Z][a-z]+[A-Z][a-z]+\d{3,4}@outlook\.com`. I queried each email's GitHub commit-search reach:

```bash
gh api -X GET search/commits -f q="author-email:bmqx9295@163.com" -f per_page=100 \
  --jq '{count, owners: [.items[].repository.owner.login] | unique}'
```

Smoking-gun result: `bmqx9295@163.com` returned commits across **two GitHub accounts** — `luliguyu` AND `tusmart-grouptt`. Same email, two owners. **Same operator behind both.** Repeat for `naobingdz407945@163.com` linking `luliguyu` and `countneurooman`. Now Cluster A had 4 confirmed accounts.

## Phase 3 — kraken cross-account fingerprint

`kraken` independently corroborated the cross-account attribution:

```bash
kraken kyasbalme --depth 2 --max-repos 30 -f json -o kyasbalme.json
kraken luliguyu --depth 2 --max-repos 30 -f json -o luliguyu.json
jq '.persons[0].fingerprint' kyasbalme.json luliguyu.json
```

Both fingerprint vectors matched to four decimals on `rhythm_period: 13.0`, `burst_rate: 0.0`, `star_concentration: 0.0`, `career_hops: 0`. Those values reflect the *automation* doing the laundering, not anything about the underlying repo content. Independent corroboration of operator identity.

`kraken` also surfaced what I'd missed by eye: `kyasbalme.profile.website = "http://blu3mo.com/"` — **a real Japanese researcher's homepage**. Operator A is impersonating a real person's website on the profile of one of their sock-puppet accounts.

## Phase 4 — "what does this email pattern reach beyond our 16 repos?"

Cross-referencing the 8 known sock-puppet emails against GitHub commit search revealed:
- `BensonJennifer6145@outlook.com` → 782 commits, 3 repos
- `DelacruzDawn1338@outlook.com` → 1,120 commits, 4 repos
- 4 of the 8 emails returned 0 results (commits exist locally in the cloned repos but GitHub's search index doesn't surface them, possibly because `yeah.net`/`126.com` are obscure providers)

This phase confirmed the operator's reach but didn't add new owner accounts. The next move that *did* add accounts was a structurally different query: `claude-code@anthropic.local`.

## Phase 5 — the second cluster

Sampling `Co-Authored-By: Claude` results across pages, I noticed one author email that didn't fit the Cluster A pattern: `Claude Code <claude-code@anthropic.local>`. `anthropic.local` is not a real domain. Anthropic's actual Claude Code does not author commits this way. Querying directly:

```bash
gh api -X GET search/commits -f q='author-email:claude-code@anthropic.local' \
  --jq '{total: .total_count, repos: [.items[].repository.full_name] | unique}'
# → 23 commits across 8 distinct repos under 8 distinct owner accounts
```

That's Cluster B. Mixed origin: some accounts are days old (`esrfdev` — same day as the laundered repo), some are 4-5 years old (`CaMaGuee`, `jun564`, `rvadapally` — likely compromised dormant accounts).

## Phase 6 — the third cluster, by accident

Searching for *other* WildDet3D clones (Operator A had laundered `allenai/WildDet3D` 4 days after release) returned `Silicon23/WildDet3D-data-demo`, `Silicon23/WildDet3D-model-comparison-demo`, `ToberJ/ToberJ-WildDet3D_in_your_pocket_souce_code`, and `DelbyIntelligence/demo-delby-wilddet3d-oracle-real-time-out-of-`. The last one was the lead.

```bash
gh api orgs/DelbyIntelligence --jq '{login, type, created_at, public_repos}'
# → {"login":"DelbyIntelligence","type":"Organization",
#    "created_at":"2026-04-03T15:20:31Z","public_repos":3112}
```

**3,112 public repos in 22 days.** That's Cluster C.

Full enumeration (32 pages × 100 repos):

```bash
for p in $(seq 1 32); do
  gh api "orgs/DelbyIntelligence/repos?per_page=100&page=$p&sort=created&direction=desc" \
    --jq '.[] | {n:.name, c:.created_at, ...}' >> delby_full.jsonl
  sleep 1.2
done
```

Aggregating: 87% have GitHub Pages enabled, 87% are HTML, 100% have zero stars, names follow `demo-{product}-{descriptors}` pattern truncated at GitHub's 100-char limit, and a few had giveaway substrings: `demo-sensor-fusion-puzzle-hunt-viral-recruitm` and `demo-ai-lab-seed-agents-challenge-entry-long-`.

## Phase 7 — the brand-squat

`delby.ai` turned out to be a **real Indian physical-AI startup** ("500+ vehicles, V-L-A models"). Their website doesn't link to a `DelbyIntelligence` GitHub org. The HTML inside `delbyintelligence.github.io/{repo}/` lists `<link rel="canonical" href="https://delbyai.github.io/delby-agents/" />` — a different account name.

```bash
gh api users/delbyai          # → 404
curl -sI https://delbyai.github.io/  # → HTTP/2 404
curl -s "http://archive.org/wayback/available?url=delbyai.github.io"
# → archived_snapshots: {} (Wayback never indexed it)
```

**Conclusion:** the canonical URL is misdirection. The real Indian Delby company never had this presence. The GitHub org is brand-squatting them.

## Phase 8 — the operator behind the org

Looking at the `actor` field in DelbyIntelligence's CreateEvents and PushEvents:

```bash
gh api 'orgs/DelbyIntelligence/events?per_page=20' --jq '.[] | "\(.actor.login)"'
# → all events: actor = "delby-ai"
```

**`delby-ai`** is a separate user account. Created **2026-04-03 at 15:18:59 UTC** — exactly **92 seconds before** the org. Empty everywhere (0 followers, 0 listed repos, no profile fields). It's the operator handle.

## Phase 9 — the bot-star service

The 403-star and 319-star repos under `tusmart-grouptt` and `countneurooman` (the two dormant Cluster A accounts) had wall-to-wall bot stargazers. Pulling 30 stargazers from each:

```bash
gh api 'repos/tusmart-grouptt/crewrktabletsn/stargazers?per_page=30' --jq '[.[] | .login]'
# → ["tASDFG12345m", "7228735902", "liiiiiii1i1i1", "8888x82", ...]
```

Mapping the *starred-repo lists* of these bots back outward (each bot stars ~30 repos, mostly real OSS for camouflage) revealed the high-frequency cross-bot targets:

| Customer repo | Stars | Bots/6 starred |
|---|---|---|
| `iflytek/astron-agent` | 8,780 | 4 |
| `53AI/53AIHub` | 5,681 | 5 |
| `MemMachine/MemMachine` | 3,534 | 5 |
| `aiflowy/aiflowy` | 1,049 | 4 |

These are **real Chinese AI startups** (verified via their homepages — `astron.ai`, `hub.53ai.com`, `memmachine.ai`, `aiflowy.tech`). The same bot pool that promotes Operator A's farm repos is the **paid customer base of real Chinese AI startups inflating their GitHub star counts**. Two customer types, one vendor.

## Phase 10 — quantifying pollution

Sampled 232 commits across 10 pages of `gh search commits "Co-Authored-By: Claude" sort:author-date-desc`. **100/232 (43%)** trace to just two repos (Operator A's). All 30 sampled commits with `author-date > 2027` come from those same two repos. Anyone scraping the obvious GitHub query for AI-built code is being fed adversarial output as the dominant signal.

## Phase 11 — geo-attribution

Cumulative evidence pointing to operator location:

**Operator A: definitively China.** All 16 farm repos use `+0800` author timezone (the operator's local clock leaked into the fabricated dates). All sock-puppet emails use Chinese free providers (yeah.net, 163.com, 126.com, qq.com). All four account creation times fall in China daytime/evening UTC ranges. `luliguyu` watches Tuya (Chinese IoT/AI), MemMachine, and farm repos like `zhoushisheng001b/Aziiizx`.

**Operator C: night-owl Asian operator.** `delby-ai`'s 100 most recent events concentrate at UTC 17-23 (= 01-07 China time, deep night) and UTC 00-02 (08-10 China morning). The org's 3,112 events show day-of-week distribution Mon 292 → Tue 382 → Wed 475 → **Thu 681 → Fri 647** → Sat 428 → **Sun 207** — a 3.3× peak/trough ratio matching a Chinese 6-day work week. Brand-squat target is Indian, but the operator's own schedule fingerprint reads China.

**Operator B: mixed origin.** Without push-IP forensics (not available via public API), we can't attribute.

## Phase 12 — wallet-integrity check

`luliguyu/dimatura` is a clone of `theQRL/zond-web3-wallet` (cryptocurrency wallet). `luliguyu/ssaavedrad` is a clone of `Narwallets/narwallets-extension` (NEAR Protocol wallet). The most consequential question was: did the operators **modify the wallets** to steal funds?

```bash
diff narwallets-extension/extension/manifest.json ssaavedrad/extension/manifest.json
# → laundered = version 4.0.3, upstream = version 4.0.7 — STALE
```

The differences across all critical files (manifest, near-rpc.ts, transaction.ts, background.ts) are **time-based snapshots** — the laundered wallets are older versions of the upstream code, not modified payout/signing logic. **Not actively malicious.** But "stale wallet code pretending to be current" is itself a security regression — anyone installing the laundered version misses upstream security fixes.

## Phase 13 — the StarScout context

The closest published precedent is **the ICSE 2026 paper *"Six Million (Suspected) Fake Stars on GitHub"*** by CMU + NCSU + Socket researchers, with their tool **StarScout**. Their findings:

- **6M fake stars across 18,617 repos by ~301,000 accounts** detected over 20TB of GitHub metadata.
- After they reported, GitHub removed **90.42%** of flagged repositories but only **57.07%** of flagged accounts. Bot infrastructure rotates faster than account suspensions.
- **Most repos with fake-star campaigns distribute MALWARE**, typically disguised as piracy tools, game cheats, or **cryptocurrency bots**.

Our `MarilynClarke/Hyperliquid-Copy-Trading-Bot` finding — a 415-star Hyperliquid copy-trading bot heavily promoted by the same bot pool that promotes our farm repos — is a textbook fit for the StarScout-identified profile. Our investigation extends the StarScout taxonomy with new categories: **AI-themed brand-squatting** (DelbyIntelligence), **academic-paper laundering** (Allen AI WildDet3D), and **Anthropic identity impersonation** (Cluster B).

## Tools, costs, and limits

| Tool | Role | Cost |
|---|---|---|
| `gh` CLI | All GitHub REST/GraphQL queries | Free; subject to secondary rate limits at ~5 calls/minute on commit search |
| `git log` / `diff -rq` / `git cat-file` | Forensic diffing of cloned repos | Free; bandwidth-bound on clone |
| `entropyx` | Tq1 forensic summary; metric vectors per file; `author_entropy=0` was the killer signal | Free; deterministic; runs locally; ~1-3 min per repo |
| `kraken` | Identity-graph spider; behavioural fingerprint vectors | Free with `GITHUB_TOKEN`; subject to GraphQL point quotas |
| `vajra` | Structural fingerprinting (queued for later expansion) | Free |
| Wayback Machine API | Confirming `delbyai.github.io` was never archived | Free; sometimes 503-throttled |
| `whois`, `dig` | Domain-registration triangulation | Free |

The investigation took roughly **one afternoon of forensic poking**. The shape of the operation came apart in the first 90 minutes; the rest was scope expansion and corroboration.

The hard limits we hit:
- GitHub commit-search secondary rate limit (~5 calls/minute even sequentially)
- Public GitHub API does not expose push-IP, so Operator B attribution remains incomplete
- Wayback Machine has no snapshots of `delbyai.github.io` (whether by never-existed or noindex)
- We sampled 30 stargazers per bot; the real bot pool is plausibly 50-500

## What I'd do differently

- **Hash every API response at capture time** with a timestamp (so the JSON in `data/enumeration/*.txt` would be reproducibility-grade rather than my-shell-history grade). Done partially via `evidence/git_tree_sha/all_repos.tsv` and the per-commit TSVs.
- **Set up a watcher** for the laundered crypto-wallet repos so we catch any future malicious push by the operators — they've shown they can modify the code; today's snapshot is benign, tomorrow's might not be.
- **Bot-pool expansion** — pull 100+ stargazers per identified customer repo to find the wider bot network (we mapped 6, real pool likely much bigger).
