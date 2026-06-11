import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def sync_results():
    print("Starting sync process...")
    path = os.path.join(os.path.dirname(__file__), "logs", "monodas_results.json")
    
    if not os.path.exists(path):
        print(f"Error: Could not find file at {path}")
        print("Please make sure Power Automate Desktop has finished running and created the file.")
        return

    try:
        try:
            with open(path, "r", encoding="utf-16") as f:
                results = json.load(f)
        except UnicodeError:
            with open(path, "r", encoding="utf-8") as f:
                results = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    if not isinstance(results, list):
        results = [results]

    print(f"\nFound {len(results)} items in the results file. Here is exactly what PAD saved:")
    for res in results:
        print(f" -> {res}")

    print("\nConnecting to Google Sheets...")
    sheet_client = GoogleSheetsClient()
    success_count = 0

    for res in results:
        sheet_row = res.get("sheet_row")
        item_id = res.get("ebay_item_id")
        
        if not sheet_row:
            print(f"Skipping: Missing sheet_row in {res}")
            continue
            
        if not item_id:
            print(f"Skipping row {sheet_row}: eBay Item ID is empty! This means PAD could not find the ID on the webpage.")
            continue

        listing_url = f"https://www.ebay.com/itm/{item_id}"
        
        try:
            sheet_client.mark_draft_saved(sheet_row, item_id, listing_url)
            success_count += 1
            print(f"Success: Row {sheet_row} updated with eBay ID {item_id}")
        except Exception as e:
            print(f"Error updating row {sheet_row} in Google Sheets: {e}")

    if success_count > 0:
        try:
            os.remove(path)
            print(f"\nSync complete! Successfully updated {success_count} rows. Results file deleted.")
        except Exception as e:
            print(f"\nSync complete, but could not delete results file: {e}")
    else:
        print("\nSync finished, but 0 rows were updated. The results file was NOT deleted so you can inspect it.")

if __name__ == "__main__":
    sync_results()
