import json
with open('xai-td-out.json') as f:
    data = json.load(f)
output = data.get('output', [])
for i, item in enumerate(output):
    itype = item.get('type')
    if itype == 'message':
        for c in item.get('content', []):
            if c.get('type') == 'output_text':
                print(c['text'])
    elif itype == 'custom_tool_call':
        print(f'TOOL CALL: {item.get("name")}')
        inp = item.get('input', '')
        if isinstance(inp, str):
            print(inp[:500])
        else:
            print(json.dumps(inp)[:500])
