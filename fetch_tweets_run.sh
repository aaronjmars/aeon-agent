#!/bin/bash
set -e

FROM_DATE=$(date -u -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)
TO_DATE=$(date -u +%Y-%m-%d)

SEARCH_PROMPT="Search for tweets about the AEON crypto token on Base chain (contract 0xbf8e8f0e8866a7052f948c16508644347c57aba3). Only return tweets about this specific cryptocurrency token, not unrelated uses of the word aeon. Date range: ${FROM_DATE} to ${TO_DATE}. Return 10 tweets prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: the handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."

PAYLOAD=$(jq -n \
  --arg prompt "$SEARCH_PROMPT" \
  '{
    model: "grok-3-fast",
    input: [{"role": "user", "content": $prompt}],
    tools: [{"type": "x_search"}]
  }')

curl -s -X POST "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d "$PAYLOAD" | tee /tmp/xai_response.json | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text'
