import subprocess, json, os
HEAD='bf33365164c5a8b50d49a0ed64a45521dbe96771'
def blob(ref,p):
    r=subprocess.run(['git','show',f'{ref}:{p}'],capture_output=True)
    return r.stdout if r.returncode==0 else None
def lockof(ref): return json.loads(subprocess.run(['git','show',f'{ref}:eyebrowlock.json'],capture_output=True).stdout)
loc=json.load(open('eyebrowlock.json'))
hm={a.get('discoveredFrom'):a for a in lockof(HEAD)['artifacts'] if a.get('discoveredFrom')}
lm={a.get('discoveredFrom'):a for a in loc['artifacts'] if a.get('discoveredFrom')}
swapped={'skills/vuln-scanner/SKILL.md','skills/pr-review/SKILL.md','skills/feature/SKILL.md','skills/deploy-uni-hook/SKILL.md','.claude/skills/aeon/SKILL.md'}
checked=0; compat=0; differ=0
for df,h in hm.items():
    if df in swapped or df not in lm: continue
    ref=h.get('source',{}).get('ref') or os.path.dirname(df)
    same=all(os.path.exists(os.path.join(ref,f['path'])) and open(os.path.join(ref,f['path']),'rb').read()==blob(HEAD,os.path.join(ref,f['path'])) for f in h.get('files',[]))
    if not same: continue
    l=lm[df]
    match = (l.get('contentHash')==h.get('contentHash')) and (l.get('files')==h.get('files'))
    if match: compat+=1
    else:
        differ+=1
        if differ<=6: print('DIFFER', df, '| op:',l.get('contentHash'),'| head:',h.get('contentHash'))
    checked+=1
print('checked',checked,'compat',compat,'differ',differ)
