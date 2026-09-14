import json
raw=open('eyebrowlock.json').read()
obj=json.loads(raw)
d=json.dumps(obj,indent=2,ensure_ascii=False)+'\n'
# find first diff
n=min(len(d),len(raw))
for i in range(n):
    if d[i]!=raw[i]:
        print('first diff at',i)
        print('RAW:',repr(raw[i-40:i+40]))
        print('DMP:',repr(d[i-40:i+40]))
        break
else:
    print('match up to',n,'lens',len(d),len(raw))
