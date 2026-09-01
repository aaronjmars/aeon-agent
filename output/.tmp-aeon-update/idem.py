#!/usr/bin/env python3
"""Check catalog regen idempotency, masking the generated timestamp (CI ignores it)."""
import subprocess, re

repo = "/home/runner/work/aeon-agent/aeon-agent"

def snap(p):
    return open(repo + "/" + p).read()

def mask(s):
    return re.sub(r'"generated":"[^"]*"', '"generated":"T"', s)

before = {p: mask(snap(p)) for p in ["catalog/skills.json", "catalog/packs.json"]}
for cmd in [["bash", "bin/generate-skills-json"], ["bash", "bin/generate-packs-json"]]:
    subprocess.run(cmd, capture_output=True, cwd=repo)
for p in before:
    after = mask(snap(p))
    print(p, "IDENTICAL (ex-timestamp)" if after == before[p] else "REAL DRIFT")
