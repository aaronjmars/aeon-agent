import json

price_now = 0.0000328153017257836
price_1d = 0.0000199188
price_7d = 0.00001834779557
price_30d = 0.0000377653636900082

liq_now = 1845262.121
liq_1d = 1322920.0339

vol_now = 410054.813551098
vol_1d = 108494.424593603

buys_now, sells_now = 441, 368
buys_1d, sells_1d = 179, 95


def pct(new, old):
    return (new - old) / old * 100


print('1d price delta %.3f%%' % pct(price_now, price_1d))
print('7d price delta %.3f%%' % pct(price_now, price_7d))
print('30d price delta %.3f%%' % pct(price_now, price_30d))
print('liq 24h delta %.3f%%' % pct(liq_now, liq_1d))

d = json.load(open('output/.gt-ohlcv-day.json'))
candles = d['data']['attributes']['ohlcv_list']
last7 = [c[5] for c in candles[1:8]]
print('last7 vols', last7)
mean7 = sum(last7) / len(last7)
print('mean7', mean7)
print('vol ratio', vol_now / mean7)

ratio_now = buys_now / sells_now
ratio_1d = buys_1d / sells_1d
print('buy/sell ratio now', ratio_now, 'yest', ratio_1d)

ds_price = 0.00003322
dev = abs(ds_price - price_now) / price_now * 100
print('ds deviation %.3f%%' % dev)
