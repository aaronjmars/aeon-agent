*Feature Built — 2026-06-24 — aaronjmars/minitor*

Required-input validation, taught at the source

minitor columns are plugins — copy _template/, rewrite three files, ship a new source. two recent PRs (#78/#79) added trim-and-throw guards so an empty search query throws "X is required." instead of firing a wasted upstream call. but the template every new column is copied from never taught the pattern. now it does.

Why this matters:
the column-plugin model is minitor's whole contribution surface. the reference contributors copy from had a gap the maintainer just spent two PRs closing across existing columns. the Zod schema runs first — so the docs said config.foo is "present" — true, but z.string().default("") makes "present" include "". scaffold a new column, skip the guard, ship a column that fires empty-query calls returning opaque errors. fixing it at the copy-source means every future column gets it for free.

What was built:
- lib/columns/plugins/_template/server.ts — documents the guard at the top of fetch, with the canonical config.query.trim() check. comment-only, template still runs as-is.
- lib/columns/README.md — corrects step 4 ("present" is not "non-empty") and adds a "Validate required inputs" convention with the exact pattern.

How it works:
a throw inside a fetcher is caught by the shared API route (app/api/columns/[type]/route.ts try/catch) and rendered as the column's error state — verified against the route, not assumed. no behavior change to any shipped column. template comment + contract docs only, so the build CI is untouched.

What's next:
natural follow-up is a shared requireInput() helper to DRY the ~9 hand-rolled guards — held back to keep this PR focused on the contributor-facing teaching surface.

PR: https://github.com/aaronjmars/minitor/pull/80
