**To:** info@theqrl.org · cc: security@theqrl.org
**Subject:** Pre-publication notice — `theQRL/zond-web3-wallet` republished as `luliguyu/dimatura` (stale, not actively malicious — but operator controls the fork)

Hi The Quantum Resistant Ledger team,

Forensic disclosure ahead of publication in 48 hours. Wallet code is involved, so I'm flagging this with extra care.

**What was cloned.** Your `theQRL/zond-web3-wallet` repository was cloned and republished as `luliguyu/dimatura` by an account in a multi-cluster GitHub repo-laundering operation we've codenamed "Operation Long Shadow." The republished repo is named `dimatura` because the operator's pattern is to name farm repos after real upstream contributors' GitHub handles, to camouflage them as "personal forks" — `dimatura` is a real GitHub user (Daniel Maturana, robotics researcher) and they are *not* part of this operation; their handle was used as cover.

**Diff verdict (capture date 2026-04-25).** I diffed every ETH `0x` address and every critical signing/RPC file in the laundered fork against your real upstream. **No malicious modifications were detected.** The differences are time-based snapshots — the fake repo is from before your `Qrl* → Zond*` rename completed, so it's a partial-rename snapshot of older code. Every 0x address in the fake matches a test fixture in your real repo.

**However.** The operator (`luliguyu`, GitHub user, China-based per timezone evidence) controls the fake repo and could push malicious updates at any moment. Today's snapshot is benign. Tomorrow's might not be. The published investigation includes a watcher tool (`tools/wallet_watcher.py`) that re-clones both forks every 30 minutes and alerts on any new address that isn't on the captured allow-list — that watcher will run continuously.

**Asks.**
1. Confirm receipt.
2. File a DMCA / impersonation complaint at `https://github.com/contact/dmca` against `https://github.com/luliguyu/dimatura` — the personal-fork camouflage gives you strong trademark + impersonation grounds, and you have far better standing than I do.
3. Consider publishing canonical-installation guidance pointing users at your verified releases (since the `luliguyu/dimatura` fork is now ~30+ commits behind your security fixes, anyone confused into installing the fake gets stale wallet code).
4. If you'd like a copy of the address baseline I'm publishing in the watcher (so you can run your own checks), I'll send it.

I would normally publish this with a longer disclosure window, but the watcher is the time-sensitive piece — every minute the operator's repo isn't being watched is a minute they could push a payout-address swap unnoticed.

Best,
[Your name]

---

**Evidence references:**
- `evidence/wallet_addresses/CATALOG.md` and `baseline.txt` — the 13-address allow-list, all upstream-original test fixtures
- `evidence/commit_history/luliguyu_dimatura.tsv` — the 609 commits in the fake fork, with author identities + timestamps
- `tools/wallet_watcher.py` — the continuous-monitoring tool (MIT-licensed, reusable)
