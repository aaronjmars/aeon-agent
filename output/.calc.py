import json

price_now = 0.0000198930551825478
price_1d = 0.00002198748493
price_7d = 0.0000199188
price_30d = 0.00002298948585

liq_now = 1348710.4097
liq_1d = 1425289.2894

vol_now = 36309.1165498584
vol_1d = 41763.4746243392

buys_now, sells_now = 65, 73
buys_1d, sells_1d = 67, 73


def pct(new, old):
    return (new - old) / old * 100


print('1d price delta %.4f%%' % pct(price_now, price_1d))
print('7d price delta %.4f%%' % pct(price_now, price_7d))
print('30d price delta %.4f%%' % pct(price_now, price_30d))
print('liq 24h delta %.4f%%' % pct(liq_now, liq_1d))

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
