import json, sys

with open('xai-td-out.json') as f:
    data = json.load(f)

for item in data.get('output', []):
    itype = item.get('type')
    if itype == 'message':
        for c in item.get('content', []):
            if c.get('type') == 'output_text':
                print(c['text'])
    elif itype == 'tool_result':
        for c in item.get('content', []):
            if c.get('type') == 'text':
                print('[TOOL RESULT]:', c['text'][:2000])
