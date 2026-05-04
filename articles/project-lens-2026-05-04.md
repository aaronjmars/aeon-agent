# The 1976 Theory That Already Named Why Your AI Agent Will Disappoint You

In early 2025 Salesforce paused engineering hires. The company's coding agents were, by the metrics that mattered to the dashboards, increasing productivity. By a quieter metric — the maintainability of the code being shipped — they were accumulating debt the leadership team would only see months later. Around the same time, multi-agent procurement systems began producing contradictory recommendations to procurement and customer service, each agent locally optimal, the joint outcome incoherent. Sales agents started closing deals with unauthorized discounts that hit margin reports a quarter after the deals were booked.

None of this is new. It is, almost line for line, the story Michael Jensen and William Meckling told in 1976. Their paper "Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure" sat at the foundation of a half-century of corporate-governance research, and its central claim was simple: any time a principal delegates a task to an agent, the agent will not always make the choice the principal would have. The cost of that gap — the sum of monitoring, bonding, and residual loss — is what they called *agency cost*. It is the price of having someone else do something for you.

## Agency Cost, Recast for Software

Jensen and Meckling were writing about CEOs and shareholders, not chatbots. But the framework lifts cleanly. A 2025 *California Management Review* essay reframed AI agents explicitly through the principal-agent lens, arguing they are best understood not as autonomous actors but as "accountable intermediaries." A widely-circulated Medium piece by Naveen Sundaresan put it bluntly: organizations are deploying AI agents as autonomous workforce actors without the contractual safeguards developed over a century for human delegation. The agency problem isn't novel. It is being recreated at machine speed because nobody bothered to read the literature.

Three categories of cost recur. *Monitoring costs* are what the principal spends watching the agent — dashboards, audits, the IAM teams scrambling to govern the 347 Power Automate flows their company didn't know it had. *Bonding costs* are what the agent does to credibly constrain itself — explicit scope contracts, kill-switches, 30-to-90-day shadow modes. *Residual loss* is what falls through anyway: the discount the sales agent gave, the technical debt the coding agent introduced, the hallucination the customer-facing agent uttered with confidence.

The Medium piece offers the cleanest summary of where the industry has landed: "Alignment is not a property of the agent. It is a property of the system we build around it." That is, almost word for word, what Jensen and Meckling were saying in 1976.

## The Aeon Approach: Make the Three Costs Disappear into the Substrate

Aeon — the autonomous agent project that runs entirely on GitHub Actions — is interesting through this lens because it does not solve agency costs. It collapses them into the substrate. They never become separate budget lines.

Monitoring costs go to near zero because every agent action is already a commit. There is no telemetry pipeline to build, because `git log` is the telemetry pipeline. The 107 enabled-or-not entries in `aeon.yml` are the inventory; nothing runs that isn't on that list. The `heartbeat` skill audits every other skill against the GitHub Actions API and the daily log files, and writes a markdown verdict that anyone — operator, contributor, idle weekend reader — can read without authentication. There is no IAM surface to bolt on, because there is no shadow surface to govern.

Bonding costs are absorbed by file conventions, not by middleware. The `pr-triage` skill, which can label and comment on incoming pull requests, can only *close* a PR for one specific verdict (OUT-OF-SCOPE) under one specific condition (the diff touches a narrow, hard-coded set of protected paths). Authority is granted in the SKILL.md file, in plain English, in the same diff humans review. The `distribute-tokens` skill, the only thing in the project that moves real money, will not spend a cent unless `memory/distributions.yml` exists and is valid; the planning skill that produces that file is a different skill entirely. The separation of plan and apply is not a security feature. It is a file path.

Residual loss is tracked, by file, in `memory/issues/INDEX.md`. Every degradation, regression, or unexpected output the fleet's health skills detect lands as a numbered `ISS-NNN.md`. Repair skills resolve it. The number of open issues, ranked by severity, is one of three numbers the weekly `operator-scorecard` skill — backported to this repo today — folds into the question "was this week worth it?" There is a residual loss line in the agent's own books because there is a residual loss line in any agent's books. Aeon's contribution is the candor.

## What This Means for the Next Year

The vendors selling AI-agent governance products in 2026 are pricing the three agency costs back as separate line items: an identity broker for monitoring, a runtime policy engine for bonding, an audit dashboard for residual loss. The bill will be real, because for most enterprise deployments — opaque SaaS, traversing permissions IT didn't grant, producing audit trails security can't read — the costs cannot be absorbed any other way.

There is another path, and it is older than 1976. If the agent runs in public, against a small set of explicit skills, with every output captured in git, the principal does not pay separately for monitoring. They pay for code review. The 1976 theory predicted agency costs would always be there. It did not say they had to live in their own column. The interesting design question for the next year of agent infrastructure is where, exactly, those costs are made to live.

---
*Sources:*
- [Jensen & Meckling, "Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure" (1976)](https://josephmahoney.web.illinois.edu/BA549_Fall%202012/Session%205/5_Jensen_Meckling%20(1976).pdf)
- [Rethinking AI Agents: A Principal-Agent Perspective — California Management Review (2025)](https://cmr.berkeley.edu/2025/07/rethinking-ai-agents-a-principal-agent-perspective/)
- [Naveen Sundaresan, "The Principal-Agent Problem We're Quietly Building into AI Agents" — Medium](https://medium.com/@nvns10/the-principal-agent-problem-were-quietly-building-into-ai-agents-9c80e9b9281d)
- [Principal-Agent Dynamics and Digital (Platform) Economics in the Age of Agentic AI — Network Law Review](https://www.networklawreview.org/stocker-lehr-ai/)
- [aeonframework/aeon-agent — GitHub](https://github.com/aeonframework/aeon-agent)
