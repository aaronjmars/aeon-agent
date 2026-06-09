*Agent Self-Improvement — 2026-06-08*

Documented the runner-hook shell-expansion restriction system-wide in CLAUDE.md
The runner blocks $(...) and $VAR expansion in skill bash blocks. Only ${today} and ${var} are injected. Future agents writing or backporting skills now read the constraint up front instead of rediscovering it from broken skill output.

Why: The anti-pattern has driven 6 consecutive improve: PRs over 14 days (#63 weekly-shiplog, #67 push-recap, #71 heartbeat, #77 repo-pulse, #81 repo-article, #83 repo-actions + star-momentum-alert), plus a 7th mid-PR fix on mcp-pulse PR #82 (Jun-5) when the agent inherited a phantom ${today_minus_7} reference from a repo-actions idea. The class of bug was "constraint isn't in CLAUDE.md", not "another skill needs the same patch" — every skill's bash block was vulnerable independently. The push-recap on Jun-6 explicitly flagged the pattern: "Worth instrumenting the bot's pre-merge self-review pass."

What changed:
- CLAUDE.md: added Sandbox Limitations section 3 — names ${today} and ${var} as the ONLY runner-injected vars, explicitly debunks ${today_minus_N} as a phantom that resolves to a literal string and silently breaks date filters; lists the 6+1 fix history inline so the constraint is traceable to its evidence
- aeon.yml line 156: fixed stale mcp-pulse comment that still claimed ${today_minus_7} cutoff even though the actual skill body explicitly says "there is no ${today_minus_7} template var" in 3 places (SKILL.md:36, :127, :307) — last stale survivor of the documentation mismatch
- memory/logs/2026-06-08.md: self-improve log entry

Impact: CLAUDE.md is the system-wide preamble every skill run reads first. Documenting the runner-hook constraint here propagates to all future skill runs, including non-feature skills like repo-actions that originated the phantom-variable suggestion in the first place. Higher leverage than instrumenting feature's self-review pass alone, and recent backports (Jun-07 skill-of-the-day, Jun-08 ecosystem-links) already shipped clean with zero mid-PR fixes — the pattern was trending down, this fix preserves that trend in writing.

PR: https://github.com/aaronjmars/aeon-agent/pull/89
