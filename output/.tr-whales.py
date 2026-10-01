import json
AEON = '0xbf8e8f0e8866a7052f948c16508644347c57aba3'
d = json.load(open('output/.tr-trades.json'))
trades = d.get('data', [])
whales = []
for t in trades:
    a = t['attributes']
    kind = a.get('kind')
    vol = float(a.get('volume_in_usd', 0) or 0)
    if a.get('from_token_address', '').lower() == AEON:
        price = float(a.get('price_from_in_usd'))
    else:
        price = float(a.get('price_to_in_usd'))
    if vol >= 1000:
        whales.append((a.get('block_timestamp'), kind, vol, price))
whales.sort(key=lambda x: -x[2])
for w in whales:
    print(w)
print(len(whales))
ts = [t['attributes']['block_timestamp'] for t in trades]
print('range', min(ts), max(ts))
