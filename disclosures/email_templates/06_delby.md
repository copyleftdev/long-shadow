**To:** intelligence@delby.ai
**Subject:** Pre-publication notice — A GitHub organization called `DelbyIntelligence` is publishing 3,112 fake "Delby AI Product:" pages under your brand. You almost certainly don't know about this.

Hi Delby Intelligence team,

I am publishing a forensic investigation in 48 hours and you are the most consequential party I am giving heads-up to. Please read carefully.

**The situation.** A GitHub organization called `DelbyIntelligence` (one word, distinct from `delby.ai`) was created on **2026-04-03**. As of 2026-04-25 it has published **3,112 public repositories**, growing at roughly **140 repos per day**. Every repository's description begins **"Delby AI Product:"** — naming fictional Physical-AI products with elaborate technical descriptions ("Delby DRIVE-Cortex: Safety-Certified Edge Inference Pipeline," "Delby NuRec-Studio: Real-World to Sim Pipeline for AV Scenario," etc.). Every repo serves a static landing page on `delbyintelligence.github.io/{repo-name}/`. Several of the showcase repos name specific potential customers — including `product-multi-vendor-fleet-orchestration-demo-for-cardinal` ("Demo for Cardinal Health") and `product-federated-physical-ai-training-sandbox-live-demo-f` ("Live Demo for IIT Bombay").

**Almost certainly not your team.** Your real `delby.ai` website does not link to a `DelbyIntelligence` GitHub organization anywhere visible. The org has no description, no email, no website. The HTML inside every repo lists `<link rel="canonical" href="https://delbyai.github.io/delby-agents/" />` — a different account that **does not exist on GitHub** (HTTP 404, also no Wayback Machine snapshots ever indexed). The operator account that pushed all 3,112 repos is `delby-ai` — a fresh GitHub user created **92 seconds before** the `DelbyIntelligence` org. Activity hours and day-of-week patterns suggest a Chinese (or possibly Indian) night-owl operator.

**What this means for you.** Someone is brand-squatting Delby Intelligence at industrial scale. The squat:
- Confuses anyone investor-due-diligencing your company on GitHub (they will find 3,112 "Delby AI Product:" pages with nothing behind them).
- Damages your real brand's credibility (the operator's pages look elaborate but are vapor; this reflects on you when discovered).
- Could be used as a base for a future scam targeting your prospective customers (the showcase repos already name-target Cardinal Health and IIT Bombay — exactly the enterprise pattern a phishing follow-up would exploit).

**What I'm publishing in 48 hours.**
- Full forensic case at `github.com/copyleftdev/long-shadow`
- The `DelbyIntelligence` org name, the `delby-ai` operator account name, and the production timeline are all already publicly verifiable via GitHub's API — I'm just collecting and presenting them.

**Asks (high priority).**
1. **Confirm receipt of this notice within 48 hours** so I know you're aware before publication.
2. **File a trademark complaint at https://github.com/contact/dmca**. The 3,112-repo bulk impersonation, the "Delby AI Product:" naming convention, and the empty corporate context give you very strong removal standing. The StarScout precedent (Carnegie Mellon's research on a similar phenomenon) shows GitHub Trust & Safety removes ~90% of flagged repos when forensically reported.
3. If you've experienced any prospective-customer or investor confusion that could be related, that context would meaningfully strengthen the trademark complaint — I can help draft if useful.
4. Watch for related impersonation: operators that scale to 3,112 repos in 22 days commonly run multiple parallel squats. I'd suggest checking GitHub for variations on "delby" / "delbyai" / "delby-intelligence" and similar.

I want to underline: **this is not a story about anything Delby Intelligence has done wrong.** It is a story about an operator using your brand as an industrial-scale facade. The publication will explicitly frame it that way. But I want to give you the chance to comment, file your own takedown, or coordinate timing before it goes live.

If you want a pre-publication copy of the full report, reply and I'll send it.

Best,
[Your name]

---

**Evidence references** (will be public at `github.com/copyleftdev/long-shadow` once published):
- `data/enumeration/delby_full.jsonl` — every one of the 3,112 repo names with creation timestamps
- `data/enumeration/delby_analysis.txt` — production curve, day-of-week pattern, showcase set
- `catalog/operators.csv` — `delby-ai` and `DelbyIntelligence` account metadata
- The published article's Chapter 4 is dedicated to this case, with the full 3,112-cell visualization
