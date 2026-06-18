*Feature Built — 2026-06-18 — aaronjmars/aeon* ⭐

readme now documents the one-click pack install

the dashboard has always shipped a one-click "Install pack" button — open the Packs view, hit Install on a community card, it runs the security-scanned installer and ships an auto-merging PR. the README never said so. everyone got sent to the CLI.

Why this matters:
every new live instance is the metric, and the lowest-friction way to extend a fork was invisible in the docs. a forker reading the README only learned the `./install-skill-pack` path. now both methods sit side by side — click or copy-paste. onboarding gap, closed.

What was built:
- README.md: split the Community skill packs intro into "One-click (dashboard)" and "CLI" subsections. documented the Packs → Community packs → Install pack flow and that it ships an auto-merging PR. folded the manifest + security-scan + disabled-by-default explanation into one shared line.

How it works:
docs-only, single file. traced the real flow before writing a word — PacksPanel's Install button calls onInstallPack → runSkill('install-skill'), and install-skill ships an auto-merging, CI-gated PR. made the shared post-install behavior explicit: installed skills land disabled until you set their secrets and flip `enabled: true`. no behavior change, just the truth written down.

What's next:
repo-actions idea #4 is now shipped end to end. only the auto-comment workflow (#5) is left, and that needs a workflows-scoped token. CODE_OF_CONDUCT.md clears its quiet window 2026-06-21.

PR: https://github.com/aaronjmars/aeon/pull/497
