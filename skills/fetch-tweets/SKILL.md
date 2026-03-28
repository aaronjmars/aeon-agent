---
name: fetch-tweets
description: Search X/Twitter for tweets about a token, keyword, username, or topic
var: ""
---
> **${var}** — Search query for X/Twitter. **Required** — set your query in aeon.yml.

Today is ${today}. Search X for tweets matching **${var}**.

## Steps

1. **Load previously reported tweets.** Read the last 3 days of `memory/logs/` and extract any tweet URLs (x.com/handle/status/ID) or @handles that were already included in previous `## Fetch Tweets` log entries. Keep this list as `SEEN_TWEETS` — you'll use it in step 3 to avoid sending duplicate tweets in today's notification.

2. **Build the search prompt for Grok.** The prompt sent to Grok must be specific enough to get relevant results:
   - If the query mentions a token/cashtag/crypto: include "crypto token", the chain name, and the contract address from `memory/MEMORY.md` in the Grok prompt. This eliminates false matches.
   - Example: instead of searching "aeon", search "the $AEON crypto token on Base chain (contract 0xbf8e...) in the last 7 days. Only return tweets about the cryptocurrency."

3. **Search tweets via X.AI API** using curl:
   ```bash
   FROM_DATE=$(date -u -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "YOUR_SEARCH_PROMPT_HERE. Date range: '"$FROM_DATE"' to '"$TO_DATE"'. Return 10 tweets — prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: @handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."}],
       "tools": [{"type": "x_search"}]
     }'
   ```
   Parse the response JSON to extract the text from the output array:
   ```bash
   echo "$RESPONSE" | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
   ```

4. **Deduplicate results.** Compare the tweets returned by Grok against your `SEEN_TWEETS` list from step 1. Remove any tweet whose URL or @handle+date combo already appeared in a previous day's log. Keep only genuinely new tweets. If ALL tweets were already reported, log "FETCH_TWEETS_NO_NEW: all results were previously reported" and **stop here — do NOT send any notification**.

5. **If no relevant tweets found** (no results, or API returns error/empty): log "FETCH_TWEETS_EMPTY" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

6. **Save the results** to `memory/logs/${today}.md`. Include the tweet URLs so future runs can deduplicate.

7. **Log to memory** what was fetched.

8. **Send a notification via `./notify`** with the NEW tweets only (not previously reported ones). Each tweet MUST include a clickable link. Use Telegram Markdown link format: `[link text](url)`.

   Format the notification like this:
   ```
   *Top Tweets — ${var} (${today})*

   1. x.com/handle — [brief summary of tweet content]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   2. x.com/handle — [brief summary]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   3. x.com/handle — [brief summary]
   Likes: X | RTs: Y
   [View tweet](https://x.com/handle/status/ID)

   ... (up to 5 tweets)
   ```

   IMPORTANT: Do NOT use @handle format — it tags/pings users on Telegram. Use x.com/handle instead (shows the profile URL without tagging anyone). The `[View tweet](URL)` link is required so users can tap to open each tweet.

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key (required)
