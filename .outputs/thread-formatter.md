*Thread Draft — 2026-05-25*
Topic: Per-column webhook notifications (Minitor PR #50)

1/ Minitor columns now POST to a webhook URL when a new item matches your keywords. The request fires server-side: 5-second hard timeout, no redirects followed, 11 IP ranges blocked before the payload leaves.

2/ Until today, alert keywords in Minitor were passive. They'd highlight matching items in red when a fetch ran, but nothing happened automatically. The column sat there waiting for you to look at it.

3/ Each column can now have a webhook URL. When a fetch brings in new matching items, the server fires a POST: {columnId, columnTitle, typeId, matches, timestamp}. Re-fetches don't re-notify — only genuinely new items trigger it.

4/ The webhook URL is never included in deck exports or share links. It gets omitted deliberately — webhook URLs usually embed secrets, and the same JSON payload feeds the public /gallery share link. Security took the win over portability.

5/ Per-column webhook notifications for Minitor — keyword match fires a POST. PR #50: https://github.com/aaronjmars/minitor/pull/50

(article: articles/thread-2026-05-25.md)
