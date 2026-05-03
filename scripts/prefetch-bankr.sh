#!/usr/bin/env bash
# Pre-fetch Bankr wallet verifications OUTSIDE the Claude sandbox.
# Called by the workflow before Claude runs. Saves results to .bankr-cache/
# so skills (tweet-allocator, distribute-tokens, etc.) can read cached wallet
# mappings instead of calling the Bankr Agent API from inside the sandbox —
# where curl with BANKR_API_KEY in headers fails due to env var expansion blocks.
#
# Usage: scripts/prefetch-bankr.sh <skill-name> [var]
# Runs automatically via the `for script in scripts/prefetch-*.sh` loop in aeon.yml.
#
# Failure surface (consumed by tweet-allocator + distribute-tokens):
#   .bankr-cache/verified-handles.json        — map of {handle: wallet|null}; success cache
#   .bankr-cache/verified-handles.json.error  — written ONLY on prefetch failure with reason:
#       BANKR_API_KEY_MISSING   secret not set on this repo
#       BANKR_API_KEY_INVALID   API returned 401/403 / "Unauthorized" / "Invalid API key"
#       BANKR_LOOKUPS_FAILED    every submit call errored (network/API outage); needs >=3 candidates
#   The marker is cleared at the start of every run, so its presence means the CURRENT run
#   failed — not a stale flag from yesterday. Downstream skills check the marker first and
#   emit a single dedup'd notification instead of one error per handle.
set -euo pipefail

SKILL="${1:-}"
VAR="${2:-}"

if [ -z "$SKILL" ]; then
  echo "bankr-prefetch: no skill arg, skipping"
  exit 0
fi

# Only run for skills that consume the Bankr wallet cache
case "$SKILL" in
  tweet-allocator|distribute-tokens) ;;
  *)
    echo "bankr-prefetch: nothing to do for skill '$SKILL'"
    exit 0
    ;;
esac

mkdir -p .bankr-cache
ERRFILE=".bankr-cache/verified-handles.json.error"

# Clear any stale error marker from a previous failed run.
# Presence of the marker after this script exits => CURRENT run failed.
rm -f "$ERRFILE"

if [ -z "${BANKR_API_KEY:-}" ]; then
  echo "BANKR_API_KEY_MISSING: secret not set on this repo — tweet-allocator and distribute-tokens cannot verify wallets via Bankr. Add BANKR_API_KEY in repo Settings -> Secrets, or run those skills knowing every handle will be marked unverified." > "$ERRFILE"
  echo "::warning::bankr-prefetch: BANKR_API_KEY not set — wrote $ERRFILE marker so tweet-allocator can short-circuit"
  exit 0
fi

# Collect candidate handles from multiple sources (in freshness order):
# 1. .xai-cache/fetch-tweets.json (if prefetch-xai.sh just ran)
# 2. memory/logs/${today}.md (if fetch-tweets ran earlier and logged handles)
TODAY=$(date -u +%Y-%m-%d)
HANDLES=""

if [ -f ".xai-cache/fetch-tweets.json" ]; then
  FROM_CACHE=$(jq -r '.output[]? | select(.type == "message") | .content[]? | select(.type == "output_text") | .text' \
    .xai-cache/fetch-tweets.json 2>/dev/null \
    | grep -oE '@[A-Za-z0-9_]{1,15}' \
    | sed 's/^@//' \
    | sort -u)
  HANDLES="$FROM_CACHE"
fi

if [ -f "memory/logs/${TODAY}.md" ]; then
  FROM_LOG=$(grep -oE 'x\.com/[A-Za-z0-9_]{1,15}' "memory/logs/${TODAY}.md" 2>/dev/null \
    | sed 's|x\.com/||' \
    | sort -u)
  HANDLES=$(printf "%s\n%s\n" "$HANDLES" "$FROM_LOG" | sort -u)
fi

# Exclude project-owned accounts (never allocate to these)
HANDLES=$(echo "$HANDLES" | grep -viE '^(aaronjmars|aeonframework)$' | grep -v '^$' | head -25)

if [ -z "$HANDLES" ]; then
  echo "bankr-prefetch: no candidate handles found in .xai-cache/ or memory/logs/${TODAY}.md — nothing to verify"
  # Write an empty cache so the skill knows the prefetch ran. NO error marker — this is a
  # legitimate no-op (no candidates), not a failure.
  echo "{}" > .bankr-cache/verified-handles.json
  exit 0
fi

COUNT=$(echo "$HANDLES" | wc -l | tr -d ' ')
echo "bankr-prefetch: looking up $COUNT handles on Bankr Agent API..."

# Start from an empty map (overwrite any stale cache)
echo "{}" > .bankr-cache/verified-handles.json

# Failure-mode trackers — populated by bankr_lookup, evaluated after the loop
# to decide whether to write the .error marker.
LOOKUPS=0
SUBMIT_FAILS=0
AUTH_ERROR_DETECTED=0

bankr_lookup() {
  local handle="$1"
  LOOKUPS=$((LOOKUPS + 1))

  local payload
  payload=$(jq -n --arg h "$handle" \
    '{prompt: ("what is the wallet address for @" + $h + " on base? just tell me the 0x address or say no wallet"),
      maxMode: {enabled: true, model: "claude-sonnet-4.6"}}')

  local submit_response
  submit_response=$(curl -s --max-time 30 -w "\n__HTTP_CODE__%{http_code}" -X POST "https://api.bankr.bot/agent/prompt" \
    -H "X-API-Key: $BANKR_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null) || {
    echo "bankr-prefetch: @$handle — submit failed (curl error)"
    SUBMIT_FAILS=$((SUBMIT_FAILS + 1))
    return 1
  }

  local http_code
  http_code=$(echo "$submit_response" | grep '__HTTP_CODE__' | sed 's/__HTTP_CODE__//')
  submit_response=$(echo "$submit_response" | grep -v '__HTTP_CODE__')

  # Detect auth errors — both via HTTP code and via response body.
  # First handle that returns 401/403 trips the global flag; subsequent lookups still
  # run but the marker is set after the loop. We do not bail early so a single transient
  # 401 doesn't poison a batch — but if every lookup hits the same auth error, that's
  # a clear signal the key is wrong/expired and the marker should fire.
  if [ "$http_code" = "401" ] || [ "$http_code" = "403" ] \
     || echo "$submit_response" | grep -qiE '"(error|message)"[[:space:]]*:[[:space:]]*"[^"]*(Unauthorized|Forbidden|Invalid API key|invalid_api_key)[^"]*"'; then
    echo "bankr-prefetch: @$handle — auth error (HTTP $http_code)"
    AUTH_ERROR_DETECTED=$((AUTH_ERROR_DETECTED + 1))
    SUBMIT_FAILS=$((SUBMIT_FAILS + 1))
    return 1
  fi

  local job_id
  job_id=$(echo "$submit_response" | jq -r '.jobId // .job_id // empty' 2>/dev/null)
  if [ -z "$job_id" ]; then
    echo "bankr-prefetch: @$handle — no jobId in response: $(echo "$submit_response" | head -c 200)"
    SUBMIT_FAILS=$((SUBMIT_FAILS + 1))
    return 1
  fi

  local result=""
  local status=""
  for _ in 1 2 3 4 5 6 7 8; do
    result=$(curl -s --max-time 15 "https://api.bankr.bot/agent/job/$job_id" \
      -H "X-API-Key: $BANKR_API_KEY" 2>/dev/null) || break
    status=$(echo "$result" | jq -r '.status // ""' 2>/dev/null)
    [ "$status" = "completed" ] && break
    [ "$status" = "failed" ] && break
    sleep 8
  done

  # Try several common response shapes; grab the first 0x address we can find
  local text wallet
  text=$(echo "$result" | jq -r '.result // .output // .response // .data.response // .messages[-1].content // ""' 2>/dev/null)
  wallet=$(echo "$text" | grep -oE '0x[a-fA-F0-9]{40}' | head -1)

  local tmpfile=".bankr-cache/tmp.$$.json"
  if [ -n "$wallet" ]; then
    jq --arg h "$handle" --arg w "$wallet" '. + {($h): $w}' .bankr-cache/verified-handles.json > "$tmpfile" \
      && mv "$tmpfile" .bankr-cache/verified-handles.json
    echo "bankr-prefetch: @$handle → $wallet"
  else
    jq --arg h "$handle" '. + {($h): null}' .bankr-cache/verified-handles.json > "$tmpfile" \
      && mv "$tmpfile" .bankr-cache/verified-handles.json
    echo "bankr-prefetch: @$handle → no wallet"
  fi
}

while IFS= read -r HANDLE; do
  [ -z "$HANDLE" ] && continue
  bankr_lookup "$HANDLE" || true
done <<< "$HANDLES"

VERIFIED=$(jq -r 'to_entries | map(select(.value != null)) | length' .bankr-cache/verified-handles.json 2>/dev/null || echo 0)
TOTAL=$(jq -r 'to_entries | length' .bankr-cache/verified-handles.json 2>/dev/null || echo 0)

# Decide whether to write the failure marker. Two distinct failure modes:
#   1. Auth error on every lookup attempt — key is wrong/expired (marker: BANKR_API_KEY_INVALID)
#   2. Submit failed on every attempt with >=3 candidates — network or API outage (marker: BANKR_LOOKUPS_FAILED)
# A non-zero VERIFIED count means at least one lookup round-tripped; do not write marker.
if [ "$VERIFIED" -eq 0 ] && [ "$AUTH_ERROR_DETECTED" -ge 1 ] && [ "$AUTH_ERROR_DETECTED" -eq "$LOOKUPS" ]; then
  echo "BANKR_API_KEY_INVALID: API rejected key on all $LOOKUPS lookup attempts (HTTP 401/403 or 'Unauthorized'/'Invalid API key' in body). Rotate BANKR_API_KEY at https://bankr.bot/api and re-add the secret." > "$ERRFILE"
  echo "::warning::bankr-prefetch: API key invalid — wrote $ERRFILE marker"
elif [ "$VERIFIED" -eq 0 ] && [ "$LOOKUPS" -ge 3 ] && [ "$SUBMIT_FAILS" -eq "$LOOKUPS" ]; then
  echo "BANKR_LOOKUPS_FAILED: $SUBMIT_FAILS/$LOOKUPS submit calls failed (network or Bankr API outage). Skill should treat this run as a no-op and re-fire on next schedule; the cache is empty." > "$ERRFILE"
  echo "::warning::bankr-prefetch: all $LOOKUPS submits failed — wrote $ERRFILE marker"
fi

echo "bankr-prefetch: done — $VERIFIED/$TOTAL handles have Bankr wallets"
ls -la .bankr-cache/ 2>/dev/null || true
