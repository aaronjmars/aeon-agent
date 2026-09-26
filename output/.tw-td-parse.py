import json
from datetime import datetime, timezone

SINCE = "2026-09-23"

with open("output/.tw-td.json") as f:
    data = json.load(f)

tweets = data.get("data", {}).get("tweets", [])
rows = []
for t in tweets:
    if t.get("isReply"):
        continue
    created = t.get("createdAt", "")
    try:
        d = datetime.strptime(created, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
    except Exception:
        d = created[:10]
    if d < SINCE:
        continue
    rows.append({
        "user": t.get("author", {}).get("userName"),
        "date": d,
        "likes": t.get("likeCount"),
        "retweets": t.get("retweetCount"),
        "replies": t.get("replyCount"),
        "url": t.get("url"),
        "text": t.get("text"),
        "isRetweet": bool(t.get("retweeted_tweet") or t.get("isRetweet") or (t.get("text","").startswith("RT @"))),
    })

for r in rows:
    print(json.dumps(r, ensure_ascii=False))
