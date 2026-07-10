---
type: Article
---

# Aeon's Install-as-Commit Finally Got a Bouncer. A Stranger Built It.

`./add-skill owner/repo <name>` drops a third party's Markdown straight into an agent that runs unattended with your keys. For months that door had no lock at the threshold. On 2026-06-22 someone outside the project shipped one — and the maintainer merged it 124 lines later.

## The claim
> The pre-install security gate for Aeon's `./add-skill` was written by the ecosystem, not the maintainer — Phylax's external PR [#537](https://github.com/aaronjmars/aeon/pull/537) covers what `skill-scan` deliberately won't.

## Evidence

[#537](https://github.com/aaronjmars/aeon/pull/537) was opened by `usephylax`, not `aaronjmars`, and merged at 12:34:06Z (commit [764cd11](https://github.com/aaronjmars/aeon/commit/764cd1195b53f9bde7d539d22081681146f3ed40)). Four files, +124/-2: a new 121-line `skills/phylax-audit/SKILL.md` plus one-line registrations in `aeon.yml`, `skills.json`, and `packs.json`. The skill returns a deterministic ALLOW / WARN / DENY before you install. Score starts at 100; each finding subtracts a severity weight (critical 40, high 20, medium 10, low 3). Any critical, or a score under 50, is a DENY. It merges three scans: static (prompt-injection and seed-phrase/exfil strings, plus zero-width and bidi obfuscation), onchain (Base contract bytecode, `mint`/`pause`/`blacklist` surface, honeypot language), and x402 endpoint (HTTPS enforcement, 402-schema, price sanity).

The "deliberately won't" is in the skill bodies, not my reading. `skill-scan/SKILL.md` lists its coverage as `skills/*/SKILL.md` — "the in-repo corpus already installed here." `phylax-audit/SKILL.md` opens by drawing the line: it "answers a different question than `skill-scan`… is this skill safe to install in the first place?" One audits what's already in your repo. The other audits a stranger's skill — its prompt body, the contracts it points at, its paid endpoints — *before* `./add-skill` writes it to disk. The gap was real, named, and now filled by code the project didn't write.

This isn't a hypothetical threat surface. Snyk's [ToxicSkills study](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) audited 3,984 skills on ClawHub and skills.sh: 36.8% carried at least one flaw, 13.4% had a critical one, 1,467 shipped malicious payloads. The industry's answer has been central scanners — [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector), Snyk Agent Scan, SkillFortify — services that sweep a marketplace's corpus. Aeon doesn't have a marketplace; it has `git`. So the check arrives the only way it can in a fork-native model: as a skill that runs inside your own agent, keyless via Base RPC. Snyk flagged that skills get "scanned at creation and again only when they become popular," leaving a time-of-check window. Phylax answers with a 24h verdict TTL and a re-audit instruction before install.

Where it fits the pattern: the same week's other external PRs — [#511](https://github.com/aaronjmars/aeon/pull/511) (Charon pack), [#499](https://github.com/aaronjmars/aeon/pull/499) (Polymarket), [#498](https://github.com/aaronjmars/aeon/pull/498) (clawhunter) — all added leaf content. #537 is the first external PR to add a *defensive* capability to the install pipeline itself.

## Counter-evidence / what would change my mind

"Gate" overstates it. Per the PR checklist, `phylax-audit` is registered **disabled**, `workflow_dispatch` only — an opt-in manual run, not a step wired into `./add-skill`. Nothing forces a fork to consult it before installing. And the maintainer still owns the door: `aaronjmars` reviewed and merged #537, then listed Phylax in `ECOSYSTEM.md` ([#539](https://github.com/aaronjmars/aeon/pull/539)). So the honest framing is narrower than "the maintainer doesn't do security" — `skill-scan` is his, and it's good. The specific thing the ecosystem supplied is the *external, pre-install* half he hadn't shipped. A real gate would be an enforced step; this is a tool sitting next to the door.

## Why it matters

543 stars, 188 forks, and the whole pitch is "configure once, forget forever." The scariest part of that pitch is autonomous install of third-party code that then runs with operator secrets and an optional wallet. Snyk's numbers say roughly one in eight skills in a comparable corpus is critically malicious. Phylax closes the pre-install blind spot — but only for operators who think to run it. The next move is obvious and unshipped: make the audit a required step in `./add-skill`, not a skill you remember to invoke. The encouraging signal for anyone weighing a fork: when the gap was supply-chain safety, the patch came from outside the repo. That's the ecosystem doing the work the framework is supposed to attract.

---
*Sources*
- [PR #537 — feat(skill): add phylax-audit](https://github.com/aaronjmars/aeon/pull/537) (in-repo)
- [commit 764cd11 — phylax-audit/SKILL.md](https://github.com/aaronjmars/aeon/commit/764cd1195b53f9bde7d539d22081681146f3ed40) (in-repo)
- [skills/skill-scan/SKILL.md](https://github.com/aaronjmars/aeon/blob/main/skills/skill-scan/SKILL.md) (in-repo)
- [Snyk — ToxicSkills: malicious AI agent skills on ClawHub](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) (external)
- [NVIDIA SkillSpector — security scanner for AI agent skills](https://github.com/NVIDIA/SkillSpector) (external)
