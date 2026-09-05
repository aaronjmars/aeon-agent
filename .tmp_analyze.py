import json
with open('/home/runner/.claude/projects/-home-runner-work-aeon-agent-aeon-agent/8bf9e6ef-c022-407a-a078-c1bd75b88d97/tool-results/bx4kmbj90.txt') as f:
    content = f.read()
content = content.split('\nHTTP:')[0]
data = json.loads(content)
trades = data['data']
whales = [t for t in trades if float(t['attributes']['volume_in_usd']) >= 1000]
whales.sort(key=lambda t: float(t['attributes']['volume_in_usd']), reverse=True)
for w in whales[:3]:
    a = w['attributes']
    kind = a['kind']
    price = a['price_from_in_usd'] if kind == 'sell' else a['price_to_in_usd']
    print(kind, round(float(a['volume_in_usd']), 2), price, a['block_timestamp'])
whale_buys = len([t for t in whales if t['attributes']['kind'] == 'buy'])
whale_sells = len([t for t in whales if t['attributes']['kind'] == 'sell'])
print('whale buys', whale_buys, 'whale sells', whale_sells)
