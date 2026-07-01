import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.gsheets import GoogleSheetsClient

def fix_cap():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    data = client.api.read_range(tab, "A:BC")
    if not data or len(data) < 2:
        return
        
    headers = data[0]
    col_map = {name: idx for idx, name in enumerate(headers)}
    
    status_col = col_map.get("Listing_Status")
    sku_col = col_map.get("管理ID_SKU")
    title_col = col_map.get("ChatGPT_Title")
    desc_col = col_map.get("ChatGPT_Description")
    
    for idx, row in enumerate(data[1:], start=2):
        if len(row) > sku_col and "TEST-DEMO3-CAM" in row[sku_col]:
            # This is our camera
            print(f"Found Camera at row {idx}")
            updates = []
            
            # Replace "cap" with "cover" in Title
            if len(row) > title_col:
                new_title = row[title_col].replace("cap", "cover").replace("Cap", "Cover").replace("CAP", "COVER")
                if new_title != row[title_col]:
                    updates.append(("ChatGPT_Title", new_title))
                    print("Updated title")
            
            # Replace "cap" with "cover" in Description
            if len(row) > desc_col:
                new_desc = row[desc_col].replace("cap", "cover").replace("Cap", "Cover").replace("CAP", "COVER")
                if new_desc != row[desc_col]:
                    updates.append(("ChatGPT_Description", new_desc))
                    print("Updated description")
            
            # Set status back to pending_verification so it re-validates
            updates.append(("Listing_Status", "pending_verification"))
            
            client.batch_update_cells(idx, updates)
            print("Successfully updated the sheet for re-validation.")

if __name__ == "__main__":
    fix_cap()
