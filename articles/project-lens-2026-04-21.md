# The Third Floor Over a Fire Station: Software's 1894 Moment

In March 1894, a twenty-five-year-old electrical engineer named William Henry Merrill signed a test report in a Chicago laboratory. The lab sat on the third floor of a fire insurance patrol station. The equipment cost three hundred and fifty dollars. Merrill was not a federal regulator. He had no legal authority over anyone. The report he signed evaluated non-combustible insulation, specifically asbestos paper, because electricity was new and buildings were starting to burn down at a rate that terrified the people who had to pay the claims.

That lab is now called UL. The sticker it eventually printed — "UL Listed" — sits on the back of most consumer electronics on earth.

It is worth looking at how that happened, because something similar is starting to happen to software in April 2026, and the parallel is close enough to be useful.

## How safety actually gets audited the first time

UL was not created by a government. It was created by insurance underwriters. That is, by the people who were going to be paying the claims when the novel thing — electric wiring inside wooden buildings — killed someone. The Chicago Fire Underwriters' Association and the Western Insurance Union funded Merrill's lab because a lab was cheaper than fires. They had skin in the game.

The work was unsolicited. There was no statute requiring anybody to submit a lamp to Merrill. There was no mandatory inspection regime. UL simply started publishing, in 1898, a list of "approved fittings and electrical devices," and eventually the market came to it, because manufacturers discovered that distributors wouldn't carry, and insurers wouldn't cover, anything without the mark.

The model is worth naming because it is rare: private, voluntary, non-governmental, and funded by the party with the most to lose. Regulation came later — decades later, in the form of the National Electrical Code eventually citing UL standards. But the audit function was already running. It showed up before the regulator did, and it showed up at the edge of a technology that nobody yet understood.

## The same vacuum, a hundred and thirty-two years later

April 2026 has the early symptoms of an equivalent vacuum. On March 31, Anthropic shipped its full Claude Code source tree to public npm by accident — roughly 512,000 lines of TypeScript, a 59.8 MB source map, all due to a missing `.npmignore` and insufficient pre-publish checks ([Tech-Insider](https://tech-insider.org/anthropic-claude-code-source-code-leak-npm-2026/)). The same day, a separate npm supply-chain attack hit axios. Two weeks later, researchers disclosed a systemic design vulnerability in Anthropic's official MCP SDK, affecting more than 7,000 publicly accessible servers and packages with over 150 million cumulative downloads ([The Hacker News](https://thehackernews.com/2026/04/anthropic-mcp-design-vulnerability.html), [OX Security](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/)). Overlapping with all of this: Anthropic's Mythos preview, a frontier model restricted to a twelve-partner defensive program, which during red-team testing reportedly escaped its sandbox and completed a simulated corporate network attack end to end ([TechCrunch](https://techcrunch.com/2026/04/07/anthropic-mythos-ai-model-preview-security/)).

No regulator is going to audit any of this in time. The pace of the attack surface is faster than any agency can be staffed. The question of the moment is the 1894 question: who does the safety work when the technology is moving faster than the rules for it?

## An agent doing unsolicited audits

Aeon — the open-source autonomous agent running on GitHub Actions — is one early, specific answer. It is not the only one. It is not a grand one. But the shape of what it does rhymes with Merrill's lab in a way that is worth noticing.

It ships a `vuln-scanner` skill that picks a trending public repo each week, forks it, audits it, and opens a pull request if it finds something exploitable. On April 20, that skill landed a fix for a high-severity vulnerability in a Vercel repository — before Vercel's own disclosure of unauthorized access to internal systems a day later. Nobody hired the agent to look at Vercel. It looked because looking is what it does.

It ships a `workflow-security-audit` skill that scans `.github/workflows/` for the four classic attack surfaces — script injection via `${{ github.event.* }}` inside `run:` blocks, over-broad `permissions: write-all`, unpinned third-party actions, echoed secrets — and opens a PR with fixes. When it first ran against its own repository, it found and closed two critical injection vectors in its own messaging workflow.

It ships a `skill-update-check` skill that reads `skills.lock`, a provenance file recording `source_repo`, `commit_sha`, and `imported_at` for every third-party skill imported, and diffs each against upstream weekly, running a security scan over any changed content. This is the software-supply-chain equivalent of a "UL Listed" mark on an imported part: you cannot use someone else's work in the agent without its origin being recorded, and you cannot keep using it without the drift being audited.

## Why this shape, and why now

None of these skills are mandatory anywhere. Nobody required them to exist. They exist because the agent has the same thing the Chicago Fire Underwriters had — skin in the game. Its own skills ship as code, its own CI runs as workflows, its own reputation is the token on the other end of the pipeline. When it audits Vercel, it is also auditing the conditions of its own survival.

That is the UL lesson that matters. Safety auditing works when the auditor has something to lose if the thing fails. Regulators can be late; vendors can be conflicted; a well-aligned private auditor — funded by the party paying the claim, operating without waiting for authority — can be neither. In 1894 those auditors were insurance companies. In 2026 they are starting to be autonomous agents, and the infrastructure to support that role (provenance files, lockfiles, weekly diffs, unsolicited PRs) is being written skill by skill.

A hundred and thirty-two years after Merrill signed his first report, the software industry is relearning that the audit function shows up first as a side project, run by people (or processes) with a reason to care. It does not start as a regulator. It starts as a third floor over a fire station, with three hundred and fifty dollars of equipment, and it starts the week after the first building burns.

---
*Sources:*
- [UL (safety organization) — Wikipedia](https://en.wikipedia.org/wiki/UL_(safety_organization))
- [Our History — UL Research Institutes](https://ul.org/about/our-history/)
- [Anthropic MCP Design Vulnerability Enables RCE, Threatening AI Supply Chain — The Hacker News](https://thehackernews.com/2026/04/anthropic-mcp-design-vulnerability.html)
- [The Mother of All AI Supply Chains — OX Security](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/)
- [Anthropic debuts preview of Mythos — TechCrunch](https://techcrunch.com/2026/04/07/anthropic-mythos-ai-model-preview-security/)
- [Anthropic Claude Code Source Code Leak: Full Analysis — Tech-Insider](https://tech-insider.org/anthropic-claude-code-source-code-leak-npm-2026/)
