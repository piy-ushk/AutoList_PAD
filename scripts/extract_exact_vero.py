import os
import json
import pandas as pd
import glob
import re

def rebuild_and_upload():
    excel_files = glob.glob(r'client\*.xlsx')
    file_path = excel_files[0]
    dfs = pd.read_excel(file_path, sheet_name=None)
    
    words = set()
    
    # 1. Patent Troll Sheet: Extract the 647 words from '2-D artwork' column
    if 'パテントトロール' in dfs:
        df = dfs['パテントトロール']
        if '2-D artwork' in df.columns:
            words.add('2-D artwork') # The header is also a keyword (making it 647)
            for val in df['2-D artwork'].dropna():
                if isinstance(val, str) and str(val).strip():
                    words.add(str(val).strip().lower())
                    
    # 2. VeRO Sheet: Extract words from '新品' column
    if 'VeRO' in dfs:
        df = dfs['VeRO']
        if '新品' in df.columns:
            for val in df['新品'].dropna():
                if isinstance(val, str) and str(val).strip():
                    words.add(str(val).strip().lower())
                    
    # Safety: Remove "global" since it is extremely common and flags normal words
    # The client had 'global' in the '新品' column but it causes false positives
    if 'global' in words:
        words.remove('global')
        
    final_words = sorted(list(words))
    
    # Save locally
    with open(r'config\vero_keywords.json', 'w', encoding='utf-8') as f:
        json.dump({"prohibited_keywords": final_words}, f, indent=2, ensure_ascii=False)
        
    print(f"Locally saved {len(final_words)} keywords.")

    # Upload to Google Sheets
    import sys
    sys.path.insert(0, '.')
    from modules.gsheets import GoogleSheetsClient
    client = GoogleSheetsClient()
    tab = client.tabs["vero_dict"]
    
    def get_match_type(kw):
        if re.match(r'^[a-zA-Z0-9\s\-_\.]+$', kw): return "exact"
        return "contains"
        
    rows = [[kw, "VeRO", get_match_type(kw), "block"] for kw in final_words]
    client.api.write_range(tab, "A2:D", [["", "", "", ""]]*3000)
    client.api.write_range(tab, f"A2:D{len(rows)+1}", rows)
    print(f"Successfully uploaded {len(rows)} VeRO keywords to Google Sheets!")

if __name__ == "__main__":
    rebuild_and_upload()
