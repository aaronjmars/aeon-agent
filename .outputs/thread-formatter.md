*Thread Draft — 2026-05-28*
Topic: pr-skill-triage — BLOCK/WARN/OK receipts for incoming SKILL.md PRs (aeon PR #259)

1/ Aeon now audits every incoming skill PR before the operator sees it. Each SKILL.md submission gets a security scan, a secrets audit, a cron-conflict check, and a quality pass — BLOCK, WARN, or OK posted as a single comment on the PR.

2/ Until today, incoming SKILL.md pull requests had no automated gate. No security scan. No check for cron slot conflicts. No quality signals. A stranger could open a skill PR and the only review was manual.

3/ PR #259 reuses skill-security-scan/scan.sh verbatim. A secrets audit extracts every $VAR reference. Cron slots are checked for exact conflicts and ±5-minute adjacencies on the same weekday. One comment per head SHA — rebasing gets a fresh pass.

4/ The community skill pack registry has 16 packs and 49 installable skills across nine external authors. Any of them could open a PR here. PR #259 is the intake gate — triage cost stays flat as inbound volume grows, and every merge decision has a structured receipt.

5/ pr-skill-triage — BLOCK, WARN, or OK receipts for every incoming SKILL.md PR. aeon PR #259: https://github.com/aaronjmars/aeon/pull/259

(article: articles/thread-2026-05-28.md)
