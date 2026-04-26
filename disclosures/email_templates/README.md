# Disclosure Email Templates

Nine pre-publication notices to send 48 hours before making the `long-shadow` repo public. Send them in parallel; do not wait for replies before publishing — the 48-hour window is a courtesy, not a veto. Confirm sends in your own log; reply to anyone who responds.

| # | Recipient | What they own / why they get notified |
|---|---|---|
| 01 | Allen Institute for AI | `allenai/WildDet3D` cloned 4 days after release as `luliguyu/WildDet3D` |
| 02 | Anthropic | `claude-code@anthropic.local` author-identity forgery across 8 cluster-B repos |
| 03 | The Quantum Resistant Ledger | `theQRL/zond-web3-wallet` republished as `luliguyu/dimatura` (stale, not actively malicious — but operator controls the fork) |
| 04 | Narwallets / NEAR | `Narwallets/narwallets-extension` republished twice (4 minor versions behind real upstream) |
| 05 | yikart | `yikart/AiToEarn` republished by two sock-puppet accounts (preserves original Chinese authors verbatim) |
| 06 | Delby Intelligence (intelligence@delby.ai) | **Highest priority.** 3,112-repo brand-squat under `DelbyIntelligence` org |
| 07 | European Synchrotron Research Facility | `esrfdev` GitHub account name impersonation |
| 08 | The real `blu3mo` (via blu3mo.com contact form / DM) | Personal-website URL used in profile of laundering-account `kyasbalme` |
| 09 | GitHub Trust & Safety | Bulk evidence package for the entire enumeration; submit at https://github.com/contact/report-abuse |

## Sending checklist

Before you click send on each email:
- [ ] Replace `[Your name]` with your real name + affiliation if any
- [ ] Replace email address(es) at the top with the recipient's actual contact (URLs in each template suggest where to find them)
- [ ] Verify the GitHub URL `github.com/copyleftdev/long-shadow` matches the URL you'll actually publish at
- [ ] If you want to add a phone or Signal number for direct contact, add it to the closing
- [ ] Bcc your own address so you have a record

## After sending

- Track sends in a private log (date + who + which template).
- Reply to anyone who responds within the 48-hour window.
- After 48 hours, run the `gh repo create` step (Claude has held on this — confirm with "publish now" once you've sent these).
- Post-publication, monitor:
  - The 9 victim email addresses for follow-ups
  - The wallet_watcher / farm_watcher state files for new operator activity
  - GitHub itself for takedown actions

## Out of scope for these 9 emails

The four real Chinese AI startups currently anonymized as Customer A/B/C/D in the public report — they are referenced in the report but their identities are withheld until you have a way to reach each one directly. Once disclosed (or once they reach out), the v2 of the report can de-anonymize.
