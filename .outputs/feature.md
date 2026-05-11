*Feature Built — 2026-05-11 — aaronjmars/minitor*

GitHub Actions Status Column
Minitor's 40th column type — and the first to show CI. A new GitHub Actions column type surfaces live workflow runs for any GitHub repo, with status icon, branch, commit SHA, duration, and event source (push / pull_request / schedule / workflow_dispatch). Engineering teams that already use minitor to monitor their repos no longer need a second tab open to check whether the deploy passed.

Why this matters:
Minitor's 39 column types covered every community-signal axis on GitHub — stars, forks, PRs, issues, trending, search, backlinks, releases — but not a single column showed whether the code actually built. That's the last piece of "repo health" that lived outside the dashboard. With the GitHub Actions column, minitor goes from "watch how your community sees your repo" to "watch your whole repo, period." Closes the second of three May-10 repo-actions ideas (#1 Price Threshold Alert and #3 Auto-Merge Agent PRs landed in the same daily batch — first full per-repo feature day in Aeon history).

What was built:
- lib/columns/plugins/github-actions/plugin.ts: Zod-validated config schema with three fields — `repo` (owner/repo, required), `workflow` (optional, matches display name OR `.github/workflows/<file>.yml`), `branch` (optional, exact match — the GitHub Actions API rejects partial branch names). #2088FF GitHub-Actions-blue accent, Workflow icon, `social` category to sit alongside the other 8 github-* plugins in the Add-column picker.
- lib/columns/plugins/github-actions/server.ts: thin server fetcher delegating to a new lib/integrations/github.ts function.
- lib/columns/plugins/github-actions/client.tsx: ConfigForm with three inputs + inline help text. ItemRenderer with a status pill that distinguishes in-flight (Loader2 spinner) / queued / 9 terminal conclusions (success/failure/cancelled/neutral/skipped/timed_out/action_required/stale/startup_failure) each with its own icon and ring color.
- lib/integrations/github.ts: new `fetchWorkflowRuns(repo, workflow, branch, limit, page)` and the GHActionRunMeta type that backs it.
- Three registry edits (manifest.ts / registry.ts / server-registry.ts) — the server-registry's init-time parity check throws loudly if any of the three are out of sync.
- README: column count 39 → 40, GitHub cluster row 8 → 9, top-line bullet now mentions "GitHub (including CI runs)."

How it works:
The /repos/{owner}/{repo}/actions/runs REST endpoint is public and keyless for public repos (60 req/hr per IP unauthenticated, 5000/hr with the optional GITHUB_TOKEN already used by every other github-* plugin). Three integration quirks documented inline because they're each one bug away from being subtle problems: (1) the workflow filter must be applied client-side because the API only accepts a numeric workflow_id, not a name — the user-friendly thing is matching by display name or filename, so the column does that itself; (2) page-completeness uses raw upstream length (not post-filter length), so the workflow filter doesn't prematurely terminate pagination and Load more keeps working; (3) duration is only computed when status=completed — for in-flight runs the column leaves it undefined rather than render a misleading partial-duration number that grows in the UI. Color coding by conclusion is the operator-scannable signal: green check for success, red X for failure, amber for action-required.

What's next:
With CI visibility added, minitor is now a complete repo-health surface — pair a Stars + Forks + PRs + Issues + Actions stack and you have everything an engineering team would otherwise open 5 tabs for. Natural next column types (open in the May-10 ideas pipeline): npm Trends (#5, the discovery layer for the TypeScript audience minitor actually serves) and Fork Release Tracker (#4, complementing fork-cohort's "is the fork alive" signal with "did the fork ship a release"). Could also extend this plugin with a rerun-failed action — the API supports it and the UI has room for a "rerun" button.

PR: https://github.com/aaronjmars/minitor/pull/34
