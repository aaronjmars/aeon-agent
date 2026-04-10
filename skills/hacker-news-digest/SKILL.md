---
name: Hacker News Digest
description: Top HN stories filtered by keywords relevant to your interests
var: ""
---
> **${var}** — Topic filter for stories. If empty, uses interests from MEMORY.md.

If `${var}` is set, only include stories matching that topic.


Read memory/MEMORY.md for tracked topics and interests.
Read the last 2 days of memory/logs/ to avoid repeating stories.

Steps:
1. **Load previously reported stories.** Read the last 2 days of `memory/logs/` and extract any HN story IDs or URLs (news.ycombinator.com/item?id=ID) from prior `## HN Digest` log entries. Keep this as `SEEN_IDS`.

2. Fetch top stories from the HN API:
   ```bash
   # Get top 30 story IDs
   STORY_IDS=$(curl -s "https://hacker-news.firebaseio.com/v0/topstories.json" | jq '.[0:30][]')
   # Fetch each story's metadata
   for ID in $STORY_IDS; do
     curl -s "https://hacker-news.firebaseio.com/v0/item/${ID}.json"
   done
   ```

3. Filter stories by relevance to topics in MEMORY.md (AI, crypto, neuroscience, programming, etc.).
   Also include anything with 200+ points regardless of topic.
   **Remove any story whose ID is in `SEEN_IDS`.** If all relevant stories were already reported, log "HN_DIGEST_QUIET: all top stories already reported" and **stop here — do NOT send any notification**.

4. For the top 5-7 new stories:
   - If the story has a URL, fetch it with WebFetch for more context
   - Write a 1-2 sentence summary
   - Include the HN discussion link: `https://news.ycombinator.com/item?id=ID`

5. Format and send via `./notify` (under 4000 chars):
   ```
   *HN Digest — ${today}*

   1. [Title](url) (250 pts, 89 comments)
      Summary of why it matters.
      [Discussion](https://news.ycombinator.com/item?id=ID)

   2. ...
   ```

6. Log to `memory/logs/${today}.md` — include the story IDs so future runs can deduplicate:
   ```
   ## HN Digest
   - Stories reported: ID1, ID2, ID3, ID4, ID5
   - Notification sent: yes
   ```

If no relevant stories found, log "HN_DIGEST_OK" and end.
