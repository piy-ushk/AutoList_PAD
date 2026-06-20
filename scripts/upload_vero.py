import json, os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.gsheets import GoogleSheetsClient

def upload_vero_keywords():
    client = GoogleSheetsClient()
    tab = client.tabs["vero_dict"]
    
    with open(r"config\vero_keywords.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    keywords = data.get("prohibited_keywords", [])
    
    import re
    def get_match_type(kw):
        # If the keyword is purely English/Ascii, use exact match to avoid substring matches like "ck" in "background"
        if re.match(r'^[a-zA-Z0-9\s\-_\.]+$', kw):
            return "exact"
        # For Japanese, word boundaries (\b) fail because there are no spaces, so use contains
        return "contains"
        
    # Format for sheets (4 columns so len(row) >= 4)
    rows = [[kw, "VeRO", get_match_type(kw), "block"] for kw in keywords]
    
    # Clear existing and write
    client.api.write_range(tab, "A2:D", [["", "", "", ""]]*3000) # Clear up to 3000 rows
    client.api.write_range(tab, f"A2:D{len(rows)+1}", rows)
    print(f"Successfully uploaded {len(rows)} VeRO keywords to Google Sheets!")

if __name__ == "__main__":
    upload_vero_keywords()
