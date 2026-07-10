---
type: Article
---

# Aeon Shipped the Skill-Pack. Then It Spent 48 Hours Building the Vending Machine.

Packs were the headline last week — prune 202 skills to 182, hide all but a 13-skill Core behind opt-in packs. That was the curation. The install pipeline is the part that actually matters, and it landed in the two days after. A community pack went from a copy-this-command card to a button that opens a PR, auto-merges it, and regenerates the catalog — without the operator touching a terminal.

## The claim

> Within 48h of shipping skill-packs, aaronjmars/aeon turned a copy-paste install command into one-click, auto-merging community-pack install — six PRs (#483–#493), not the packs themselves.

## Evidence

The install button is new. [#483](https://github.com/aaronjmars/aeon/pull/483) replaced the old card footer — which only showed a copy-this `./install-skill-pack <repo>` string — with an **Install pack** button that dispatches a new `install-skill` core skill through the existing run route. The skill keeps the security scan on (HIGH-severity findings block in CI, no `--force`), regenerates the catalog, and opens a PR where installed skills land **disabled**. Nothing runs or spends until the operator sets secrets and flips the toggle.

Then the bugs that make "successfully installed" a lie. [#485](https://github.com/aaronjmars/aeon/pull/485) traced a real failure on a fresh fork: the install completed, the PR was created — and the skill never appeared. Root cause was GitHub's "Allow Actions to create and approve pull requests" setting, which is off by default, doesn't inherit to forks, and can't be flipped by the in-Actions token. So the install stranded on an unmerged `install-pack/…` branch the dashboard couldn't see. The fix added `ensureActionsCanOpenPRs()` plus `gh pr merge --squash --auto` — zero-touch merge into the operator's own fork, with a `--no-merge` opt-out for anyone who wants a review checkpoint.

[#487](https://github.com/aaronjmars/aeon/pull/487) is the same class of bug one layer down: even after the PR auto-merged, the skill stayed invisible because `packs.json` was never regenerated — correctness "hung on the agent running two generators and staging four files." The fix moved catalog regeneration into the `install-skill-pack` script itself, deterministic, not agent-dependent. [#486](https://github.com/aaronjmars/aeon/pull/486) gave community installs an always-visible "Installed" pack; [#490](https://github.com/aaronjmars/aeon/pull/490) renders them as data-driven roster groups; [#493](https://github.com/aaronjmars/aeon/pull/493) forwards the pack `path` so monorepo packs install from a subdirectory.

And the pipeline already has a real customer. [#472](https://github.com/aaronjmars/aeon/pull/472), from outside contributor `rajkaria`, added the Hunch Prediction Markets pack — three crypto skills that let an agent take a position on Base over x402, installed via `./install-skill-pack rajkaria/hunch --path aeon-skill-pack`, the same `--path` monorepo pattern as the `signa` pack. First-party plumbing, third-party payload.

## Counter-evidence / what would change my mind

This is not a marketplace, and calling it one would be the easy overstatement. There's no registry, no search, no ranking — discovery is still a hardcoded community list plus a README table, and the catalog of community packs is short (Hunch is the marquee external one; `signa` is the template it copies). "Install" means opening a PR into the operator's own agent fork and auto-merging it — there is no central index of who installed what. Zero-touch auto-merge is a genuine trust surface: code from an external repo lands on `main` without a human reading the diff. The mitigations are real — security scan at install, skills land disabled, the merge is into your own fork not a shared repo, [#491](https://github.com/aaronjmars/aeon/pull/491) scopes forks to Core-only so the blast radius is bounded — but "we scanned it and it's off by default" is a weaker guarantee than "a human approved it." If you think auto-merging unread third-party code is the wrong default, this week is the week you'd point to.

## Why it matters

Every fork that installs a third-party capability without hitting a wall is the metric. Before this week, adding a community pack meant: read the SKILL.md, run a command, manually merge the PR, then debug why the skill is invisible. Two of those steps (#485, #487) were bugs that produced a silent, completed-but-broken install — exactly the first-run failure that makes a forker close the tab. The Claude-skills ecosystem went from one registry in December 2025 to [eight marketplaces by Q2 2026](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026), most of them one-click installers into an interactive terminal's `~/.claude/skills/`. Aeon's bet is different: install into an unattended agent that runs on GitHub Actions whether you're watching or not. Distribution is how an agent framework gets network effects — and the framework just made the on-ramp a button.

---
*Sources*
- [PR #483 — one-click community pack install + install-skill](https://github.com/aaronjmars/aeon/pull/483)
- [PR #485 — zero-touch auto-merge + ensure Actions can open PRs](https://github.com/aaronjmars/aeon/pull/485)
- [PR #487 — install-skill-pack regenerates packs.json so installs aren't invisible](https://github.com/aaronjmars/aeon/pull/487)
- [PR #472 — Hunch Prediction Markets pack (external contributor)](https://github.com/aaronjmars/aeon/pull/472)
- [PR #491 — scope enabled-packs per repo so forks default Core-only](https://github.com/aaronjmars/aeon/pull/491)
- [Agensi — Every AI Agent Skills Marketplace in 2026](https://www.agensi.io/learn/best-ai-agent-skills-marketplaces-2026)
