import json
usk={s['slug']:s for s in json.load(open('output/.up-skills.json'))['skills']}
new=usk['deploy-uni-hook']['description']
p=json.loads(open('catalog/packs.json').read())
old=None
for pack in p['packs']:
    for s in pack.get('skills',[]):
        if isinstance(s,dict) and s.get('slug')=='deploy-uni-hook':
            old=s['description']
praw=open('catalog/packs.json').read()
assert old in praw and old!=new, (old==new, old in praw)
open('catalog/packs.json','w').write(praw.replace(old,new))
print('packs.json updated; new desc ends:',new[-60:])
