import json
usk={s['slug']:s for s in json.load(open('output/.up-skills.json'))['skills']}
new=usk['deploy-uni-hook']['description']
p=json.loads(open('catalog/packs.json').read())
old=None
for pack in p['packs']:
    for s in pack.get('skills',[]):
        if isinstance(s,dict) and s.get('slug')=='deploy-uni-hook':
            old=s['description']
old_j=json.dumps(old, ensure_ascii=False)   # escaped JSON string incl outer quotes
new_j=json.dumps(new, ensure_ascii=False)
praw=open('catalog/packs.json').read()
cnt=praw.count(old_j)
assert cnt>=1 and old!=new, (cnt, old==new)
open('catalog/packs.json','w').write(praw.replace(old_j,new_j))
print('packs.json: replaced', cnt, 'occurrence(s); OK')
