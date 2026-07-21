import json, sys

with open('/home/runner/work/aeon-agent/aeon-agent/xai-td-out.json') as f:
    data = json.load(f)

for item in data.get('output', []):
    t = item.get('type')
    print(f"=== ITEM TYPE: {t}")
    if t == 'message':
        for c in item.get('content', []):
            ct = c.get('type')
            print(f"CONTENT TYPE: {ct}")
            if ct in ('text', 'output_text'):
                print(c.get('text', ''))
    elif t == 'tool_use':
        print(f"TOOL: {item.get('name')}")
        inp = item.get('input', {})
        print(f"INPUT: {json.dumps(inp)[:500]}")
    elif t == 'tool_result':
        content = item.get('content', '')
        print(str(content)[:3000])
    elif t == 'custom_tool_call':
        print(f"TOOL: {item.get('name')}")
        print(f"INPUT: {item.get('input', '')[:500]}")
    else:
        print(json.dumps(item)[:2000])
