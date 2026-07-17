import json
with open('xai-td-out.json') as f:
    data = json.load(f)
print('Keys:', list(data.keys()))
output = data.get('output', [])
print('Output items:', len(output))
for i, item in enumerate(output):
    itype = item.get('type')
    irole = item.get('role', '')
    print(f'  Item {i}: type={itype} role={irole}')
    if itype == 'message':
        for c in item.get('content', []):
            ctype = c.get('type')
            print(f'    content type: {ctype}')
            if ctype == 'text':
                print(c['text'][:3000])
    elif itype == 'tool_use':
        print(f'    tool: {item.get("name")}')
        inp = item.get('input', {})
        print(f'    input keys: {list(inp.keys())}')
    elif itype == 'tool_result':
        content = item.get('content', '')
        if isinstance(content, str):
            print(content[:3000])
        elif isinstance(content, list):
            for c in content:
                if c.get('type') == 'text':
                    print(c['text'][:3000])
