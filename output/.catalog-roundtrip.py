import json
for fn in ['catalog/skills.json','catalog/packs.json','catalog/skill-icons.json']:
    raw=open(fn).read()
    obj=json.loads(raw)
    dumped=json.dumps(obj,separators=(',',':'),ensure_ascii=False)
    # try with trailing newline variants
    match = dumped==raw or dumped+'\n'==raw or dumped==raw.rstrip('\n')
    print(fn, 'roundtrip-match=', match, 'raw_end=', repr(raw[-3:]), 'lendiff=', len(raw)-len(dumped))
