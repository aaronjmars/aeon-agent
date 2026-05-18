*Agent Self-Improvement — 2026-05-18*

refresh-x prefetch-cache rewrite
The refresh-x skill was the last enabled-eligible XAI consumer still doing a direct `curl -H "Authorization: Bearer $XAI_API_KEY"` as its primary path — the same pattern PR #48 fixed for token-report two days ago. Rewrote step 1 to read from `.xai-cache/refresh-x.json` (which `scripts/prefetch-xai.sh` already produces) with the same four-path ladder fetch-tweets uses: A (cache) / A-error short-circuit / A-truncated marker / B (direct curl, local-mode only) / C (WebSearch).

Why: Latent-bug audit. Inside the GitHub Actions sandbox, env-var expansion in curl headers is blocked, so the original step-1 curl always fails and the "If XAI_API_KEY is not set, skip and log that the skill requires it" line gets written as a false-positive — exactly the noise that wrote "XAI_API_KEY not set" into token-report's daily log for five straight days (May 13–16) before PR #48 fixed it. refresh-x is currently `enabled: false`, so this is a pre-emptive fix rather than a live incident — if enabled today it would have started producing the same daily noise.

What changed:
- skills/refresh-x/SKILL.md: step 1 rewritten with the four-path ladder; step 3 log template extended with Source / Status fields so the four states (cache / truncated / prefetch-failed / no-prefetch) are distinguishable downstream; step 5 notification adapts to status; misleading "If XAI_API_KEY is not set" line removed; Sandbox note appended pointing at the prefetch script case + line numbers.

Impact: Fourth explicit-marker / cache-read contract since May 10 (after PR #37 `.error`, PR #43 `.truncated`, PR #48 fetch-tweets-log fallback). All four eliminate misleading "key not set" / "cache empty" lines that conflate sandbox limitations with real config gaps. refresh-x is now ready to be enabled without immediately producing the same false-positive log noise.

PR: https://github.com/aaronjmars/aeon-agent/pull/51
