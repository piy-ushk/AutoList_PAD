import json, urllib.request, os, sys

# Add current directory to path so modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def clear_test_data():
    client = GoogleSheetsClient()
    if not client.access_token or not client.spreadsheet_id:
        print("Missing token or sheet ID")
        return
    
    base_url = f"https://sheets.googleapis.com/v4/spreadsheets/{client.spreadsheet_id}/values:batchClear"
    headers = {
        "Authorization": f"Bearer {client.access_token}", 
        "Content-Type": "application/json"
    }
    
    # Clear from row 2 downwards for all tabs to reset them, except VERO which has 15 rows initially.
    ranges = []
    for tab_key, tab_name in client.tabs.items():
        if tab_key == "vero_dict":
            # setup_sheets.py creates 1 header + 14 sample rows = 15 rows. Clear from row 16.
            ranges.append(f"'{tab_name}'!A16:BC1000")
        else:
            ranges.append(f"'{tab_name}'!A2:BC1000")
            
    body = json.dumps({"ranges": ranges}).encode("utf-8")
    req = urllib.request.Request(base_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print("Successfully cleared all test cells from the Google Sheets tabs.")
    except Exception as e:
        print(f"Error clearing sheets: {e}")

if __name__ == "__main__":
    clear_test_data()
