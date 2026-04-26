#!/usr/bin/env python3
"""
farm_watcher.py — periodic monitor for new activity from known farm operator
accounts. Catches newly-laundered repos within minutes of publication.

What it watches:
  - For each operator account in catalog/operators.csv: pull current public
    repos. Diff against previous state. Alert on new repos.
  - For DelbyIntelligence org: pull current repo count. Alert if it grows
    by more than N repos since last run.
  - For each sock-puppet email: re-query GitHub commit-search. Alert on new
    owner accounts that ever-appear (= new operator account discovered).

Usage:
  GITHUB_TOKEN=$(gh auth token) \\
    python3 farm_watcher.py --workdir /var/lib/farmwatch

Exit codes:
  0 = no new findings
  1 = new findings (ALERT)
  2 = setup error

Cron deployment:
  */15 * * * * GITHUB_TOKEN=... /usr/bin/python3 /path/to/farm_watcher.py \\
    --workdir /var/lib/farmwatch \\
    --webhook https://hooks.slack.com/...

Requires: Python 3.9+, requests. Reads operators.csv from the catalog/ dir.
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

GH = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "farm_watcher/1.0",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def gh(path, **params):
    r = requests.get(f"{GH}/{path.lstrip('/')}", headers=HEADERS, params=params, timeout=30)
    if r.status_code == 403 and "rate limit" in r.text.lower():
        print(f"rate-limited: {r.text[:200]}", file=sys.stderr)
        sys.exit(2)
    r.raise_for_status()
    return r.json()


def list_repos(account, account_type):
    out, page = [], 1
    while True:
        path = f"orgs/{account}/repos" if account_type == "Organization" else f"users/{account}/repos"
        try:
            items = gh(path, per_page=100, page=page)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None  # account deleted/suspended
            raise
        if not items:
            break
        out.extend(items)
        page += 1
        if len(items) < 100:
            break
        time.sleep(0.5)
    return [
        {
            "name": r["name"],
            "full_name": r["full_name"],
            "created_at": r["created_at"],
            "pushed_at": r["pushed_at"],
            "stars": r["stargazers_count"],
            "language": r.get("language"),
            "fork": r.get("fork", False),
            "default_branch": r.get("default_branch"),
        }
        for r in out
    ]


def email_reach(email):
    try:
        r = gh("search/commits", q=f"author-email:{email}", per_page=100)
    except requests.HTTPError as e:
        return {"error": str(e)}
    items = r.get("items", [])
    return {
        "total_count": r.get("total_count"),
        "owners": sorted({i["repository"]["owner"]["login"] for i in items}),
        "repos": sorted({i["repository"]["full_name"] for i in items}),
    }


def load_operators(catalog_csv):
    accounts = []
    with open(catalog_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            accounts.append(
                {
                    "cluster": row["cluster"],
                    "account": row["account"],
                    "type": row["account_type"],
                }
            )
    return accounts


def load_sockpuppets(catalog_csv):
    emails = []
    with open(catalog_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row["email"]
            # Skip preserved-upstream emails (real authors, not sock-puppets)
            if "preserved upstream" in row.get("evidence_file", "").lower():
                continue
            if email.endswith(("@allenai.org", "@anthropic.local")):
                # We know these; first is real, second is impersonation.
                # Watch the impersonation but not the real one.
                if email.endswith("@anthropic.local"):
                    emails.append(email)
                continue
            emails.append(email)
    return emails


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--workdir", required=True)
    parser.add_argument(
        "--operators-csv",
        default=None,
        help="path to catalog/operators.csv (default: relative to this script)",
    )
    parser.add_argument(
        "--sockpuppets-csv",
        default=None,
        help="path to catalog/sock_puppet_emails.csv (default: relative to this script)",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--webhook", default=None)
    parser.add_argument(
        "--skip-email-reach",
        action="store_true",
        help="don't query the commit search for sock-puppet emails (slow, rate-limited)",
    )
    args = parser.parse_args()

    if not TOKEN:
        sys.exit("GITHUB_TOKEN not set")

    here = Path(__file__).resolve().parent.parent
    operators_csv = Path(args.operators_csv) if args.operators_csv else here / "catalog" / "operators.csv"
    sockpuppets_csv = (
        Path(args.sockpuppets_csv) if args.sockpuppets_csv else here / "catalog" / "sock_puppet_emails.csv"
    )

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    state_file = workdir / "state.json"
    prev = json.loads(state_file.read_text()) if state_file.exists() else {}
    prev_repos = prev.get("repos_by_account", {})
    prev_emails = prev.get("emails", {})

    operators = load_operators(operators_csv)
    sockpuppets = load_sockpuppets(sockpuppets_csv)

    new_state = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "repos_by_account": {},
        "emails": {},
        "alerts": [],
    }

    # 1. Watch operator accounts for new repos
    for op in operators:
        try:
            repos = list_repos(op["account"], op["type"])
        except Exception as e:
            new_state["repos_by_account"][op["account"]] = {"error": str(e)}
            continue
        if repos is None:
            new_state["repos_by_account"][op["account"]] = {"deleted_or_suspended": True}
            if op["account"] in prev_repos and "deleted_or_suspended" not in prev_repos[op["account"]]:
                new_state["alerts"].append(
                    {
                        "kind": "account_disappeared",
                        "account": op["account"],
                        "cluster": op["cluster"],
                    }
                )
            continue
        new_state["repos_by_account"][op["account"]] = {"count": len(repos), "repos": repos}
        prev_names = {r["name"] for r in prev_repos.get(op["account"], {}).get("repos", [])}
        new_names = {r["name"] for r in repos}
        added = sorted(new_names - prev_names)
        if added and op["account"] in prev_repos:  # only alert if we have a baseline
            new_state["alerts"].append(
                {
                    "kind": "new_repos_on_known_operator",
                    "account": op["account"],
                    "cluster": op["cluster"],
                    "added_repos": added,
                }
            )
        time.sleep(1.5)

    # 2. Watch sock-puppet email reach
    if not args.skip_email_reach:
        for email in sockpuppets:
            try:
                reach = email_reach(email)
            except Exception as e:
                new_state["emails"][email] = {"error": str(e)}
                continue
            new_state["emails"][email] = reach
            prev_owners = set(prev_emails.get(email, {}).get("owners", []))
            new_owners = set(reach.get("owners", []))
            added_owners = sorted(new_owners - prev_owners)
            if added_owners and email in prev_emails:
                new_state["alerts"].append(
                    {
                        "kind": "new_operator_account_via_email",
                        "email": email,
                        "new_owner_accounts": added_owners,
                    }
                )
            time.sleep(35)  # respect commit-search secondary rate limit

    state_file.write_text(json.dumps(new_state, indent=2))

    if args.json:
        print(json.dumps(new_state, indent=2))
    else:
        print(f"== farm_watcher snapshot {new_state['captured_at']} ==")
        for op in operators:
            entry = new_state["repos_by_account"].get(op["account"], {})
            count = entry.get("count", "?")
            note = ""
            if entry.get("deleted_or_suspended"):
                note = " [DELETED/SUSPENDED]"
            elif "error" in entry:
                note = f" [error: {entry['error'][:80]}]"
            print(f"  [{op['cluster']}] {op['account']:30s} repos={count}{note}")
        if not args.skip_email_reach:
            print()
            print("== sock-puppet email reach ==")
            for email in sockpuppets:
                e = new_state["emails"].get(email, {})
                if "error" in e:
                    print(f"  {email}: error")
                else:
                    print(
                        f"  {email}: {e.get('total_count', 0)} commits "
                        f"across {len(e.get('owners', []))} owner accounts"
                    )
        if new_state["alerts"]:
            print()
            print(f"!!! ALERTS ({len(new_state['alerts'])}):")
            for a in new_state["alerts"]:
                print(f"  {a['kind']}: {a}")
        else:
            print()
            print("(no new alerts since previous run)")

    if args.webhook and new_state["alerts"]:
        import subprocess
        subprocess.run(
            [
                "curl", "-sS", "-X", "POST",
                "-H", "content-type: application/json",
                "-d", json.dumps({"alerts": new_state["alerts"]}),
                args.webhook,
            ],
            check=False,
        )

    sys.exit(1 if new_state["alerts"] else 0)


if __name__ == "__main__":
    main()
