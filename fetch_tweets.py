import os, json, urllib.request, sys

api_key = os.environ.get('XAI_API_KEY', '')
url = 'https://api.x.ai/v1/responses'
payload = {
    'model': 'grok-3-fast',
    'input': [{'role': 'user', 'content': 'Search X/Twitter for recent tweets (last 7 days, March 29 to April 5 2026) about the AEON crypto token on Base chain (contract 0xbf8e8f0e8866a7052f948c16508644347c57aba3 or cashtag AEON). Only return tweets about this specific cryptocurrency, not unrelated uses of the word aeon. Prioritize interesting, insightful, or highly-engaged posts. For each tweet include: handle, full text, date, likes, retweets, and direct URL. Return as a numbered list of up to 10 tweets.'}],
    'tools': [{'type': 'x_search'}]
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
})
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode('utf-8')
        result = json.loads(body)
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
