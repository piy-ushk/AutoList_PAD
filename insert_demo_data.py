import json, os, sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_demo_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    
    # We will append a row to the end. 
    # Let's map it based on the columns
    col_map = client.config["column_mapping"]
    # It's a list from A to BB (54 columns)
    row_data = [""] * 54
    
    mapping = {
        "管理ID_SKU": "PKMN-001",
        "出品日": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "eBayアカウント": "store_main",
        "販売形式": "FixedPrice",
        "商品名_JP": "ポケモンカード ピカチュウ VMAX クライマックス UR",
        "Category": "Pokemon Cards",
        "Condition": "Used",
        "Brand": "Nintendo",
        "出品価格_USD": "150",
        "仕入URL": "https://mercari.com/example_pikachu",
        "画像URLs": "https://example.com/pikachu.jpg",
        "担当者": "Test Staff",
        "Listing_Status": "pending_ai"
    }
    
    # map to index
    for i in range(54):
        col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
        field_name = col_map.get(col_letter)
        if field_name in mapping:
            row_data[i] = mapping[field_name]
            
    try:
        client.api.append_range(tab, "A:BB", [row_data])
        print("Successfully inserted Pokemon Card demo data into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting demo data: {e}")

if __name__ == "__main__":
    insert_demo_data()
