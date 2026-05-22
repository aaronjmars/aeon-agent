*Thread Draft — 2026-05-22*
Topic: install-skill-pack CLI — community skill pack install protocol; first external pack registered twenty minutes after the CLI merged

1/ Twenty minutes after Aeon's community skill pack installer merged, the first external pack was already in the trusted-sources registry.

2/ Before today, the README listed two community packs but no install command. Operators who wanted them cloned the repos and copied the files by hand.

3/ ./install-skill-pack reads a skills-pack.json manifest, runs the security scanner against each declared SKILL.md, prompts on HIGH findings, and writes provenance to skills.lock and aeon.yml. One command.

4/ Five independent packs now exist — AntFleet, zer0, gitbounty, baseddevoloper, danbuildss. The sixth will be a one-line PR to skills-pack.json. That's what a standard looks like when it ships into an active ecosystem.

5/ PR #213 — community skill pack install protocol: https://github.com/aaronjmars/aeon/pull/213

(article: articles/thread-2026-05-22.md)
