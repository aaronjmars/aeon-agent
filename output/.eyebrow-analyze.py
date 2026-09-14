import json
loc=json.load(open('eyebrowlock.json'))['artifacts']
up=json.load(open('output/.up-eyebrowlock.json'))['artifacts']
def by(a): return {x['discoveredFrom']:x for x in a}
L=by(loc); U=by(up)
changed_add=['skills/compute-resell/SKILL.md','skills/miroshark-matchday/SKILL.md','skills/submit-hook/SKILL.md']
changed_upd=['skills/aeon-update/SKILL.md','skills/changelog/SKILL.md','skills/competitor-monitor/SKILL.md','skills/deploy-uni-hook/SKILL.md','skills/github-trending/SKILL.md','skills/vuln-scanner/SKILL.md']
print('local-only (fork-only):', sorted(set(L)-set(U)))
print('upstream-only (to add):', sorted(set(U)-set(L)))
mism=[]
for k in set(L)&set(U):
    if k in changed_upd: continue
    if L[k]['files']!=U[k]['files'] or L[k]['contentHash']!=U[k]['contentHash']:
        mism.append(k)
print('shared unchanged with hash MISMATCH:', mism)
print('count shared-unchanged checked:', len(set(L)&set(U))-len(changed_upd))
for k in changed_upd:
    print('UPD present L/U:',k, k in L, k in U)
for k in changed_add:
    print('ADD present U/L:',k, k in U, k in L)
