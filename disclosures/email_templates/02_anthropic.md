**To:** security@anthropic.com · cc: trust@anthropic.com
**Subject:** Pre-publication notice — `claude-code@anthropic.local` author-identity forgery across 8+ GitHub repos

Hi Anthropic Security / Trust & Safety,

I'm publishing a forensic investigation in 48 hours and need to brief you on a pattern I found that involves your brand directly.

**The forge.** A separate operator cluster (distinct from the one targeting Allen AI / yikart / theQRL) is using the forged author identity `Claude Code <claude-code@anthropic.local>` on commits across at least 8 GitHub repositories under 8 different owner accounts. `anthropic.local` is not a real domain. Your actual Claude Code does not author commits this way. The forgery appears designed to make republished/laundered code appear as if Anthropic's Claude Code authored it. The pattern fingerprint:

```
gh api -X GET search/commits -f q='author-email:claude-code@anthropic.local'
→ 23 commits across 8 distinct repos, 8 distinct owner accounts
```

**Affected accounts** (mix of fresh-attacker and compromised-dormant):
- `CaMaGuee/invest.co.kr` (account created 2021)
- `esrfdev/ESRF-clean` (account created same day as repo, also impersonates European Synchrotron's `esrfdev` developer org name)
- `gdhughey/CISTracker`
- `jun564/jwcore-review` (account created 2021)
- `mctils12-arch/voltradeai` (account created same day as repo)
- `mearley24/AI-Server`
- `rvadapally/PracticeX.App` (account created 2021)
- `vpneoterra/forge-ecs-platform` (15-repo coordinated fake fusion-energy startup posture)

**Adjacent context.** This is *not* the same operation as the well-publicized "Hackerbot-Claw" AI bot (StepSecurity / Datadog wrote that up in March). That bot openly identifies as Claude-powered. This pattern is the inverse: it pretends to *be* Claude itself, in commit metadata, on republished/laundered code — and the operator is not making any public claim about it.

**What I'm publishing in 48 hours.**
- Full taxonomy at `github.com/copyleftdev/long-shadow`, codenamed "Operation Long Shadow"
- Detection signature documented in `tools/vet.py` and the `claude-code@anthropic.local` pattern called out explicitly so other defenders can match
- Recommendation in the disclosure doc: Anthropic could publish guidance that Claude Code never sets `*.anthropic.local` as an author email — *anyone seeing that pattern is observing a forge*. That advisory would let downstream defenders (GitHub T&S, Socket, StarScout, Sigstore, etc.) block on it directly.

**Asks.**
1. Confirm receipt.
2. Let me know if you'd like the pattern called out differently, or if you'd prefer a coordinated joint advisory.
3. If you want to file impersonation complaints with GitHub against the 8 owner accounts before I publish, you have far stronger trademark standing than I do.

Happy to send a pre-publication copy on request.

Best,
[Your name]

---

**Evidence references:**
- `data/enumeration/farm_b_c.txt` — full enumeration of the 8 owner accounts + creation timestamps
- `catalog/sock_puppet_emails.csv` row for `claude-code@anthropic.local`
- `catalog/operators.csv` cluster B
