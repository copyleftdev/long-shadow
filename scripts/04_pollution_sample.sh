#!/usr/bin/env bash
# Section 11 of REPLAY.md — quantify pollution rate.
set -u
out=${1:-/tmp/pollution_sample.jsonl}
: > "$out"
for p in $(seq 1 10); do
  gh api -X GET search/commits \
    -f q='"Co-Authored-By: Claude"' \
    -f sort=author-date -f order=desc \
    -f per_page=100 -f page=$p \
    --jq '.items[] | {repo: .repository.full_name, owner: .repository.owner.login, sha: .sha, author_email: .commit.author.email, date: .commit.author.date}' >> "$out"
  sleep 5
done
echo "Total commits sampled: $(wc -l < $out)"
echo "Top 5 repos in sample:"
jq -r '.repo' "$out" | sort | uniq -c | sort -rn | head -5
echo "Far-future-dated commits (year 2027+):"
jq -r 'select(.date > "2027-01-01") | "\(.date)\t\(.repo)"' "$out" | sort -u | head -10
