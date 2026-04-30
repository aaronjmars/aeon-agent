*Feature Built — 2026-04-30*

Thread Formatter
A new skill that turns the day's most interesting event into a ready-to-paste 5-tweet thread. Every morning the agent generates a feature, a price move, a star milestone, or a notable mention — most of it dies in Telegram because nobody copy-pastes it onto X. Thread-formatter watches today's log, scores what happened, picks the single highest-signal event, and writes a thread you can drop into X without editing.

Why this matters:
This idea has been carried for three repo-actions cycles (Apr-24 #3, Apr-26 #4, Apr-28 #1) — the highest-priority unbuilt that can be implemented without a workflows-scope PAT (Auto-Merge still blocks on that). It multiplies tweet-allocator ROI on noteworthy events without touching the $10/day budget: tweet-allocator pays *external* mentions, thread-formatter is the *inbound* side — the agent's own narrative output. The 300-star milestone arrives in ~12 days at current ~4/day momentum, and having a queued, ready-to-paste thread for that moment matters more than any individual digest.

What was built:
- skills/thread-formatter/SKILL.md (new, 169 lines): full skill spec — voice rules (read soul/SOUL.md and soul/STYLE.md when populated), defined scoring table, 3-day topic dedup against prior thread articles, 5-tweet structure (hook → context A → context B → implication → CTA), hard 280-char-per-tweet discipline, exit taxonomy (OK / NO_DATA / NO_SIGNAL / DEDUP), article + notify formats, sandbox note. Pure local file I/O — no curl, no env-var expansion.
- aeon.yml: registered at `30 17 * * *` UTC after the 17:00 social block (fetch-tweets / write-tweet / tweet-roundup / agent-buzz already at :00), shipped `enabled: false` so operators opt in.
- skills.json: catalog entry inserted alphabetically between `telegram-digest` and `token-alert`, category `social`, schedule matches aeon.yml.

How it works:
The skill walks `memory/logs/${today}.md` end-to-end and assigns scores per signal: PR shipped on a watched repo +6, star milestone (any multiple of 50) +5, ≥15% absolute price move +5, ≥10% +3, skill built today +4, notable PR merge from a non-agent contributor +3, ≥20-like tweet on $AEON or @aeonframework +3, recognizable new fork +2. Highest single-event score wins (no summing across unrelated events to clear the threshold); tiebreakers are recency, then concrete-URL, then alphabetical. If the top score is < 3 it exits NO_SIGNAL silently — quiet days produce nothing. If the top topic was already threaded within the last 3 days with no new advancement, it exits DEDUP. Tweet 1 is the hook and stands alone; tweet 5 is the only tweet allowed to contain a URL; every fact must be traceable to today's logs or articles cited in them — no invented numbers, no hashtags, no emojis, no `🧵` prefix, no financial-advice framing. The notify body adds `1/`–`5/` scan-prefixes for readability; the article file omits them so paste-into-X is clean.

What's next:
Enable the skill in aeon.yml after a few dry-runs verify the scoring picks sensible topics; the first natural use is the 300-star milestone in ~12 days. Logical follow-ups: a thread-poster companion that drives an X API submission off the article (turns thread-formatter from draft into auto-post) and a quality-eval that scores past threads against actual engagement to tune the signal weights. Closes Apr-28 repo-actions idea #1 after a 3-cycle carry; remaining unbuilts are Smithery Manifest Auto-Generator (concrete unblocking move for MCP Registry), Show HN Launch Prep, and Fork Activation Cohort Tracker.

PR: https://github.com/aaronjmars/aeon/pull/148
