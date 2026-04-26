#!/usr/bin/env python3
"""
star_watcher.py — periodic monitor for the bot-star service customer base.

What it does:
  - For each known bot account in catalog/operators.csv (cluster D), pull the
    list of repos they have starred. Diff against previous state. Newly-starred
    repos = newly-paying customers of the star-buying service.
  - For known customer repos in catalog/bot_star_customers.csv, track star
    counts over time. Spikes indicate fresh purchases.

Usage:
  GITHUB_TOKEN=$(gh auth token) \\
    python3 star_watcher.py --workdir /var/lib/farmwatch-stars

Exit codes:
  0 = no new findings
  1 = new findings (ALERT)
  2 = setup error
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
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "star_watcher/1.0"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def gh(path, **params):
    r = requests.get(f"{GH}/{path.lstrip('/')}", headers=HEADERS, params=params, timeout=30)
    if r.status_code == 403 and "rate limit" in r.text.lower():
        print(f"rate-limited: {r.text[:200]}", file=sys.stderr)
        sys.exit(2)
    r.raise_for_status()
    return r.json()


def list_starred(account, max_pages=5):
    out, page = [], 1
    while page <= max_pages:
        try:
            items = gh(f"users/{account}/starred", per_page=100, page=page)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
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
            "full_name": r["full_name"],
            "stars": r["stargazers_count"],
            "language": r.get("language"),
            "created_at": r["created_at"],
            "pushed_at": r["pushed_at"],
        }
        for r in out
    ]


def repo_meta(full_name):
    return gh(f"repos/{full_name}")


def load_bots(operators_csv):
    bots = []
    with open(operators_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["cluster"] == "D":
                bots.append(row["account"])
    return bots


def load_customers(customers_csv):
    customers = []
    with open(customers_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(row["customer_repo"])
    return customers


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--operators-csv", default=None)
    parser.add_argument("--customers-csv", default=None)
    parser.add_argument(
        "--star-spike-threshold",
        type=int,
        default=50,
        help="alert when a customer repo's star count grows by this many "
        "between runs (default 50)",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not TOKEN:
        sys.exit("GITHUB_TOKEN not set")

    here = Path(__file__).resolve().parent.parent
    operators_csv = (
        Path(args.operators_csv) if args.operators_csv else here / "catalog" / "operators.csv"
    )
    customers_csv = (
        Path(args.customers_csv)
        if args.customers_csv
        else here / "catalog" / "bot_star_customers.csv"
    )

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    state_file = workdir / "state.json"
    prev = json.loads(state_file.read_text()) if state_file.exists() else {}
    prev_starred = prev.get("starred_by_bot", {})
    prev_customer_stars = prev.get("customer_stars", {})

    bots = load_bots(operators_csv)
    customers = load_customers(customers_csv)

    new_state = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "starred_by_bot": {},
        "customer_stars": {},
        "alerts": [],
    }

    # 1. Watch bot starring activity for new customer repos
    for bot in bots:
        starred = list_starred(bot)
        if starred is None:
            new_state["starred_by_bot"][bot] = {"deleted_or_suspended": True}
            if bot in prev_starred and "deleted_or_suspended" not in prev_starred[bot]:
                new_state["alerts"].append({"kind": "bot_account_disappeared", "bot": bot})
            continue
        names = [r["full_name"] for r in starred]
        new_state["starred_by_bot"][bot] = {"count": len(names), "repos": names}
        prev_set = set(prev_starred.get(bot, {}).get("repos", []))
        added = sorted(set(names) - prev_set)
        if added and bot in prev_starred:
            new_state["alerts"].append(
                {
                    "kind": "bot_starred_new_repos",
                    "bot": bot,
                    "newly_starred": added,
                    "comment": "candidate-new-customer or candidate-new-farm-repo",
                }
            )
        time.sleep(2)

    # 2. Watch customer repo star counts for spikes
    for cust in customers:
        try:
            m = repo_meta(cust)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                new_state["customer_stars"][cust] = {"deleted": True}
                continue
            raise
        cur = m["stargazers_count"]
        new_state["customer_stars"][cust] = {"stars": cur, "checked_at": new_state["captured_at"]}
        prev_count = prev_customer_stars.get(cust, {}).get("stars")
        if prev_count is not None and cur - prev_count >= args.star_spike_threshold:
            new_state["alerts"].append(
                {
                    "kind": "customer_star_spike",
                    "customer": cust,
                    "previous_stars": prev_count,
                    "current_stars": cur,
                    "delta": cur - prev_count,
                }
            )
        time.sleep(1.5)

    state_file.write_text(json.dumps(new_state, indent=2))

    if args.json:
        print(json.dumps(new_state, indent=2))
    else:
        print(f"== star_watcher snapshot {new_state['captured_at']} ==")
        print()
        print("Bot accounts:")
        for bot in bots:
            entry = new_state["starred_by_bot"].get(bot, {})
            note = ""
            if entry.get("deleted_or_suspended"):
                note = " [DELETED/SUSPENDED]"
            print(f"  {bot:25s} starred={entry.get('count', '?')}{note}")
        print()
        print("Customer repo star counts:")
        for cust in customers:
            entry = new_state["customer_stars"].get(cust, {})
            stars = entry.get("stars", "?")
            note = " [DELETED]" if entry.get("deleted") else ""
            print(f"  {cust:50s} stars={stars}{note}")
        if new_state["alerts"]:
            print()
            print(f"!!! ALERTS ({len(new_state['alerts'])}):")
            for a in new_state["alerts"]:
                print(f"  {a['kind']}: {json.dumps(a)[:200]}")
        else:
            print()
            print("(no new alerts)")

    sys.exit(1 if new_state["alerts"] else 0)


if __name__ == "__main__":
    main()
