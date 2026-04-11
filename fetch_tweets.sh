#!/bin/bash
FROM_DATE=$(date -u -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -u -v-7d +%Y-%m-%d)
TO_DATE=$(date -u +%Y-%m-%d)
echo "Date range: $FROM_DATE to $TO_DATE"

SEARCH_PROMPT="Search for recent tweets about the AEON crypto token on Base chain (contract address 0xbf8e8f0e8866a7052f948c16508644347c57aba3) OR the GitHub repo https://github.com/aaronjmars/aeon (an autonomous AI agent framework). Date range: ${FROM_DATE} to ${TO_DATE}. Only return tweets clearly about this specific cryptocurrency token or the Aeon AI agent GitHub project — exclude any unrelated uses of the word aeon. Return 10 tweets — prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: handle (as x.com/handle), the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list."

PAYLOAD=$(jq -n \
  --arg prompt "$SEARCH_PROMPT" \
  '{
    model: "grok-3-fast",
    input: [{"role": "user", "content": $prompt}],
    tools: [{"type": "x_search"}]
  }')

RESPONSE=$(curl -s -X POST "https://api.x.ai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d "$PAYLOAD")

RESULT=$(echo "$RESPONSE" | jq -r '.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text' 2>/dev/null)

if [ -z "$RESULT" ]; then
  echo "Parse error or empty. Raw response:"
  echo "$RESPONSE" | head -c 3000
else
  echo "$RESULT"
fi
