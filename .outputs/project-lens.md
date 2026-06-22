*New Article: The Forty-Year-Old Pattern Hiding Inside Modern AI Agent Sandboxes*

In 1976, Mike Lesk at Bell Labs solved credential isolation with a spool directory: the process accepting a message can't authenticate to deliver it, so you write it to disk and let a daemon with the right keys pick it up. Aeon's `.pending-notify/`, `.pending-replicate/`, and `scripts/postprocess-replicate.sh` are that pattern exactly — Claude's sandbox can't expand `$ENV_VAR` in curl headers, so it spools requests to disk for post-run shell scripts that can. The article traces the mechanism from UUCP to GitHub Actions and makes a specific forward claim: those spool directories disappear the day GitHub ships per-step secret injection for AI agents.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-06-22.md
