---
name: Fetch Tweets
description: Search X/Twitter for tweets about a token, keyword, username, or topic
var: ""
tags: [social]
---
> **${var}** — Search query for X/Twitter. **Required** — set your query in aeon.yml.

Today is ${today}. Search X for tweets matching **${var}**.

## Steps

1. **Load previously-reported tweet URLs** from two sources, then union them into `SEEN_TWEETS`:
   - **Persistent seen-file** (`memory/fetch-tweets-seen.txt`) — if it exists, read all URLs. This file contains every tweet URL ever reported, preventing stale tweets from cycling back into notifications once log entries age out of the 3-day window.
   - **Last 3 days of `memory/logs/`** — grep each log file for lines matching `https://x.com/` (catches URLs not yet in the seen-file).
   
   You'll use `SEEN_TWEETS` in step 5 to filter duplicates.

2. **Build the search prompt for Grok.** Pass `${var}` to Grok **verbatim** as the search query. Do NOT narrow it to a single angle (e.g. don't force "crypto token only", don't inject a contract address, don't filter by chain). Let Grok interpret OR/AND operators in the var as-is. The goal is broad coverage — token mentions, repo mentions, handle mentions, general chatter, all of it.

3. **Search tweets.** Use whichever path is available:

   **Path A — pre-fetched cache** (preferred, when the workflow ran `scripts/prefetch-xai.sh`):
   ```bash
   cat .xai-cache/fetch-tweets.json 2>/dev/null | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
   ```

   **Path A error short-circuit:** if `.xai-cache/fetch-tweets.json` is missing AND `.xai-cache/fetch-tweets.json.error` exists, the prefetch failed (XAI api timeout, HTTP error, etc.). In that case **skip Paths B and C entirely** — Path B's curl call requires `$XAI_API_KEY` env-var expansion which the sandbox blocks, and Path C's WebSearch path consistently returns 0 fresh tweets when XAI is the actual source of truth. Read the one-line reason from `.xai-cache/fetch-tweets.json.error`, jump straight to step 4 with status `FETCH_TWEETS_PREFETCH_FAILED`, and include the prefetch error reason in the notification so operators can spot persistent XAI outages.

   **Path A truncation marker:** if `.xai-cache/fetch-tweets.json.truncated` exists, the cache was written but the XAI response hit the `max_output_tokens` ceiling — the cache is real but **incomplete** (e.g. May-12: cut mid-tweet-#2 with 4 thread_fetch calls consuming budget). Continue processing the cache normally, but: (a) set status to `FETCH_TWEETS_OK_TRUNCATED` (not plain `OK`) when logging; (b) append a single line to the notification: `⚠️ XAI cache truncated (output_tokens=N/max=M); results may be incomplete.` — read the values from the marker file (format `output_tokens=N reasoning_tokens=R max_output_tokens=M`). This distinguishes a genuinely-quiet tweet day from a budget-exhaustion day, so the operator doesn't mistake a short notification for low activity.

   **Path B — X.AI API** (fallback, use when `XAI_API_KEY` is set and cache is empty):
   ```bash
   FROM_DATE=$(date -u -d "yesterday" +%Y-%m-%d 2>/dev/null || date -u -v-1d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for ALL tweets about: ${var}. Date range: '"$FROM_DATE"' to '"$TO_DATE"'. Return at least 10 tweets (more if available) — prioritize the most interesting, insightful, or highly-engaged posts but also include smaller accounts. For each tweet include: @handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."}],
       "tools": [{"type": "x_search"}]
     }'
   ```
   Parse the response JSON to extract the text from the output array:
   ```bash
   echo "$RESPONSE" | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
   ```

   **Path C — WebSearch fallback** (use when both cache and XAI_API_KEY are unavailable):
   Use the built-in WebSearch tool to search for recent tweets. Construct a query like:
   `site:x.com "${query_terms}" after:${FROM_DATE}`
   Note at the top of the log entry: "XAI_API_KEY not available; results compiled via WebSearch". WebSearch rankings favour high-engagement older tweets — **prioritise results that mention a date within the last 48 hours** when possible.

4. **If no relevant tweets found** (no results, API error, or empty): log `FETCH_TWEETS_EMPTY` (or `FETCH_TWEETS_PREFETCH_FAILED` with the prefetch error reason if Path A short-circuited) to `memory/logs/${today}.md`, send a one-line notification via `./notify`, and stop.

   **Required log line:** every ending state in this step MUST log an explicit `- **Notification sent**: yes` (or `no (<reason>)`) line so heartbeat's 48h dedup / 3-day escalation logic can track this skill the same way it tracks every other one. Without this line heartbeat can't tell repeat failures apart and won't escalate when XAI is down for days.

   **Operator-actionable PREFETCH_FAILED variants** — when `.xai-cache/fetch-tweets.json.error` exists, parse the `HTTP <code>` prefix from its first line and pick the matching template (transient codes are noisy on a single hit, persistent codes need operator action TODAY):
   - **HTTP 401 / 403** (auth/credits): `🚨 Fetch Tweets — ${today}: XAI prefetch HTTP <code> (auth/credits exhausted). Operator action: rotate XAI_API_KEY or top up at https://console.x.ai. Downstream skills (tweet-allocator, token-report social section) will be empty until fixed.` — this is a **persistent** failure, log it explicitly so the next day's heartbeat can count consecutive-failure days.
   - **HTTP 429** (rate limit): `Fetch Tweets — ${today}: XAI prefetch HTTP 429 rate-limited; should self-resolve. If persistent across 3+ days, lower the daily fetch frequency in aeon.yml.`
   - **HTTP 5xx** (XAI service): `Fetch Tweets — ${today}: XAI prefetch HTTP <code> (XAI service issue); expect resolution within hours.`
   - **curl error / timeout / unreachable** (no HTTP code in error file): `Fetch Tweets — ${today}: XAI prefetch network/timeout (${reason}); no tweets fetched.`
   - **Generic fallback** (any other shape): `Fetch Tweets — ${today}: prefetch failed (${reason}); no tweets fetched.`

   Pick the variant by checking the prefix of the error file's first line. Do NOT try to be clever about partial matches — the prefetch script writes `HTTP <code> from XAI api:` (success path: errfile written at scripts/prefetch-xai.sh:117) or `curl error <N> after <M> attempts` (curl path: scripts/prefetch-xai.sh:100). Anything else falls through to the generic fallback.

5. **Deduplicate against `SEEN_TWEETS` from step 1.** Compare each candidate tweet URL against the collected set of already-reported URLs. Remove any tweet that was already reported in the last 3 days. If ALL tweets found are already in the recent logs: log "FETCH_TWEETS_NO_NEW: all results already reported" to `memory/logs/${today}.md`, send a one-line notification via `./notify` (e.g. `Fetch Tweets — ${today}: N results found, all already reported in last 3 days.`), include the same `- **Notification sent**: yes` line required in step 4, and stop.

5b. **Quarantine stock-watchlist spam.** Mark a tweet as spam (`SPAM_FLAG`) when it matches **all** of these signals — this is a tight, conservative filter, not a general low-quality cull:
   - Engagement is 0 likes **AND** 0 retweets **AND** 0 replies.
   - The tweet body treats `$AEON` as one entry in a list of stock tickers (3+ tickers, no link to `aeonframework`/`github.com/aaronjmars/aeon`, no mention of agents/framework/token contract).
   - The author handle has no prior `aeon`/`aeonframework` mention in `memory/fetch-tweets-seen.txt` or recent logs, AND looks like a stock-spam bot pattern (e.g. `FirstnameLastnameNNNNN` with trailing random digits, generic-influencer template handle).

   Quarantined tweets are **still** added to the seen-file in step 6b (so they don't recycle) and **still** logged in step 6 — but under a separate `### Filtered (spam)` subsection rather than the main numbered list. They are **excluded** from the notification in step 7 so the daily message stays signal-only. If filtering would leave fewer than 3 tweets in the notification, fall back to including borderline cases (rank by engagement) so the notification is never empty when real tweets exist.

6. **Save the results** (new tweets only) to `memory/logs/${today}.md`. Include the tweet URLs, handles, and engagement so future runs can deduplicate and so downstream skills (like `tweet-allocator`) can consume them. List quarantined spam tweets under a `### Filtered (spam)` subsection with the reason (e.g. "stock-watchlist spam, 0 engagement"), keeping the main numbered list signal-only.

6b. **Update the persistent seen-file** — append every new tweet URL, **including spam-flagged ones**, to `memory/fetch-tweets-seen.txt` (one per line). Create the file if it doesn't exist. Spam tweets get tracked here too so the same accounts don't cycle back into future notifications.

7. **Send a notification via `./notify`** with up to 10 NEW non-spam tweets (those that survived dedup AND were not quarantined in step 5b). Each tweet MUST include a clickable link. Use Telegram Markdown link format: `[link text](url)`.

   Format the notification like this:
   ```
   *Top Tweets — ${var} (${today})*

   1. x.com/handle — [brief summary of tweet content]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   2. x.com/handle — [brief summary]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   ... (up to 10 tweets)
   ```

   IMPORTANT: Do NOT use @handle format — it tags/pings users on Telegram. Use x.com/handle instead (shows the profile URL without tagging anyone). The `[View tweet](URL)` link is required so users can tap to open each tweet.

   After sending the notification, append the same `- **Notification sent**: yes` line to the log entry required in step 4 — so heartbeat sees a uniform marker across every exit path of this skill.

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key (optional; skill falls back to WebSearch when not set, but quality is lower)
