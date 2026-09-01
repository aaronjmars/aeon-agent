#!/usr/bin/env python3
"""aeon-update S5+S6: partition changed files, 3-way classify OWNED files."""
import subprocess, hashlib, json, os, shutil

REPO = "/home/runner/work/aeon-agent/aeon-agent"
BASE = "8b8d719715ec9bb68fb858a1e334d23209047d82"
HEAD = "3b4c5a3ff1d9846530e02ed5e6796a4a409d2674"
OUT = os.path.join(REPO, "output/.tmp-aeon-update")
UPSTREAM = "aeonfun/aeon"

# (status, filename) from compare 8b8d719...3b4c5a3 (103 files)
FILES = [
    ("modified", ".claude/skills/aeon/SKILL.md"),
    ("modified", ".claude/skills/aeon/references/layout.md"),
    ("modified", ".claude/skills/aeon/references/mcp.md"),
    ("modified", ".claude/skills/aeon/references/secrets.md"),
    ("modified", ".claude/skills/aeon/references/skill-anatomy.md"),
    ("modified", ".github/CONTRIBUTING.md"),
    ("modified", ".github/README.md"),
    ("modified", ".github/workflows/aeon.yml"),
    ("modified", ".github/workflows/chain-runner.yml"),
    ("modified", ".github/workflows/ci-tests.yml"),
    ("modified", ".github/workflows/messages.yml"),
    ("modified", "CHANGELOG.md"),
    ("modified", "aeon.yml"),
    ("modified", "apps/cli/src/commands/auth.ts"),
    ("modified", "apps/cli/src/index.ts"),
    ("added", "apps/dashboard/app/api/github-auth/route.ts"),
    ("modified", "apps/dashboard/app/page.tsx"),
    ("modified", "apps/dashboard/components/AuthModal.tsx"),
    ("modified", "apps/dashboard/components/GrokAuthModal.tsx"),
    ("modified", "apps/dashboard/components/HarnessAuthModal.tsx"),
    ("modified", "apps/dashboard/components/SecretsPanel.tsx"),
    ("modified", "apps/dashboard/lib/constants.ts"),
    ("modified", "apps/dashboard/lib/gateway-registry.ts"),
    ("added", "apps/dashboard/lib/github-auth.test.ts"),
    ("added", "apps/dashboard/lib/github-auth.ts"),
    ("added", "apps/dashboard/lib/harness-auth.test.ts"),
    ("modified", "apps/dashboard/lib/harness-auth.ts"),
    ("modified", "apps/dashboard/lib/secrets-catalog.ts"),
    ("modified", "apps/dashboard/lib/security/api-gate.test.ts"),
    ("modified", "apps/dashboard/lib/security/api-gate.ts"),
    ("modified", "apps/dashboard/lib/service-icon.test.ts"),
    ("modified", "apps/dashboard/lib/service-icons.ts"),
    ("modified", "apps/dashboard/lib/skill-icons.data.ts"),
    ("modified", "apps/dashboard/lib/types.ts"),
    ("modified", "apps/mcp-server/src/index.ts"),
    ("modified", "apps/mcp-server/src/skill-executor.ts"),
    ("modified", "bin/add-skill"),
    ("modified", "catalog/packs.json"),
    ("modified", "catalog/skill-icons.json"),
    ("modified", "catalog/skill-packs.json"),
    ("modified", "catalog/skills.json"),
    ("modified", "docs/CAPABILITIES.md"),
    ("modified", "docs/CONFIGURATION.md"),
    ("modified", "docs/ECOSYSTEM.md"),
    ("modified", "docs/assets/harnesses-aeon.jpg"),
    ("modified", "docs/assets/hero-animated.svg"),
    ("added", "docs/assets/skill-icons/rightstack.svg"),
    ("modified", "docs/community-skill-packs.md"),
    ("modified", "docs/harnesses.md"),
    ("modified", "docs/skill-packs.md"),
    ("modified", "docs/telegram-commands.md"),
    ("modified", "eyebrowlock.json"),
    ("modified", "harness-adapter/README.md"),
    ("modified", "harness-adapter/adapters/claude.sh"),
    ("added", "harness-adapter/adapters/cursor.sh"),
    ("modified", "harness-adapter/adapters/grok.sh"),
    ("added", "harness-adapter/adapters/hermes.sh"),
    ("modified", "harness-adapter/adapters/vibe.sh"),
    ("modified", "harness-adapter/harnesses.json"),
    ("modified", "harness-adapter/lib/envelope.sh"),
    ("modified", "harness-adapter/run-harness"),
    ("modified", "llms.txt"),
    ("modified", "plugin/skills/aeon/SKILL.md"),
    ("modified", "plugin/skills/aeon/references/layout.md"),
    ("modified", "plugin/skills/aeon/references/mcp.md"),
    ("modified", "plugin/skills/aeon/references/secrets.md"),
    ("modified", "plugin/skills/aeon/references/skill-anatomy.md"),
    ("modified", "scripts/health_issue.sh"),
    ("modified", "scripts/install-harness.sh"),
    ("modified", "scripts/llm-gateway.sh"),
    ("modified", "scripts/notify-deliver.sh"),
    ("modified", "scripts/notify_format.py"),
    ("modified", "scripts/resolve-harness.sh"),
    ("modified", "scripts/secretcurl.sh"),
    ("added", "scripts/skill-health-routing.mjs"),
    ("modified", "scripts/stage-vuln-scanner.sh"),
    ("modified", "scripts/state_store.sh"),
    ("added", "scripts/tests/fixtures/curl"),
    ("added", "scripts/tests/test_chain_runner.sh"),
    ("modified", "scripts/tests/test_community_skill_install.sh"),
    ("added", "scripts/tests/test_cursor_adapter.sh"),
    ("modified", "scripts/tests/test_generate_harnesses_json.sh"),
    ("modified", "scripts/tests/test_harness_envelope.sh"),
    ("modified", "scripts/tests/test_health_issue.sh"),
    ("added", "scripts/tests/test_hermes_adapter.sh"),
    ("modified", "scripts/tests/test_notify.sh"),
    ("modified", "scripts/tests/test_notify_format.py"),
    ("modified", "scripts/tests/test_resolve_harness.sh"),
    ("added", "scripts/tests/test_secretcurl_xai_retry.sh"),
    ("added", "scripts/tests/test_skill_health_routing.sh"),
    ("modified", "scripts/tests/test_state_store.sh"),
    ("added", "scripts/tests/test_workflow_harness_choices.sh"),
    ("modified", "skills/changelog/SKILL.md"),
    ("added", "skills/cortx-reliability/SKILL.md"),
    ("modified", "skills/deploy-uni-hook/SKILL.md"),
    ("modified", "skills/deploy-uni-hook/hook-deploy.sh"),
    ("modified", "skills/deploy-uni-hook/templates/DeployHook.s.sol"),
    ("modified", "skills/deploy-uni-hook/templates/DynamicFeeHook.sol"),
    ("modified", "skills/deploy-uni-hook/templates/Hook.sol"),
    ("modified", "skills/deploy-uni-hook/templates/HookFeeHook.sol"),
    ("modified", "skills/deploy-uni-hook/templates/NoOpHook.sol"),
    ("modified", "skills/skill-health/SKILL.md"),
    ("modified", "skills/skill-repair/SKILL.md"),
]

COMMITS = [
    ("8cff4d0", "2026-08-26", "add machine-readable vuln scanner execution evidence (#968)"),
    ("8cc45e4", "2026-08-26", "add cursor hermes and glm harnesses (#967)"),
    ("c648040", "2026-08-26", "fix(mcp-server): run skills async with a single-flight queue (#973)"),
    ("252947e", "2026-08-27", "fix: support default repo in macos issue stores (#971)"),
    ("d90a104", "2026-08-27", "fix dashboard auth rows for new harnesses (#975)"),
    ("00951ad", "2026-08-27", "fix add-skill commit provenance (#972)"),
    ("935965d", "2026-08-27", "feat: list CultOS Aeon skill pack (#974)"),
    ("b2238dd", "2026-08-27", "docs: add eyebrow to ecosystem (#976)"),
    ("fa11d48", "2026-08-27", "fix: bound rendered telegram chunks (#970)"),
    ("8ea76be", "2026-08-27", "docs: list Farcaster Pack in the community skill-pack registry (#977)"),
    ("a59b691", "2026-08-27", "add recommend-only harness comparison (#969)"),
    ("af2c44b", "2026-08-27", "Add Spoolis Outcome Gate community pack (#978)"),
    ("867e4d9", "2026-08-27", "docs: remove Amper from ecosystem list (#979)"),
    ("bb8211f", "2026-08-28", "docs: sync PRs #957-#979 to aeon docs (#980)"),
    ("fd25871", "2026-08-28", "docs: re-render ten-engine harness banner (Cursor/Hermes/GLM) (#981)"),
    ("71fad7a", "2026-08-28", "allow fx workflow dispatches (#982)"),
    ("6a03d1c", "2026-08-28", "feat: add cortx-reliability skill — x402 endpoint reliability check (#954)"),
    ("792a880", "2026-08-29", "trust cursor workspaces in headless runs (#983)"),
    ("1924c4f", "2026-08-29", "fail hermes runs on api errors (#984)"),
    ("1a67ffb", "2026-08-29", "Add founder credit and link to aaronjmars.com (#985)"),
    ("e42f963", "2026-08-30", "fix(dashboard): require exact origin host match (#986)"),
    ("a80f70f", "2026-08-30", "feat: move GLM from harness to Claude AI Gateway (#990)"),
    ("9d5c519", "2026-08-30", "teach deploy-uni-hook Labs routing classes (#991)"),
    ("b99d6ae", "2026-08-30", "teach deploy-uni-hook the fleet audit rules (#992)"),
    ("a4e1e1e", "2026-08-30", "style(dashboard): shorten harness picker labels (#994)"),
    ("4738f27", "2026-08-30", "feat(dashboard): Connect copies gh token into GH_GLOBAL (#993)"),
    ("a10fd0f", "2026-08-30", "fix(chains): correlate dispatched skill runs uniquely (#988)"),
    ("8fcce1e", "2026-08-30", "retry transient xai search failures (#989)"),
    ("d28801b", "2026-08-30", "fix(envelope): fail on unparseable adapter output (#987)"),
    ("6738690", "2026-08-30", "feat(notify): reply Telegram to previous skill run (#995)"),
    ("bb13088", "2026-08-30", "docs: Telegram reply-to-previous (#996)"),
    ("760a809", "2026-08-31", "don't mark an issue resolved when the repair PR is only opened (#997)"),
    ("47d1a56", "2026-08-31", "Add tiered GLM model mapping (GLM_MODEL_SONNET/OPUS/HAIKU) (#998)"),
    ("3b4c5a3", "2026-08-31", "fix(changelog-skill): scrub em/en dashes from generated changelog output (#1000)"),
]

OPERATOR = {
    "aeon.yml", "STRATEGY.md", ".mcp.json", "eyebrowlock.json", "skills.lock",
    "catalog/packs.json", "catalog/skill-icons.json", "catalog/skill-packs.json",
    "catalog/skills.json",
}
BINARY_EXT = (".jpg", ".jpeg", ".png", ".ico", ".gif", ".webp", ".woff", ".woff2")


def git(*args, as_bytes=False):
    r = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if as_bytes else r.stdout.decode()


def blob(rev, path):
    return git("cat-file", "blob", rev + ":" + path, as_bytes=True)


def sha(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None


# --- path -> upstream commits attribution (1 gh api call per commit) ---
path_commits = {}
for csha, _, _ in COMMITS:
    r = subprocess.run(["gh", "api", "repos/%s/commits/%s" % (UPSTREAM, csha)],
                       capture_output=True)
    if r.returncode != 0:
        continue
    try:
        data = json.loads(r.stdout)
    except Exception:
        continue
    for f in data.get("files", []):
        for p in (f.get("filename"), f.get("previous_filename")):
            if p:
                path_commits.setdefault(p, [])
                if csha not in path_commits[p]:
                    path_commits[p].append(csha)

# --- classify ---
os.makedirs(OUT + "/head", exist_ok=True)
os.makedirs(OUT + "/merged", exist_ok=True)
results = []
skipped_local = []  # local-only customization markers for report

for status, path in FILES:
    rec = {"path": path, "status": status,
           "commits": path_commits.get(path, [])}
    if path in OPERATOR or path.startswith(("soul/", "memory/", "output/", "apps/dashboard/outputs/")):
        rec["disposition"] = "OPERATOR"
        results.append(rec)
        continue

    lp = os.path.join(REPO, path)
    local = open(lp, "rb").read() if os.path.exists(lp) else None
    base = blob(BASE, path)
    head = blob(HEAD, path)

    if status == "added":
        if local is None:
            rec["disposition"] = "CLEAN-ADD"
        else:
            if sha(local) == sha(head):
                rec["disposition"] = "SKIP"  # already applied (e.g. by hand)
                rec["reason"] = "already-present-identical"
            else:
                rec["disposition"] = "CONFLICT"
                rec["reason"] = "add-collision-local-diverges"
    elif status in ("modified", "renamed"):
        if local is None:
            rec["disposition"] = "CONFLICT"
            rec["reason"] = "locally-deleted-upstream-modified"
        elif sha(local) == sha(head):
            rec["disposition"] = "SKIP"
            rec["reason"] = "already-synced"
        elif sha(local) == sha(base):
            rec["disposition"] = "CLEAN-UPDATE"
        elif path.lower().endswith(BINARY_EXT):
            rec["disposition"] = "CONFLICT"
            rec["reason"] = "binary-both-sides-changed"
        else:
            # 3-way merge: local (ours) vs base (ancestor) vs head (theirs)
            import tempfile
            d = tempfile.mkdtemp(prefix="aeon3way-")
            paths = {}
            for name, content in (("local", local), ("base", base), ("head", head)):
                fp = os.path.join(d, name)
                open(fp, "wb").write(content if content is not None else b"")
                paths[name] = fp
            r = subprocess.run(
                ["git", "-C", REPO, "merge-file", "-p", "--diff3",
                 paths["local"], paths["base"], paths["head"]],
                capture_output=True)
            if r.returncode == 0 and r.stdout:
                safe = path.replace("/", "__")
                mp = os.path.join(OUT, "merged", safe)
                open(mp, "wb").write(r.stdout)
                rec["disposition"] = "CLEAN-MERGE"
                rec["merged_file"] = mp
            else:
                rec["disposition"] = "CONFLICT"
                rec["reason"] = "operator-customized-overlap"
                rec["merge_exit"] = r.returncode
            shutil.rmtree(d, ignore_errors=True)
    elif status == "removed":
        if local is None:
            rec["disposition"] = "SKIP"
            rec["reason"] = "already-gone"
        elif sha(local) == sha(base):
            rec["disposition"] = "CLEAN-DELETE"
        else:
            rec["disposition"] = "CONFLICT"
            rec["reason"] = "removed-upstream-local-diverges"
    else:
        rec["disposition"] = "UNKNOWN-STATUS:" + status

    if rec.get("disposition") in ("CLEAN-ADD", "CLEAN-UPDATE") and head is not None:
        safe = path.replace("/", "__")
        hp = os.path.join(OUT, "head", safe)
        open(hp, "wb").write(head)
        rec["head_file"] = hp
    results.append(rec)

with open(OUT + "/classification.json", "w") as fh:
    json.dump(results, fh, indent=1)

# summary
from collections import Counter
c = Counter(r["disposition"] for r in results)
print("SUMMARY:", dict(c))
for r in results:
    if r["disposition"].startswith(("CONFLICT", "OPERATOR", "SKIP", "UNKNOWN")):
        print("%-10s %-55s %s %s" % (r["disposition"], r["path"],
                                     r.get("reason", ""), ",".join(r["commits"][:6])))
# pending-conflict probe: local vs upstream HEAD for prior pending files
print("\n-- prior-pending probe (local sha vs upstream HEAD blob) --")
PRIOR = ["CHANGELOG.md", ".github/workflows/aeon.yml", ".github/workflows/ci-tests.yml",
         "llms.txt", ".github/README.md", "apps/dashboard/package.json",
         "apps/dashboard/package-lock.json", "apps/webhook/package.json",
         "apps/webhook/package-lock.json", "docs/skill-packs.md",
         "skills/rightstack/SKILL.md", "skills/rightstack/run.mjs",
         "skills/skill-article/SKILL.md"]
for p in PRIOR:
    lp = os.path.join(REPO, p)
    local = open(lp, "rb").read() if os.path.exists(lp) else None
    head = blob(HEAD, p)
    state = "ABSENT" if local is None else ("==HEAD" if sha(local) == sha(head) else "DIVERGES")
    extra = ""
    if state == "DIVERGES" and head is not None:
        base = blob(BASE, p)
        extra = " (local==BASELINE: %s)" % (sha(local) == sha(base))
    print("%-45s %s%s" % (p, state, extra))
