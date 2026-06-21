*Feature Built — 2026-06-21 — aaronjmars/aeon* ⭐

dependabot for the whole repo
aeon now watches its own dependencies. added `.github/dependabot.yml` covering github actions plus all four npm apps — dashboard, mcp-server, a2a-server, webhook. one weekly pass, capped at 5 PRs per ecosystem, routed to the maintainer.

why this matters:
aeon runs autonomous code with operator secrets and runs community-pack skills on a cron. no dependabot meant npm vulns in the next.js/react stack and mutable-tag action hijacks piled up silently — no PRs, no audit trail. a maintained dep posture is exactly what forkers check before they adopt. repo-actions flagged the gap on 06-20: four npm workspaces, eight workflows on floating @v4/@v5, zero dependency automation.

what was built:
- .github/dependabot.yml (new): 5 update blocks — one github-actions (dir `/`) + four npm (each app dir). weekly monday, open-PR limit 5, assignee aaronjmars, conventional `chore(deps)` / `chore(deps-dev)` prefixes matching repo commit style.

how it works:
dependabot reads the config on merge — no install, no token, github activates it natively. each block scopes to a directory with a package.json so the four independent apps each get their own update stream instead of one noisy queue. github actions block catches the floating tags across all 8 workflows. covered all four apps, not the three the scan suggested — webhook's wrangler dep was the easy one to miss.

what's next:
first weekly run lands monday. follow-on is SHA-pinning the action tags dependabot surfaces — that needs a workflows-scoped token the default GITHUB_TOKEN doesn't have.

PR: https://github.com/aaronjmars/aeon/pull/513
