*Feature Built — 2026-06-16 — aaronjmars/minitor*

a CONTRIBUTING guide for minitor
minitor ships 49 column types but had no top-level guide for people who want to add a 50th. this adds a root CONTRIBUTING.md: how to run it locally, how the codebase is laid out, and a step-by-step walkthrough for building a new column — the most common contribution.

Why this matters:
the detailed plugin contract already lived in lib/columns/README.md. what was missing was the layer above it — the dev loop, the project map, the PR workflow, and a signpost pointing at that contract. without it a forker reverse-engineers everything from existing folders, and GitHub's Community Standards flags the file as absent. every new column is someone deciding minitor is worth extending.

What was built:
- CONTRIBUTING.md (new): ./minitor local setup (Node 20+, keyless-by-default, PGlite bundled), a project-layout table, an "Adding a column type" walkthrough (copy _template → edit plugin.ts/client.tsx/server.ts → register in manifest.ts + the two registries → npm run build), conventions (keyless-first, client/server split, opaque cursors, integrations boundary), and the branch/PR flow with the build+lint gate.

How it works:
plain markdown at the repo root — github surfaces it on the new-PR and new-issue screens automatically. it deliberately summarizes the column flow and defers the full contract to lib/columns/README.md, so there's one source of truth and the guide can't drift out of sync with the code. the registration step names the exact parity check (manifest vs both registries) that npm run build enforces, so a missing import fails the build instead of 404ing at runtime.

What's next:
minitor's still pre-LICENSE/CODE_OF_CONDUCT at the file level — CONTRIBUTING is the first Community Standards box checked; the rest follow the same lower-the-barrier thread.

PR: https://github.com/aaronjmars/minitor/pull/75
