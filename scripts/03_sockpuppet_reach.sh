#!/usr/bin/env bash
# Section 3 of REPLAY.md — query each sock-puppet email's GitHub reach.
set -u
emails=(
  "BensonJennifer6145@outlook.com"
  "DelacruzDawn1338@outlook.com"
  "kuqkz736@yeah.net"
  "sbolr9514@yeah.net"
  "bmqx9295@163.com"
  "io64083@yeah.net"
  "czmahaixuan@126.com"
  "naobingdz407945@163.com"
)
for e in "${emails[@]}"; do
  echo "===== $e ====="
  gh api -X GET search/commits -f q="author-email:$e" -f per_page=100 \
    --jq '{count: .total_count, owners: [.items[].repository.owner.login] | unique, repos: [.items[].repository.full_name] | unique}'
  sleep 35
done
