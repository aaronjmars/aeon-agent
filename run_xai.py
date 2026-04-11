#!/usr/bin/env python3
import os
import json
import urllib.request
import sys

api_key = os.environ.get("XAI_API_KEY", "")
if not api_key:
    print("ERROR: XAI_API_KEY not set")
    sys.exit(1)

payload = {
    "model": "grok-3-fast",
    "input": [
        {
            "role": "user",
            "content": (
                "Search for recent tweets from 2026-04-04 to 2026-04-11 about: "
                "(1) the AEON crypto token on Base chain with contract address 0xbf8e8f0e8866a7052f948c16508644347c57aba3, "
                "OR (2) the GitHub repo github.com/aaronjmars/aeon which is an autonomous AI agent framework. "
                "Exclude any unrelated uses of the word aeon. "
                "Return 10 tweets prioritizing the most interesting and highly-engaged posts. "
                "For each tweet include: x.com/handle, full text, date, likes, retweets, and direct link https://x.com/handle/status/ID. "
                "Return as a numbered list."
            )
        }
    ],
    "tools": [{"type": "x_search"}]
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "https://api.x.ai/v1/responses",
    data=data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
        result = json.loads(body)
        for item in result.get("output", []):
            if item.get("type") == "message":
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        print(content["text"])
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
