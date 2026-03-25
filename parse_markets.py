import json
import urllib.request

# Fetch volume data
url1 = "https://gamma-api.polymarket.com/markets?closed=false&order=volume24hr&ascending=false&limit=20"
with urllib.request.urlopen(url1) as resp:
    volume_data = json.loads(resp.read())

# Fetch new markets
url2 = "https://gamma-api.polymarket.com/markets?closed=false&order=startDate&ascending=false&limit=20"
with urllib.request.urlopen(url2) as resp:
    new_data = json.loads(resp.read())

def parse_prices(m):
    try:
        prices = json.loads(m.get('outcomePrices', '[]'))
        yes_p = float(prices[0]) * 100
        no_p = float(prices[1]) * 100 if len(prices) > 1 else 100 - yes_p
    except:
        yes_p, no_p = 0, 0
    return yes_p, no_p

def fmt_vol(v):
    if v >= 1_000_000:
        return f"${v/1_000_000:.1f}m"
    elif v >= 1_000:
        return f"${v/1_000:.0f}k"
    else:
        return f"${v:.0f}"

print("=== TOP MARKETS BY 24H VOLUME ===")
count = 0
for m in volume_data:
    vol = m.get('volumeNum', 0)
    vol24 = m.get('volume24hr', 0) or 0
    yes_p, no_p = parse_prices(m)
    liq = m.get('liquidityNum', 0)
    if vol < 1000 or (yes_p == 0 and no_p == 0):
        continue
    count += 1
    if count > 15:
        break
    q = m['question']
    print(f"{count}. \"{q}\"")
    print(f"   YES {yes_p:.1f}% / NO {no_p:.1f}% | 24h Vol: {fmt_vol(vol24)} | Total: {fmt_vol(vol)} | Liq: {fmt_vol(liq)}")

print()
print("=== NEW & NOTABLE ===")
skip_terms = ['up or down', 'updown', '5m', '15m', '1h', 'Up/Down']
for m in new_data:
    vol = m.get('volumeNum', 0)
    q = m['question']
    if vol < 1000:
        continue
    q_lower = q.lower()
    if any(t.lower() in q_lower for t in skip_terms):
        continue
    yes_p, no_p = parse_prices(m)
    start = m.get('startDateIso', '')
    print(f"- \"{q}\" | YES {yes_p:.1f}% | Vol: {fmt_vol(vol)} | Started: {start}")

print()
print("=== LIQUIDITY LEADERS ===")
by_liq = sorted(volume_data, key=lambda x: x.get('liquidityNum', 0), reverse=True)
for i, m in enumerate(by_liq[:5]):
    q = m['question']
    liq = m.get('liquidityNum', 0)
    yes_p, no_p = parse_prices(m)
    print(f"{i+1}. \"{q}\" | YES {yes_p:.1f}% | Liq: {fmt_vol(liq)}")
