import os, json, urllib.request, sys

api_key = os.environ.get('XAI_API_KEY', '')
url = 'https://api.x.ai/v1/responses'
payload = {
    'model': 'grok-3-fast',
    'input': [{'role': 'user', 'content': 'Search for recent tweets about the $AEON crypto token on Base chain (contract address 0xbf8e8f0e8866a7052f948c16508644347c57aba3). Only return tweets about this specific cryptocurrency — not any other meaning of aeon. Date range: 2026-03-30 to 2026-04-06. Return 10 tweets — prioritize the most interesting, insightful, or highly-engaged posts. For each tweet include: @handle, the full text, date posted, engagement (likes/retweets if available), and the direct link (https://x.com/handle/status/ID). Return as a numbered list.'}],
    'tools': [{'type': 'x_search'}]
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
})
try:
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = resp.read().decode('utf-8')
        result = json.loads(body)
        # Save full JSON
        with open('xai_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        text_parts = []
        for item in result.get('output', []):
            if item.get('type') == 'message':
                for content in item.get('content', []):
                    if content.get('type') == 'output_text':
                        text_parts.append(content.get('text', ''))
        if text_parts:
            print('\n'.join(text_parts))
        else:
            print(body)
except Exception as e:
    print('ERROR:', e, file=sys.stderr)
    sys.exit(1)
