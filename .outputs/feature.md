*Feature Built — 2026-06-25 — aaronjmars/aeon*

shipped the validator config-validator was already trying to call ⭐

config-validator's SKILL.md tells the agent to run `node scripts/validate-config.js` as its "fast path." that script was never committed. so the fast path failed every single run and the skill quietly fell back to weaker inline checks — a dangling reference inside the skill whose whole job is catching dangling references. fixed it by shipping the missing script.

Why this matters:
the inline fallback only checked skills with `enabled: true` written in single-line `{ }` form. that's 1 of 183 configured skills right now. prune a skill but leave it behind in a disabled entry, a multi-line entry, or a chains: pipeline and nothing flags it — the scheduler just fires a phantom at cron time and the run dies. this is the exact deletion-cost gap that cost four cleanup PRs back on 06-19. self-repair is the moat; the config that guards the harness shouldn't have a hole in it.

What was built:
- scripts/validate-config.js: one-pass validator, three invariant checks (checkout ordering, duplicate skill keys, skill-reference integrity)
- checks 1 & 2 mirror the SKILL.md logic verbatim — identical behavior to the fallback, zero new false positives
- check 3 is strengthened: validates every skills: entry (enabled or not, inline or multi-line) AND every chains: parallel/skill/consume ref resolves to skills/<name>/SKILL.md

How it works:
pure node, no deps, reads local files only. it tracks the skills: and chains: blocks by top-level-key boundaries, pulls every reference, and checks skills/<name>/SKILL.md exists. exit 0 + PASS lines = clean, exit 1 + FAIL lines = issues — the exact contract config-validator already reads. ran clean against main (183 refs resolve, no dup keys, checkout ok) and unit-tested that it catches inline, multi-line, and chain phantoms without false-flagging real skills.

What's next:
the SKILL.md also names a pre-merge workflow ci-config-validate.yml that doesn't exist yet — wiring this into CI needs a workflows-scoped token (same blocker as the SHA-pin work). script's built to drop straight in when that token lands.

PR: https://github.com/aaronjmars/aeon/pull/546
