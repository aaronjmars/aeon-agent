---
name: feature
description: Build a feature for every watched repo — picks from yesterday's repo-actions ideas first
var: ""
tags: [dev]
---
> **${var}** — Optional. If set, build this specific feature for the FIRST watched repo only. If empty, iterate every watched repo and pick per-repo.

Today is ${today}. Your task is to build a new feature for **every repo** listed in `memory/watched-repos.md` (not this agent repo). Each repo gets its own branch, PR, and notification.

## Steps

1. **Load the target list** — read `memory/watched-repos.md` and parse every `- owner/repo` line into a list. If `${var}` is set, restrict the list to the first repo only and use `${var}` as the feature spec for it.

2. **For each repo in the list, run steps 3–10 independently.** A failure on one repo must NOT stop the others — log the failure and continue. Use a fresh working directory per repo (e.g. `/tmp/build-target-{repo-name}`).

3. **Pick what to build for this repo** (in this priority order):
   a. If `${var}` is set AND this is the first repo, build that.
   b. Check yesterday's `repo-actions` output in `articles/repo-actions-*.md` (most recent file) for ideas relevant to THIS repo. Pick the highest-impact idea scoped for autonomous implementation.
   c. Check open GitHub issues labelled "ai-build" on this repo: `gh issue list -R owner/repo --label ai-build`.
   d. Check `memory/MEMORY.md` for planned features or next priorities tied to this repo.
   e. If none of the above yields anything for this repo, log "FEATURE_SKIP: {repo} — no suitable feature found" and **skip to the next repo. Do NOT send a notification for skipped repos.**

4. **Clone the repo** into a per-repo temp directory and work from there:
   ```bash
   gh repo clone owner/repo /tmp/build-target-{repo-name}
   cd /tmp/build-target-{repo-name}
   ```

5. **Read the codebase** — understand the project structure, README, package.json/config files, and the area you'll be modifying.

6. **Implement the feature.** Write clean, complete code. No TODOs or placeholders.

7. **Create a branch and push** to the repo:
   ```bash
   cd /tmp/build-target-{repo-name}
   git checkout -b feat/short-feature-name
   git add -A
   git commit -m "feat: description of what was built"
   git push -u origin feat/short-feature-name
   ```

8. **Open a PR** on the repo:
   ```bash
   gh pr create -R owner/repo \
     --title "feat: short description" \
     --body "## What
   Description of the feature.

   ## Why
   What triggered this — repo-actions idea, issue, or gap identified.

   ## Changes
   - file1: what changed
   - file2: what changed

   ---
   *Built autonomously by Aeon*"
   ```

9. **Update memory** — log what was built (per repo) to `memory/logs/${today}.md` and update `memory/MEMORY.md` Skills Built table. Include the repo name in every log line so the per-repo history stays distinct.

10. **Send a DETAILED notification** via `./notify` for THIS repo. Send one notification per successfully-built feature (one per repo). The notification goes to a Telegram group and must be rich enough that readers understand exactly what was built, why it matters, and how it works WITHOUT clicking the PR link.

    DO NOT compress this into 1-2 lines. Every section below is REQUIRED:

    ```
    *Feature Built — ${today} — owner/repo*

    [Feature name]
    [2-3 sentence description of what the feature does in plain language. Explain it like you're telling a non-technical person in the community what just got added to the project.]

    Why this matters:
    [2-3 sentences on why this feature is relevant to the project RIGHT NOW. What problem did users/developers have before? What triggered building this — a repo-actions idea, a GitHub issue, a gap noticed in the codebase? How does it move the project forward?]

    What was built:
    - [file/component 1]: [what was added/modified — be specific about the functionality, not just "added endpoint"]
    - [file/component 2]: [same level of detail]
    - [file/component 3 if applicable]
    - [file/component 4 if applicable]

    How it works:
    [3-4 sentences explaining the technical implementation. What approach was chosen and why? What libraries/APIs does it use? How does it integrate with existing code? Any interesting design decisions?]

    What's next:
    [1-2 sentences on follow-up work, potential improvements, or how this connects to the broader roadmap]

    PR: [url]
    ```

    BAD example (too short — DO NOT do this):
    "Feature Built: Simulation Data Export. Users can download results as JSON/CSV. PR: url"

    GOOD example (this is the level of detail expected):
    "Feature Built — 2026-03-25 — aaronjmars/MiroShark

    Simulation Data Export
    MiroShark simulations now have a one-click export feature. Users can download their full simulation results — including all agent states, interaction logs, and performance metrics — as either JSON (for programmatic use) or CSV (for spreadsheets and analysis).

    Why this matters:
    Until now, simulation data was trapped in the browser. Researchers and developers running MiroShark swarms had no way to extract results for external analysis, comparison across runs, or sharing with collaborators. This was the #2 most requested feature in repo-actions and directly supports the project's goal of being a serious research tool, not just a demo.

    What was built:
    - api/export/route.ts: New API endpoint that serializes simulation state to JSON or CSV based on Accept header. Handles large datasets with streaming response to avoid memory issues.
    - components/ExportButton.tsx: Download buttons added to the simulation results panel. JSON and CSV options with proper MIME types and generated filenames.
    - lib/serializer.ts: Conversion logic that flattens nested agent state trees into tabular CSV format while preserving full structure in JSON output.

    How it works:
    The export endpoint reads the simulation ID from the request, pulls the full state tree from the in-memory store, and streams it as either application/json or text/csv. The CSV serializer walks the nested agent hierarchy depth-first and flattens each agent's state into a row with dot-notation column headers (e.g. agent.memory.shortTerm). The frontend buttons trigger a fetch with the appropriate Accept header and use the download attribute for a clean save-as experience.

    What's next:
    Could add PDF report generation with charts, or a shareable link that hosts the export temporarily for collaboration.

    PR: https://github.com/aaronjmars/MiroShark/pull/1"

11. **Final wrap-up** — after iterating every repo, end with a `## Summary` listing each watched repo and its outcome (PR url, skipped, or failed). If every repo was skipped, do NOT send a notification at all.

Write complete, working code. No TODOs or placeholders.
