#!/usr/bin/env python3
import subprocess, json, os, sys
HEAD="bf33365164c5a8b50d49a0ed64a45521dbe96771"
plan=json.load(open(".aeon-update-tmp/plan.json"))
merges=json.load(open(".aeon-update-tmp/merges.json"))

def blob(ref,path):
    r=subprocess.run(["git","show",f"{ref}:{path}"],capture_output=True)
    if r.returncode!=0:
        raise SystemExit(f"FATAL: cannot read {ref}:{path}")
    return r.stdout

def write(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path,"wb") as f:
        f.write(data)

written=[]
for p in plan["CLEAN-ADD"]:
    write(p, blob(HEAD,p)); written.append(p)
for p in plan["CLEAN-UPDATE"]:
    write(p, blob(HEAD,p)); written.append(p)
for p, content in merges.items():
    write(p, content.encode("utf-8")); written.append(p)

print(f"wrote {len(written)} files")

# validate parse
errs=[]
for p in written:
    if p.endswith(".json"):
        try: json.load(open(p,encoding="utf-8"))
        except Exception as e: errs.append((p,f"JSON: {e}"))
    elif p.endswith((".yml",".yaml")):
        try:
            import yaml; yaml.safe_load(open(p,encoding="utf-8"))
        except ImportError:
            pass
        except Exception as e: errs.append((p,f"YAML: {e}"))
if errs:
    print("PARSE ERRORS:")
    for p,e in errs: print("  ",p,e)
    sys.exit(1)
print("all written files parse OK (json/yaml)")
