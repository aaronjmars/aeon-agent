#!/bin/bash
# Prefetch recent tweets for each tracked account into .xai-cache/ before Claude runs.
# Reads handles from memory/topics/tracked-accounts.yml. Requires XAI_API_KEY.
# Sandbox note: this runs with full env access (outside the Claude sandbox), so the
# Authorization header expands correctly here — the skill then reads the cached JSON.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CACHE="$ROOT/.xai-cache"
CONFIG="$ROOT/memory/topics/tracked-accounts.yml"
mkdir -p "$CACHE"

if [ -z "${XAI_API_KEY:-}" ]; then
  echo "prefetch-xai-tweet-digest: XAI_API_KEY unset, skipping"
  exit 0
fi
if [ ! -f "$CONFIG" ]; then
  echo "prefetch-xai-tweet-digest: no config at $CONFIG, skipping"
  exit 0
fi

# Extract bare handles from the YAML (lines like "  - handle: foo")
HANDLES=$(grep -E '^\s*-\s*handle:' "$CONFIG" | sed -E 's/.*handle:\s*//' | tr -d ' ' )

for HANDLE in $HANDLES; do
  [ -z "$HANDLE" ] && continue
  echo "prefetch-xai-tweet-digest: fetching @$HANDLE"
  curl -m 60 -s -X POST "https://api.x.ai/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${XAI_API_KEY}" \
    -d "{
      \"model\": \"grok-4-1-fast\",
      \"input\": [{
        \"role\": \"user\",
        \"content\": \"Search X for the latest tweets from:${HANDLE} in the last 3 days. Return up to the 5 most interesting or substantive tweets. For each: full text, date, direct link (https://x.com/${HANDLE}/status/ID). Skip retweets of others.\"
      }],
      \"tools\": [{\"type\": \"x_search\"}]
    }" > "$CACHE/tweet-digest-${HANDLE}.json"
  echo "  -> $CACHE/tweet-digest-${HANDLE}.json ($(wc -c < "$CACHE/tweet-digest-${HANDLE}.json") bytes)"
done
