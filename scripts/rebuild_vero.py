import os
import json
import pandas as pd
import re

def rebuild_and_upload():
    import glob
    excel_files = glob.glob(r"client\*.xlsx")
    file_path = excel_files[0]
    dfs = pd.read_excel(file_path, sheet_name=None)
    
    words = set(['replica', 'fake', 'counterfeit', 'unauthorized', 'bootleg'])
    
    # Process Patent Troll (all columns)
    if 'パテントトロール' in dfs:
        df = dfs['パテントトロール']
        for col in df.columns:
            for val in df[col].dropna():
                if isinstance(val, str):
                    val = val.strip()
                    if len(val) > 1 and not val.startswith('http') and not val.startswith('www'):
                        words.add(val.lower())
                        
    # Process VeRO (only first column)
    if 'VeRO' in dfs:
        df = dfs['VeRO']
        first_col = df.columns[0]
        for val in df[first_col].dropna():
            if isinstance(val, str):
                val = val.strip()
                if len(val) > 1:
                    words.add(val.lower())
                    
    # Remove problematic common words that might have been picked up
    bad_words = {"アイテム", "global", "ck", "alo", "nan", "vero", "block", "contains", "exact"}
    final_words = [w for w in words if w not in bad_words]
    
    # Save locally
    with open(r'config\vero_keywords.json', 'w', encoding='utf-8') as f:
        json.dump({"prohibited_keywords": sorted(final_words)}, f, indent=2, ensure_ascii=False)
        
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
