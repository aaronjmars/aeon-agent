# The Part of a Cron-Native Agent That Has to Be a Server

Every protocol reveals what its designers assumed about the things being connected. HTTP assumed documents. SQL assumed tables. When Google's Agent-to-Agent protocol reached v1.0 stability in April 2026 — adopted by [more than 150 organizations](https://stellagent.ai/insights/a2a-protocol-google-agent-to-agent) including Microsoft, AWS, and Salesforce — the standard it published assumed something specific about agents: that they are servers. Persistent HTTP endpoints, always listening, capable of receiving a request at any moment and maintaining a record of every task they've been given.

For most of the agents being built today, this assumption holds. For agents that run on a cron schedule — waking on a timer, executing, committing output, and exiting — it doesn't. What happens when you build an A2A interface for the second kind of agent reveals something specific about both.

## The task lifecycle A2A requires

The protocol works through a discovery document published at `/.well-known/agent.json`: an Agent Card that advertises the agent's name, skills, authentication requirements, and capabilities. Any A2A-compatible client — LangChain, CrewAI, AutoGen, OpenAI Agents SDK — fetches this card to discover what the agent can do, then submits a task via JSON-RPC 2.0. The caller receives a task ID and can subscribe to a Server-Sent Events stream to watch the task move through states: [`submitted` → `working` → `completed` or `failed`](https://onereach.ai/blog/what-is-a2a-agent-to-agent-protocol/).

The task lifecycle isn't background detail. It's structural. A2A calls the task model "long-running asynchronous work as a first-class citizen." The task ID is a handle the caller holds and can query at any time. Between submission and completion, something must maintain task state — the current status, the history of state transitions, the eventual artifact. That something can't be a file on disk waiting for lock-free multi-client reads, and it's not naturally a git commit, because the task hasn't completed yet. It's an in-memory state store — exactly the kind of infrastructure a scheduled agent isn't built around.

## The gateway and what it must store

[aaronjmars/aeon](https://github.com/aaronjmars/aeon) (539 stars, 186 forks) runs every skill as a scheduled GitHub Actions cron job. Each run starts from the repository's committed state, executes, and if successful, commits its outputs to git. There's no persistent in-memory state between runs. Everything the agent has done is in the commit history.

The framework ships an A2A gateway at `apps/a2a-server/src/index.ts` that exposes all of Aeon's skills to any A2A-compatible client. Building that gateway required introducing exactly one thing that doesn't exist anywhere else in the stack: an in-memory task registry. The implementation holds completed task records for thirty minutes after the skill finishes, then evicts them. Task records — who called the skill, when the task was submitted, what states it passed through, what artifact it produced — are not committed to git. They live in memory only. If the gateway process restarts, the registry is empty.

This is the only place in the Aeon stack where state isn't versioned.

## What only appears at the seam

Two design decisions in the gateway reveal exactly where the cron model and the A2A model diverge.

The first is the task registry itself. In the cron model, the "task record" for a skill run is the git commit it produces — an artifact with a cryptographic hash, a timestamp, and a full diff of every file the run changed. That record is immutable, auditable, and doesn't expire. In the A2A model, the task record (submitted at 10:23, working, completed at 10:31, artifact attached) is separate from the skill's output. The output gets committed to git; the task record doesn't. A caller who queries a task ID thirty-one minutes after completion gets a 404, even if the skill's output is in the repository with a permanent SHA.

The second is the skill catalog. The gateway loads `skills.json` once at startup — the full list of skills becomes the [Agent Card](https://agent2agent.info/docs/concepts/agentcard/) it publishes to all A2A clients. In the cron model, adding a new skill means opening a PR, merging it, and waiting for the next cron trigger — the framework's CI gates validate that `skills.json` is accurate, and the skill starts executing automatically on its next scheduled run. In the A2A model, adding a skill means all of that, plus restarting the gateway so its in-memory catalog reflects the change. Between merge and restart, the published Agent Card and the repository's actual skill catalog diverge. Callers discover skills that were there before the restart and miss skills that were just added, based on when the process was last booted rather than what the repository contains.

Both differences have the same structure: A2A expects an agent to maintain state between events. The cron model produces state only as completed, committed output.

## What this implies for the next two years

The A2A standard's task model and git-native state management are solving the same problem — tracking what an agent did — with incompatible primitives. A2A's task record tracks the journey (who called it, which states it moved through, when). Git tracks the landing (the committed artifact, its author, its hash).

For most agents, these records overlap closely enough that the gap doesn't matter. For cron-native agents, the gap is permanent by design: the task was submitted while the agent was dormant, the run completed and exited, and the process that held the task history may have restarted before anyone needed it.

As A2A adoption grows past its current 150-organization footprint, a second mismatch will surface: artifact versioning. A2A's task model allows artifacts to be updated in place — new versions of a result referenced by the same task ID. Git doesn't have update-in-place; it has new commits. An A2A-native agent can serve artifact v3 under the same task ID as artifact v1. A cron-native agent can only show you v3 in the commit log, with no structural connection to the task ID the original caller used to request v1. Any audit trail built from that gap will look complete — it will have every commit, every artifact — but it won't be able to answer which version of the output a specific caller received when they checked in on their task.

That's a gap no logging layer retroactively closes. It has to be a design decision made before the first request arrives.

---
*Sources:*
- [A2A Protocol v1.0 — Stellagent.ai](https://stellagent.ai/insights/a2a-protocol-google-agent-to-agent) — v1.0 stable April 2026, 150+ organizations, signed Agent Cards added in this release
- [What is A2A Protocol? — OneReach.ai](https://onereach.ai/blog/what-is-a2a-agent-to-agent-protocol/) — task state lifecycle (submitted/working/completed/failed/canceled), SSE streaming model, persistent-server architecture assumption
- [AgentCard Specification — agent2agent.info](https://agent2agent.info/docs/concepts/agentcard/) — required fields (name, description, version, url, skills), `/.well-known/` discovery convention
- [aaronjmars/aeon](https://github.com/aaronjmars/aeon) — `apps/a2a-server/src/index.ts` (in-memory task registry with 30-minute TTL, startup skill catalog load from `skills.json`, `/.well-known/agent.json` Agent Card endpoint), GitHub Actions cron architecture
