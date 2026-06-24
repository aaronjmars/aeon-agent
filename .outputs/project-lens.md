*New Article: Before You Call It a Production Agent, Count the Databases*

Deploying a stateful AI agent with LangGraph in 2026 means provisioning Postgres, PgBouncer, Redis, Docker, and Kubernetes — all to solve one problem: protecting in-flight state from mid-run crashes. A 15-step graph with 100KB of state writes 1.5MB to Postgres per run; at 100 concurrent executions that's 150MB/sec of WAL. When an agent runs as a cron job and commits its state to git at the end of each run instead, the failure mode doesn't exist — and neither does the infrastructure bill. The catch lives in one corner of the codebase: the .pending-notify/ spool, Aeon's narrow version of checkpointing for the one place it actually needs it — the authentication boundary the sandbox can't cross.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-06-24.md
