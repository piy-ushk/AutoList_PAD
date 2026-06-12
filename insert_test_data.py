import json, os, sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_test_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    
    col_map = client.config["column_mapping"]
    
    listings = [
        {
            "管理ID_SKU": "TEST-001",
            "商品名_JP": "テストカード 1",
            "仕入URL": "https://jp.mercari.com/item/m12345678901",
            "出品価格_USD": "10",
            "Shipping_Policy": "DDP(1～50USD)Economy"
        },
        {
            "管理ID_SKU": "TEST-002",
            "商品名_JP": "テストカード 2",
            "仕入URL": "https://jp.mercari.com/item/m12345678902",
            "出品価格_USD": "20",
            "Shipping_Policy": "DDP(101～200USD)Expedited"
        },
        {
            "管理ID_SKU": "TEST-003",
            "商品名_JP": "テストカード 3",
            "仕入URL": "https://jp.mercari.com/item/m12345678903",
            "出品価格_USD": "30",
            "Shipping_Policy": "DDP(101～200USD)Expedited無在庫10日handling"
        },
        {
            "管理ID_SKU": "TEST-004",
            "商品名_JP": "テストカード 4",
            "仕入URL": "https://jp.mercari.com/item/m12345678904",
            "出品価格_USD": "40",
            "Shipping_Policy": "DDP(101～200USD)Expedited荷物大南米除外"
        },
        {
            "管理ID_SKU": "TEST-005",
            "商品名_JP": "テストカード 5",
            "仕入URL": "https://jp.mercari.com/item/m12345678905",
            "出品価格_USD": "50",
            "Shipping_Policy": "DDP(101～200USD)Expedited無在庫20日handling"
        }
    ]

    rows_to_insert = []
    for item in listings:
        row_data = [""] * 54
        mapping = {
            "管理ID_SKU": item["管理ID_SKU"],
            "出品日": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "eBayアカウント": "store_main",
            "販売形式": "FixedPrice",
            "商品名_JP": item["商品名_JP"],
            "Category": "Pokemon Cards",
            "Condition": "Used",
            "Brand": "Nintendo",
            "出品価格_USD": item["出品価格_USD"],
            "Shipping_Policy": item["Shipping_Policy"],
            "仕入URL": item["仕入URL"],
            "画像URLs": "https://upload.wikimedia.org/wikipedia/en/a/a6/Pok%C3%A9mon_Pikachu_art.png",
            "担当者": "Test Staff",
            "Listing_Status": "pending_ai"
        }
        
        for i in range(54):
            col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
            field_name = col_map.get(col_letter)
            if field_name in mapping:
                row_data[i] = mapping[field_name]
        rows_to_insert.append(row_data)
            
    try:
        client.api.append_range(tab, "A:BB", rows_to_insert)
        print(f"Successfully inserted {len(rows_to_insert)} TEST listings into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting TEST listings: {e}")

if __name__ == "__main__":
    insert_test_data()
