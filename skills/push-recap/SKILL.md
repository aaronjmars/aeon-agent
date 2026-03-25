---
name: Push Recap
description: Daily recap of pushes and commits across watched repos
var: ""
---
> **${var}** — Repo (owner/repo) to recap. If empty, recaps all watched repos.

If `${var}` is set, only recap that repo (owner/repo format).


## Config

This skill reads repos from `memory/watched-repos.md`. If the file doesn't exist yet, create it or skip this skill.

```markdown
# memory/watched-repos.md
- owner/repo
- another-owner/another-repo
```

---

Read memory/MEMORY.md and the last 2 days of memory/logs/ for context.
Read memory/watched-repos.md for the list of repos to scan.

Steps:

1. For each repo, fetch today's push activity using the Events API:
   ```bash
   gh api repos/owner/repo/events --jq '[.[] | select(.type == "PushEvent") | {actor: .actor.login, branch: .payload.ref | sub("refs/heads/";""), commits: [.payload.commits[] | {sha: .sha[0:7], message: .message | split("\n")[0]}], date: .created_at}]'
   ```

2. Also fetch recent commits on the default branch for the last 24h:
   ```bash
   gh api "repos/owner/repo/commits?since=$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ)" --jq '.[] | {sha: .sha[0:7], message: .commit.message | split("\n")[0], author: .commit.author.name, date: .commit.author.date}'
   ```

3. Deduplicate commits by SHA. Group by repo, then by author.

4. Write the recap to `articles/push-recap-${today}.md`:
   ```markdown
   # Push Recap — ${today}

   ## owner/repo
   **author-name** (3 commits):
   - feat: add new endpoint (`abc1234`)
   - fix: handle null case (`def5678`)
   - chore: update deps (`9ab0123`)

   **another-author** (1 commit):
   - docs: update README (`hij4567`)
   ```

5. Send a concise summary via `./notify`:
   ```
   *Push Recap — ${today}*
   [repo] 4 commits by 2 authors — feat: add new endpoint, fix: handle null case, +2 more
   [repo2] quiet day, no pushes
   ```

6. Log to memory/logs/${today}.md.
   If no pushes found across any repo, log "PUSH_RECAP_OK: no activity" and notify that it was a quiet day.
