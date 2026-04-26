**To:** [find blu3mo's contact via blu3mo.com — likely a contact form, Twitter DM, or public email on the site]
**Subject:** A GitHub account is using your blu3mo.com URL on its profile to laundered repos

Hi blu3mo,

I'm reaching out before publishing a forensic investigation in 48 hours because your personal-website URL is being used in an impersonation pattern that I want you to know about.

**The situation.** A GitHub user account named `kyasbalme` was created on **2025-10-25**. Its profile bio reads "CS & Philosophy @ Columbia," its location reads "NYC & Tokyo," and its profile **website is set to `http://blu3mo.com/`** — your personal site. The account is one of four in a confirmed China-based GitHub repo-laundering operation (codenamed "Long Shadow"). Among the laundered repos under this account is `kyasbalme/Scrapbox`, which is a clone of a Japanese Shogi-AI project (you can see why your name surfaced — Scrapbox is a Nota Inc. product you're closely associated with through the Japanese tech-research community).

Practical effect: anyone investigating the `kyasbalme` GitHub account follows the website link to your real site. Your real reputation gets dragged into proximity to a laundering account.

**What I'm publishing in 48 hours.**
- The full investigation at `github.com/copyleftdev/long-shadow`
- Your name appears in the article only as the *victim* of the profile-website impersonation. I am NOT attributing any of the operator's actions to you.
- I would like to keep your name out of the public report entirely if you prefer — just reply and I'll redact you. The forensic case stands without naming you.

**Asks.**
1. Confirm receipt (or just reply with "leave me out").
2. If you'd like the impersonation reported to GitHub, you can file at `https://github.com/contact/report-abuse` → "Impersonation". You have standing as the real holder of `blu3mo.com` and the real human being impersonated.
3. If there's specific framing you'd prefer in the publication, tell me.

Apologies for the unsolicited contact. The publication is happening either way; the question is just how to handle your name in it.

Best,
[Your name]

---

**Evidence reference:**
- `data/kraken/kyasbalme.json` — kraken identity-graph spider showing `profile.website = "http://blu3mo.com/"` on the `kyasbalme` account
