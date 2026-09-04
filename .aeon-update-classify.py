#!/usr/bin/env python3
import subprocess, hashlib, os, json, sys

BASE = "3b4c5a3ff1d9846530e02ed5e6796a4a409d2674"
HEAD = "bf33365164c5a8b50d49a0ed64a45521dbe96771"

added = [
 "scripts/dev-loop-pr.sh",
 "scripts/skill_health_recovery.py",
 "scripts/tests/fixtures/vuln-poc-foundry/foundry.toml",
 "scripts/tests/fixtures/vuln-poc-foundry/src/Fixture.sol",
 "scripts/tests/live_vuln_poc_gate.sh",
 "scripts/tests/test_chain_runner_invalid_dispatch.sh",
 "scripts/tests/test_dev_loop_handoff.sh",
 "scripts/tests/test_fleet_scorecard.mjs",
 "scripts/tests/test_llm_gateway.sh",
 "scripts/tests/test_skill_health_recovery.py",
 "scripts/tests/test_vuln_poc_gate.sh",
 "scripts/vuln-poc-gate.sh",
]
modified = [
 ".claude/skills/aeon/references/secrets.md",
 ".github/dependabot.yml",
 ".github/workflows/aeon.yml",
 ".github/workflows/chain-runner.yml",
 ".github/workflows/ci-skill-integrity.yml",
 ".github/workflows/ci-tests.yml",
 ".github/workflows/messages.yml",
 "CHANGELOG.md",
 "apps/cli/package-lock.json",
 "apps/cli/package.json",
 "apps/dashboard/package-lock.json",
 "apps/dashboard/package.json",
 "apps/mcp-server/package-lock.json",
 "apps/mcp-server/package.json",
 "apps/webhook/package-lock.json",
 "apps/webhook/package.json",
 "docs/CONFIGURATION.md",
 "docs/ECOSYSTEM.md",
 "docs/skill-integrity.md",
 "plugin/skills/aeon/references/secrets.md",
 "scripts/fleet-scorecard.mjs",
 "scripts/llm-gateway.sh",
 "scripts/notify-deliver.sh",
 "scripts/skill_mode.sh",
 "scripts/stage-vuln-scanner.sh",
 "scripts/tests/test_notify.sh",
 "scripts/tests/test_skill_mode.sh",
 "skills/deploy-uni-hook/templates/DeployHook.s.sol",
 "skills/deploy-uni-hook/templates/Hook.t.sol",
 "skills/feature/SKILL.md",
 "skills/pr-review/SKILL.md",
 "skills/remotion/project/package-lock.json",
 "skills/skill-health/SKILL.md",
 "skills/vuln-scanner/SKILL.md",
]

def blob(ref, path):
    r = subprocess.run(["git","show",f"{ref}:{path}"],capture_output=True)
    if r.returncode!=0: return None
    return r.stdout

def sh(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None

def local(path):
    if not os.path.exists(path): return None
    with open(path,"rb") as f: return f.read()

results={"CLEAN-ADD":[],"CLEAN-UPDATE":[],"CLEAN-MERGE":[],"CLEAN-DELETE":[],"SKIP":[],"CONFLICT":[]}

for p in added:
    l=local(p)
    if l is None:
        results["CLEAN-ADD"].append(p)
    else:
        h=blob(HEAD,p)
        if sh(l)==sh(h):
            results["SKIP"].append((p,"added-but-identical-local"))
        else:
            results["CONFLICT"].append((p,"add-collision"))

for p in modified:
    l=local(p); b=blob(BASE,p); h=blob(HEAD,p)
    if l is None:
        results["CONFLICT"].append((p,"modified-upstream-absent-local"))
        continue
    if sh(l)==sh(h):
        results["SKIP"].append((p,"already-synced"))
    elif sh(l)==sh(b):
        results["CLEAN-UPDATE"].append(p)
    else:
        # 3-way merge
        os.makedirs(".aeon-update-tmp",exist_ok=True)
        lp=".aeon-update-tmp/local"; bp=".aeon-update-tmp/base"; hp=".aeon-update-tmp/head"
        with open(lp,"wb") as f: f.write(l)
        with open(bp,"wb") as f: f.write(b if b else b"")
        with open(hp,"wb") as f: f.write(h if h else b"")
        r=subprocess.run(["git","merge-file","-p","--diff3",lp,bp,hp],capture_output=True)
        if r.returncode==0:
            results["CLEAN-MERGE"].append((p,r.stdout.decode("utf-8","replace")))
        else:
            results["CONFLICT"].append((p,"operator-customized-overlap"))

# print summary
for k in ["CLEAN-ADD","CLEAN-UPDATE","CLEAN-DELETE","SKIP","CONFLICT"]:
    print(f"== {k} ({len(results[k])}) ==")
    for item in results[k]:
        print("  ", item if isinstance(item,str) else f"{item[0]}  [{item[1]}]")
print(f"== CLEAN-MERGE ({len(results['CLEAN-MERGE'])}) ==")
for p,_ in results["CLEAN-MERGE"]:
    print("  ",p)

# save merged outputs + full result for apply step
with open(".aeon-update-tmp/merges.json","w") as f:
    json.dump({p:m for p,m in results["CLEAN-MERGE"]},f)
with open(".aeon-update-tmp/plan.json","w") as f:
    json.dump({
        "CLEAN-ADD":results["CLEAN-ADD"],
        "CLEAN-UPDATE":results["CLEAN-UPDATE"],
        "CLEAN-MERGE":[p for p,_ in results["CLEAN-MERGE"]],
        "SKIP":[list(x) if not isinstance(x,str) else x for x in results["SKIP"]],
        "CONFLICT":[list(x) if not isinstance(x,str) else x for x in results["CONFLICT"]],
    },f)
