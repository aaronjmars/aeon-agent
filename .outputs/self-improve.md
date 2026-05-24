*Agent Self-Improvement — 2026-05-24*

fetch-tweets — operator-actionable PREFETCH_FAILED variants + Notification-sent log contract.

When XAI prefetch fails, the skill now picks a notification template based on the HTTP code in the error file (401/403 = credits/auth, persistent, includes top-up link; 429 = rate limit; 5xx = service; curl error = network). Every exit path of the skill must now log "Notification sent: yes/no" so heartbeat dedup/escalation can actually track this skill.

Why: today's run logged FETCH_TWEETS_PREFETCH_FAILED with reason "HTTP 403, team credits exhausted (monthly spend limit reached)" — the first 403 in the log history. The existing notification was generic ("prefetch failed; no tweets fetched") with no operator action, and the log entry omitted the Notification-sent line heartbeat dedup depends on. Downstream impact today: tweet-allocator empty, token-report social section degraded.

What changed:
- skills/fetch-tweets/SKILL.md: step 4 expanded with five PREFETCH_FAILED variants keyed off the prefetch error-file's HTTP prefix; steps 4/5/7 all now require the same "Notification sent" log line.
- memory/logs/2026-05-24.md + memory/MEMORY.md: log entry + Open Improvement PRs updated (PR #54 + #57 already merged).

Impact: when credits run out again, the operator gets a one-line actionable nudge (top up at console.x.ai) instead of a generic "prefetch failed" line, AND heartbeat can now escalate after 3 consecutive failed days.

PR: https://github.com/aaronjmars/aeon-agent/pull/60
