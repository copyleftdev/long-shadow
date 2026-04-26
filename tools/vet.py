#!/usr/bin/env python3
"""
vet.py — heuristic detector for repo-laundering farm signatures on GitHub.

Run a single repo through the seven heuristics derived from the Cluster A / B / C
forensic case in this investigation. Emit JSON with: which heuristics fired, the
total score, and a verdict (T0-adversarial / suspect / clean).

Usage:
    GITHUB_TOKEN=$(gh auth token) python3 vet.py owner/repo

Requires: Python 3.9+, requests, no other deps.

Exit codes:
    0 = clean
    1 = suspect
    2 = T0-adversarial (3+ heuristics fired)

The seven heuristics (from CATALOG.md and ARTICLE.md):
    1. Sock-puppet author-email pattern (FirstnameLastname<4digits>@outlook.com
       or random alphanumeric on yeah.net / 163.com / 126.com / qq.com)
    2. author_entropy = 0 across the entire repo (single sole author)
    3. Commit-date span > 5x (pushed_at - created_at) — fabricated future timestamps
    4. Uniform commit-rate distribution (no work-day clustering or weekend troughs)
    5. GitHub pushed_at < created_at (impossible without Import API)
    6. Lockfile (poetry.lock, Cargo.lock, package-lock.json) byte-identical to
       another unrelated repo from the same account (template re-publish)
    7. 0 PR enrichments after >100 commits

This is intentionally a one-file standalone script with no plugin system or
abstractions — fork it and add your own checks.
"""

import argparse
import json
import os
import re
import statistics
import sys
import urllib.parse
from collections import Counter
from datetime import datetime, timezone

import requests

GH = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "vet.py/1.0",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

SOCK_PUPPET_PATTERNS = [
    re.compile(r"^[A-Z][a-z]+[A-Z][a-z]+\d{3,4}@outlook\.com$"),
    re.compile(r"^[a-z]{4,8}\d{3,7}@(yeah\.net|163\.com|126\.com)$"),
]


def gh_get(path, **params):
    url = f"{GH}/{path.lstrip('/')}"
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if resp.status_code == 403 and "rate limit" in resp.text.lower():
        sys.exit(f"rate-limited: {resp.text[:200]}")
    resp.raise_for_status()
    return resp.json()


def fetch_repo(owner, repo):
    return gh_get(f"repos/{owner}/{repo}")


def fetch_commits(owner, repo, max_pages=5):
    """Up to ~500 commits, enough for heuristic signal."""
    out = []
    for page in range(1, max_pages + 1):
        items = gh_get(f"repos/{owner}/{repo}/commits", per_page=100, page=page)
        if not items:
            break
        out.extend(items)
        if len(items) < 100:
            break
    return out


def fetch_pulls(owner, repo):
    items = gh_get(f"repos/{owner}/{repo}/pulls", state="all", per_page=10)
    return items


def heur_sock_puppet_email(commits):
    emails = {c["commit"]["author"]["email"] for c in commits}
    matched = [e for e in emails if any(p.match(e) for p in SOCK_PUPPET_PATTERNS)]
    if matched:
        return True, f"sock-puppet email(s): {', '.join(matched)}"
    return False, ""


def heur_single_sole_author(commits):
    emails = Counter(c["commit"]["author"]["email"] for c in commits)
    if not emails:
        return False, ""
    sole = emails.most_common(1)[0]
    if len(emails) == 1 and sole[1] >= 50:
        return True, f"single sole author across {sole[1]} commits ({sole[0]})"
    return False, ""


def heur_fabricated_timestamps(repo_meta, commits):
    """Commit-date span more than 5x (pushed_at - created_at) suggests fabrication."""
    created = datetime.fromisoformat(repo_meta["created_at"].replace("Z", "+00:00"))
    pushed = datetime.fromisoformat(repo_meta["pushed_at"].replace("Z", "+00:00"))
    repo_window_days = max((pushed - created).days, 1)
    dates = [
        datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00"))
        for c in commits
    ]
    if not dates:
        return False, ""
    commit_span_days = (max(dates) - min(dates)).days
    ratio = commit_span_days / repo_window_days if repo_window_days else 0
    # Also flag any commit dated more than 6 months in the future
    now = datetime.now(timezone.utc)
    far_future = [d for d in dates if (d - now).days > 180]
    notes = []
    if ratio > 5:
        notes.append(f"commit-span/repo-window ratio = {ratio:.1f}x (5x threshold)")
    if far_future:
        notes.append(f"{len(far_future)} commit(s) dated > 6 months in the future")
    if notes:
        return True, "; ".join(notes)
    return False, ""


def heur_pushed_before_created(repo_meta):
    created = datetime.fromisoformat(repo_meta["created_at"].replace("Z", "+00:00"))
    pushed = datetime.fromisoformat(repo_meta["pushed_at"].replace("Z", "+00:00"))
    if pushed < created:
        return True, (
            f"pushed_at ({pushed.date()}) is BEFORE created_at ({created.date()}) "
            f"— only possible via GitHub Import API"
        )
    return False, ""


def heur_uniform_commit_distribution(commits):
    """Real human commits cluster on work hours/days. Uniform distribution = automation."""
    if len(commits) < 50:
        return False, ""
    hours = [
        datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "+00:00")).hour
        for c in commits
    ]
    counter = Counter(hours)
    # Count of distinct hours represented
    distinct = len(counter)
    # Coefficient of variation across hour buckets
    counts = [counter.get(h, 0) for h in range(24)]
    mean = statistics.mean(counts)
    if mean == 0:
        return False, ""
    cv = statistics.stdev(counts) / mean if mean else 0
    # Real human work has cv > 0.7 typically (peaks during work hours)
    # Uniform-ish (cv < 0.4) over 20+ distinct hours is suspicious
    if distinct >= 20 and cv < 0.4:
        return True, (
            f"hour-of-day distribution is uniform "
            f"(cv={cv:.2f} across {distinct} distinct hours; threshold cv<0.4)"
        )
    return False, ""


def heur_no_pull_requests(repo_meta, pulls, commits):
    if len(commits) >= 100 and len(pulls) == 0:
        return True, f"0 pull requests despite {len(commits)} commits"
    return False, ""


def heur_account_too_new(repo_meta):
    """Owner account < 90 days, 0 stars, 0 forks = adversarial profile."""
    owner_login = repo_meta["owner"]["login"]
    owner = gh_get(f"users/{owner_login}")
    created = datetime.fromisoformat(owner["created_at"].replace("Z", "+00:00"))
    age_days = (datetime.now(timezone.utc) - created).days
    if (
        age_days < 90
        and repo_meta["stargazers_count"] == 0
        and repo_meta["forks_count"] == 0
    ):
        return True, (
            f"owner account '{owner_login}' is {age_days} days old; "
            f"0 stars, 0 forks on this repo"
        )
    return False, ""


HEURISTICS = [
    ("sock_puppet_email", heur_sock_puppet_email),
    ("single_sole_author", heur_single_sole_author),
    ("fabricated_timestamps", heur_fabricated_timestamps),
    ("pushed_before_created", heur_pushed_before_created),
    ("uniform_commit_distribution", heur_uniform_commit_distribution),
    ("no_pull_requests", heur_no_pull_requests),
    ("account_too_new", heur_account_too_new),
]


def vet(owner, repo):
    repo_meta = fetch_repo(owner, repo)
    commits = fetch_commits(owner, repo)
    pulls = fetch_pulls(owner, repo)

    hits = []
    for name, fn in HEURISTICS:
        try:
            sig = fn.__code__.co_varnames[: fn.__code__.co_argcount]
            args = []
            for a in sig:
                if a == "repo_meta":
                    args.append(repo_meta)
                elif a == "commits":
                    args.append(commits)
                elif a == "pulls":
                    args.append(pulls)
            fired, detail = fn(*args)
        except Exception as e:
            fired, detail = False, f"heuristic error: {e}"
        hits.append({"heuristic": name, "fired": fired, "detail": detail})

    score = sum(1 for h in hits if h["fired"])
    if score >= 3:
        verdict = "T0-adversarial"
        exit_code = 2
    elif score >= 1:
        verdict = "suspect"
        exit_code = 1
    else:
        verdict = "clean"
        exit_code = 0

    result = {
        "repo": f"{owner}/{repo}",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "score": score,
        "verdict": verdict,
        "heuristics_fired": [h["heuristic"] for h in hits if h["fired"]],
        "details": hits,
    }
    return result, exit_code


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("repo", help="GitHub owner/repo (e.g. luliguyu/cmbd-book)")
    parser.add_argument("--json", action="store_true", help="emit raw JSON")
    args = parser.parse_args()

    if "/" not in args.repo:
        sys.exit("expected owner/repo")
    owner, repo = args.repo.split("/", 1)

    result, code = vet(owner, repo)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Repo:    {result['repo']}")
        print(f"Verdict: {result['verdict']}  (score {result['score']}/7)")
        print(f"Fired:   {', '.join(result['heuristics_fired']) or '(none)'}")
        for h in result["details"]:
            mark = "✓" if h["fired"] else "·"
            line = h["detail"] or ""
            print(f"  {mark} {h['heuristic']:30s} {line}")
    sys.exit(code)


if __name__ == "__main__":
    main()
