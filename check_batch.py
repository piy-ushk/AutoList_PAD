import json
data = json.load(open('logs/monodas_task_batch.json', encoding='utf-8'))
for t in data:
    specs = t.get('item_specifics', '').split(' | ')
    print(f"{t.get('sku')} | Fields Extracted: {len(specs)}")
    for s in specs:
        print(f"  - {s}")
