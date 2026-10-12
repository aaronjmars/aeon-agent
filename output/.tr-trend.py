import json, datetime

with open("output/.gt-ohlcv-day.json") as f:
    d = json.load(f)
ohlcv = d["data"]["attributes"]["ohlcv_list"]
highs = [(row[2], datetime.datetime.utcfromtimestamp(row[0]).strftime("%Y-%m-%d")) for row in ohlcv]
highs.sort(key=lambda x: -x[0])
print("top highs 30d:", highs[:5])
lows = [(row[3], datetime.datetime.utcfromtimestamp(row[0]).strftime("%Y-%m-%d")) for row in ohlcv]
lows.sort(key=lambda x: x[0])
print("lowest lows 30d:", lows[:5])
