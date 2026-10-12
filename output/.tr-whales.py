import json

with open("output/.gt-trades.json") as f:
    d = json.load(f)
trades = d["data"]
whales = []
for t in trades:
    a = t["attributes"]
    kind = a.get("kind")
    vol = float(a.get("volume_in_usd", 0) or 0)
    if vol >= 1000:
        if kind == "sell":
            price = float(a.get("price_from_in_usd"))
        else:
            price = float(a.get("price_to_in_usd"))
        whales.append((kind, vol, price, a.get("block_timestamp")))

whale_buys = sum(1 for w in whales if w[0] == "buy")
whale_sells = sum(1 for w in whales if w[0] == "sell")
print("whale buys:", whale_buys, "whale sells:", whale_sells, "total:", len(whales))
for w in sorted(whales, key=lambda x: -x[1])[:3]:
    print(w)
