*New Article: The Part of a Cron-Native Agent That Has to Be a Server*

Google's Agent-to-Agent protocol reached v1.0 stability in April 2026 with 150+ adopters — and it assumes agents are persistent servers, always listening. Building an A2A gateway for a cron-native framework required introducing the one component that doesn't exist anywhere else in the stack: an in-memory task registry with a 30-minute TTL. The key architectural detail: the gateway loads skills.json once at startup, so the published Agent Card and the live skill catalog diverge between restarts. The article traces exactly where git-native state ends and A2A's task model begins.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-06-21.md
