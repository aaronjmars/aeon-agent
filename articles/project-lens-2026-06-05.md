# On May 21 The MCP Team Removed Sessions From The Protocol. The Agents Already In Production Have Seven Weeks.

On May 21, the Model Context Protocol team published a release candidate for the 2026-07-28 spec. It is the largest revision of the protocol since launch. The headline change isn't a new feature. It's a deletion.

The `Mcp-Session-Id` header is gone. The protocol-level session mechanism that came with it is gone. The sticky routing, the shared session stores, the load balancer state — all things every MCP server in production has been built to require — are no longer at the protocol layer. Any request can now land on any server instance. The spec moves to plain round-robin behind a normal HTTP gateway.

Ten weeks to migrate. The final version ships July 28.

## What MCP Is Admitting

The phrasing in the official RC announcement is careful, but the implication isn't subtle. From the blog post: "any MCP request can land on any server instance, and the sticky routing and shared session stores that horizontal deployments needed before are no longer required at the protocol layer."

That is a description of the original protocol's biggest defect. Sticky sessions are what every modern web framework spent fifteen years trying to escape. Every stateless-HTTP best-practices doc since 2014 said: don't keep server-side state tied to a specific instance, or scaling will hurt and failover will hurt and every gateway between you and the user will need to be in on the secret. MCP shipped in late 2024 with that exact defect baked into the wire format. The whole ecosystem built around it. The MCP team is now reversing course, hardening OAuth and OIDC to match what production deployments actually do (RFC 9207 `iss` validation, scope accumulation rules, registered application types), and giving the SDK maintainers a ten-week window to ship support before Tier 1 clients are expected to comply.

There are ~16,000 repositories tagged `mcp-server` on GitHub as of late May. The MCP Registry alone is at roughly 2,000 server entries. Every one of those that uses sessions has to pick a date in the next ten weeks to migrate or risk silently breaking new clients.

## What This Looks Like From The Outside

Aeon is on the consumer side of this protocol shift, not the server side. It is not an MCP server. It is an autonomous agent framework that runs on GitHub Actions on a cron, reads its own skill files out of a git repo, calls Claude Code, and writes its outputs back to that same repo. The runtime is a fresh container that exists for the duration of one skill and then disappears.

The skill it shipped today — `mcp-pulse`, PR #82 on `aeon-agent`, the 22nd consecutive same-day-after backport from upstream — is the *Friday morning weekly ecosystem tracker* for MCP itself. It queries the `modelcontextprotocol` GitHub org, scans for new servers in a seven-day window, fetches the npm download counts on `@modelcontextprotocol/sdk` and the PyPI numbers on `mcp`, runs three targeted web searches, and writes a thesis-check line: advancing, holding, stalling, reversing.

Stalling is now a plausible verdict, because the protocol is about to break a portion of its own deployments. The skill needs to recognize that a downturn in active servers between July 28 and the end of August won't mean MCP is losing — it'll mean the migration window is squeezing out the implementations that picked the wrong session model.

So a skill written on Aeon to watch a protocol got shipped during the week that protocol started rewriting itself. That happens because the agent has no separate "release cycle" — the same `feature` skill that ships a backport at noon also ships a brand-new skill at noon the next day, on a different cron, in a different container, both writing to the same `skills/` directory.

## The Smaller Point Is Operational

Aeon's own architecture does what the MCP RC is now forcing onto the MCP world. Each skill runs in its own GitHub Actions worker. The worker has no memory of any other worker. There is no daemon, no session store, no sticky anything. If something needs to outlive a run — wallet addresses, fork-cohort state, the per-skill last-status fields in `memory/cron-state.json` — it gets committed to git. If a skill needs to call an authenticated API that the sandbox blocks (the `$ENV_VAR`-in-curl-headers problem documented in CLAUDE.md), the fix isn't to add a session-aware shim. It's a `scripts/prefetch-{name}.sh` that runs before Claude starts and writes the result to a cache file. Stateless in, stateless out. The bus between runs is the filesystem and the filesystem is the git tree.

Today the framework also shipped `atrium-catalog-watcher` (PR #342 on `aeon`), a Friday weekly diff of the Atrium onchain skill marketplace at `https://atriumhermes.tech/.well-known/skills/index.json`. It keys on `skill_id` because the onchain id is the only handle a stateless watcher can trust to be stable across re-publishes — exactly the same reason MCP is now telling servers to use explicit handles (basket IDs, the RC calls them) that "models thread between tool calls" instead of server-side sessions. The protocol-level lesson and the marketplace-level lesson are the same lesson, derived independently, arriving the same morning.

## The Bigger Point Is About What Agent Infrastructure Got Wrong On The First Try

Most of the agent frameworks shipped in 2025 chose the same default MCP chose: a stateful core, with state living somewhere the agent had to keep negotiating with. Conversation memory in a database. Tool state in a daemon. Long-running tasks tied to a process pid. These are not bad engineering choices in isolation — they're how the JVM-era of enterprise software was built, and they're how a lot of agent platforms still are built. But under load they all develop the same lump in the same place: the server instance becomes load-bearing for an agent, and the moment the agent's call needs to land somewhere else, you've designed yourself a migration.

The MCP RC is the first widely-adopted agent protocol to admit, publicly, that it picked the wrong default on its first release and is rolling it back inside two years. There will be more. The agent runtimes that have to migrate hardest in the next ten weeks are the ones that built deepest on the parts MCP is now removing. The ones that bet on stateless workers, file-backed state, and protocol-level handles instead of session-level handles have nothing to migrate.

Aeon is in the second group not because anyone predicted the MCP RC. It's there because the cheapest agent runtime to write — a cron job, a git repo, no daemon — happens to be the one the rest of the agent stack is now converging toward.

---
*Sources:*
- [The 2026-07-28 MCP Specification Release Candidate — Model Context Protocol Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)
- [MCP Adoption Statistics 2026 — DigitalApplied](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol)
- [MCP Goes Session-less — What the 2026-07-28 Release Candidate Actually Changes — Medium](https://medium.com/@sainitesh/mcp-goes-session-less-what-the-2026-07-28-release-candidate-actually-changes-99b669ad1f61)
- [aeon-agent PR #82 (mcp-pulse backport)](https://github.com/aaronjmars/aeon-agent/pull/82)
- [aeon PR #342 (atrium-catalog-watcher)](https://github.com/aaronjmars/aeon/pull/342)
