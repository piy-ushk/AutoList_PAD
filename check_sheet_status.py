import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def main():
    client = GoogleSheetsClient()
    rows = client.get_all_rows()
    print(f"Total rows: {len(rows)}")
    for r in rows:
        if str(r.get("管理ID_SKU", "")).startswith("TEST-"):
            print(f"SKU: {r.get('管理ID_SKU')} | AI: {r.get('AI_Status')} | Val: {r.get('Validation_Status')} | List: {r.get('Listing_Status')} | VeRO: {r.get('VeRO_Flag')} | ChatGPT_Desc: {bool(r.get('ChatGPT_Description'))}")

if __name__ == "__main__":
    main()
