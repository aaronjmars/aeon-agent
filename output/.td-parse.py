import json
import datetime

with open('/tmp/tw-td.json') as f:
    data = json.load(f)
tweets = data.get('data', {}).get('tweets', [])
since = '2026-09-13'
for t in tweets:
    if t.get('isReply'):
        continue
    created = t.get('createdAt', '')
    try:
        dt = datetime.datetime.strptime(created, '%a %b %d %H:%M:%S %z %Y')
        d = dt.strftime('%Y-%m-%d')
    except Exception:
        d = created[:10]
    if d < since:
        continue
    text = (t.get('text') or '').replace('\n', ' ')[:300]
    row = [
        t.get('author', {}).get('userName', ''),
        d,
        str(t.get('likeCount')),
        str(t.get('retweetCount')),
        str(t.get('replyCount')),
        t.get('url', ''),
        text,
    ]
    print('\t'.join(row))
