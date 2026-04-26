**To:** team@narwallets.com · cc: security@narwallets.com (or whichever Narwallets / NEAR Protocol contact is listed at https://narwallets.com/contact)
**Subject:** Pre-publication notice — `Narwallets/narwallets-extension` republished TWICE (stale v4.0.3 vs your v4.0.7 — security regression for users)

Hi Narwallets / NEAR team,

Forensic disclosure ahead of publication in 48 hours. Wallet extension is involved, so flagging with care.

**What was cloned.** Your `Narwallets/narwallets-extension` Chrome extension code was cloned and republished **twice** by a multi-account operator we've codenamed "Operation Long Shadow":

- `luliguyu/ssaavedrad` — 496 commits
- `countneurooman/ssaavedrad` — also republished under a second operator-controlled account

Both fakes are named after `ssaavedrad`, who is a real Narwallets contributor. Their handle was used as **personal-fork camouflage** — anyone searching for "ssaavedrad" might land on these fakes thinking they're the real contributor's personal fork. They are not.

**Diff verdict (capture date 2026-04-25).** I diffed every NEAR address (mainnet token contracts, factory.bridge.near identifiers, etc.) and every critical signing / RPC / background-script file. **No malicious modifications detected.** The 15 NEAR addresses in the fake match the well-known mainnet token contracts (UNI, USDC, USDT, DAI, LINK, WBTC, wNEAR, etc.) byte-for-byte against your upstream.

**However.** The fake's `manifest.json` is at version **4.0.3**; your real upstream is at **4.0.7**. The fake is **four minor versions behind** your security fixes. Anyone confused into installing the laundered fork instead of the real Narwallets extension is running stale wallet code missing your subsequent security work.

The operator controls both fake repos and could push a malicious update at any moment. The published investigation includes `tools/wallet_watcher.py` which re-clones both fakes every 30 minutes and alerts on any new address not on the captured allow-list.

**Asks.**
1. Confirm receipt.
2. File DMCA / impersonation complaints at `https://github.com/contact/dmca` against `https://github.com/luliguyu/ssaavedrad` and `https://github.com/countneurooman/ssaavedrad` — your standing as the trademark holder is much stronger than mine.
3. Consider notifying the real `ssaavedrad` user that their handle is being used as personal-fork camouflage (so they can flag it on their profile or social presence).
4. If you'd like the captured address baseline + watcher script tailored to your monitoring, happy to coordinate.

Best,
[Your name]

---

**Evidence references:**
- `evidence/wallet_addresses/CATALOG.md` and `baseline.txt` — the 15-address NEAR allow-list
- `evidence/commit_history/luliguyu_ssaavedrad.tsv` — 496-commit history of the first fake
- `scripts/06_wallet_integrity_diff.sh` — reproducible diff command
