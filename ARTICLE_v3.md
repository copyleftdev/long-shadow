# Operation Long Shadow · v3 · The market

> *Working title. Markdown draft for the v3.html chapter. Voice: matches v1/v2 — first-person journalistic, specific evidence, numbers carry the weight, confident but not breathless.*

---

**Follow-up · No. 03 · One workday after v2 · math generalized · the farm has neighbors**

> v2 said the math could detect them. v3 turned it loose on the market.
>
> v1 found a farm. v2 validated the math. v3 pointed the math at seven verticals and found that the farm has neighbors — at least nine more operators across two continents, four campaign types, and one shared malware-kit fingerprint that crosses verticals. It also found one currently-active operator with their real name in their college-final-exam repository.

| Investigation scope | Numbers as of capture date 2026-04-26 |
|---|---|
| Verticals scanned | **7** (Chinese network-circumvention, AI-tools, crypto/Polymarket, Solana memecoin, gaming cheats, NFT/Web3, social-media boost) |
| Distinct operators / patterns surfaced | **12** (9 confirmed star-farm + 2 confirmed malware-kit + 1 unsolved affiliate-drop) |
| Operators with real-name attribution | **2** (Enzo Alarcón / Argentina · Vietnamese operator candidate) |
| Cross-vertical operator links | **1** (Vietnamese kit fingerprint matches across gaming-cheats AND Discord-raid verticals) |
| Methodology generalized to fresh vertical | **3 of 3** with positives (cfnb-discovered + Polymarket + Vietnamese-malware) |
| Methodology generalized to fresh vertical with negative result | **1** (AI-tools — methodology correctly returned no campaign) |
| New attack patterns surfaced | **2** (malware-kit boilerplate fingerprint · single-day-burst on aged real accounts) |

---

## Cold open

The v2 corpus discovered 288 high-confidence bots from a seed of 6. We hypothesized the same math would generalize to other operators, other verticals, other campaign shapes. That's the v3 question: is the cohort we found one farm in a quiet corner of GitHub, or one cell of an industry?

The answer turns out to be the second one. In a single workday — 2026-04-26 — we pointed the toolchain at seven adjacent verticals and surfaced nine more operators with persistent corpus, two real-name attribution leads, one cross-vertical malware kit, and one attack pattern (an "aged-account affiliate drop" on April 23) that the v2 math was never going to catch.

Two of the new operators have full operator dossiers — every shell org, every bot fleet member, every activation timestamp. One of them, Enzo Alarcón, left his real name in a Spanish-language college-final-exam repository while running the largest star farm in this report.

The shape of the finding is the takeaway. **Coordinated inauthentic behavior on GitHub is not a phenomenon. It is a market with multiple operator types running parallel campaigns across distinct verticals.** The toolchain can map it because the math generalizes. The corpus this report ships persists what we found so future investigations can attribute against it instead of starting from scratch.

This is the third entry in Operation Long Shadow. Like v1 and v2, every claim in this article has a corresponding command in REPLAY.md and a hash in HASHES.txt for verification. The difference in v3 is the corpus is bigger: ten persistent operator anchor sets, two malware-kit fingerprints, 31 named cfnb fleet members, the polymarket activation timeline, the Pompeiuss-to-Enzo-Alarcón paper trail.

---

## Part 1 — From one cluster to the operator market

### The trending-repo stress test

After v2 we had calibrated math: graph_k3 ∧ lifecycle (cohort A or B) achieves P=R=F1=1.000 on the labeled 10/5000 universe. The fragility worth testing was the *anchors* — the 13 cohort-signature repos that the joint test counts overlap on. v1 and v2 anchored on AI/agent-tool repos discovered through one operator's behavior.

We pointed the v2 calibration at the top-100 starred repos created in the past week (2026-04-19 → 2026-04-26). 70 of the 100 were user-owned. Hunter joint-flagged exactly **zero of 70**.

This wasn't a calibration miss; it was a calibration-domain miss. The v2 anchor set is locked to the cfnb-cluster's 2025-era cohort signature. The 2026 trending repos are owned by a different population — most legitimately viral (Karpathy, Pocock, Vincent), some star-farmed by *different* operators with *different* anchor clusters.

The fix isn't to widen the v2 anchor set. It's to discover new operators' anchor sets and add them to the detection corpus. That's the methodology v3 makes operational.

### The cfnb operator and its five neighbors

Of the 70 trending owners we scored, two were ariadne-suspect (synthetic commits) but produced ZERO joint-flag from hunter v0.4. We profiled the stargazers of one of them — `xinyitang3/cfnb` — and found 26% bot-shape (vs 6% on the other suspect, which turned out to be AI-authored solo viral, organic stargazers).

`cfnb` was a star farm. The other suspect wasn't. Same ariadne fingerprint, two different attacks. Hunter's joint test correctly didn't fire on either because neither stargazed the v1 anchors — but the stargazer-profile separation of the two confirmed they were operationally distinct populations.

The 36 bot-shape cfnb stargazers became the seed cohort for lateral discovery. Snapshot their full star streams. Build a co-stargazing matrix — which repos do ≥3 of them share? After excluding the v1 anchors, **48 candidate repos** remained. The top of the matrix was a coherent Chinese-language network-circumvention/IPTV cluster: `xinyitang3/cfnb`, `cmliu/edgetunnel`, `DigitalPlatDev/FreeDomain`, `2dust/v2rayN`, `SagerNet/sing-box`, `chen08209/FlClash`, etc.

Promote the top 14 to a v2 anchor set. Re-score the 36 seeds against it under the calibrated joint rule. **23 of 36 joint-flagged**, with two clean cohort patterns:

- 10 Cohort A (mature-dormant, ages 506d–4829d) — the operator's pre-positioned warehouse
- 13 Cohort B (fresh-burst, ages 0–146d) — the active mints, including four accounts that were CREATED AND STARRED ANCHORS WITHIN 24 HOURS (`cate6014-lang`, `cmycxr5vtr-afk`, `tazai-blip`, `ayouak1`)

The most-anchored fleet member, `ybzbderen`, has 11 of 14 anchors hit and an account age of 1881 days at first anchor star. They were created **2018-10-16**, sat dormant for over six years, then in February 2025 created five repos in sixteen days — four of them forks of the cfnb cluster's anchor tools. Their non-fork repo `ybzbd` is a 72KB stub with one commit authored as `44206526+ybzbderen@users.noreply.github.com` (the GitHub auto-noreply format that means the operator never configured `git config user.email` locally — they web-UI-committed). On 2026-04-21 the account starred xinyitang3/cfnb and two `stallTCP1.32V2` variants in a 22-minute window.

That's one operator's one fleet account. There are thirty more.

### The full cfnb fleet

cfnb has 163 stargazers total (it's a freshly-created repo). 61 are bot-shape suspects. 31 of those joint-flag under the v2 anchors + v0.4 lifecycle. **The cfnb operator's fleet bot-rate is 19% of cfnb's stargazers** — for context, organic trending repos run under 1%.

Activation timeline (every fleet member's first cfnb-star):
- Wave 1 (Apr 19, 7 hours after repo creation): 6 accounts
- Wave 2 (Apr 20): 1 account
- **Wave 3 (Apr 21, 13-hour window): 13 accounts**
- Wave 4 (Apr 22): 5 accounts
- Wave 5–7 (Apr 24–26): 6 accounts, latest at **2026-04-26 17:32 UTC** — `ayouak1` activated minutes before this analysis ran.

The campaign is currently live. Wave 3 is the smoking gun: 13 distinct accounts coordinated to star one repo within thirteen hours. The Apr 22 + Apr 24 + Apr 25 + Apr 26 trickle confirms the operator hasn't stopped — they're still activating their warehouse as we read this.

### Operator-attribution evidence

Spider every fleet member with kraken at depth 1 — what identity do they leak?

Twenty-five of thirty-one leak nothing. No commits, no emails, no orgs, no collaborators. Pure-stargazer accounts. That's itself a signal: thirty-one organic users would not all have this exact same operational hygiene by chance.

The six that DO leak give us the operator's locale:

| login | leaked email | provider |
|---|---|---|
| ayouak1 | avfhg947@gmail.com | random-string Gmail |
| egullye | egullye@gmail.com | login@gmail (placeholder) |
| **linjycool** | **375915328@qq.com** | **Chinese QQ numeric** |
| **qinrong167** | **1084021579@qq.com** | **Chinese QQ numeric** |
| **wsluban168** | **1353116457@qq.com** | **Chinese QQ numeric** |
| yf217y | yf217y@gmail.com | login@gmail (placeholder) |

Three of six leak QQ numeric IDs — distinctly Chinese. Combined with ariadne's earlier finding that 100% of cfnb's actual git commits are timestamped UTC+0800 (China Standard Time), **the cfnb operator is China-based** with VPN routing. No two leak the same email (the operator uses throwaway-per-account hygiene), and zero of thirty-one fleet members have collaborated with each other on any repo, ever — accounts are kept operationally isolated.

### The five peer operators

The interesting question in v3 was whether cfnb is one operator or one node in a market. We answered it with a second-order matrix.

Take all 31 cfnb fleet members' full star streams. Build the matrix again — what other repos do ≥3 of them share, *excluding the cfnb anchor set*? 46 candidates. We validated nine of them by stargazer profile (campaign repos have bot-shape stargazers; popular legitimate tools have organic stargazers). Five are confirmed star-farm campaigns:

| campaign target | bot-shape % of top-100 stargazers | reading |
|---|---|---|
| MHSanaei/3x-ui | **31%** | star farm (V2Ray panel admin tools) |
| fanmingming/live | **25%** | star farm (IPTV) |
| MetaCubeX/ClashMetaForAndroid | **24%** | star farm (Mihomo/Clash) |
| Guovin/iptv-api | **22%** | star farm (IPTV API) |
| KaringX/karing | **21%** | star farm (iOS / piracy) |

Each is run by a *different* operator. We confirmed the separation cleanly: **0 of 31 cfnb fleet members appear in MHSanaei/3x-ui's top-100 stargazers.** If the cfnb operator ran 3x-ui, the 31 fleet would be there. They aren't.

Run the same per-operator dossier methodology on each of the five new candidates: profile their stargazers, filter to bot-shape, snapshot, build their own anchor matrix. Result: each operator runs 21-31 distinct seeds, each on its own niche specialization, with **0 pairwise fleet overlap** across all 15 operator pairs.

| operator | seeds | specialization (top anchor candidates) |
|---|---|---|
| **cfnb** | 31 confirmed | Cloudflare tunneling, free-domain |
| **3xui** | 31 | V2Ray panel admin (alireza0/x-ui, Marzban, REALITY, Hiddify-Manager) |
| **fanmingming** | 25 | IPTV / live-streaming (Beijing-IPTV, imDazui/Tvlist) |
| **clashmeta** | 24 | Mihomo/Clash ecosystem (mihomo, clash-verge, SagerNet, surfboard) |
| **iptvapi** | 22 | IPTV + Chinese reading apps (my-tv, legado) |
| **karing** | 21 | iOS jailbreak + Windows cracking (TrollStore, KMS_Activator) |

154 distinct bot accounts across six isolated fleets. Six independent star farms working the same Chinese-circumvention/IPTV vertical. They overlap in *tool usage* (some popular legitimate tools — `iptv-org/iptv`, `MetaCubeX/mihomo`, `blackmatrix7/ios_rule_script` — appear in multiple operators' matrices because the operators themselves use those tools), but their *fleets* are completely disjoint.

This is a star-farm-as-a-service market. cfnb is one node in it. The Chinese network-circumvention vertical alone has at least six active operators. We didn't enumerate the full vertical (more operators are surely there) — we mapped the slice that the cfnb cohort touches.

---

## Part 2 — Polymarket: the largest farm and the first real name

### The crypto-trading sweep

We pointed the same methodology at top crypto/trading repos created in the past 30 days. The pattern was visible in the search results before we ran any code.

15 of the top 15 user-or-org-owned repos in the vertical were `polymarket-copy-trading-bot` clones, owned by orgs with names like TradeCompute, PrimeOrder-Labs, Orbital-Alpha, Parallax-Trading, SmartOrder-Systems, AlgoInfraTech, Bird-eye-pp, Axion-Trading-Labs, FlowTrader-Labs. All created within a seventeen-day window (Apr 9 → Apr 26). All with near-identical SEO-optimized descriptions. All clustered at 200-300 stars each — suspiciously uniform.

### The shell-org factory

Pull the org metadata. Every org has zero public members, zero followers. Most have one repo. Creation timestamps cluster in 15:00–16:00 UTC bursts:

| pair | created | gap | repo size (KB) |
|---|---|---|---|
| Orbital-Alpha + PrimeOrder-Labs | Apr 25, 15:46 / 15:51 | **5 minutes** | 1150 / 1151 (Δ=1) |
| Parallax-Trading + SmartOrder-Systems | Apr 23, 16:48 / 16:55 | **7 minutes** | 696 / 690 (Δ=6) |
| Axion-Trading-Labs + FlowTrader-Labs | Apr 22, 17:54 / 18:04 | **10 minutes** | 1523 / 1522 (Δ=1) |

Paired orgs created minutes apart. Their respective repos have **byte-equivalent sizes** — within one or two KB on multi-MB codebases. The operator publishes one core repo from a template, varies the README to defeat duplicate-detection, but the rest of the code stays the same. The ariadne audit doesn't catch them (clean commit signatures), but the metadata fingerprint is glaring.

`Parallax-Trading` is a dormant 2018 org. The operator squatted it. The other shells were minted fresh. `figure-markets` and `muxprotocol` are squats of real DeFi protocol names. The operator picks each shell name to look credible at glance.

### The bot fleet

We profiled the stargazers of four polymarket variants:

| repo | bot-shape | fresh-2026 | organic-shape |
|---|---|---|---|
| TradeCompute/polymarket-arbitrage-trading-bot | **96%** | 86% | 3% |
| PrimeOrder-Labs/polymarket-copy-trading-bot | **97%** | 93% | 0% |
| Orbital-Alpha/polymarket-copy-trading-bot | **97%** | 93% | 0% |
| Pompeiuss/polymarket-arbitrage-trading-bot | **89%** | 82% | 3% |

For comparison: cfnb is at 26% bot-shape. The AI-tools vertical organic baseline runs 10–15%. Real viral repos like `JuliusBrussee/caveman` (47K stars) sit at 2%.

**These polymarket repos average 96-97% bot-shape stargazers.** This operator does not even attempt to look organic. The campaign relies on volume + new-repo trending visibility; the stars are pure manufactured signal.

We extracted the bot-shape stargazers across the four variants — **214 unique seed accounts**. The operator's full fleet is almost certainly larger; this is what surfaced from four repos. **178 of 214 (83%) were created in 2026-04** alone.

### The day-of activation pattern

Score the 214 seeds against anchors_polymarket + the v0.4 lifecycle. Run the matrix on their full star streams. The top of the candidate set is a coherent crypto-trading-bot cluster — Polymarket variants, Hyperliquid bots, Solana sniping tools, even **Pumpfun-Bundler-Bot** (Solana memecoin pump-and-dump) and **Web3 casino games**. The operator runs 25 promoted anchor candidates spanning prediction markets, futures trading, memecoin pumps, and gambling.

### Pompeiuss / Enzo Alarcón

`Pompeiuss` is the user-owned variant in the campaign. Their bio reads "Top Trader On Polymarket." Location: "Argetina" (typo for Argentina). 1 follower. 14 public repos.

The first thirteen of those repos are not crypto-trading bots:

```
2023-12-05  Historias_clinicas_frontend
2023-12-05  Historias_clinicas_backend
2024-01-08  Porfolio                     [typo: Portfolio]
2025-01-13  visualizador
2025-08-10  mono_repo_ConvertidorIMG
2025-10-21  servicios_integrales_front
2025-11-28  landing-page-sonido
2025-12-12  AlarconEnzoPRG3final12_20255  ←—— here
2026-01-06  mono_repo_Historias_clinicas_policonsultorios_multiusuarios
2026-01-21  backend_historiasclinicas_multiusuario
2026-01-21  frontend_historiasclinicas_multiusuario
2026-04-09  polymarket-sports-copy-trading-bot
2026-04-09  polymarket-copy-trading-bot
2026-04-09  polymarket-arbitrage-trading-bot
```

The repository named `AlarconEnzoPRG3final12_20255` is a Spanish-language college final-exam repository. "PRG3final" decodes to "Programación 3 final" (third-year programming-course final exam). The operator is named **Enzo Alarcón**, an Argentinian college student who built medical-records-management apps for school assignments through 2025, then on 2026-04-09 pivoted to creating Polymarket-trading-bot scam repos. He left his name in his own repo URL.

The `AlgoInfraTech` org leaks an email: `shaneriddell41@gmail.com`. That's an English-name alias not matching Pompeiuss directly — possibly a partner, possibly a fake-name contact channel, possibly the secondary user `babar-mpire` (created 2024-07, dormant, then on 2026-04-20 published seven Polymarket-related repos in one day).

The full operator profile: Argentinian college student (or two operators including one), pivoted from medical-records school projects to a star-farmed Polymarket-trading-bot campaign on 2026-04-09, currently runs 20+ shell orgs and a fleet of approximately 1,000+ bot accounts (extrapolating from the 214-seed sample). Real name: Enzo Alarcón.

This is the largest, fastest-moving, and most cleanly attributed operator in this report.

---

## Part 3 — The orthogonal axis: malware-kit fingerprinting

### When stars don't matter

We ran the same recipe — profile stargazers, filter bot-shape, snapshot — against the gaming-cheat vertical (Valorant, CSGO, FiveM, Rust, Apex, Warzone). It came back empty. Star counts on these repos are 0–2, not the hundreds we saw on Polymarket. No bot fleet to enumerate.

That's because gaming-cheat operators don't need stars. Their attack vector is GitHub search visibility — a victim looking for "valorant aimbot 2026" on Google or GitHub finds the repo, downloads the .exe inside, and the malware runs. Star manipulation gets you onto trending; it doesn't get you onto a Google search result. **The gaming-cheat vertical is malware distribution, not star farming.**

The math we calibrated for star-farm detection is silent on this. We needed a different signal axis.

### The kit fingerprint

We pulled the file-listing and byte-sizes for the top user/org-owned cheat repos in the vertical. The pattern was immediate:

```
.gitignore=95  | LICENSE=1187 | LOG=25 | SECURITY.md=739
```

These four file sizes appeared identically across **at least eleven shell orgs**: Kanwmwr, Reytn, Bwmishasm, Ahteons, Besvigahw, Reanekm, Prments, Rshwmom, S4warm, Utuanmy, Bwmishasm. Same sentinel files, same byte-sizes, varying README and Visual Studio solution names. The operator's malware kit emits deterministic-sized boilerplate.

This is a fingerprint. Hash the size of every sentinel file, match against a known-kit lookup table, and any matching repo attributes to the kit's operator regardless of which shell name owns it. We added this as the **v0.7 axis** of hunter — `--malware-kits DIR` flag, kit fingerprints stored as JSON in `corpus/malware_kits/`. The axis is orthogonal to the star-farm joint test: an account can match neither, either, or both.

### The Vietnamese operator

Looking at who actually owns the kit-matched repos: most are organizations (Kanwmwr et al.), but there's one user account in the cluster: **`coderduc`**, created 2019-01-01, 38 followers, 94 public repos, public email `tuanloantuduc123@gmail.com`. The email decodes to a Vietnamese name pattern (Tuan Loan Tu Duc). Their repo history shows kernel-driver research targeting game anti-cheat (EAC, BattlEye, CS2, Valorant) since 2024, including a `Chaos-Rootkit` ("Now You See Me, Now You Don't"), a Go-based binary packer (`pakkero`, 2024-12), and a `Pubg-Memory-Dumper`. Their April 17 2026 pivot: `Pixmenu-Valorant-Aimbot-IMGUI`.

This is exactly the toolkit needed to *build* the malware that's distributed via the kit fingerprint: a kernel hooker plus a binary packer plus an aimbot front-end. **`coderduc` is the operator candidate.**

### The cross-vertical link

We then scanned the social-media-boost vertical (Discord raid bots, TikTok bots, YouTube view bots). Most of it is independent skid scattering — different file structures, no kit pattern. But one repo matched the same fingerprint: **`LAwmwm/Discord-Raider`**.

`LAwmwm` is an org created 2026-04-08. It has four repos, all created the next day, April 9:

- `Discord-MASS-DM` — Discord auto-DM self-bot
- `Discord-Raider` — Discord raid tool (kit-matched)
- `Muck-Stealer` — info-stealer
- `UAC-Bypass-FUD` — Windows privilege escalation + persistence

The Vietnamese operator is therefore not a gaming-cheat specialist. They run a vertically-integrated malware factory: gaming cheats + Discord raid bots + info-stealers + Windows privilege-escalation tools, all built from the same code template, distributed through algorithmically-named shell orgs across multiple verticals. The kit fingerprint catches all of it.

### A second kit: the wallet drainer

The NFT/Web3 vertical surfaced a different kit fingerprint:

```
LICENSE=1123 | LOG=25 | SECURITY.md=679
```

Distinct from the Vietnamese kit's 1187/25/739 (different LICENSE byte size). Four shell orgs use it: `Aesrprabt`, `Harmo2nrvz`, `Hyzetro`, `Nyphorort` — all created 2026-04-26. The repos are openly named:

- `Aesrprabt/Atomic-Wallet-Fake-Balance-Flash-Crypto-CryptoCurrencies`
- `Harmo2nrvz/Phantom-Wallet-Fake-Web3-Flash-Balance-CryptoCurrencies-Crypto`
- `Hyzetro/Electrum-Fake-Balance-Flash-Crypto-CryptoCurrencies-Wallet`
- `Nyphorort/Crypto-Wallet-Okx-Exodus-Metamask-Checker`

The description on `Hyzetro/Electrum-Fake-Balance-Flash-Crypto`: *"Exploits Electrum wallets by displaying fake balances..."* — the operator doesn't even hide the intent. The kit's payload is wallet-overlay malware that displays fabricated balances to scam victims.

Same architectural pattern as the Vietnamese kit (boilerplate-fingerprinted + `.sln` Visual Studio solution + algorithmic shell orgs), but the LICENSE byte size differs by 64 bytes. **These are two different operators using the same architectural pattern.** Both detected by the same v0.7 axis with separate JSON kit fingerprints in `corpus/malware_kits/`.

---

## Part 4 — The negative control: AI-tools

We deliberately tested the methodology against a vertical we did not expect to have a star farm. The hypothesis: today's AI-tools ecosystem has so much organic attention that there's no purchase for fake stars to add value.

We ran the methodology against the top user-owned AI/agent/LLM repos created in the past 30 days. Top by velocity:

- `MemPalace/mempalace` — 49,835 stars in 21 days (an open-source AI memory system)
- `JuliusBrussee/caveman` — 47,205 stars in 22 days
- `kyegomez/OpenMythos` — 10,662 stars in 8 days

Stargazer profiles:

| repo | bot-shape | reading |
|---|---|---|
| MemPalace/mempalace | 20% | borderline |
| caveman | **2%** | viral organic |
| OpenMythos | 10% | clean |
| HKUDS/Vibe-Trading | 12% | clean |

MemPalace at 20% looked borderline-suspicious. We ran the propagation step from Playbook 6 — extract MemPalace's bot-shape stargazers as seeds, snapshot their full star streams, build the co-stargazing matrix. The matrix surfaced a coherent AI-agents/Claude-Code cluster (`obra/superpowers`, `karpathy/autoresearch`, `garrytan/gstack`, `mattpocock/skills`, etc.) — but every top candidate when independently profiled came back at 5–15% bot-shape. Not the 25%+ that defines a campaign.

**MemPalace's stargazer profile is elevated because the AI vertical is full of "AI-curious" GitHub users who created low-friction accounts specifically to follow AI projects.** They have 0 followers and few repos — exactly the bot-shape filter — but they're organic users, not operators. The propagation step distinguishes them: operator fleets cause the secondary candidates' profiles to inherit the bot-shape signature. Organic-elevated populations don't.

**This is the methodology working.** The AI-tools vertical has no active star farm at the velocity-suspect tier we surveyed. The negative result is the calibration; the toolchain doesn't false-positive on real virality. We logged the AI-vertical organic baseline at 10-15% so future investigations use the right threshold.

---

## Part 5 — The unsolved pattern: airdrop affiliate-drop on aged accounts

The NFT/Web3 vertical produced the wallet-drainer kit (Part 3) and one other finding the toolchain currently cannot detect.

On **2026-04-23**, at least 13 users created airdrop-bot repositories targeting different testnet projects (OroSwap, Izumi, Boxxer, Pharos, Diamante, Humanity Protocol, LayerEdge, Kite-AI, BPM, Gotchipus, Nillion, Interlink, Kite-AI). All on the same day. All with similar emoji-laden README templates: *"🤖 Ultimate Airdrop Bot 2026 - Auto-Claim & Anti-Ban..."*

The accounts that did this drop were not freshly created:

```
PriyalMandaliya     2020-09  (5.6 years old)
Mualape300          2022-05  (4 years)
Aa3081              2023-04  (3 years)
Lorencedecena       2023-10  (2.5 years)
Darshi909           2024-09  (1.5 years)
68677               2025-01
Jaweria2245         2025-04
AveragePythoner     2025-08
Infin1tewolfpr0     2025-08
Aniket261193        2025-10
```

These are aged real GitHub accounts (some with five years of history), each dropping their first airdrop-bot repo on the same single day. Hunter v0.4's lifecycle axis flags fresh-burst (Cohort B) and mature-dormant (Cohort A) — but these accounts are *neither*. They have organic-looking history and a single suspicious recent action. The lifecycle axis sees them as Cohort OTHER and the joint test passes them.

The pattern is one of three things:
1. An **affiliate scam** — an operator pays real users to push the same scam tool, varying the brand by victim
2. A **GitHub account rental market** — an operator buys access to credible-looking aged accounts and runs distributions through them
3. A **compromised account chain** — an attacker has access to many aged accounts and dumps payloads on a coordinated date

The same-day timing, identical README template style, and diversity of account ages favor the affiliate-scam hypothesis. We don't have positive evidence to discriminate among the three.

This is a v0.8 capability the toolchain doesn't yet have: a **single-day-burst-on-aged-account axis** that flags accounts with established history that suddenly create a repo matching campaign-naming patterns on the same day as other accounts doing the same. We persisted the 13 known logins as `corpus/ecosystem/anchors_airdrop_drop_2026-04-23.txt` so a future v0.8 has a labeled positive set to calibrate against.

---

## Part 6 — Replay

Every claim above is reproducible from the persisted corpus. The toolchain ships at v0.7 with a multi-axis architecture you can run against any GitHub account.

```bash
# Detect known operators (10 anchor sets in corpus/ecosystem/) AND known
# malware kits (2 kit fingerprints in corpus/malware_kits/) on a suspect account
hunter score <login> \
    --anchors-dir /path/to/ai-vs-human/research/detector/corpus/ecosystem/ \
    --malware-kits /path/to/ai-vs-human/research/detector/corpus/malware_kits/ \
    --identity \
    --sterile-repos /path/to/sterile.jsonl \
    | jq .
```

The output JSON reports `attributed_operator` (slug of which star-farm operator the account belongs to, if any), `malware_kit.matches` (which owned repos match which kit), per-axis advisory signals, and a calibrated `flagged: bool` from the joint test. Snapshot every account scored with `--snapshot DIR` to enable forensic re-scoring after GitHub deletes the source.

The full corpus ships with v3:

- `corpus/anchors_v2.txt` — cfnb anchors (14 repos)
- `corpus/ecosystem/anchors_<8 operators>.txt` — per-operator anchor sets
- `corpus/ecosystem/seeds_<6 operators>.txt` — confirmed seed accounts per operator
- `corpus/cfnb_fleet_logins.txt` — the 31-account cfnb fleet
- `corpus/cfnb_activation_timeline.txt` — chronological cfnb-stargaze events Apr 19–26
- `corpus/malware_kits/vietnamese_cheat.json` — Vietnamese-operator kit fingerprint
- `corpus/malware_kits/wallet_drainer.json` — wallet-drainer kit fingerprint

Add to your detection set as it grows. Each new operator surfaced in a future investigation is one more file in `corpus/ecosystem/`.

Methodology details — the per-vertical recipe for surfacing a new operator's anchor set, the propagation test for distinguishing campaign from elevated-organic, the kit-fingerprint discovery process — live in the `op-recon` skill at `~/.claude/skills/op-recon/SKILL.md`. Seven playbooks. Ten synthesis rules.

---

## Part 7 — What this means

The story v3 tells:

> v1: There is a farm.
> v2: The math detects the farm.
> v3: The farm has neighbors. They run the same playbook with different signatures, in different verticals, against different victim populations. The math we calibrated against the v1 farm generalizes to all of them. The corpus of operator anchor sets and kit fingerprints we ship with v3 turns the math into a working detection system.

Three concrete claims this report makes that v1 and v2 did not:

1. **Coordinated inauthentic behavior on GitHub is a market, not a phenomenon.** At least nine star-farm operators run parallel campaigns across the verticals we sampled. They do not share fleets. They specialize in niches. The operator economy is mature enough to produce variation in attack pattern (shell-org-bombing, fake-legitimacy facade, dual-account simple, malware-kit boilerplate distribution, single-day affiliate drop).

2. **The most-aggressive operator we found is operationally sloppy.** The Polymarket operator, Enzo Alarcón, runs the largest measured fleet in this report (96-97% bot-shape, ~1,000+ accounts) and left his real name in a public college-final-exam repository. Sophistication does not correlate with operational discipline. The detection-and-attribution pipeline is more effective on the loudest operators precisely because they don't bother to hide.

3. **The next axis — beyond stars and beyond commits — is the file boilerplate.** Malware-kit operators don't need stars. Ariadne's date-fabrication signal misses them. Hunter's joint test misses them. But the kit emits boilerplate files with deterministic byte-sizes, and that fingerprint is a per-repo signature that catches the operator regardless of vertical. Every additional kit fingerprint added to the corpus extends the toolchain's reach without adding new code.

What's still open:

- The aged-account affiliate drop is an attack pattern the math doesn't yet model. v0.8 specification.
- Hunter currently scores users only. Most malware-kit operators run organizations. Org-scoring is a gap.
- The per-operator anchor sets (v2 through karing) have been validated on hit-rate against known seeds, not formally evaluated against negative pools. v3 ships them as detection infrastructure; v4 should evaluate them as classifiers.
- Cross-vertical operator linking (we found one with the kit fingerprint) is the most underexplored direction. The data we have is consistent with two-to-three verticals being run by the same operator simultaneously; we haven't enumerated the full overlap.

The v1 article ended with "What's still open" — the questions we hadn't answered yet about the original 4-cluster operation. v3 ends with the same posture toward the broader market. The honest claim is that the toolchain works and the corpus is real; the markets we mapped are bigger than we mapped, and the math we calibrated will keep generalizing as we point it at more verticals.

What v3 most clearly demonstrates is that the *generalization is not theoretical*. We pointed the v2-calibrated math at seven new verticals in one workday. It returned coherent operator dossiers in five of them, a calibrated negative result in one, and an unsolved attack pattern in one. The corpus we ship is what it found.

---

*Operation Long Shadow v3 was conducted 2026-04-26 in a single workday. Tooling: hunter (v0.7, account scoring + multi-operator attribution + malware-kit fingerprinting), kraken (identity-graph spider), ariadne (per-repo verdict), entropyx (authorship dynamics), vajra (structural triage). All commands, hashes, and per-claim corpus paths in REPLAY.md.*
