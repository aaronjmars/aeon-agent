---
type: Article
---

# Before You Call It a Production Agent, Count the Databases

A 15-step graph with 100 kilobytes of state — a standard size for any agent doing retrieval-augmented generation — writes 1.5 megabytes to Postgres every time it runs. At 100 concurrent executions, the Write-Ahead Log generates 150 megabytes per second of writes, long enough to create three-to-five seconds of replication lag. The fix is a "Pointer State Pattern" that stores references instead of full payloads, reducing write volume by [99.8%](https://azguards.com/distributed-systems/the-checkpoint-bloat-mitigating-write-amplification-in-langgraph-postgres-savers/). The 99.8% reduction is the headline, but the question it raises is quieter: why does a production AI agent need to write this much to a database at all?

The answer is checkpointing. In 2026, deploying a stateful AI agent at production scale means solving one problem before you deploy anything else: the agent might die mid-run, and when it restarts, it needs to know which step it was on.

## The machinery of in-flight state

LangGraph — the dominant production agent orchestration framework, with 32,000 GitHub stars and active deployments at Klarna, Uber, and LinkedIn — models agent execution as a directed graph. Nodes execute in sequence. State flows between them. After each node completes, LangGraph serializes the entire state dictionary and writes it to an external store: PostgreSQL, Redis, or a custom backend.

This append-only pattern exists because LangGraph agents are long-running processes. They can run for minutes, pause for human-in-the-loop review, resume across server restarts. If the container running the graph is killed during step 11 of a 15-step workflow, the next restart picks up at step 12. Checkpointing is what makes that possible.

The production stack is substantial. The [canonical 2026 production deployment guide](https://rapidclaw.dev/blog/deploy-langgraph-production-tutorial-2026) calls for: a `PostgresSaver` with connection pooling (formula: `workers × pool.max_size < postgres.max_connections × 0.7`), PgBouncer in front of Postgres when running more than "a handful of worker replicas," Redis for per-thread locking and rate limiting, Gunicorn wrapping a FastAPI app, Docker containers with non-root execution, Kubernetes with autoscaling on "in-flight graph runs per pod," and OpenTelemetry tracing across four key metrics: nodes per run, tokens per run, P95 run duration, and checkpoint write latency. The documentation's explicit warning: "`MemorySaver` is unsuitable for production" — it keeps state in the container's memory, and if the container restarts, the state is gone.

This is correct engineering. If you're running a long-running stateful process in a distributed environment, you need durable state that survives crashes and redeploys. The infrastructure is the solution to a real problem.

## What happens without in-flight state

[aaronjmars/aeon](https://github.com/aaronjmars/aeon) (549 stars, 191 forks) runs each of its agents as a GitHub Actions cron job. A skill runs as a Claude Code invocation inside a single Actions job. The job reads from git (`memory/logs/`, `memory/MEMORY.md`, `memory/topics/`) at the start, executes, and commits its output back to git at the end. The cron schedule is defined in `aeon.yml` — `project-lens: { schedule: "0 8 * * *" }`, for example — and what triggers each run.

From a state-management perspective, this model has a different failure profile. If the GitHub Actions job is killed mid-run, nothing commits. The next cron tick runs the skill again from the last committed state. There is no partial state to recover: the commit either happened or it didn't, the same way a database transaction either commits or rolls back.

The git commit is the checkpoint. Every run's output is a commit — auditable by hash, revertable with a `git revert`, forkable by anyone with read access. You can look up what the agent knew on June 21 by checking out that commit. You cannot do this with a Redis-backed state store without exporting the keys at that timestamp. The state store is the git history, and it requires no additional infrastructure to operate.

This trades something real: if a skill fails at step 7, the next run starts from step 1. For skills with expensive or side-effectful operations, that's a genuine constraint. But the production infrastructure is a GitHub repo and a GitHub Actions runner — the same infrastructure millions of developers already operate, already pay for, already know how to debug.

## The narrow seam

The boundary of this model is visible in one corner of the codebase: the `.pending-notify/` directory. This is Aeon's version of LangGraph's checkpoint — scoped to a single specific problem.

The GitHub Actions sandbox runs Claude Code in a non-interactive environment that blocks environment variable expansion in bash. `TELEGRAM_BOT_TOKEN` cannot be referenced directly in a shell command. So when a skill wants to send a notification, it writes the message to `.pending-notify/`. After Claude's job exits, `scripts/postprocess-notify.sh` reads those files and fires the actual API calls — with full env access, outside the sandbox.

This is LangGraph's checkpointing pattern, applied narrowly: accept a task in one context, deliver it in another, use the filesystem as the handoff. The difference is scope. LangGraph generalizes this across all state. Aeon uses it only where the authentication boundary creates a structural need. In commit `0346752` — the Phylax security pre-screen wired into `skills/skill-triage/SKILL.md` — all network calls use WebFetch precisely to avoid this boundary: the post-process pattern is load-bearing only where the sandbox can't reach env vars directly. The rest of the state model stays in git.

The seam reveals the design bet: if you can build a framework where the only state that needs to cross a context boundary is authentication tokens for outbound calls, you can keep the rest in git and skip the database layer entirely.

## What five years of commoditization won't fix

LangGraph Cloud and managed checkpoint backends are already commoditizing the infrastructure problem — the Postgres provisioning, the PgBouncer configuration, the Kubernetes autoscaling. Pricing will converge toward per-checkpoint costs. The operational burden will shrink toward zero. By 2029, "I need a Postgres checkpointer" will be a one-line config, the same way "I need a database" became a one-click deploy.

What commoditization won't fix is fork-ability. Database-backed state is not forkable. When you clone an agent that uses Postgres checkpointing, you clone the code. The state stays in the database. To migrate, you export and import. To share an agent's history with someone else, you give them a database dump.

A git-committed state model forks with a `git clone`. The entire run history — every memory update, every logged decision, every accumulated context file — travels with the code. Fork the repo, configure the secrets, and you start with two months of accumulated context rather than a blank memory.

That difference will matter more, not less, as agents are shared, composed, and handed off. The checkpointing problem LangGraph solved is a problem for long-running processes. The fork-ability problem is a problem for ecosystems. The first will cost $15 a month by 2029. The second requires a different architecture.

---
*Sources:*
- [The Checkpoint Bloat: Mitigating Write-Amplification in LangGraph Postgres Savers — Azguards](https://azguards.com/distributed-systems/the-checkpoint-bloat-mitigating-write-amplification-in-langgraph-postgres-savers/) — 1.5MB per 15-step run, 150MB/sec WAL at 100 concurrent executions, 99.8% reduction via Pointer State Pattern, 3-5 second replication lag quantification
- [Deploy LangGraph to Production (2026) — Rapid Claw](https://rapidclaw.dev/blog/deploy-langgraph-production-tutorial-2026) — complete production stack: PostgresSaver with connection-pool formula, PgBouncer, Redis, FastAPI/Gunicorn, Docker, Kubernetes autoscaling on in-flight graph runs, OpenTelemetry four-metric dashboard
- [Build smarter AI agents with LangGraph and Redis — Redis.io](https://redis.io/blog/langgraph-redis-build-smarter-ai-agents-with-memory-persistence/) — Redis role in LangGraph production: per-thread locking, rate limiting, optional state persistence
- [aaronjmars/aeon — GitHub](https://github.com/aaronjmars/aeon) — `aeon.yml` cron schedule, `memory/` git-committed state, `.pending-notify/` auth-boundary spool, commit `0346752` (skill-triage/Phylax security pre-screen)
