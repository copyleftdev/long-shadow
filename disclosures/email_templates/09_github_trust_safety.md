**To:** GitHub abuse form at https://github.com/contact/report-abuse → category "Spam" + "Impersonation" (multiple submissions, one per cluster)
**Subject (use as report description):** Coordinated repo-laundering operation: 3,150+ repos, 4 operator clusters, brand impersonation including Allen AI / Anthropic / ESRF / a real Indian Physical-AI company (Delby)

GitHub Trust & Safety,

I'm filing this in coordination with a forensic investigation I'm publishing publicly in 48 hours. The investigation enumerates **four distinct operator clusters** running a coordinated repo-laundering and brand-impersonation operation on GitHub. Total confirmed scope:

- **3,150+ laundered or fake-product repositories** (3,112 from one operator alone, in 22 days)
- **17+ operator GitHub accounts** (4 + 8 + 1 org + ≥6 bot accounts)
- **9+ sock-puppet author email addresses** (5 provider patterns)
- **Multiple impersonations of real organizations and individuals**: Allen Institute for AI (`allenai/WildDet3D` cloned 4 days after release), Anthropic (`claude-code@anthropic.local` author identity forged on commits in 8+ repos), European Synchrotron Research Facility (`esrfdev` GitHub account name impersonation), the real Indian Physical-AI startup `delby.ai` (full-org `DelbyIntelligence` brand-squat with 3,112 fake "Delby AI Product:" pages), and a real Japanese researcher whose personal website is being used in the profile of a Long-Shadow-operator GitHub account.
- **Two cryptocurrency wallets republished** as "personal forks" using stolen contributor handles as camouflage (`theQRL/zond-web3-wallet` and `Narwallets/narwallets-extension` — both currently benign on diff but operator-controlled).
- **A paid bot-star service** inflating both farm repos and at least 4 real Chinese AI startups (~19,000 inflated stars combined across just the four largest customers).

This explicitly violates the **GitHub Acceptable Use Policies** prohibition on:
- *"automated excessive bulk activity and coordinated inauthentic activity, such as creation of or participation in secondary markets for the purpose of the proliferation of inauthentic activity"*
- *"content or activity that impersonates any person or entity"*

**Bulk evidence pack:** All raw enumeration data, commit-SHA evidence files, kraken identity-graph data, entropyx forensic scans, and full reproduction scripts will be public at `github.com/copyleftdev/long-shadow` in 48 hours. The published report (per-cluster catalog, replay commands, evidence hashes) is the bulk-removal package.

**Operator account list (priority order):**

| Cluster | Account | Type | Suggested action |
|---|---|---|---|
| C | `delby-ai` | User | Suspension — operator account that pushed all 3,112 fake AI-product pages |
| C | `DelbyIntelligence` | Org | Bulk org removal — 3,112 brand-squat pages of real `delby.ai` company |
| A | `kyasbalme` | User | Suspension — fresh-attacker account, identity theft via profile field |
| A | `luliguyu` | User | Suspension — fresh-attacker account |
| A | `tusmart-grouptt` | User | Investigate — older account, recent farm activity, likely compromised |
| A | `countneurooman` | User | Investigate — older account, recent farm activity, likely compromised |
| B | `esrfdev` | User | Suspension — same-day-as-repo, ESRF impersonation |
| B | `mctils12-arch` | User | Suspension — same-day-as-repo |
| B | `gdhughey` | User | Investigate |
| B | `vpneoterra` | User | Investigate — 15-repo coordinated fake fusion-startup |
| B | `CaMaGuee`, `jun564`, `rvadapally`, `mearley24` | Users | Likely compromised dormant accounts — original-owner notification recommended before action |
| D | `RPaez09l`, `tASDFG12345m`, `7228735902`, `superdaysk3wom` | Users | Bot-star participants in inauthentic-engagement secondary market |
| D | `liiiiiii1i1i1`, `8888x82` | Users | Fresh bulk-star accounts created together in April 2025 — bot pool provisioning |

**Reference:** This investigation extends the methodology of the StarScout paper (Hao He, Christian Kästner et al., CMU + NCSU + Socket, ICSE 2026) and applies it to AI-themed brand-squatting, Anthropic-identity forgery, and academic-paper laundering — three categories beyond StarScout's original fake-star taxonomy.

I am happy to coordinate timing, share advance access to the evidence repo, or assist with any further triage your team needs.

Best,
[Your name]

---

**Linked submissions for trademark complaints** (separate forms at `https://github.com/contact/dmca` — recommend filing in parallel):
- Allen Institute for AI → `luliguyu/WildDet3D`
- Anthropic → 8 forged-author commits across cluster B
- The Quantum Resistant Ledger → `luliguyu/dimatura`
- Narwallets → `luliguyu/ssaavedrad` + `countneurooman/ssaavedrad`
- yikart → `kyasbalme/AiToEarn` + `tusmart-grouptt/AiToEarn`
- Delby Intelligence (intelligence@delby.ai) → entire `DelbyIntelligence` org
- European Synchrotron Research Facility → `esrfdev`

The owners are receiving direct notice in parallel with this report.
