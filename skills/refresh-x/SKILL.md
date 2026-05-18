---
name: Refresh X
description: Fetch a tracked X/Twitter account's latest tweets and save the gist to memory
var: ""
tags: [social]
---
> **${var}** — The @handle to check (e.g. "@elonmusk", "vitalikbuterin"). **Required** — set this in aeon.yml or pass it when triggering the skill.

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid logging duplicate tweets.

## Steps

1. **Fetch the latest tweets for the specified account.** Use whichever path is available, in order:

   ```bash
   FROM_DATE=$(date -u -d "yesterday" +%Y-%m-%d 2>/dev/null || date -u -v-1d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)
   ACCOUNT="${var}"
   ACCOUNT="${ACCOUNT#@}"

   if [ -z "$ACCOUNT" ]; then
     echo "Error: var must be set to a Twitter handle (e.g. 'elonmusk')"
     exit 1
   fi
   ```

   **Path A — pre-fetched cache** (preferred — `scripts/prefetch-xai.sh` already covers `refresh-x` and writes the response to `.xai-cache/refresh-x.json`):
   ```bash
   cat .xai-cache/refresh-x.json 2>/dev/null | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
   ```

   **Path A error short-circuit:** if `.xai-cache/refresh-x.json` is missing AND `.xai-cache/refresh-x.json.error` exists, the prefetch failed (XAI api timeout, HTTP error, etc.). In that case **skip Paths B and C entirely** — Path B's curl call requires `$XAI_API_KEY` env-var expansion which the sandbox blocks (the historical failure mode that wrote a misleading "XAI_API_KEY not set" line into the log even when the key was set), and Path C's WebSearch path consistently returns 0 fresh per-account tweets when XAI is the real source of truth. Read the one-line reason from `.xai-cache/refresh-x.json.error`, jump straight to step 3 with status `REFRESH_X_PREFETCH_FAILED`, and include the prefetch error reason in the log + notification.

   **Path A truncation marker:** if `.xai-cache/refresh-x.json.truncated` exists, the cache was written but the XAI response hit the `max_output_tokens` ceiling — the cache is real but **incomplete**. Continue processing normally, but: (a) tag the status as `REFRESH_X_OK_TRUNCATED` (not plain `OK`) when logging; (b) append a single line to the notification: `⚠️ XAI cache truncated (output_tokens=N/max=M); results may be incomplete.` — read the values from the marker file (format `output_tokens=N reasoning_tokens=R max_output_tokens=M`).

   **Path B — X.AI API direct** (fallback for local runs where the sandbox does not block env-var expansion in curl headers — does NOT work inside GitHub Actions' Claude sandbox; the prefetch is the supported path there):
   ```bash
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for all tweets posted by @'"$ACCOUNT"' from '"$FROM_DATE"' to '"$TO_DATE"'. Return every tweet — not just popular ones. For each: the full tweet text, date/time posted, engagement stats (likes, retweets, replies), and the direct link (https://x.com/'"$ACCOUNT"'/status/ID). If it was a reply, note who it was replying to. If it was a quote tweet, include what was quoted. Return as a chronological list."}],
       "tools": [{"type": "x_search", "from_date": "'"$FROM_DATE"'", "to_date": "'"$TO_DATE"'"}]
     }'
   ```

   **Path C — WebSearch fallback** (use only when both cache and Path B are unavailable — coverage is partial because WebSearch favours older high-engagement tweets):
   Use the built-in WebSearch tool with `site:x.com/${ACCOUNT} after:${FROM_DATE}`. Note at the top of the log entry: "results compiled via WebSearch — coverage partial".

   Do **not** write a line claiming "XAI_API_KEY not set" — the data source on the cron path is the prefetch cache, not a live key inside the skill. If the cache is absent and there is no `.error` marker, that means the prefetch was never invoked for this skill (e.g. when refresh-x runs ad-hoc without going through `chain-runner.yml` / `aeon.yml`); in that case go to Path C, and log `REFRESH_X_NO_PREFETCH: prefetch not invoked`.

2. Summarize what was posted:
   - How many tweets/replies/quote tweets
   - Top themes and topics covered
   - Which tweets got the most engagement and why
   - Any threads or multi-tweet arcs
   - Tone/mood of the day (shitposting? serious? argumentative?)

3. Save the gist to memory/logs/${today}.md:
   ```
   ## Refresh X
   - **Account:** @ACCOUNT
   - **Source:** Path A (prefetch cache) | Path A truncated | Path B (direct XAI) | Path C (WebSearch) | prefetch failed (reason)
   - **Status:** REFRESH_X_OK | REFRESH_X_OK_TRUNCATED | REFRESH_X_PREFETCH_FAILED | REFRESH_X_NO_PREFETCH | REFRESH_X_EMPTY
   - **Tweets found:** N (X original, Y replies, Z quotes)
   - **Top themes:** theme1, theme2, theme3
   - **Best performing:** "[tweet excerpt]" — X likes, Y RTs
   - **Gist:** [2-3 sentence summary of what they were talking about and the vibe]
   ```

4. If there are tweets worth remembering (strong takes, announcements, threads), also note them in memory/MEMORY.md under a relevant section.

5. Send a brief summary via `./notify`:
   ```
   x refresh: @ACCOUNT posted N tweets yesterday
   top themes: theme1, theme2
   best: "[excerpt]" (X likes)
   ```

   If the status is `REFRESH_X_PREFETCH_FAILED`, send a one-line notification including the prefetch error reason (so persistent XAI outages are visible) instead of the normal summary. If the status is `REFRESH_X_OK_TRUNCATED`, append the truncation warning line described in step 1.

## Sandbox note

`scripts/prefetch-xai.sh` (case `refresh-x)`, lines 149-160) runs OUTSIDE the Claude sandbox and writes the XAI response — plus `.error` / `.truncated` marker files on failure — to `.xai-cache/refresh-x.json`. The skill's primary path is the cache read. The direct-curl Path B is kept for local-mode invocations where env-var expansion in curl headers works; on the GitHub Actions cron path the sandbox blocks `$XAI_API_KEY` expansion in curl headers, so Path B is **expected** to fail there and the cache or markers are the source of truth.

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key (consumed by the prefetch script, not by the skill directly on the cron path)
