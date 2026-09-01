#!/usr/bin/env python3
"""aeon-update S7: apply CLEAN-ADD / CLEAN-UPDATE / CLEAN-MERGE files."""
import subprocess, json, os, stat, sys

REPO = "/home/runner/work/aeon-agent/aeon-agent"
HEAD = "3b4c5a3ff1d9846530e02ed5e6796a4a409d2674"
OUT = os.path.join(REPO, "output/.tmp-aeon-update")
EXTRA = sys.argv[1:]  # optional extra paths to CLEAN-ADD from upstream HEAD (prior held-back skills)

def git(*args):
    r = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (args[:3], r.stderr.decode()[:300]))
    return r.stdout

def blob(rev, path):
    return git("cat-file", "blob", rev + ":" + path)

def mode(rev, path):
    out = git("ls-tree", rev, "--", path).decode().split()
    return out[0] if out else "100644"

rs = json.load(open(OUT + "/classification.json"))
applied = {"added": 0, "updated": 0, "merged": 0, "deleted": 0}
paths_touched = []

def write_blob(path, content, executable):
    fp = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "wb").write(content)
    m = os.stat(fp).st_mode
    want = 0o755 if executable else 0o644
    os.chmod(fp, want)
    return want != m

for r in rs:
    d = r["disposition"]
    p = r["path"]
    if d in ("CLEAN-ADD", "CLEAN-UPDATE"):
        content = blob(HEAD, p)
        write_blob(p, content, mode(HEAD, p) == "100755")
        applied["added" if d == "CLEAN-ADD" else "updated"] += 1
        paths_touched.append(p)
    elif d == "CLEAN-MERGE":
        merged = open(r["merged_file"], "rb").read()
        write_blob(p, merged, mode(HEAD, p) == "100755")
        applied["merged"] += 1
        paths_touched.append(p)
    elif d == "CLEAN-DELETE":
        git("rm", "-r", "--", p)
        applied["deleted"] += 1
        paths_touched.append(p)

# extra held-back skills from prior windows (explicit opt-in args)
for p in EXTRA:
    content = blob(HEAD, p)
    write_blob(p, content, mode(HEAD, p) == "100755")
    applied["added"] += 1
    paths_touched.append(p)

open(OUT + "/applied.json", "w").write(json.dumps(
    {"applied": applied, "paths": paths_touched}, indent=1))
print("APPLIED:", applied, "total files:", len(paths_touched))
if EXTRA:
    print("EXTRA adds:", EXTRA)
