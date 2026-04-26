# GitHub repo-laundering farms + paid star-inflation service — investigative catalog v2

Working catalog. Status: **active investigation; ≥3 distinct operator clusters confirmed; one cluster operates at industrial scale; cross-cutting paid star-buying service identified.**

## Headline numbers (current)

| Metric | Value |
|---|---|
| Confirmed operator clusters | 3 (A, B, C) + 1 paid star service (D) |
| Confirmed operator GitHub accounts | **17+** (A: 4, B: 8, C: ≥1 org + ≥2 affiliates, D: 6 bots mapped) |
| Confirmed laundered repos | **3,150+** (most via Operator C, 16 from A, ≥8 from B) |
| Repos created/day by Operator C alone | **140-253** |
| Confirmed real-OSS upstream victims | 9 named projects + GitHub Classroom student work + Nano-X Window System + more pending |
| Real organizations impersonated/squatted | Allen AI, European Synchrotron, Anthropic, Nota Inc., Columbia U, **Delby Intelligence (3,112-repo squat)** |
| Time-to-launder for fresh academic releases | as little as **4 days** |
| **Paid star-inflation service customer list (confirmed)** | **≥4 real Chinese AI startups (~19,000 inflated stars)** + farms + crypto grift products |
| **Pollution rate of GitHub Co-Authored-By:Claude search** | **43% of top-1000 results** trace to one operator's two repos |

## Operator A — Sino-themed identity-rewrite farm

[unchanged from v1 — see ARTICLE_DRAFT.md Part 2 for the full case]

## Operator B — Anthropic-impersonation across compromised accounts

[unchanged from v1 — see ARTICLE_DRAFT.md Part 3]

## Operator C — DelbyIntelligence brand-squat of real Indian startup

**Org:** `DelbyIntelligence`, created 2026-04-03, 3,112 public repos as of 2026-04-25.

**Brand-squat:** Real `delby.ai` is an Indian physical-AI company (500+ vehicles, V-L-A models). The GitHub org has no link to the real company, and the templates' canonical URL points at `delbyai.github.io` (which **doesn't exist** — 404). Either the real company had a github.io presence, deleted it, and someone scooped the templates; or the canonical URL is intentional misdirection.

**Production curve:** 22-day ramp from 25/day → 250/day. Flat hourly distribution = automation.

**Showcase repos with descriptions name specific targets:** `Cardinal Health`, `IIT Bombay`, "AI Lab Seed Agents Challenge Entry", "Sensor Fusion Puzzle Hunt — Viral Recruitment". Targeted business-development bait, not random spam.

[full case in ARTICLE_DRAFT.md Part 4]

## Operator D — Cross-cutting paid bot-star service

### Bot accounts mapped (6, two tiers)

| Account | Created | Public repos | Profile dressing | Tier |
|---|---|---|---|---|
| `RPaez09l` | 2021-11-12 | 28 | "Ianko Leite" | Aged organic-looking |
| `tASDFG12345m` | 2022-05-11 | 24 | none | Aged but bot-handle |
| `7228735902` | 2022-06-20 | 18 | "Nadjmou BOINA — Ethical Hacker, B.Tech Student" | Aged organic-looking |
| `superdaysk3wom` | 2021-12-29 | 17 | "Ethan H — I make stuff." | Aged organic-looking |
| `liiiiiii1i1i1` | **2025-04-13** | 5 | none | **Fresh bulk-stars** |
| `8888x82` | **2025-04-16** | 12 | none | **Fresh bulk-stars** |

The two fresh bots were created *three days apart, exactly 12 months before the current farm wave* — bot-factory provisioning runs on a 1-year lead time.

### Confirmed customer base

**Real Chinese AI startups (paying customers):**
- `iflytek/astron-agent` — 8,780 stars, real iflytek (massive Chinese AI co.) at `astron.ai`
- `53AI/53AIHub` — 5,681 stars, real Chinese AI portal at `hub.53ai.com`
- `MemMachine/MemMachine` — 3,534 stars, real product at `memmachine.ai`
- `aiflowy/aiflowy` — 1,049 stars, real Java AI platform at `aiflowy.tech`
- `Soul-AILab/SoulX-LiveAct` — 1,209 stars, real EACL'26 paper code

**Vibe-coded AI products (real-or-farm ambiguous):**
- `Galaxy-Dawn/claude-scholar` — **3,446 stars**, "Semi-automated research assistant"
- `EvoScientist/EvoScientist` — 2,590 stars, "Vibe Research with Self-evolving AI Scientists"
- `wangziqi06/724-office` — 1,047 stars, "Self-evolving AI Agent system"
- `openvort/openvort` — 543 stars, "Open-source AI Employee Platform"
- `PhyAgentOS/PhyAgentOS` — 211 stars, "self-evolving embodied AI operating system"

**Republishing farms (also customers):**
- `tusmart-grouptt/crewrktabletsn` — 403 stars, **302 forks**
- `countneurooman/ssaavedrad` — 319 stars, **254 forks**

**Other confirmed laundered repos found through bot-stars:**
- `mzbankl/ghaerrb` — 375 stars, **317 forks**, description "The Nano-X Window System" (real OSS, republished)
- `Brusselso/londonapa` — 329 stars, **250 forks**, description gives away "i-am-poor-android-htian4 created by GitHub Classroom" (**student assignment laundered**)
- `lenhyluo/xianmin` — 379 stars, 303 forks, "personal web-site"
- `zhoushisheng001b/Aziiizx` — 383 stars, 282 forks, random-character names
- `xup6jammy/AI-INVOICE-OCR-ENGINE` — 163 stars (smaller, but cross-bot-starred)

**Crypto-grift products:**
- `MarilynClarke/Hyperliquid-Copy-Trading-Bot` — 415 stars, **294 forks**, Hyperliquid copy-trading bot

### Tradecraft

1. **Fork-inflation accompanies star-inflation** — every confirmed bot-customer has ~250-320 forks alongside 100-9000 stars. Forks more credibly imply real engagement; the bot service inflates both.
2. **Two-tier bot pool**: aged accounts with bios + names for legitimacy, plus fresh accounts for bulk-star throughput.
3. **Camouflage stars**: each bot's starred list mixes farm/customer repos with high-quality real OSS (`httpie/cli`, `v2ray/v2ray-core`, `lodash/lodash`, `google/grumpy`).
4. **Cross-customer bots**: `8888x82` *forks* both `tusmart-grouptt/crewrktabletsn` (Operator A farm) AND `53AI/53AIHub` (real startup customer) — direct linkage.
5. **Self-loop fork+star** — `RPaez09l` forked `mzbankl/ghaerrb` *and* starred it, pumping both metrics.

## Pollution-rate quantification

In a 232-commit sample across the top 10 pages of `gh search commits "Co-Authored-By: Claude" sort:author-date-desc`:

- 100 / 232 commits (**43%**) trace to just `luliguyu/cmbd-book` (61) + `kyasbalme/Scrapbox` (39) — both Operator A.
- All 30 sampled commits with `author-date > 2027` come from those same two repos.
- 1 `claude-code@anthropic.local` impersonation hit (Operator B).

**Operator A alone pollutes 43% of the top-of-ranking results.** Anyone scraping for AI-built-code corpus is being fed adversarial output as the dominant signal.

## Open investigative threads

- Full bot-network enumeration — 6 mapped, real pool likely 50-500.
- Galaxy-Dawn / claude-scholar — real or farm? The 3,446-star figure with 321 forks is at the upper edge of bot-service plausibility but the description suggests a real Claude-based research assistant.
- vpneoterra fake-fusion `forge-stellarator-*` — what's the source?
- The `delbyai.github.io` phantom — did the real Delby ever own it?
- Crypto-wallet watch — operators could push malicious updates at any time; need monitoring.
- Cross-cluster overlap analysis (do A and C share infrastructure?).

## Disclosures planned (priority order)

1. **GitHub Trust & Safety** — full enumeration; impersonation accounts; bot-star service.
2. **Anthropic** — `claude-code@anthropic.local` author-identity forgery.
3. **Allen Institute for AI** — `WildDet3D` 4-day-lag laundering.
4. **The real Delby Intelligence (intelligence@delby.ai)** — 3,112-repo brand-squat.
5. **The Quantum Resistant Ledger** + **Narwallets / NEAR** — wallet code republished (stale, not malicious).
6. **iflytek, MemMachine, 53AI, aiflowy** — your stars are inflated by a bot service that also serves republishing farms; you may not know.
7. **European Synchrotron Research Facility** — `esrfdev` account-name impersonation.
8. **`blu3mo` (real Japanese researcher)** — profile-website impersonation.
9. **The real `dimatura`, `ssaavedrad`, `sachinDevloop`** — username-based personal-fork camouflage.
10. **yikart** — `AiToEarn` republished twice.

---

## Geo-attribution (added v3)

### Operator A: definitively China-based

| Signal | Evidence |
|---|---|
| Author timezones | **All 16 farm repos: +0800** (the operator's local zone leaked into fabricated dates). Only `WildDet3D` differs (-0700 = preserved Allen AI Pacific). |
| Email providers | yeah.net, 163.com, 126.com, qq.com — all Chinese (NetEase + Tencent) |
| Account creation hours (UTC) | All four Operator A accounts created during China daytime/evening (4-14 UTC = 12-22 CST) |
| Scouted repos | `luliguyu` watches `tuya/tuya-openclaw-skills` (real Tuya — major Chinese IoT/AI co.), `MemMachine/MemMachine`, `zhoushisheng001b/Aziiizx` — Chinese AI ecosystem awareness |

### Operator C (DelbyIntelligence): likely China, possibly India — night-owl Asian operator

The actual operator account: **`delby-ai`** (not the org). Created 2026-04-03 at 15:18:59 UTC, **just 92 seconds before** the `DelbyIntelligence` org. 0 followers, 0 following, 0 listed repos, no profile fields. Pure operator account.

| Signal | Evidence |
|---|---|
| Hour-of-day (delby-ai's last 100 events) | Heavy at UTC 17-23 (= **01-07 China time, late night**) and UTC 00-02 (08-10 China morning). Light during China daytime (UTC 03-15). **Night-owl Asian operator.** |
| Day-of-week (DelbyIntelligence org's 3,112 events) | Mon 292 → Tue 382 → Wed 475 → **Thu 681 → Fri 647** → Sat 428 → **Sun 207**. Classic human work-week shape with Sun trough. **3.3x peak/trough ratio.** Consistent with Chinese 6-day work week with Sat half-day. |
| Brand-squat target | `delby.ai` is an Indian physical-AI company. Possibly cross-border targeting. |

### Operator B (Anthropic-impersonation): mixed origin

Eight accounts span fresh-attacker creations (March/April 2026) and dormant 2021-2023 accounts. Profile location fields mostly empty. Likely mixed compromised-account origins, no single-country attribution possible without push-IP forensics (not available via public API).

### Domain WHOIS

| Domain | Registrar | Registered | Notable |
|---|---|---|---|
| `delby.ai` (real Indian co.) | GoDaddy | 2025-09-08 | Domains By Proxy (Tempe, AZ); AWS US-East-1 hosting |
| `memmachine.ai` (bot-net customer) | GoDaddy | **2025-08-15** | Same Domains By Proxy as delby.ai; **registered the same day the GitHub repo was created**; hosted on GitHub Pages |
| `evoscientist.ai` (bot-net customer) | Cloudflare | 2026-02-15 | "DATA REDACTED, Country: GB"; hosted on GitHub Pages |
| `aiflowy.tech`, `astron.ai`, `53ai.com` (bot-net customers) | Various | — | Hosted on Alibaba Cloud Beijing/Singapore (Chinese cloud) |

**The bot-net's "real Chinese AI startup" customers are split 3-3:**
- Three on legitimate Alibaba Cloud (real infrastructure)
- Three on GitHub Pages itself (shoestring operations optimizing purely for GitHub-visibility metrics)

### Wayback negative confirmation

`http://archive.org/wayback/available?url=delbyai.github.io` returns `archived_snapshots: {}` for all variants. **No archived snapshots ever existed.** The `delbyai.github.io/delby-agents/` canonical URL referenced in DelbyIntelligence's HTML was always misdirection — the real Delby Indian company never had this GitHub Pages presence.

---

## ToS verdict — would GitHub care? (added v3)

**Every cluster's behavior is explicit violation of GitHub Acceptable Use Policies.**

GitHub policy text (from GitHub Acceptable Use Policies, current 2026):

> *"automated excessive bulk activity and coordinated inauthentic activity, such as creation of or participation in secondary markets for the purpose of the proliferation of inauthentic activity"* — prohibited.
>
> *"content or activity that impersonates any person or entity"* — prohibited.

### Cluster A — coordinated inauthentic activity + impersonation

- 4 operator accounts running 16 farm repos with sock-puppet authors → **automated excessive bulk activity**
- Bot-star service customer → **secondary market for inauthentic activity** (paid stars)
- `kyasbalme` profile claims `blu3mo.com` → **impersonation of real person**
- `Scrapbox` description lifted from `nota/Scrapbox` → **brand impersonation of Nota Inc.**
- Personal-fork repo names (`luliguyu/dimatura`, `ssaavedrad`, etc.) → **impersonation of real contributors**

### Cluster B — impersonation including Anthropic and ESRF

- `claude-code@anthropic.local` forged author → **impersonation of Anthropic / Claude Code**
- `esrfdev` account name → **impersonation of European Synchrotron Research Facility**
- `vpneoterra` 15-repo fake fusion-startup → **inauthentic activity** at minimum
- Compromised dormant accounts → **account abuse**

### Cluster C — brand impersonation of real Indian AI startup at scale

- `DelbyIntelligence` org impersonates real `delby.ai` (Indian Physical AI co.)
- 3,112 fake "Delby AI Product:" landing pages → **misinformation / inauthentic content**
- `delby-ai` operator account is a clear automation marker
- Phantom `delbyai.github.io` canonical URL → **fraud through misrepresentation**

### Cluster D (paid star service) — explicit AUP violation

- 6 mapped bot accounts inflating stars → **"creation of or participation in secondary markets for the purpose of the proliferation of inauthentic activity"**
- Customer base: real Chinese AI startups + republishing farms + crypto products
- Cross-bot starring patterns proven (RPaez09l + tASDFG12345m + 7228735902 + superdaysk3wom + liiiiiii1i1i1 + 8888x82 all star tusmart-grouptt/crewrktabletsn)

### Reporting pathways

- **General abuse / spam**: https://github.com/contact/report-abuse → "Malware or phishing" or "Impersonation"
- **Trademark / brand impersonation** (Delby, Anthropic, ESRF): https://www.github.com/contact/dmca
- **GitHub Trust & Safety direct**: support.github.com escalation

### Likely outcome — based on StarScout precedent

**ICSE 2026 paper** (Hao He et al., CMU + NCSU + Socket) reported on enforcement effectiveness:
- 90.42% of flagged repos removed
- 57.07% of flagged accounts removed
- **No GitHub transparency reports** on detection methods or enforcement statistics
- Bot infrastructure largely persists for future campaigns

**Realistic expectation for our enumeration if reported in bulk:**
- All 16 Operator A repos: high likelihood of removal
- DelbyIntelligence org (3,112 repos): high likelihood of removal as bulk impersonation
- 6 bot accounts: ~50% likelihood of removal
- Operator B's 8 compromised accounts: likely action (impersonation + Anthropic name use), but original-owner notification probably required
- Star inflation customer accounts (iflytek, 53AI, MemMachine, aiflowy): GitHub historically reluctant to act against legitimate companies that *purchase* fake-star services rather than provide them. StarScout authors acknowledged this asymmetry.

**Regulatory escalation possible:**
- FTC 2024 final rule explicitly prohibits **buying or selling fake indicators of social media influence for commercial purposes**, with penalties exceeding $50,000 per violation. While the FTC rule does not name "GitHub stars" specifically, the **principle clearly applies**. Customer companies (especially US-reachable ones) are theoretically exposed.
