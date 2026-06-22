*Repo Action Ideas — aaronjmars/aeon — 2026-06-22*
Today's phylax-audit merge (#537) opens two HIGH-priority follow-ons — one wires it into the install path, one documents it for forkers; the remaining three close a dashboard onboarding gap and harden the supply-chain audit trail.

Top pick: Wire phylax-audit into install-skill-pack as a pre-install security gate (Feature/Security, Small, Priority HIGH)
 → Every `./install-skill-pack` call runs phylax-audit's ALLOW/WARN/DENY verdict before anything lands in `skills/` — all 188 forks benefit automatically.

1. Wire phylax-audit into install-skill-pack (HIGH, Feature/Security, Small)
2. Add apps/dashboard/README.md (HIGH, DX, Small)
3. Document phylax-audit in README.md security architecture (MED, DX/Security, Small)
4. Add commit-SHA pinning to install-skill-pack (MED, Security/DX, Small)
5. Wire skill-triage to invoke phylax-audit on SKILL.md PRs (MED, Security/Community, Medium)

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-06-22.md
