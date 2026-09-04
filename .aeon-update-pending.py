#!/usr/bin/env python3
import subprocess, hashlib, os
HEAD="bf33365164c5a8b50d49a0ed64a45521dbe96771"
BASE="3b4c5a3ff1d9846530e02ed5e6796a4a409d2674"
pending=["CHANGELOG.md",".github/workflows/aeon.yml",".github/workflows/ci-tests.yml",
 ".github/workflows/messages.yml","scripts/llm-gateway.sh","llms.txt",".github/README.md","docs/skill-packs.md"]
def blob(ref,path):
    r=subprocess.run(["git","show",f"{ref}:{path}"],capture_output=True)
    return r.stdout if r.returncode==0 else None
def sh(b): return hashlib.sha256(b).hexdigest() if b is not None else None
def local(p):
    if not os.path.exists(p): return None
    return open(p,"rb").read()
for p in pending:
    l=local(p); h=blob(HEAD,p); b=blob(BASE,p)
    still = sh(l)!=sh(h)
    hd_moved = sh(h)!=sh(b)
    print(f"{p}: local==HEAD? {sh(l)==sh(h)} | HEAD moved since baseline? {hd_moved} | still_divergent={still}")
