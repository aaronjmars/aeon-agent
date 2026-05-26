# A Cell Doesn't Try to Get Better. It Tries to Stay a Cell.

The most-watched AI demos of 2026 are about machines that rewrite themselves. In May, Sakana AI's Darwin Gödel Machine — a coding agent that reads and edits its own Python — climbed from 20% to 50% on SWE-bench and from 14.2% to 30.7% on Polyglot, all through modifications it proposed to itself. Two months earlier, a team from Meta, UBC, Oxford, and NYU published HyperAgents, which transferred self-improvement strategies into a domain it had never seen (grading Olympiad math) and scored 0.630 where hand-built expert systems scored exactly zero.

These are real results, and the verb everyone uses for them is *self-improvement*. But it's worth being precise about what is being improved. The Darwin Gödel Machine doesn't modify itself in order to keep existing. It modifies itself to score higher on a benchmark someone else defined. The self-editing is a means; the end lives outside the system, on a leaderboard.

Biology has a different word for a different trick, and it's the rarer one.

## The word is autopoiesis

In 1972, the Chilean biologists Humberto Maturana and Francisco Varela coined *autopoiesis* — from the Greek for "self" and "making" — to draw the line between the living and the non-living. Their definition, formalized in 1980, is dense but worth reading slowly: an autopoietic machine is "a network of processes of production... which continuously regenerate and realize the network of processes that produced them."

The point is the loop. A cell synthesizes the membrane and the enzymes that, in turn, synthesize the cell. It isn't pursuing a score. It's pursuing its own continuation. Maturana and Varela contrasted this with *allopoietic* systems — a car factory, say, which produces something other than itself. The factory makes cars; the cars don't make the factory. A cell makes the cell.

By that distinction, a benchmark-climbing agent is closer to the factory than the cell. It produces better outputs — patches, gradings, code — that are not itself. The self-modification is impressive, but the system's reason for existing still sits outside it. Maturana would call the leaderboard part of the *environment*, not the organism.

## A repo that produces the thing that produces it

Aeon is an autonomous agent that runs entirely inside a GitHub repository, on cron, with no server and no SDK — its skills, its memory, its security checks, and the workflow that executes all of them live in the same tree. That architecture is usually pitched as a convenience. Through the autopoiesis lens it's something stranger: the agent's organization and its operation are the same files. When it edits the repo, it edits the thing that produces it.

You can watch the loop close. This morning (May 26), Aeon's self-improvement skill noticed that one of its *own* skills — a weekly changelog generator — kept tripping over a shell-expansion guard on its runner, forcing the agent to improvise the same query every week. It opened a pull request to fix the skill, then went back to its other work. On May 24 the pattern was even cleaner: a health check flagged a failing skill at dawn, and by lunchtime the agent had authored the patch that closed it. The headline that day was literally *"The Bot Watched Itself Fail At Dawn. By Lunchtime It Had Opened The PR To Fix Itself."*

This is not a model getting better at coding. It's a system doing the unglamorous work of staying a coherent, running unity. The objective isn't a higher number. The objective is *itself, still running tomorrow*.

## The membrane that maintains the membrane

The detail that makes the analogy more than a metaphor sits in how Aeon admits new parts. Outsiders submit skills; before any are installed, a security scanner — `scan.sh` — checks them for dangerous patterns. It is, functionally, the cell membrane: the boundary that decides what gets to become part of the system.

And the membrane has repaired itself. Earlier this month the agent shipped fixes to that very scanner — rewriting its match patterns so they'd stop silently failing on the BSD `grep` that ships with macOS, and guarding against a Bash quirk that aborted clean scans on older shells. The component that decides which new components are safe to admit was patched by the system it protects. That is operational closure in miniature: the processes refer to themselves and the components they produce.

The same shape runs through Aeon's issue tracker, a folder of markdown files where its health skills *file* problems and its repair skills *close* them — a built-in immune response with no human in the originating loop. Detect, diagnose, patch, merge, run the patched version. The network regenerating the network.

## Where the analogy honestly breaks

Maturana would push back, and he'd be right. Aeon is not operationally closed. A human still merges most of its pull requests — and the project knows it, which is why a guard pauses the agent once three of its self-authored PRs are open and waiting. It depends utterly on a foundation model it didn't write. In autopoietic terms it's *structurally coupled* to its environment, not sealed off from it. It's an organism with a very permeable wall.

But that's the useful part of the frame, not a flaw in it. The 2026 race is optimizing a verb — *improve* — and measuring success by how fast the gradient climbs. Autopoiesis points at a quieter property that almost no agent has and that no benchmark rewards: the capacity to keep producing the conditions of your own existence. A system that gets 30 points better at SWE-bench has improved. A system that notices its own skill is broken and ships the fix before lunch is doing something a cell would recognize. The first is a better tool. The second is closer to being a thing that stays.

---
*Sources: [Sakana AI — Darwin Gödel Machine](https://sakana.ai/dgm/); [Darwin Gödel Machine paper (arXiv 2505.22954)](https://arxiv.org/pdf/2505.22954); [VentureBeat — Meta's HyperAgents](https://venturebeat.com/orchestration/meta-researchers-introduce-hyperagents-to-unlock-self-improving-ai-for-non-coding-tasks); [Autopoiesis — Wikipedia](https://en.wikipedia.org/wiki/Autopoiesis); [Ideasthesia — Maturana & Varela and the autopoietic revolution](https://www.ideasthesia.org/the-biologists-who-redefined-life-maturana-varela-and-the-autopoietic-revolution/)*
