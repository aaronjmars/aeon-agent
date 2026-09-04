#!/usr/bin/env python3
import subprocess, json, os, hashlib
HEAD='bf33365164c5a8b50d49a0ed64a45521dbe96771'
def blob(ref,p):
    r=subprocess.run(['git','show',f'{ref}:{p}'],capture_output=True)
    return r.stdout if r.returncode==0 else None
def lockof(ref): return json.loads(subprocess.run(['git','show',f'{ref}:eyebrowlock.json'],capture_output=True).stdout)

loc=json.load(open('eyebrowlock.json'))
head=lockof(HEAD)
hm={a.get('discoveredFrom'):a for a in head['artifacts'] if a.get('discoveredFrom')}

# artifacts whose underlying files I changed to HEAD content this sync
candidates=[
 'skills/vuln-scanner/SKILL.md',
 'skills/pr-review/SKILL.md',
 'skills/feature/SKILL.md',
 'skills/deploy-uni-hook/SKILL.md',
 '.claude/skills/aeon/SKILL.md',
 'plugin/skills/aeon/SKILL.md',
]

def artifact_byte_identical_to_head(art):
    """True iff every file in HEAD's artifact is byte-identical on the branch."""
    h=hm.get(art)
    if not h: return False,'no-head-entry'
    ref=h.get('source',{}).get('ref') or os.path.dirname(art)
    for f in h.get('files',[]):
        fp=os.path.join(ref,f['path'])
        if not os.path.exists(fp): return False,f'missing:{fp}'
        if open(fp,'rb').read()!=blob(HEAD,fp): return False,f'differs:{fp}'
    return True,'ok'

swaps={}
for c in candidates:
    if c not in hm:
        print('SKIP (no head artifact):',c); continue
    ok,why=artifact_byte_identical_to_head(c)
    print(('SWAP ' if ok else 'NO-SWAP '),c,why)
    if ok: swaps[c]=hm[c]

# apply swaps into loc
by_df={id(a):a for a in loc['artifacts']}
new_arts=[]
swapped=0
for a in loc['artifacts']:
    df=a.get('discoveredFrom')
    if df in swaps:
        new_arts.append(swaps[df]); swapped+=1
    else:
        new_arts.append(a)
loc['artifacts']=new_arts
with open('eyebrowlock.json','w') as f:
    json.dump(loc, f, indent=2, ensure_ascii=False)
    f.write('\n')
print(f'swapped {swapped} artifact entries; wrote eyebrowlock.json')
