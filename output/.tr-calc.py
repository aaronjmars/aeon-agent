price_now = 0.00001861637393
price_1d = 0.0000195656186
price_7d = 0.00001888702516
price_30d = 0.00001865999789

liq_now = 400875.84
liq_1d = 393636.205

vol_now = 59856.6774557402
vols_7 = [247224.310282593, 78281.4265222777, 61720.0314603942, 40852.2516340579, 63280.4119392557, 16788.9652773149]

buys_now = None  # fill from trades
sells_now = None
buys_1d = 41
sells_1d = 39


def pct(now, prior):
    return (now - prior) / prior * 100

print("24h price delta:", pct(price_now, price_1d))
print("7d price delta:", pct(price_now, price_7d))
print("30d price delta:", pct(price_now, price_30d))
print("liq 24h delta:", pct(liq_now, liq_1d))
mean7 = sum(vols_7) / len(vols_7)
print("mean7 vol:", mean7)
print("vol ratio:", vol_now / mean7)
