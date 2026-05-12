*Feature Built — 2026-05-12 — aaronjmars/aeon*

Fork Release Tracker
Aeon now watches every fork of the main aeon repo and announces it on Telegram the moment any of them ships a tagged GitHub release. The skill runs once a week on Sunday evening and stays completely silent in weeks when nothing happens — but the first time a fork cuts a real release, that release lands in the operator's notifications with the fork name, the tag, and the release notes.

Why this matters:
fork-cohort already answers 'is this fork alive?' (workflow runs in 7 days) and contributor-spotlight already answers 'who is pushing the most code?' (POWER-fork operator callouts). Neither answers the load-bearing question: has any fork shipped a real product? A tagged release on a fork is the strongest possible signal that someone is treating aeon as infrastructure, not a toy — they trusted it enough to put a version number on something. This skill marks that moment. It was the #4 idea from the May-10 repo-actions brief and is one of the last burns from that cohort.

What was built:
- skills/fork-release-tracker/SKILL.md: 10-step skill with 10-status exit taxonomy (OK / QUIET / NEW_RELEASE / MULTI_RELEASE / DRY_RUN / NO_FORKS / API_FAIL / PARENT_CHANGED / STATE_CORRUPT / BAD_VAR). Paginates /forks, fetches each fork's most recent release, filters to a rolling 7-day window, dedups via state file capped at 50 entries (LRU by announced_at).
- aeon.yml: registered enabled:false, Sunday 19:30 UTC (30 min after fork-cohort), sonnet-4-6 model.
- skills.json: total bumped 115 → 116, dev category.

How it works:
The skill resolves the parent repo from parent.full_name (or uses the current repo when run on the upstream itself), paginates /forks to enumerate the cohort, and queries /releases?per_page=1 on each fork. Drafts are skipped; pre-releases are included but flagged in the message. Each (fork, tag) tuple is deduped against memory/topics/fork-release-state.json so the same release never re-announces. The notification template has two shapes — a single-release celebration with the fork name in the hero line, and a multi-release weekly digest with the newest as the lead and the rest as an 'Also this week' tail. Release bodies are treated as untrusted input (prompt-injection-safe per CLAUDE.md): if a body looks like instructions, it's replaced with '(release notes omitted — flagged as untrusted)' rather than suppressed entirely.

What's next:
Enable in aeon.yml once the operator wants the weekly signal active — first natural Sunday run May 17. Backport to aeon-agent on the same-day-after pattern once it's running cleanly upstream. Closes the last remaining May-10 repo-actions idea.

PR: https://github.com/aaronjmars/aeon/pull/166
