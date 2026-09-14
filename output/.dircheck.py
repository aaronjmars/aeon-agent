import subprocess, json, os
def up_tree(path):
    r=subprocess.run(['gh','api',f'repos/aeonfun/aeon/contents/{path}?ref=95142d19705ca379815e7fc9493a497ee0504e8d',
                      '--jq','.[].name'],capture_output=True,text=True)
    return sorted(r.stdout.split())
def up_tree_rec(path):
    out=[]
    r=subprocess.run(['gh','api',f'repos/aeonfun/aeon/contents/{path}?ref=95142d19705ca379815e7fc9493a497ee0504e8d',
                      '--jq','.[] | .type+" "+.name'],capture_output=True,text=True)
    for line in r.stdout.strip().splitlines():
        t,n=line.split(' ',1)
        if t=='dir': out+= [n+'/'+x for x in up_tree_rec(path+'/'+n)]
        else: out.append(n)
    return sorted(out)
def loc_tree(path):
    out=[]
    for root,ds,fs in os.walk(path):
        for f in fs:
            out.append(os.path.relpath(os.path.join(root,f),path))
    return sorted(out)
for d in ['skills/deploy-uni-hook','skills/vuln-scanner']:
    u=up_tree_rec(d); l=loc_tree(d)
    print(d,'match=',u==l)
    if u!=l:
        print('  only upstream:', [x for x in u if x not in l])
        print('  only local   :', [x for x in l if x not in u])
