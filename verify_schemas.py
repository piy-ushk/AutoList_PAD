import os, sys, json, ast
sys.path.insert(0, os.path.dirname(os.path.abspath('main.py')))
from modules.chatgpt import ChatGPTCaller

with open('insert_final_demo.py', 'r', encoding='utf-8') as f:
    source = f.read()

import re
match = re.search(r'demo_items\s*=\s*(\[\s*\{.*?\}\s*\])', source, re.DOTALL)
if not match:
    print('Failed to find demo_items')
    sys.exit(1)
    
demo_items = ast.literal_eval(match.group(1))

caller = ChatGPTCaller()
for i, item in enumerate(demo_items):
    sys_p, _ = caller.build_prompts(item)
    start_str = '  "itemSpecifics": '
    end_str = ',\n  "nested_sections":'
    start_idx = sys_p.find(start_str)
    end_idx = sys_p.find(end_str)
    
    if start_idx != -1 and end_idx != -1:
        schema_json_str = sys_p[start_idx + len(start_str):end_idx]
        try:
            schema = json.loads(schema_json_str)
            props = len(schema) if isinstance(schema, dict) and 'properties' not in schema else len(schema.get('properties', {}))
            print(f'Item {i+1} ({item["Category"]}) Schema Valid! Fields: {props}')
        except Exception as e:
            print(f'Item {i+1} ({item["Category"]}) Schema INVALID: {e}')
