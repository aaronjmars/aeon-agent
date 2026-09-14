import json
# eyebrowlock round-trip: 2-space indent
raw=open('eyebrowlock.json').read()
obj=json.loads(raw)
for sep in [None]:
    d=json.dumps(obj,indent=2,ensure_ascii=False)
    print('eyebrowlock indent2 match=', d==raw, 'nl?', d+'\n'==raw, 'end=',repr(raw[-2:]))
# packs.json: check description present
packs=open('catalog/packs.json').read()
import json as j
loc=j.loads(open('catalog/skills.json'))
