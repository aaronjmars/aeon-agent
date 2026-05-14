*Agent Self-Improvement — 2026-05-12*

xai-prefetch truncation marker — surface XAI cache truncation to consumer skills.

When `scripts/prefetch-xai.sh` detects the XAI response hit the `max_output_tokens` ceiling (output_tokens within 5% of cap, the existing 16384 ceiling), it now writes a `.xai-cache/<file>.truncated` marker alongside the existing `::warning::` GH annotation. Consumer skills can read the marker inline.

`skills/fetch-tweets/SKILL.md` gains a Path A truncation paragraph mirroring the existing `.error` short-circuit: status becomes `FETCH_TWEETS_OK_TRUNCATED` and the notification appends `⚠️ XAI cache truncated (output_tokens=N/max=M); results may be incomplete.`

Why: today's fetch-tweets run logged `output truncated after tweet #2 ... 4 thread_fetch calls also present` — Grok burned its 16384-token budget on thread_fetch calls and the cache shipped with only 1 usable tweet. Second recurrence of the May-6 symptom; the May-8 `::warning::` annotation (PR #33) fires but only `skill-runs --failures` + heartbeat see it. The consumer skill couldn't distinguish "quiet tweet day" from "cache cut in half."

What changed:
- `scripts/prefetch-xai.sh`: write `.xai-cache/<outfile>.truncated` (content: `output_tokens=N reasoning_tokens=R max_output_tokens=M`) when the existing 95%-threshold fires; clear stale marker at start of each call alongside `.error`.
- `skills/fetch-tweets/SKILL.md`: add Path A truncation paragraph defining `FETCH_TWEETS_OK_TRUNCATED` and the operator-visible warning line.

Impact: budget-exhaustion days are now legible at the skill level — operator sees an explicit "cache truncated" warning in the notification, not a silent short result. Marker is generic so refresh-x / remix-tweets / tweet-roundup / narrative-tracker / article can adopt the same short-circuit on first truncation.

PR: https://github.com/aaronjmars/aeon-agent/pull/40
