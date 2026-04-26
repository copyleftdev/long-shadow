**To:** info@allenai.org · cc: research-security@allenai.org · weikaih@allenai.org
**Subject:** Pre-publication notice — `allenai/WildDet3D` cloned 4 days after release as `luliguyu/WildDet3D`

Hi Allen AI team,

I'm publishing a forensic investigation in 48 hours and want to give you a heads-up so you can act before the public report goes live.

**What I found.** A GitHub account `luliguyu` (created 2025-10-21) cloned and republished your `allenai/WildDet3D` repository as `luliguyu/WildDet3D` on **2026-04-07** — four days after your 2026-04-03 official release. The fake repo preserves your researcher Weikai Huang's 17 commits and `weikaih@allenai.org` author identity verbatim. The `luliguyu` owner account is the second of four GitHub accounts I've identified as belonging to a single China-based operator running a multi-cluster repo-laundering operation we've codenamed "Long Shadow."

**Severity.** This is real-time academic IP theft (4-day lag from release). It is not, as far as I have been able to verify, malicious code modification — the cloned repo appears to be a straight import of your code. The harm is reputational and attributional: your work is mirrored under a sock-puppet account, and could be confused with an authorized fork.

**What I'm publishing.**
- The full investigation: a four-cluster taxonomy of the operation (16 known farm repos, 9 sock-puppet emails, 3,112 brand-squat repos under another cluster).
- All raw evidence (commit SHAs, kraken identity-graph data, entropyx forensic scans, reproduction scripts).
- The page goes live at `github.com/copyleftdev/long-shadow` in 48 hours.

**What I'm asking.**
1. Confirm receipt of this notice.
2. If you'd like specific framing, redaction, or additional context included before publication, let me know within 48 hours.
3. If you want to file the GitHub DMCA / impersonation report yourself before I publish (you have stronger standing than I do), the abuse form is at https://github.com/contact/dmca and the relevant fake repo is `https://github.com/luliguyu/WildDet3D`.

I'm not asking you to do anything publicly — this is courtesy disclosure. Reply if you have any questions or would like a pre-publication copy of the report.

Best,
[Your name]

---

**Evidence references** (will be public at `github.com/copyleftdev/long-shadow` once published):
- `evidence/commit_history/luliguyu_WildDet3D.tsv` — 17 commits with preserved `weikaih@allenai.org` identity
- `data/enumeration/evidence_pack.txt` — confirms `allenai/WildDet3D` real upstream metadata at the time of capture
- `catalog/upstream_victims.csv` — full list of upstream victims across all four clusters
