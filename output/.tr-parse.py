import json, datetime

with open("output/.gt-ohlcv-day.json") as f:
    d = json.load(f)
ohlcv = d["data"]["attributes"]["ohlcv_list"]
for row in ohlcv[:5]:
    ts = datetime.datetime.utcfromtimestamp(row[0]).strftime("%Y-%m-%d")
    print(ts, row)
print("count", len(ohlcv))
print("---30d ago (last element, oldest)---")
print(ohlcv[-1])
