---
name: fetch-tweets
description: Search X/Twitter for tweets about a token, keyword, username, or topic
var: ""
---
> **${var}** — Search query for X/Twitter. **Required** — set your query in aeon.yml.

Today is ${today}. Search X for tweets matching **${var}**.

## Important: Cashtag searches

If the var contains "cashtag" (e.g. "cashtag aeon OR $aeon token"), the search MUST focus on the **crypto token** with that ticker symbol. Specifically:
- Search for the dollar-sign cashtag (e.g. `$AEON`, `$MIROSHARK`)
- Focus on crypto/token/trading context — price discussion, buy/sell, charts, community
- EXCLUDE unrelated results (fandom ships, gaming, other meanings of the word)
- If results are mostly non-crypto, note that the token has low social visibility this period

## Steps

1. **Search tweets via X.AI API** using curl:
   ```bash
   FROM_DATE=$(date -u -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)
   TO_DATE=$(date -u +%Y-%m-%d)
   curl -s -X POST "https://api.x.ai/v1/responses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $XAI_API_KEY" \
     -d '{
       "model": "grok-4-1-fast",
       "input": [{"role": "user", "content": "Search X for: ${var}. Date range: '"$FROM_DATE"' to '"$TO_DATE"'. Return 10 tweets — prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: @handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."}],
       "tools": [{"type": "x_search", "from_date": "'"$FROM_DATE"'", "to_date": "'"$TO_DATE"'"}]
     }'
   ```
   Parse the response JSON to extract the assistant's output text.

2. **If no relevant tweets found** (no crypto-related results, or API returns error/empty): log "FETCH_TWEETS_EMPTY" to `memory/logs/${today}.md` and **stop here — do NOT send any notification**.

3. **Filter results** — if this is a cashtag search, discard any tweets that are clearly not about the crypto token (fandom, gaming, unrelated uses of the word).

4. **Save the results** to `memory/logs/${today}.md`.

5. **Log to memory** what was fetched.

6. **Send a notification via `./notify`** with a summary of the relevant tweets found.

## Environment Variables Required

- `XAI_API_KEY` — X.AI API key (required)
