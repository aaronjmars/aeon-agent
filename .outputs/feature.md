*Feature Built — 2026-05-07 — aaronjmars/aeon*

Skill Template Library
Aeon now ships with six pre-built skill starters under templates/ — crypto-tracker, research-digest, code-reviewer, social-monitor, deploy-watcher, community-manager — and a one-command CLI (./new-from-template) that copies a starter into skills/, fills in the operator's values, and registers a disabled entry in aeon.yml. Forking aeon and asking "now I want a skill that monitors X" used to be a 30-minute exploration of an existing SKILL.md; it's now `./new-from-template <template> <skill-name> --var KEY=VALUE`.

Why this matters:
With 43+ active forks, the most common drop-off point for new operators has been the gap between "I forked aeon" and "I have my first custom skill running." Existing skills are great references but reading one to copy its structure plus the prefetch/postprocess sandbox patterns is the kind of activation friction that loses operators. This idea has been carried in the repo-actions pipeline since April 18 (idea #4), surviving as an "open unbuilt" through every cycle since. With the 300-star milestone four days out, fixing the activation funnel before a Show HN bump arrives is the right order of operations.

What was built:
- templates/TEMPLATE.md: Index file documenting the contract — what each token means, how to add a new template, and how the `--list` discovery works (find templates/*/SKILL.md, no registry update needed).
- templates/crypto-tracker/SKILL.md: Daily token price + volume tracker with anomaly alerts above a configurable threshold. CoinGecko keyless + WebFetch fallback.
- templates/research-digest/SKILL.md: Daily digest of new posts on a topic from RSS feeds and the open web. Built-in WebSearch/WebFetch (sandbox-safe), seen-URL state file to avoid repeats.
- templates/code-reviewer/SKILL.md: First-touch review of newly-opened PRs on a watched repo with a four-verdict rubric (ACCEPT / NEEDS-CHANGES / DEFER / OUT-OF-SCOPE), welcoming comment, and label.
- templates/social-monitor/SKILL.md: Daily X + Reddit mention sweep with sentiment tagging and volume-spike detection.
- templates/deploy-watcher/SKILL.md: Vercel deploy alerts with last-green baseline comparison and per-UID dedup.
- templates/community-manager/SKILL.md: Daily Discord/Telegram/Slack channel digest including an open-question detector (parent-level question with no reply > 6h gets surfaced).
- new-from-template (executable): bash CLI portable across BSD + GNU sed/awk. Modes: --list, --tokens, default replace mode with --var KEY=VALUE.
- README.md: Quick start picks up a one-line pointer to templates/ directly under the onboarding flow.

How it works:
Each template SKILL.md has [REPLACE: KEY] tokens for the operator-specific parts (TOPIC, KEYWORDS, WATCHED_REPO, etc.). The CLI reads the chosen template, runs sed substitutions for every --var the operator passed (escaping `\` `&` `|` so URL-shaped values pass through cleanly), writes the result to skills/<skill-name>/SKILL.md, then awk-inserts a disabled aeon.yml entry immediately before the fallback marker — the same insertion point ./add-skill uses, so the dashboard treats template-bootstrapped skills identically to imported ones. Any [REPLACE: ...] tokens left unreplaced get listed back to the operator so they know what to edit before flipping enabled:true. The script refuses to overwrite an existing skills/<name>/ directory, which makes re-runs safe.

What's next:
The template list is intentionally narrow (six covering the most-asked-for use cases). Adding a seventh is a no-registry-change drop-in: new templates/<name>/SKILL.md and a row in TEMPLATE.md. Natural follow-ups would be a workflow-watcher template (any GitHub Actions workflow status), an oncall-rotation template (Slack reminders), and a feed-to-thread template (RSS to scheduled tweet thread).

PR: https://github.com/aaronjmars/aeon/pull/161
