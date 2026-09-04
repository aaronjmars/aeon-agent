#!/usr/bin/env python3
import subprocess, json, hashlib
BASE="3b4c5a3ff1d9846530e02ed5e6796a4a409d2674"
HEAD="bf33365164c5a8b50d49a0ed64a45521dbe96771"
def lock(ref):
    return json.loads(subprocess.run(["git","show",f"{ref}:eyebrowlock.json"],capture_output=True).stdout)
def bymap(d):
    return {a.get("discoveredFrom"):a for a in d["artifacts"] if a.get("discoveredFrom")}
loc=json.load(open("eyebrowlock.json"))
base=lock(BASE); head=lock(HEAD)
lm=bymap(loc); bm=bymap(base); hm=bymap(head)

def sig(a):
    return (json.dumps(a.get("files"),sort_keys=True), a.get("contentHash"))

print("=== drifted upstream (base->head) ===")
drift=[]
for k,h in hm.items():
    b=bm.get(k)
    if b is None:
        print("  NEW-upstream-artifact",k); continue
    if sig(h)!=sig(b):
        drift.append(k); print("  DRIFT",k)

print("\n=== for each drifted: does operator local == upstream base? (safe to swap) ===")
for k in drift:
    l=lm.get(k); b=bm.get(k)
    if l is None:
        print("  MISSING-in-local",k)
    elif sig(l)==sig(b):
        print("  OK-local-eq-base (safe swap)",k)
    else:
        print("  LOCAL-DIVERGED-from-base",k)

# Also: does the SKILL.md content I wrote match HEAD's recorded hash?
print("\n=== verify written SKILL.md matches HEAD lock hash ===")
for k in drift:
    if not k.startswith("skills/"): continue
    try:
        data=open(k,"rb").read()
        hh=hashlib.sha256(data).hexdigest()
    except FileNotFoundError:
        print("  file-missing",k); continue
    rec=hm[k]["files"][0]["hash"] if hm[k].get("files") else None
    print("  ", "MATCH" if hh==rec else "MISMATCH", k)
