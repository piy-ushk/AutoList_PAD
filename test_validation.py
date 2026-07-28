import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def main():
    client = GoogleSheetsClient()
    rows = client.get_all_rows()
    print(f"Total rows: {len(rows)}")
    val_rows = client.get_validated_rows()
    print(f"Validated rows: {len(val_rows)}")
    for r in rows:
        sku = str(r.get("管理ID_SKU", ""))
        if sku.startswith("TEST-"):
            # Also test the logic in get_validated_rows
            val_stat = str(r.get("Validation_Status", "")).strip()
            list_stat = str(r.get("Listing_Status", "")).strip()
            included = (val_stat == "validated") and (list_stat not in ["draft_saved", "listed", "active", "error"])
            print(f"SKU: {sku} | Validated? {included} (val: {val_stat}, list: {list_stat})")

if __name__ == "__main__":
    main()
