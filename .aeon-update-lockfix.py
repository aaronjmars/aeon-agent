#!/usr/bin/env python3
import subprocess, hashlib, json, os
HEAD='bf33365164c5a8b50d49a0ed64a45521dbe96771'
def blob(ref,p):
    r=subprocess.run(['git','show',f'{ref}:{p}'],capture_output=True)
    return r.stdout if r.returncode==0 else None
def lock(ref): return json.loads(subprocess.run(['git','show',f'{ref}:eyebrowlock.json'],capture_output=True).stdout)
def sha(b): return hashlib.sha256(b).hexdigest() if b is not None else None

loc=json.load(open('eyebrowlock.json'))
hm={a.get('discoveredFrom'):a for a in lock(HEAD)['artifacts'] if a.get('discoveredFrom')}

def local_files_hashes(art):
    # eyebrow files[].path are relative to the skill dir (source.ref)
    ref=art.get('source',{}).get('ref') or os.path.dirname(art['discoveredFrom'])
    out={}
    for f in art.get('files',[]):
        fp=os.path.join(ref,f['path'])
        out[f['path']]=(f['hash'], sha(open(fp,'rb').read()) if os.path.exists(fp) else None)
    return out

drift=[]
for art in loc['artifacts']:
    df=art.get('discoveredFrom')
    if not df: continue
    fh=local_files_hashes(art)
    mism=[p for p,(rec,cur) in fh.items() if rec!=cur]
    if mism:
        drift.append((df,mism))

print('=== drifted artifacts on branch (lock hash != current file) ===')
for df,m in drift:
    # can we swap from HEAD?
    h=hm.get(df)
    swap='NO-HEAD-ENTRY'
    if h:
        # does current branch file match HEAD lock's recorded hash for each file?
        ref=h.get('source',{}).get('ref') or os.path.dirname(df)
        ok=all(os.path.exists(os.path.join(ref,f['path'])) and sha(open(os.path.join(ref,f['path']),'rb').read())==f['hash'] for f in h.get('files',[]))
        swap='SWAP-OK(content==HEAD)' if ok else 'HEAD-ENTRY-DIFFERS'
    print(f'  {df}  files={m}  -> {swap}')
