#!/usr/bin/env python3
import subprocess, difflib, sys
HEAD="bf33365164c5a8b50d49a0ed64a45521dbe96771"
BASE="3b4c5a3ff1d9846530e02ed5e6796a4a409d2674"
def blob(ref,path):
    r=subprocess.run(["git","show",f"{ref}:{path}"],capture_output=True)
    return r.stdout.decode("utf-8","replace").splitlines(keepends=True) if r.returncode==0 else []
def local(p):
    try: return open(p,encoding="utf-8",errors="replace").read().splitlines(keepends=True)
    except: return []
for p in sys.argv[1:]:
    print(f"##### {p} : LOCAL vs upstream HEAD #####")
    d=difflib.unified_diff(blob(HEAD,p),local(p),fromfile="upstream-HEAD",tofile="local",n=2)
    out="".join(d)
    print(out if out else "(identical)")
    print()
