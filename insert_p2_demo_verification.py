import json
import os
import sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_p2_demo_data():
    client = GoogleSheetsClient()
    tab_listings = client.tabs["listings"]
    tab_staff = client.tabs.get("staff", "スタッフ管理")
    col_map = client.config["column_mapping"]
    
    # 4 items: 1 base item and 3 duplicates to trigger JAN, Model, and URL blocking respectively
    listings = [
        {
            "管理ID_SKU": "TEST-V-001",
            "商品名_JP": "ポケモンカード ピカチュウ Base Card",
            "Category": "Pokemon Cards",
            "Brand": "Nintendo",
            "Model_Number": "M-001",
            "JAN_Code": "4900000000001",
            "Condition": "Used",
            "出品価格_USD": "45.00",
            "仕入URL": "https://jp.mercari.com/item/m001",
            "画像URLs": "https://picsum.photos/id/1025/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-V-002",
            "商品名_JP": "ポケモンカード ミュウ Duplicate JAN Card",
            "Category": "Pokemon Cards",
            "Brand": "Nintendo",
            "Model_Number": "M-002",
            "JAN_Code": "4900000000001", # Duplicate JAN (should block)
            "Condition": "Used",
            "出品価格_USD": "25.00",
            "仕入URL": "https://jp.mercari.com/item/m002",
            "画像URLs": "https://picsum.photos/id/1062/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-V-003",
            "商品名_JP": "ポケモンカード リザードン Duplicate Model Card",
            "Category": "Pokemon Cards",
            "Brand": "Nintendo",
            "Model_Number": "M-001", # Duplicate Model Number (should block)
            "JAN_Code": "4900000000003",
            "Condition": "Used",
            "出品価格_USD": "35.00",
            "仕入URL": "https://jp.mercari.com/item/m003",
            "画像URLs": "https://picsum.photos/id/1074/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-V-004",
            "商品名_JP": "ポケモンカード イーブイ Duplicate URL Card",
            "Category": "Pokemon Cards",
            "Brand": "Nintendo",
            "Model_Number": "M-004",
            "JAN_Code": "4900000000004",
            "Condition": "Used",
            "出品価格_USD": "22.00",
            "仕入URL": "https://jp.mercari.com/item/m001", # Duplicate URL (should block)
            "画像URLs": "https://picsum.photos/id/1084/400/400",
            "Listing_Status": "pending_ai"
        }
    ]

    # Clean the sheets listings, duplicate DB, error log, and staff tabs first
    base_url = f"https://sheets.googleapis.com/v4/spreadsheets/{client.spreadsheet_id}/values:batchClear"
    headers = {
        "Authorization": f"Bearer {client.access_token}", 
        "Content-Type": "application/json"
    }
    ranges = [
        f"'{client.tabs['listings']}'!A2:BC100",
        f"'{client.tabs['duplicate_db']}'!A2:K100",
        f"'{client.tabs['error_log']}'!A2:I100",
        f"'{tab_staff}'!A2:I100"
    ]
    import urllib.request
    body = json.dumps({"ranges": ranges}).encode("utf-8")
    req = urllib.request.Request(base_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print("Successfully cleared previous verification data from Sheets.")
    except Exception as e:
        print(f"Error resetting sheets: {e}")

    # Insert sample staff member "John Doe"
    staff_row = ["STAFF-01", "John Doe", "Operator", "john@example.com", "store_main", "YES", "0", "0", "0"]
    try:
        client.api.append_range(tab_staff, "A:I", [staff_row])
        print("Successfully added John Doe to the Staff Management sheet!")
    except Exception as e:
        print(f"Error inserting staff: {e}")

    rows_to_insert = []
    for item in listings:
        row_data = [""] * 60
        mapping = {
            "管理ID_SKU": item["管理ID_SKU"],
            "出品日": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "eBayアカウント": "store_main",
            "販売形式": "FixedPrice",
            "商品名_JP": item["商品名_JP"],
            "Category": item["Category"],
            "Condition": item["Condition"],
            "Brand": item["Brand"],
            "Model_Number": item["Model_Number"],
            "JAN_Code": item["JAN_Code"],
            "出品価格_USD": item["出品価格_USD"],
            "仕入URL": item["仕入URL"],
            "画像URLs": item["画像URLs"],
            "担当者": "John Doe", # Assign to John Doe
            "Listing_Status": item["Listing_Status"]
        }

        for i in range(57):
            col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
            field_name = col_map.get(col_letter)
            if field_name in mapping:
                row_data[i] = mapping[field_name]
        rows_to_insert.append(row_data)
            
    try:
        client.api.append_range(tab_listings, "A:BC", rows_to_insert)
        print("Successfully inserted Phase 2 Verification data into Google Sheet!")
    except Exception as e:
        print(f"Error inserting listings: {e}")

if __name__ == "__main__":
    insert_p2_demo_data()
