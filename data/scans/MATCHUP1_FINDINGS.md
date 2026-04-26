# Matchup 1 — Findings (preliminary, atom/atom scan still running)

## TL;DR

The two top "Co-Authored-By: Claude" repos by commit count on GitHub (`kyasbalme/Scrapbox` and `luliguyu/cmbd-book`, 101 trailer-matched commits each) are **not** organic AI-built code. They are products of a **search-ranking exploit**:

1. An attacker cloned a real Japanese Shogi-AI project (path-fingerprint `src/maou/...`) which itself happened to use Claude.
2. They preserved the original commit messages (including the Claude trailer) so the repos surface in `Co-Authored-By: Claude` searches.
3. They rewrote author identity to disposable `FirstnameLastname####@outlook.com` sock-puppets.
4. They scrambled both author and committer Unix timestamps uniformly across **2024 → 2037**, putting future-dated commits at the top of `sort:author-date-desc` results.
5. They published the result under throwaway GitHub user accounts created in October 2025 and pushed once, within 2 minutes of each other, on 2026-02-20.

**Implication for the experiment:** any "AI vs human" study that selects repos from raw GitHub commit-search results will be polluted by adversarial corpus at the top of the ranking. We need a vetting layer before any repo enters tiers T2/T3.

## The forensic case

### File-level identity

| Check | Scrapbox | cmbd-book |
|---|---|---|
| Files (excl `.git`) | 156 | 156 |
| Working-tree size | 3.9 MB | 3.9 MB |
| File-type histogram | 85 .py / 9 .md / 4 .csa / 3 .yml / 3 .txt / 3 .sh / 3 .pyi / 3 .npy / … | identical |
| `LICENSE` size | 35,149 B | 35,149 B |
| `poetry.lock` size | 256,748 B | 256,748 B (byte-identical) |
| `pyproject.toml` size | 2,880 B | 2,880 B |
| `AGENTS.md` size | 7,488 B | 7,488 B |
| `CLAUDE.md` size | 10,503 B | 10,503 B |
| `README.md` size | 2,254 B | 2,255 B |
| `diff -rq` (excl `.git`) | only `README.md` differs | — |

Every non-README file in both repos is byte-identical.

### Identity & ownership

| Field | Scrapbox | cmbd-book |
|---|---|---|
| Owner GitHub login | `kyasbalme` | `luliguyu` |
| Sole git author | `BensonJennifer6145@outlook.com` | `DelacruzDawn1338@outlook.com` |
| Author email pattern | `FirstnameLastname<4digits>@outlook.com` | same |
| Repo created | 2025-10-25 | 2025-10-21 (4 days apart) |
| Repo last pushed | 2026-02-20 22:51 UTC | 2026-02-20 22:53 UTC |
| Stars / forks | 0 / 0 | 0 / 0 |
| GitHub description | lifted from `nota/Scrapbox` (real wiki) | lifted from a Japanese textbook companion site |
| Author timezone | +0800 | +0800 |

### Git-history fabrication

| Check | Scrapbox | cmbd-book |
|---|---|---|
| Commit count | 625 | 623 |
| Author-date earliest | 2024-04-08 | 2024-04-07 |
| Author-date latest | 2037-06-01 | 2036-10-04 |
| Committer-date max | 2037-06-01 | 2036-10-04 |
| Distribution shape | uniform ~2 commits/day across 12 yrs | identical |

Real human commit cadence is bursty (work weeks, weekends, holidays, sprints). A clean uniform distribution across 12 years with ≤2 commits/day is the signature of a `git filter-branch`/`git replace`-style timestamp rewrite.

### Trailer camouflage

`git cat-file commit <sha>` shows the cloned commits **do** carry their original trailers — including dependabot Signed-off-by lines and the original author's `Co-Authored-By: Claude` trailers. The Claude trailer count (101 in each repo) is what they inherited from the upstream "maou" project, not anything they generated. The visible commit messages still mention Bumping `pytest 7.4.2 → 7.4.3` etc. — the artifact of a preserved upstream history.

### entropyx fingerprint identity

| Metric (mean over 156 files) | Scrapbox | cmbd-book |
|---|---|---|
| `change_density` | 0.0551 | 0.0550 |
| `author_entropy` | 0.0000 | 0.0000 |
| `temporal_volatility` | 0.3827 | 0.3772 |
| `coupling_stress` | 0.2713 | 0.2713 |
| `blame_youth` | 0.4292 | 0.4213 |
| `semantic_drift` | 0.0958 | 0.0958 |
| `test_cooevolution` | 0.6681 | 0.6687 |
| `composite` | 0.1390 | 0.1376 |

Event histogram:

| Event kind | Scrapbox | cmbd-book |
|---|---|---|
| `incident_aftershock` | 77 | 76 |
| `rename` | 24 | 24 |
| `hotspot` | 14 | 13 |

entropyx — a deterministic forensic instrument — produces near-identical fingerprints because the repos *are* near-identical. `author_entropy = 0.0` across every file confirms the single-author dominance.

## What this changes for the experiment

A new tier is needed at the top of the corpus hierarchy:

> **T0 — Adversarial / synthetic.** Repos engineered to surface in AI-attribution searches but not actually built by the claimed AI. Must be detected and excluded (or studied as a *separate* class — adversarial generation is its own research target).

Detection heuristics observed here, all cheap to compute:

1. Author-email matches `^[A-Z][a-z]+[A-Z][a-z]+\d{3,4}@outlook\.com$` (sock-puppet generator).
2. Sole author across the entire history (`author_entropy = 0` from entropyx).
3. Commit dates extending more than ~6 months past `repo.pushed_at` (fabricated future timestamps).
4. Uniform commit-rate distribution (no weekend/sprint/holiday troughs).
5. `repo.created_at - repo.pushed_at` window much shorter than apparent git history span.
6. Identical `poetry.lock` / `Cargo.lock` byte-size against an unrelated repo (template re-publish).
7. PR enrichment count == 0 despite hundreds of commits.

**Next-step recommendation:** add a `vet.py` step before each tier-{2,3} repo enters analysis. Reject any repo failing 3+ heuristics; re-tier-as-T0 anything failing 5+.

## Farm scope — confirmed industrial operation

Tracing the two sock-puppet emails reveals this is not two repos but a multi-repo farm:

| Sock-puppet email | Total commits | Owner account | Owner created | Public repos | Followers | Bio claim |
|---|---|---|---|---|---|---|
| `BensonJennifer6145@outlook.com` | 782 | `kyasbalme` | 2025-10-25 | 6 | 0 | "CS & Philosophy @ Columbia" (false-credibility text) |
| `DelacruzDawn1338@outlook.com` | 1,120 | `luliguyu` | 2025-10-21 | 10 | 1 | none |

`kyasbalme` repos: `AiToEarn`, `MMF`, `ojosama`, `robokssay`, `Scrapbox`, `vovo` — all 0 stars, all created on the same day (2025-10-25) except for two created later in 2025-11 / 2026-01.

`luliguyu` repos: `academ`, `cmbd-book`, `crewrktabletsn`, `dimatura`, `grammar_11`, `one-click`, `sachinDevloop`, `ssaavedrad`, `statbox2`, `WildDet3D` — all 0 stars; **most have `pushed_at` BEFORE `created_at`** (e.g. `academ` created 2026-02-25, pushed 2025-07-20). That is impossible from normal `git push` and indicates GitHub's *Import Repository* was used (which preserves source `pushed_at`).

The repo names map to *real* existing OSS projects — `ojosama` (jiro4989/ojosama, a Japanese text converter), `dimatura` (real robotics OSS contributor handle), `grammar_11`, `statbox2`, `sachinDevloop`. The farm imports real projects, rewrites author identity to a sock-puppet, scrambles commit timestamps, and re-publishes under fabricated owner accounts.

**16 repos confirmed across these two accounts. The same pattern almost certainly exists at scale across more sock-puppet pairs we have not yet enumerated.**

## Likely motivation

Three plausible drivers, in rough order of fit:

1. **GitHub-activity-gated incentives** — crypto airdrops, Web3 hackathon eligibility, dev-grant qualifying activity, "verified contributor" badges. The behaviour (many small repos, 0 stars, future-dated activity to signal recency) matches farms that exist to satisfy heuristic activity gates.
2. **Search-ranking exploit / reputation laundering for "AI-built code"** — putting these at the top of `Co-Authored-By: Claude sort:author-date-desc` search may be marketing or sandbagging for an AI tool, or training-data poisoning aimed at downstream classifiers.
3. **Career portfolio fabrication** — the false bio ("CS & Philosophy @ Columbia") supports the hypothesis that some of these accounts are intended to look hireable.

We cannot distinguish these without further attribution work (kraken would help — see next).

## Awaiting

- `atom/atom` entropyx scan (38,533 commits, ~8 min elapsed) — once complete, we will have the human-baseline metric distributions to contrast against the T0/AI distributions.

## Suggested follow-ups

1. **Run kraken** against `kyasbalme` and `luliguyu` to surface the wider sock-puppet network — co-temporal pairs, shared infrastructure (push IPs), behavioural clustering.
2. **Search GitHub** for the email pattern `[A-Z][a-z]+[A-Z][a-z]+\d{3,4}@outlook\.com` across recent commits to enumerate the full farm.
3. **Add a vetting layer** (`vet.py`) that auto-tiers any candidate repo into T0-adversarial when ≥3 of these heuristics hit:
   - sock-puppet author email pattern
   - `author_entropy = 0`
   - commit-date span > 5× (`pushed_at - created_at`)
   - uniform commit-rate distribution
   - `pushed_at < created_at`
   - identical lockfile size against an unrelated repo from the same account
   - 0 PR enrichments after >100 commits
4. **Re-rank T2** by re-running the original `Co-Authored-By: Claude` search but excluding repos that match the T0 heuristics. The "real" top-N AI-trailer repos are still in the corpus — they were just buried under farm output.
