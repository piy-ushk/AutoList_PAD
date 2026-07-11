import json
with open('config/genre_templates.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
for k, v in config['genres'].items():
    if 'camera' in k.lower():
        print(f"{k}: keywords={v.get('keywords', [])}, match_keywords={v.get('match_keywords', [])}")
