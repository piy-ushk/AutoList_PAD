import json
import re
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

with open(r'config\vero_keywords.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keywords = data.get("prohibited_keywords", [])

bad_words = {'アイテム', 'global', 'vero', 'block', 'contains', 'exact', 'nan', 'true', 'false', 'category', 'keyword', 'action', 'match'}

filtered = []
for kw in keywords:
    kw_clean = kw.strip().lower()
    
    # Exclude explicitly bad words
    if kw_clean in bad_words:
        continue
        
    # Exclude purely English words that are < 4 chars (e.g. "ck", "alo")
    if re.match(r'^[a-zA-Z0-9\s\-_]+$', kw_clean) and len(kw_clean) < 4:
        continue
        
    filtered.append(kw_clean)

# Deduplicate
filtered = sorted(list(set(filtered)))

# Save
with open(r'config\vero_keywords.json', 'w', encoding='utf-8') as f:
    json.dump({"prohibited_keywords": filtered}, f, indent=2, ensure_ascii=False)

print(f"Filtered down to {len(filtered)} keywords.")

# Now upload to Google Sheets!
sys.path.insert(0, '.')
from modules.gsheets import GoogleSheetsClient
client = GoogleSheetsClient()
tab = client.tabs["vero_dict"]

def get_match_type(kw):
    if re.match(r'^[a-zA-Z0-9\s\-_\.]+$', kw):
        return "exact"
    return "contains"

rows = [[kw, "VeRO", get_match_type(kw), "block"] for kw in filtered]
client.api.write_range(tab, "A2:D", [["", "", "", ""]]*3000)
client.api.write_range(tab, f"A2:D{len(rows)+1}", rows)
print(f"Uploaded {len(rows)} to Google Sheets!")
