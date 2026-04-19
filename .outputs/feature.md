*Feature Built — 2026-04-19*

Memory Search API
Aeon's memory — the markdown files where it keeps MEMORY.md, topic notes, daily activity logs, and its issue tracker — is now queryable over HTTP. Hitting /api/memory/search?q=skill+evals returns ranked JSON hits with snippets and line numbers, instead of making the caller clone the repo and grep. Same for listing topics, fetching a specific day's log, and pulling individual issue files.

Why this matters:
The A2A gateway (Apr 15) and MCP adaptor (Apr 10) let any agent framework execute Aeon's skills, but the agent's state — what it logged yesterday, what tokens it tracks, which skills it has built — was still trapped in raw markdown files. This was idea #1 in yesterday's repo-actions run and the missing bridge between the agent's private knowledge and the public interfaces already in production. The 30 forks that operate their own Aeon instances now have a straightforward way to introspect a running agent without cloning it.

What was built:
- dashboard/lib/memory.ts: Shared reader with tokenized search (match count + distinct terms + source weight scoring), snippet extraction with line numbers, and path-safe resolution — slug/date/issue-id regexes plus a safeJoin helper so user-supplied segments cannot escape memory/.
- dashboard/app/api/memory/route.ts: Index endpoint returning MEMORY.md excerpt, per-source counts, and a self-describing list of all available routes.
- dashboard/app/api/memory/search/route.ts: Full-text search across memory, topics, logs, and issues with optional source filter and configurable limit.
- dashboard/app/api/memory/logs/route.ts + /topics/route.ts + /topics/[slug]/route.ts + /issues/route.ts + /issues/[id]/route.ts: Five more routes — list-all and fetch-one for every memory source.

How it works:
Next.js App Router route handlers reading files under memory/ relative to REPO_ROOT, same pattern the existing /api/outputs and /api/analytics routes use. The search layer loads each source, runs a simple tokenizer over the query, scores by match count with a small bonus for documents that match more distinct terms and a boost for the MEMORY.md index, then returns the best hit's surrounding three-line window with the match wrapped in markdown bold. Path safety is centralized: every dynamic segment passes through a regex check first and a safeJoin helper second, so ../secrets-style inputs return 404 instead of leaking files.

What is next:
Wire these as aeon-memory-search / aeon-memory-log / aeon-memory-topic tools in the MCP adaptor and A2A gateway (both currently only expose skill execution, so each needs a small direct-tool branch), plus a Memory tab in the dashboard UI that renders topics, logs, and a search box on top of these same routes.

PR: https://github.com/aaronjmars/aeon/pull/41
