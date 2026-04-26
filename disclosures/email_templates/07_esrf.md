**To:** computing@esrf.fr · cc: any ESRF developer-org GitHub admin email if discoverable
**Subject:** Pre-publication notice — GitHub user account `esrfdev` impersonating ESRF's developer presence

Hi ESRF Computing / IT,

Brief forensic disclosure ahead of publication in 48 hours.

**The situation.** A GitHub user account named `esrfdev` (lowercase) was created on **2026-04-12**. The same day, it published its only repository: `esrfdev/ESRF-clean`. That repo's commits are forged with the author identity `Claude Code <claude-code@anthropic.local>` (a fake domain — Anthropic's actual Claude Code does not author commits this way). The account's name + repo naming pattern + same-day creation are consistent with **fresh-attacker-created impersonation** of ESRF's institutional developer presence, presumably to gain credibility for whatever the laundered code is.

This is one of 8 GitHub accounts in a cluster I've been investigating ("Operator B" in the larger taxonomy) — distinct from the well-publicized Hackerbot-Claw incident from earlier this year, but using a similar Claude-impersonation theme.

**What I'm publishing in 48 hours.**
- Full investigation at `github.com/copyleftdev/long-shadow`
- The `esrfdev` account name and `ESRF-clean` repo are explicitly called out as ESRF impersonation in the disclosure section.

**Asks.**
1. Confirm receipt.
2. If ESRF has a real `esrfdev` GitHub account (or any institutional GitHub presence) that could be confused with this fake, file a trademark / impersonation complaint at `https://github.com/contact/dmca`. Your standing as the rightful institution far exceeds mine.
3. If you'd prefer different framing in the publication, let me know.

Best,
[Your name]

---

**Evidence references:**
- `catalog/operators.csv` cluster B — `esrfdev` row
- `data/enumeration/farm_b_c.txt`
