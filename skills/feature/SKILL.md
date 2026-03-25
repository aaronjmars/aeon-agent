---
name: Feature Builder
description: Build new features from GitHub issues or improve the agent
var: ""
---
> **${var}** — Feature to build. If empty, picks from GitHub issues or memory.

If `${var}` is set, build that feature instead of picking from issues.


Today is ${today}. Your task is to build a new feature for this repository.

Steps:
1. Read `memory/MEMORY.md` for context.
2. Check open GitHub issues labelled "ai-build" using `gh issue list --label ai-build`.
   If there are none, check memory for planned features, or pick a reasonable
   improvement (e.g. a new skill, better prompts).
3. Read the relevant existing files to understand the codebase.
4. Implement the feature. Write clean code.
5. Create a branch, commit, and open a PR with a clear title and description.
6. Update memory/MEMORY.md to record what was built.
7. Log what you did to memory/logs/${today}.md.
8. Send a notification via `./notify`: "Feature built: [name] — PR: [url]"

Write complete, working code. No TODOs or placeholders.
