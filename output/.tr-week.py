import json, datetime

with open("output/.gt-ohlcv-day.json") as f:
    d = json.load(f)
ohlcv = d["data"]["attributes"]["ohlcv_list"]
for row in ohlcv[:8]:
    ts = datetime.datetime.utcfromtimestamp(row[0]).strftime("%Y-%m-%d")
    print(ts, "open=%.8f high=%.8f low=%.8f close=%.8f" % tuple(row[1:5]))
