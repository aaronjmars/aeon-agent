#!/bin/bash
FROM_DATE=$(date -u -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)
TO_DATE=$(date -u +%Y-%m-%d)
echo "Date range: $FROM_DATE to $TO_DATE" >&2

SEARCH_PROMPT="Search for tweets about: (1) the AEON crypto token on Base chain (contract 0xbf8e8f0e8866a7052f948c16508644347c57aba3) AND/OR (2) the GitHub repo aaronjmars/aeon (an autonomous AI agent framework). Only return tweets actually mentioning AEON as a crypto token or the aaronjmars/aeon GitHub project. Exclude unrelated uses of the word aeon. Date range: ${FROM_DATE} to ${TO_DATE}. Return 10 tweets - prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."

PAYLOAD=$(jq -n \
  --arg model "grok-3-fast" \
  --arg content "$SEARCH_PROMPT" \
  '{
    model: $model,
    input: [{"role": "user", "content": $content}],
    tools: [{"type": "x_search"}]
  }')

curl -s -X POST "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d "$PAYLOAD"
