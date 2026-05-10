*Agent Self-Improvement — 2026-05-10*

Tightened tweet-allocator's failure-mode contract. The skill now reads `.bankr-cache/verified-handles.json.error` first and surfaces its content verbatim — instead of relying on Claude to infer the marker existed.

Why: today's tweet-allocator run hit BANKR_API_KEY_INVALID (API rejected key on all 5 lookup attempts, HTTP 401/403). The notification was correct, but only because the model went looking for the prefetch's error marker on its own — the SKILL.md only said "check cache missing or empty." That contract is fragile: a future run could legitimately report "cache missing" when the real cause is an expired key, an invalid key, or a Bankr API outage — three failure modes the prefetch already distinguishes (BANKR_API_KEY_MISSING / BANKR_API_KEY_INVALID / BANKR_LOOKUPS_FAILED), each with its own operator action.

What changed:
- skills/tweet-allocator/SKILL.md: step 4 reordered — read the .error marker first, log + notify with verbatim content, stop. Fall through to verified-handles.json only when no marker exists. Sandbox note now documents the two-file failure surface (cache + .error marker, cleared each run). Status-flags section enumerates the three marker codes.

Impact: deterministic operator routing for the three Bankr failure modes — no more "cache missing" red herring when the cause is a 401 or an outage. The prefetch already wrote the right text per failure mode (since aeon-agent PR #24); this PR makes the skill's contract match.

PR: https://github.com/aaronjmars/aeon-agent/pull/37
