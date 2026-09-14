import json
loc=json.load(open('catalog/skills.json'))
up=json.load(open('output/.up-skills.json'))
L={s['slug']:s for s in loc['skills']}
U={s['slug']:s for s in up['skills']}
updated=['aeon-update','changelog','competitor-monitor','deploy-uni-hook','github-trending','vuln-scanner']
new=['compute-resell','miroshark-matchday','submit-hook']
NORM=lambda d:{k:v for k,v in d.items() if k not in ('sha','updated')}
print('=== UPDATED skills: local-vs-upstream semantic diff (ignoring sha/updated) ===')
for s in updated:
    l=NORM(L.get(s,{})); u=NORM(U.get(s,{}))
    if l!=u:
        diffk=[k for k in set(l)|set(u) if l.get(k)!=u.get(k)]
        print(f'{s}: DIFFERS in {diffk}')
        for k in diffk:
            print(f'   local[{k}]={l.get(k)!r}'.replace('!r',''))
            print(f'   up   [{k}]={u.get(k)!r}'.replace('!r',''))
    else:
        print(f'{s}: identical (no catalog change)')
print('=== NEW skills present in upstream catalog? ===')
for s in new:
    print(s, 'in upstream:', s in U, 'in local:', s in L)
print('local total field:', loc.get('total'), 'upstream total:', up.get('total'))
