#!/usr/bin/env bash
# Section 7 of REPLAY.md — paginate all DelbyIntelligence repos.
set -u
out=${1:-/tmp/delby_full.jsonl}
: > "$out"
for p in $(seq 1 32); do
  gh api "orgs/DelbyIntelligence/repos?per_page=100&page=$p&sort=created&direction=desc" \
    --jq '.[] | {n: .name, c: .created_at, p: .pushed_at, s: .stargazers_count, l: .language, h: .has_pages, d: .description}' >> "$out"
  echo "page $p done — total rows: $(wc -l < $out)" >&2
  sleep 1.2
done
