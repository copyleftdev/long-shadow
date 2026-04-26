#!/usr/bin/env bash
# Section 0 of REPLAY.md — total counts of AI-attribution signatures across GitHub.
# Output: a single JSON line written to stdout.
set -u
out=$(mktemp)
trap 'rm -f $out' EXIT

declare -A queries=(
  ["claude_trailer"]='"Co-Authored-By: Claude"'
  ["openhands_trailer"]='"Co-Authored-By: openhands"'
  ["copilot_swe_agent"]='author:copilot-swe-agent[bot]'
  ["devin_bot"]='author:devin-ai-integration[bot]'
  ["cursor_signature"]='"Generated with Cursor"'
  ["aider_signature"]='"aider:"'
  ["claude_code_anthropic_local"]='author-email:claude-code@anthropic.local'
)

echo '{'
first=1
for k in "${!queries[@]}"; do
  q="${queries[$k]}"
  count=$(gh api -X GET search/commits -f q="$q" --jq '.total_count' 2>/dev/null)
  [ $first -eq 0 ] && echo ','
  printf '  "%s": %s' "$k" "$count"
  first=0
  sleep 35  # respect secondary rate limit
done
echo
echo '}'
