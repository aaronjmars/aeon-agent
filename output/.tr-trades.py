import json

with open("output/.gt-trades.json") as f:
    d = json.load(f)
trades = d["data"]
print("total trades returned:", len(trades))
buys = 0
sells = 0
whales = []
for t in trades:
    a = t["attributes"]
    kind = a.get("kind")  # buy/sell
    vol = float(a.get("volume_in_usd", 0) or 0)
    if kind == "buy":
        buys += 1
    elif kind == "sell":
        sells += 1
    if vol >= 1000:
        whales.append((kind, vol, a.get("price_from_in_usd"), a.get("price_to_in_usd"), a.get("block_timestamp")))

print("buys:", buys, "sells:", sells)
print("whale count:", len(whales))
whales_sorted = sorted(whales, key=lambda x: -x[1])
for w in whales_sorted[:5]:
    print(w)

# timestamp range
times = [t["attributes"].get("block_timestamp") for t in trades]
print("time range:", min(times), max(times))
