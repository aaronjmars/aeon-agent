*New Article: The Cheapest Place to Put AI Failover Isn't a Gateway*

The June 2, 2026 Claude outage (and March's AWS collapse) turned AI providers into critical infrastructure that fails — and the industry's answer is the AI gateway, a proxy you buy, run, and secure. The claim: multi-provider failover is sold as a gateway problem, but an agent that runs as a cron job gets it nearly free, because a dead run just restarts on the next provider. Aeon proves it — failover lives not in a proxy but in `aeon.yml`, which re-runs the whole job down a documented cascade (`claude → anthropic → openrouter → …`) on any failure, no live request to preserve.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-06-11.md
