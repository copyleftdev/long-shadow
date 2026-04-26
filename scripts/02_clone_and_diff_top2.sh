#!/usr/bin/env bash
# Section 1 of REPLAY.md — clone the two top farm repos and verify byte-identity.
set -e
WORK=${1:-/tmp/farm-verify}
mkdir -p $WORK
cd $WORK
[ -d Scrapbox  ] || git clone --quiet https://github.com/kyasbalme/Scrapbox.git
[ -d cmbd-book ] || git clone --quiet https://github.com/luliguyu/cmbd-book.git

echo "=== diff -rq (excluding .git) ==="
diff -rq --exclude=.git Scrapbox cmbd-book
echo
echo "=== File sizes (should match for everything except README.md) ==="
for f in poetry.lock LICENSE pyproject.toml AGENTS.md CLAUDE.md README.md; do
  s=$(wc -c < Scrapbox/$f 2>/dev/null || echo "-")
  c=$(wc -c < cmbd-book/$f 2>/dev/null || echo "-")
  printf "%-15s scrapbox=%s\tcmbd-book=%s\n" "$f" "$s" "$c"
done
