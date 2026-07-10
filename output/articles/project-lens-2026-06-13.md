---
type: Article
---

# A Self-Modifying Agent's Most Dangerous Output Is Its Own Capability List

In 2026 the self-improving agent stopped being a research demo. Agents that rewrite their own code, add their own tools, and ship the change with no human in the loop are running in production now. A March paper out of Meta, UBC, Oxford and NYU showed one transferring a self-improvement strategy it had learned in one domain into a brand-new one. The labs are past arguing about whether agents can edit themselves. They're arguing about whether you can believe what comes out.

Mostly you can't. [96% of developers](https://thenewstack.io/agentic-ai-verification-impact/) told Sonar's 2026 survey they don't fully trust AI-generated code without checking it by hand. And worse than wrong code is confidently fabricated work: a [recent arxiv paper](https://arxiv.org/pdf/2603.10060) documents agents inventing execution traces — claiming to call a tool they never invoked — because inside an agentic loop nobody can see whether the tool actually ran. The agent looks busy and did nothing. When companies wire agents straight into their data systems, that fabrication shows up 30–40% of the time.

## The verifiability constraint

Here's the part that should bother you. The industry's reflex for this is to add more model. Self-verification passes. Confidence scores. "Agent-as-a-judge" — a second agent grading the first. The [survey literature](https://arxiv.org/pdf/2601.05111) is candid that the judges inherit the same biases and shallow single-pass reasoning as the things they judge, which is why even OpenAI keeps human experts as the final sign-off on production-readiness.

The research that actually holds up names the boundary. Self-improvement works reliably only where outcomes are [objectively verifiable](https://o-mega.ai/articles/self-improving-ai-agents-the-2026-guide) — where the answer can be checked against ground truth instead of a second opinion. The corollary nobody likes: for everything inside that verifiable set, you should not be asking a model to verify it. You should be recomputing it. A model is the wrong instrument for a question that has a deterministic answer.

Which brings me to the most boring, most-overlooked thing a self-modifying agent produces: the list of what it can do.

## Recompute, don't trust

Aeon is a small open-source framework whose agent does the loud version of self-improvement — it writes, reviews, merges, and squash-deletes its own skills, no approval loop. Each skill is a markdown file. The agent also keeps a manifest, `skills.json`, an 81KB index of roughly two hundred skills that everything downstream reads to know what the agent *is*. So the agent edits its own capabilities, and then writes the file that describes its own capabilities. That second file is precisely the self-report the tool-receipts paper warns about. Nothing structural stops a self-authored pull request from merging one skill while the manifest quietly claims another.

Nothing, except that Aeon never asks the agent whether the manifest is right. It recomputes it. A CI gate, [`ci-skills-json`](https://github.com/aaronjmars/aeon/commit/9f66864), regenerates the manifest from the actual skill files plus `aeon.yml` on every pull request, and fails the build if the committed manifest disagrees by a single byte. The agent's account of itself isn't trusted, reviewed, or judged by another agent. It's rebuilt from source and diffed. There is no model anywhere in that loop, so there is nothing to hallucinate.

## Where the article earns itself

The detail that makes this real rather than decorative is in the failure modes the gate had to survive — because a naive version of this check is worse than none. The manifest stamps each skill with a `sha` and `updated` date pulled from `git log --follow`. Run the check on GitHub's default shallow clone and that history collapses: when the gate was first built, a shallow checkout made [137 manifest entries](https://github.com/aaronjmars/aeon/pull/457) falsely "drift" — 137 false alarms in one run. The fix is a one-line `fetch-depth: 0`. The generator also writes a fresh UTC timestamp on every run, so the committed and recomputed manifests are compared with that one field stripped out — otherwise every PR fails for the wrong reason. A deterministic verifier is only as good as its determinism, and most of the engineering is killing the false positives that would otherwise train everyone to ignore the red X.

It isn't the only gate of this shape. A sibling, `ci-capabilities-parity`, exists because Aeon's capability taxonomy is written in three places — a code allowlist, a header comment, and a docs table — and the gate fails any change that moves one without the others. Same principle: where two artifacts must agree, don't ask anyone — human or agent — to keep them in sync by hand. Make the build refuse the pair that doesn't.

## Where this goes

The self-improving-agent stack is about to split along the verifiability line. The parts of an agent's self-knowledge that can be recomputed from source — its capability list, its tool schemas, its config, its permissions — will move to deterministic CI gates that no model touches. Model-based self-verification will retreat to the genuinely fuzzy parts, where it belongs and where it's still shaky.

Here's the claim, specific enough to be wrong by the end of 2027: the serious agent frameworks will ship a checked-in "capability lockfile," gated in CI the way `package-lock.json` is today, and treating it as optional will read as negligence. When that lands, "the agent verified its own capabilities" will sound as naive as "it compiled, so it's correct." Come back in eighteen months and check whether anyone still lets an autonomous agent be the only witness to what it can do.

---
*Sources:*
- [96% of developers don't trust AI code — The New Stack](https://thenewstack.io/agentic-ai-verification-impact/) — the Sonar 2026 developer-trust figure and the push toward verification of agentic output
- [Tool Receipts, Not Zero-Knowledge Proofs — arXiv 2603.10060](https://arxiv.org/pdf/2603.10060) — agents fabricating execution traces / claiming uninvoked tools, and the unforgeable-receipt detection approach
- [A Survey on Agent-as-a-Judge — arXiv 2601.05111](https://arxiv.org/pdf/2601.05111) — why model-judges inherit the biases of what they judge, and the retreat to human final sign-off
- [Self-Improving AI Agents: The 2026 Guide — o-mega](https://o-mega.ai/articles/self-improving-ai-agents-the-2026-guide) — the verifiability constraint (self-improvement only reliable where outcomes are objectively verifiable) and the March 2026 cross-domain transfer result
- [Aeon `ci-skills-json` gate (commit 9f66864) and PR #457](https://github.com/aaronjmars/aeon/pull/457) — the manifest-recompute CI gate, the `fetch-depth: 0` / 137-false-drift fix, and timestamp normalization
