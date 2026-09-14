import json
raw=open('eyebrowlock.json').read()
obj=json.loads(raw)
for ea in (True,):
    d=json.dumps(obj,indent=2,ensure_ascii=ea)+'\n'
    print('ensure_ascii',ea,'match=', d==raw, 'lens',len(d),len(raw))
    if d!=raw:
        n=min(len(d),len(raw))
        for i in range(n):
            if d[i]!=raw[i]:
                print(' diff@',i, repr(raw[i-30:i+20]),'|',repr(d[i-30:i+20])); break
