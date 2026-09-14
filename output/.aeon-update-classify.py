#!/usr/bin/env python3
import subprocess, json, hashlib, os, base64, tempfile, sys

UPSTREAM = "aeonfun/aeon"
BASELINE = "21b82dbb7d4927515ec0ad6cbf36f7daac6cc225"
HEAD = "95142d19705ca379815e7fc9493a497ee0504e8d"
APPLY = "--apply" in sys.argv

def gh(args):
    return subprocess.run(["gh"]+args, capture_output=True, text=True)

def fetch(path, ref):
    # returns bytes or None
    r = subprocess.run(["gh","api",f"repos/{UPSTREAM}/contents/{path}?ref={ref}","--jq",".content"],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return base64.b64decode(r.stdout.strip())
    except Exception:
        return None

def sha(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None

def local_bytes(path):
    if os.path.exists(path):
        with open(path,"rb") as f:
            return f.read()
    return None

# operator-owned matcher
def is_operator(p):
    if p == "aeon.yml": return True
    if p == "STRATEGY.md": return True
    if p.startswith("soul/"): return True
    if p.startswith("memory/"): return True
    if p.startswith("output/"): return True
    if p == ".mcp.json": return True
    if p.startswith(".env"): return True
    if p == "aeon.db": return True
    if p == "skills.lock": return True
    if p == "eyebrowlock.json": return True
    if p.startswith("catalog/") and p.endswith(".json"): return True
    if p.startswith("apps/dashboard/outputs/"): return True
    if p.startswith(".claude/"):
        if p.startswith(".claude/skills/aeon/"): return False  # OWNED exception
        return True
    return False

# get compare files
r = gh(["api",f"repos/{UPSTREAM}/compare/{BASELINE}...{HEAD}",
        "--jq",".files[] | {filename, status, previous_filename}"])
files = [json.loads(l) for l in r.stdout.strip().splitlines()]

plan = {"CLEAN-ADD":[], "CLEAN-UPDATE":[], "CLEAN-MERGE":[], "CLEAN-DELETE":[],
        "SKIP":[], "CONFLICT":[], "OPERATOR":[], "UNREADABLE":[]}
merged_content = {}  # path -> bytes for CLEAN-MERGE / CLEAN-ADD / CLEAN-UPDATE

def handle_added(path, entry):
    lb = local_bytes(path)
    head = fetch(path, HEAD)
    if head is None:
        plan["UNREADABLE"].append({"path":path,"reason":"head-fetch-failed"}); return
    if lb is None:
        plan["CLEAN-ADD"].append(path); merged_content[path]=head
    else:
        if sha(lb)==sha(head):
            plan["SKIP"].append({"path":path,"reason":"already-present-identical"})
        else:
            plan["CONFLICT"].append({"path":path,"reason":"added-upstream-but-present-locally-diverged"})

def handle_modified(path, entry):
    lb = local_bytes(path)
    head = fetch(path, HEAD)
    base = fetch(path, BASELINE)
    if head is None:
        plan["UNREADABLE"].append({"path":path,"reason":"head-fetch-failed"}); return
    if lb is None:
        # local missing but upstream modified -> treat like add
        plan["CLEAN-ADD"].append(path); merged_content[path]=head; return
    if sha(lb)==sha(head):
        plan["SKIP"].append({"path":path,"reason":"already-synced"}); return
    if base is not None and sha(lb)==sha(base):
        plan["CLEAN-UPDATE"].append(path); merged_content[path]=head; return
    # 3-way
    if base is None:
        plan["CONFLICT"].append({"path":path,"reason":"no-base-blob-cannot-3way"}); return
    with tempfile.TemporaryDirectory() as wd:
        lp=os.path.join(wd,"local"); bp=os.path.join(wd,"base"); hp=os.path.join(wd,"head")
        with open(lp,"wb") as f: f.write(lb)
        with open(bp,"wb") as f: f.write(base)
        with open(hp,"wb") as f: f.write(head)
        mr = subprocess.run(["git","merge-file","-p","--diff3",lp,bp,hp],
                            capture_output=True)
        if mr.returncode==0:
            plan["CLEAN-MERGE"].append(path); merged_content[path]=mr.stdout
        else:
            plan["CONFLICT"].append({"path":path,"reason":"operator-customized-overlap"})

def handle_removed(path, entry):
    lb = local_bytes(path)
    base = fetch(path, BASELINE)
    if lb is None:
        plan["SKIP"].append({"path":path,"reason":"already-absent"}); return
    if base is not None and sha(lb)==sha(base):
        plan["CLEAN-DELETE"].append(path)
    else:
        plan["CONFLICT"].append({"path":path,"reason":"removed-upstream-local-diverged"})

for e in files:
    p = e["filename"]; st=e["status"]
    if is_operator(p):
        plan["OPERATOR"].append({"path":p,"status":st}); continue
    if st=="added":
        handle_added(p,e)
    elif st=="modified" or st=="changed":
        handle_modified(p,e)
    elif st=="removed":
        handle_removed(p,e)
    elif st=="renamed":
        # removed previous + added new
        prev=e.get("previous_filename")
        if prev and not is_operator(prev):
            handle_removed(prev,{})
        handle_added(p,e)
    else:
        plan["CONFLICT"].append({"path":p,"reason":f"unknown-status-{st}"})

# summary
summary={k:len(v) for k,v in plan.items()}
print("SUMMARY:", json.dumps(summary))
for k in plan:
    if plan[k]:
        print(f"\n== {k} ==")
        for item in plan[k]:
            print("  ", item if isinstance(item,str) else json.dumps(item))

if APPLY:
    applied={"added":0,"updated":0,"merged":0,"deleted":0}
    for p in plan["CLEAN-ADD"]:
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        with open(p,"wb") as f: f.write(merged_content[p]); applied["added"]+=1
    for p in plan["CLEAN-UPDATE"]:
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        with open(p,"wb") as f: f.write(merged_content[p]); applied["updated"]+=1
    for p in plan["CLEAN-MERGE"]:
        with open(p,"wb") as f: f.write(merged_content[p]); applied["merged"]+=1
    for p in plan["CLEAN-DELETE"]:
        subprocess.run(["git","rm","-q",p])
        applied["deleted"]+=1
    print("\nAPPLIED:", json.dumps(applied))
    with open("output/.aeon-update-plan.json","w") as f:
        json.dump({"plan":plan,"applied":applied},f,indent=2)
    print("wrote output/.aeon-update-plan.json")
