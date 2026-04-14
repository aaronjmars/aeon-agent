#!/usr/bin/env python3
import os, json, sys
from datetime import datetime, timedelta
import urllib.request

api_key = os.environ.get("XAI_API_KEY", "")
if not api_key:
    print("ERROR: XAI_API_KEY not set", file=sys.stderr)
    sys.exit(1)

from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
to_date = datetime.utcnow().strftime("%Y-%m-%d")

search_prompt = (
    f"Search for tweets about: (1) the AEON crypto token on Base chain "
    f"(contract 0xbf8e8f0e8866a7052f948c16508644347c57aba3) AND/OR (2) the GitHub repo "
    f"aaronjmars/aeon (an autonomous AI agent framework). Only return tweets actually "
    f"mentioning AEON as a crypto token or the aaronjmars/aeon GitHub project. Exclude "
    f"unrelated uses of the word aeon. Date range: {from_date} to {to_date}. "
    f"Return 10 tweets - prioritize the most interesting, insightful, or highly-engaged posts. "
    f"For each tweet include: handle, the full text, date posted, engagement "
    f"(likes/retweets if available), and the direct link (https://x.com/handle/status/ID). "
    f"Return as a numbered list."
)

payload = json.dumps({
    "model": "grok-3-fast",
    "input": [{"role": "user", "content": search_prompt}],
    "tools": [{"type": "x_search"}]
}).encode()

req = urllib.request.Request(
    "https://api.x.ai/v1/responses",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    for item in data.get("output", []):
        if item.get("type") == "message":
            for block in item.get("content", []):
                if block.get("type") == "output_text":
                    print(block["text"])
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
