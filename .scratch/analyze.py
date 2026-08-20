import json, re, math

markets = json.load(open('.scratch/cg-markets.json'))
trending_raw = json.load(open('.scratch/cg-trending.json'))
trending_ids = set()
trending_list = []
for t in trending_raw.get('coins', [])[:7]:
    item = t['item']
    trending_ids.add(item['id'])
    trending_list.append(item)

STABLE_IDS = {'tether','usd-coin','dai','first-digital-usd','usde','tusd','usdd','pyusd','fdusd','paxg'}

def is_stable(c):
    sym = c['symbol'].upper()
    name = c['name'].lower()
    if c['id'] in STABLE_IDS:
        return True
    if sym.startswith('USD') or sym.startswith('EUR') or sym.startswith('GBP'):
        return True
    if 'stablecoin' in name:
        return True
    return False

filtered = []
for c in markets:
    if is_stable(c):
        continue
    vol = c.get('total_volume') or 0
    if vol < 1_000_000:
        continue
    filtered.append(c)

print("total markets:", len(markets), "post-filter:", len(filtered))

# wrapped dupes dedup - keep only one of wbtc/weth/steth if it would dominate; skip for now, minor
WRAPPED = {'wrapped-bitcoin':'bitcoin','weth':'ethereum','staked-ether':'ethereum','wrapped-steth':'ethereum'}

filtered_dedup = [c for c in filtered if c['id'] not in WRAPPED]

def pct(c, key):
    v = c.get(key)
    return v if v is not None else 0

filtered_dedup.sort(key=lambda c: pct(c,'price_change_percentage_24h'), reverse=True)
winners = filtered_dedup[:10]
losers = sorted(filtered_dedup, key=lambda c: pct(c,'price_change_percentage_24h'))[:10]

def tags_for(c):
    tags = []
    pc24 = pct(c,'price_change_percentage_24h_in_currency') or pct(c,'price_change_percentage_24h')
    pc7d = c.get('price_change_percentage_7d_in_currency') or 0
    pc1h = c.get('price_change_percentage_1h_in_currency') or 0
    rank = c.get('market_cap_rank') or 9999
    mcap = c.get('market_cap') or 0
    vol = c.get('total_volume') or 0
    in_trend = c['id'] in trending_ids
    is_winner = c in winners
    is_loser = c in losers
    if in_trend and is_winner:
        tags.append('TRENDING+UP')
    if in_trend and is_loser:
        tags.append('TRENDING+DOWN')
    if pc24 > 15 and pc7d > 25:
        tags.append('BREAKOUT')
    if pc24 > 20 and pc7d < 0:
        tags.append('FADE')
    ratio = vol/mcap if mcap else 0
    if pc24 < -10 and ratio > 0.25:
        tags.append('CAPITULATION')
    if rank > 150 and pc24 > 30:
        tags.append('PUMP-RISK')
    if mcap < 50_000_000 and mcap > 0:
        tags.append('MICROCAP')
    if rank <= 20:
        tags.append('MAJOR')
    return tags[:2]

for c in winners + losers:
    c['_tags'] = tags_for(c)

for t in trending_list:
    # find matching market data if present
    match = next((c for c in filtered_dedup if c['id']==t['id']), None)
    t['_tags'] = tags_for(match) if match else []
    t['_match'] = match

# market pulse: top 100 by mcap post-filter
top100 = filtered_dedup[:100]
pos = sum(1 for c in top100 if pct(c,'price_change_percentage_24h') > 0)
top50 = filtered_dedup[:50]
median50 = sorted([pct(c,'price_change_percentage_24h') for c in top50])
med = median50[len(median50)//2]

print("PULSE top100 positive:", pos, "/", len(top100), "median top50 24h:", round(med,2))

def fmt_price(p):
    if p is None:
        return "N/A"
    if p < 0.01:
        return f"${p:.6f}"
    elif p < 1:
        return f"${p:.4f}"
    else:
        return f"${p:,.2f}"

def fmt_big(v):
    if v is None:
        return "N/A"
    if v >= 1e9:
        return f"${v/1e9:.1f}B"
    elif v >= 1e6:
        return f"${v/1e6:.0f}M"
    elif v >= 1e3:
        return f"${v/1e3:.0f}K"
    return f"${v:.0f}"

print("\n=== WINNERS ===")
for i,c in enumerate(winners,1):
    print(i, c['symbol'].upper(), c['name'], fmt_price(c['current_price']),
          round(pct(c,'price_change_percentage_24h'),1),
          round(c.get('price_change_percentage_7d_in_currency') or 0,1),
          round(c.get('price_change_percentage_1h_in_currency') or 0,1),
          fmt_big(c['total_volume']), c['market_cap_rank'], c['_tags'])

print("\n=== LOSERS ===")
for i,c in enumerate(losers,1):
    print(i, c['symbol'].upper(), c['name'], fmt_price(c['current_price']),
          round(pct(c,'price_change_percentage_24h'),1),
          round(c.get('price_change_percentage_7d_in_currency') or 0,1),
          round(c.get('price_change_percentage_1h_in_currency') or 0,1),
          fmt_big(c['total_volume']), c['market_cap_rank'], c['_tags'])

print("\n=== TRENDING ===")
for i,t in enumerate(trending_list,1):
    m = t['_match']
    price = m['current_price'] if m else t.get('data',{}).get('price')
    pc24 = pct(m,'price_change_percentage_24h') if m else None
    print(i, t['symbol'].upper(), t['name'], t.get('market_cap_rank'), fmt_price(price) if isinstance(price,(int,float)) else price, pc24, t['_tags'])
