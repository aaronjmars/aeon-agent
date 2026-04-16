---
name: fetch-tweets
description: Search X/Twitter for tweets about a token, keyword, username, or topic
var: ""
---
> **${var}** — Search query for X/Twitter. **Required** — set your query in aeon.yml.

Today is ${today}. Search X for tweets matching **${var}**.

## Important — no deduplication

**Do NOT deduplicate against `memory/logs/`.** Do not read prior `## Fetch Tweets` entries to filter out "already reported" tweets. Do not compute any SEEN_TWEETS set. If Grok returns a tweet URL that was reported yesterday, include it again today. Every run emits whatever Grok returns, unfiltered. Previous runs of this skill may show dedup language in the logs — that was an earlier behavior and has been removed. Ignore that pattern.

## Steps

1. **Build the search prompt for Grok.** Pass `${var}` to Grok **verbatim** as the search query. Do NOT narrow it to a single angle (e.g. don't force "crypto token only", don't inject a contract address, don't filter by chain). Let Grok interpret OR/AND operators in the var as-is. The goal is broad coverage — token mentions, repo mentions, handle mentions, general chatter, all of it.

2. **Search tweets — check pre-fetched cache first, then fall back to API.**

   The workflow pre-fetches X.AI results outside the sandbox before Claude starts. Always try the cache first:
   ```bash
   cat .xai-cache/fetch-tweets.json 2>/dev/null
   ```
   - If `.xai-cache/fetch-tweets.json` exists and contains valid JSON with tweet data, **use that data**. Parse the response to extract the tweet text:
     ```bash
     cat .xai-cache/fetch-tweets.json | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
     ```
   - If the cache file is missing or empty, **fall back to the direct API call** (this may fail inside the sandbox):
     ```bash
     FROM_DATE=$(date -u -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)
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
   - If both cache and direct API fail, **fall back to WebSearch**:
     - Use WebSearch with queries like `site:x.com "${var}"` and related variations
     - Extract any tweet URLs and summaries from the search results
     - If WebSearch also returns nothing, log `FETCH_TWEETS_EMPTY` and stop

3. **If no relevant tweets found** (no results, or API returns error/empty): log "FETCH_TWEETS_EMPTY" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

4. **Save the results** to `memory/logs/${today}.md`. Include tweet URLs, handles, and engagement so downstream skills (like `tweet-allocator`) can consume them. Do **NOT** add a "Deduplicated" or "already reported" field. Log every tweet Grok returned.

5. **Send a notification via `./notify`** with up to 10 tweets (all of them — never "new since last report", always just "top tweets"). Each tweet MUST include a clickable link. Use Telegram Markdown link format: `[link text](url)`.

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

## Sandbox note

The X.AI API requires authentication (`XAI_API_KEY` in headers), which is blocked inside the Claude sandbox. The workflow runs `scripts/prefetch-xai.sh` **before** Claude starts — this script calls the X.AI API with full env var access and saves results to `.xai-cache/fetch-tweets.json`. Always read the cache first; only attempt the direct API call as a fallback.

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key (required for pre-fetch; direct calls fail inside sandbox)
