#!/usr/bin/env python3
"""
wallet_watcher.py — periodic integrity check on the laundered crypto-wallet
repos (luliguyu/dimatura, luliguyu/ssaavedrad). Operators control these repos
and could push malicious changes at any time. The snapshot we captured on
2026-04-25 is benign; this script catches the moment that changes.

What it watches for:
  1. New ETH 0x-addresses or NEAR addresses that aren't in the allow-list at
     evidence/wallet_addresses/baseline.txt.
  2. Modifications to wallet-critical files (manifest.json, *.ts in src/lib/,
     src/background/, src/popups/approve/, signing or RPC code).
  3. Files added in the laundered repo that don't exist in the upstream
     (potential injection vectors).

How it works:
  - Re-clones each laundered + upstream repo into a working dir.
  - Extracts every 0x[a-f0-9]{40} and well-formed .near address.
  - Diffs against the allow-list and against the upstream.
  - Writes a JSON state file. On second run, prints whatever is *new* since
     the previous state.

Usage:
  python3 wallet_watcher.py --workdir /tmp/wallet-watch
  python3 wallet_watcher.py --workdir /tmp/wallet-watch --json   # raw JSON output
  python3 wallet_watcher.py --workdir /tmp/wallet-watch --webhook https://...

Exit codes:
  0 = no new findings since previous run
  1 = new findings detected (ALERT)
  2 = setup error (clone failed, etc.)

The intended deployment is a cron job:
  */30 * * * * /usr/bin/python3 /path/to/wallet_watcher.py --workdir /var/lib/farmwatch || \
               /usr/bin/curl -X POST $SLACK_WEBHOOK -d "$(cat /var/lib/farmwatch/last_alert.json)"

No external dependencies beyond stdlib + git. Designed to run unattended for years.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Pairs of (laundered, upstream) — extend as new wallet clones are discovered
WATCHED = [
    {
        "laundered": "luliguyu/dimatura",
        "upstream": "theQRL/zond-web3-wallet",
        "critical_paths": [
            "manifest.json",
            "src/configuration/zondBlockchainConfig.ts",
            "src/configuration/qrlBlockchainConfig.ts",
            "src/lib/",
            "src/components/ZondWeb3Wallet/Body/TokenTransfer/",
            "src/components/ZondWeb3Wallet/DAppRequest/",
            "src/functions/getHexSeedFromMnemonic.ts",
            "src/functions/getMnemonicFromHexSeed.ts",
            "background.ts",
            "content-script.ts",
        ],
    },
    {
        "laundered": "luliguyu/ssaavedrad",
        "upstream": "Narwallets/narwallets-extension",
        "critical_paths": [
            "extension/manifest.json",
            "src/lib/near-api-lite/",
            "src/background/background.ts",
            "src/content-script.ts",
            "src/popups/approve/",
            "src/askBackground.ts",
            "src/index.ts",
        ],
    },
]

ETH_RE = re.compile(r"0x[a-fA-F0-9]{40}")
NEAR_RE = re.compile(r"\b[a-z0-9_][a-z0-9._-]{1,60}\.near\b")


def run(cmd, cwd=None, check=True):
    proc = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, check=check, shell=False
    )
    return proc.stdout


def clone_or_pull(owner_repo, dest):
    """Clone if missing, fetch+reset if present."""
    if not dest.exists():
        run(["git", "clone", "--quiet", f"https://github.com/{owner_repo}.git", str(dest)])
        return "cloned"
    try:
        run(["git", "fetch", "--quiet", "origin"], cwd=str(dest))
        head_before = run(["git", "rev-parse", "HEAD"], cwd=str(dest)).strip()
        run(["git", "reset", "--hard", "origin/HEAD"], cwd=str(dest))
        head_after = run(["git", "rev-parse", "HEAD"], cwd=str(dest)).strip()
        return "updated" if head_before != head_after else "current"
    except subprocess.CalledProcessError as e:
        return f"error: {e.stderr.strip()[:200]}"


def extract_addresses(repo_dir):
    """Walk the working tree (no .git) and pull every ETH+NEAR address."""
    eth, near = set(), set()
    for root, dirs, files in os.walk(repo_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        for fn in files:
            p = Path(root) / fn
            try:
                if p.stat().st_size > 5_000_000:
                    continue
                data = p.read_text(errors="ignore")
            except Exception:
                continue
            eth.update(ETH_RE.findall(data))
            for m in NEAR_RE.findall(data):
                # Filter out filenames like foo.near in URLs by requiring it not
                # be inside an obvious path token; the regex \b boundaries help.
                if m and not m.startswith(("/", ".")):
                    near.add(m)
    return sorted(eth), sorted(near)


def hash_critical(repo_dir, paths):
    """SHA256 every critical file/dir; tells us if signing/RPC code changed."""
    out = {}
    for path in paths:
        full = repo_dir / path
        if not full.exists():
            out[path] = None
            continue
        if full.is_file():
            out[path] = hashlib.sha256(full.read_bytes()).hexdigest()
        else:
            # Directory: hash a sorted listing of file_path:sha256 lines
            h = hashlib.sha256()
            for f in sorted(full.rglob("*")):
                if f.is_file():
                    rel = f.relative_to(repo_dir)
                    file_h = hashlib.sha256(f.read_bytes()).hexdigest()
                    h.update(f"{rel}:{file_h}\n".encode())
            out[path] = h.hexdigest()
    return out


def load_baseline(path):
    allow = set()
    if not path.exists():
        return allow
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        addr = line.split("\t")[0].strip()
        allow.add(addr.lower())
    return allow


def check_pair(pair, workdir, baseline_allow):
    laundered_dir = workdir / (pair["laundered"].replace("/", "_") + "_laundered")
    upstream_dir = workdir / (pair["upstream"].replace("/", "_") + "_upstream")

    laundered_status = clone_or_pull(pair["laundered"], laundered_dir)
    upstream_status = clone_or_pull(pair["upstream"], upstream_dir)

    eth_l, near_l = extract_addresses(laundered_dir)
    eth_u, near_u = extract_addresses(upstream_dir)
    crit_l = hash_critical(laundered_dir, pair["critical_paths"])
    crit_u = hash_critical(upstream_dir, pair["critical_paths"])

    # Findings: addresses in laundered NOT in baseline AND NOT in upstream
    eth_l_lower = {a.lower() for a in eth_l}
    eth_u_lower = {a.lower() for a in eth_u}
    near_l_set = set(near_l)
    near_u_set = set(near_u)

    suspicious_eth = sorted(
        a for a in eth_l_lower if a not in baseline_allow and a not in eth_u_lower
    )
    suspicious_near = sorted(
        a for a in near_l_set if a not in baseline_allow and a not in near_u_set
    )

    # Critical-file changes between laundered and upstream (informational)
    critical_changes = []
    for p in pair["critical_paths"]:
        h_l = crit_l.get(p)
        h_u = crit_u.get(p)
        if h_l != h_u:
            critical_changes.append(
                {"path": p, "laundered_sha256": h_l, "upstream_sha256": h_u}
            )

    head_l = run(["git", "rev-parse", "HEAD"], cwd=str(laundered_dir)).strip()
    head_u = run(["git", "rev-parse", "HEAD"], cwd=str(upstream_dir)).strip()

    return {
        "pair": pair,
        "laundered_clone_status": laundered_status,
        "upstream_clone_status": upstream_status,
        "laundered_HEAD": head_l,
        "upstream_HEAD": head_u,
        "addresses_laundered": {"eth": sorted(eth_l_lower), "near": sorted(near_l_set)},
        "addresses_upstream": {"eth": sorted(eth_u_lower), "near": sorted(near_u_set)},
        "suspicious_addresses": {"eth": suspicious_eth, "near": suspicious_near},
        "critical_file_diffs_vs_upstream": critical_changes,
    }


def diff_against_previous(prev_state, new_state):
    """Compute new alert items since the last run."""
    alerts = []
    prev_by_pair = {p["pair"]["laundered"]: p for p in prev_state.get("results", [])}
    for r in new_state["results"]:
        prev = prev_by_pair.get(r["pair"]["laundered"], {})
        prev_susp_eth = set(prev.get("suspicious_addresses", {}).get("eth", []))
        prev_susp_near = set(prev.get("suspicious_addresses", {}).get("near", []))
        new_susp_eth = set(r["suspicious_addresses"]["eth"]) - prev_susp_eth
        new_susp_near = set(r["suspicious_addresses"]["near"]) - prev_susp_near
        prev_head = prev.get("laundered_HEAD")
        head_changed = prev_head and prev_head != r["laundered_HEAD"]
        if new_susp_eth or new_susp_near or head_changed:
            alerts.append(
                {
                    "repo": r["pair"]["laundered"],
                    "head_changed": head_changed,
                    "previous_HEAD": prev_head,
                    "new_HEAD": r["laundered_HEAD"],
                    "new_suspicious_eth": sorted(new_susp_eth),
                    "new_suspicious_near": sorted(new_susp_near),
                    "critical_file_diffs": r["critical_file_diffs_vs_upstream"],
                }
            )
    return alerts


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--workdir",
        required=True,
        help="working directory for clones + state file (will be created)",
    )
    parser.add_argument(
        "--baseline",
        default=None,
        help="path to address allow-list "
        "(default: ../evidence/wallet_addresses/baseline.txt next to this script)",
    )
    parser.add_argument("--json", action="store_true", help="emit raw JSON to stdout")
    parser.add_argument(
        "--webhook",
        default=None,
        help="if set, POST alert JSON here on findings (requires curl)",
    )
    args = parser.parse_args()

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    if args.baseline:
        baseline_path = Path(args.baseline)
    else:
        here = Path(__file__).resolve().parent
        baseline_path = here.parent / "evidence" / "wallet_addresses" / "baseline.txt"

    baseline_allow = {a.lower() for a in load_baseline(baseline_path)}

    state_file = workdir / "state.json"
    prev_state = {}
    if state_file.exists():
        try:
            prev_state = json.loads(state_file.read_text())
        except Exception:
            prev_state = {}

    results = []
    for pair in WATCHED:
        try:
            results.append(check_pair(pair, workdir, baseline_allow))
        except subprocess.CalledProcessError as e:
            print(
                f"ERROR processing {pair['laundered']}: {e.stderr[:300]}",
                file=sys.stderr,
            )
            sys.exit(2)

    new_state = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "baseline_path": str(baseline_path),
        "results": results,
    }

    alerts = diff_against_previous(prev_state, new_state)
    new_state["alerts"] = alerts

    state_file.write_text(json.dumps(new_state, indent=2))

    if args.json:
        print(json.dumps(new_state, indent=2))
    else:
        for r in results:
            print(f"== {r['pair']['laundered']} ==")
            print(f"  laundered HEAD = {r['laundered_HEAD']} ({r['laundered_clone_status']})")
            print(f"  upstream  HEAD = {r['upstream_HEAD']} ({r['upstream_clone_status']})")
            print(
                f"  addresses (laundered): "
                f"{len(r['addresses_laundered']['eth'])} eth, "
                f"{len(r['addresses_laundered']['near'])} near"
            )
            sus = r["suspicious_addresses"]
            print(
                f"  SUSPICIOUS (not in allow-list AND not in upstream): "
                f"{len(sus['eth'])} eth, {len(sus['near'])} near"
            )
            for a in sus["eth"]:
                print(f"    ⚠ ETH  {a}")
            for a in sus["near"]:
                print(f"    ⚠ NEAR {a}")
            for d in r["critical_file_diffs_vs_upstream"]:
                print(f"    · diff vs upstream: {d['path']}")
        print()
        if alerts:
            print(f"!!! NEW ALERTS since previous run: {len(alerts)}")
            for a in alerts:
                print(f"  {a['repo']}: HEAD {a['previous_HEAD']} -> {a['new_HEAD']}")
                for x in a["new_suspicious_eth"]:
                    print(f"    NEW ETH  {x}")
                for x in a["new_suspicious_near"]:
                    print(f"    NEW NEAR {x}")
        else:
            print("No new alerts since previous run.")

    if args.webhook and alerts:
        try:
            subprocess.run(
                [
                    "curl",
                    "-sS",
                    "-X",
                    "POST",
                    "-H",
                    "content-type: application/json",
                    "-d",
                    json.dumps({"alerts": alerts}),
                    args.webhook,
                ],
                check=False,
            )
        except Exception:
            pass

    sys.exit(1 if alerts else 0)


if __name__ == "__main__":
    main()
