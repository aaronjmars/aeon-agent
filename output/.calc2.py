import json

d = json.load(open('output/.gt-trades.json'))
trades = d['data']
buy_vol = sum(float(t['attributes']['volume_in_usd']) for t in trades
              if t['attributes']['volume_in_usd'] and float(t['attributes']['volume_in_usd']) >= 1000
              and t['attributes']['kind'] == 'buy')
sell_vol = sum(float(t['attributes']['volume_in_usd']) for t in trades
               if t['attributes']['volume_in_usd'] and float(t['attributes']['volume_in_usd']) >= 1000
               and t['attributes']['kind'] == 'sell')
print('whale buy vol', buy_vol, 'whale sell vol', sell_vol, 'net', buy_vol - sell_vol)
