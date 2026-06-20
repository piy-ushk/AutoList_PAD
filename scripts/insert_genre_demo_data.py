import json, os, sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_genre_demo_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    col_map = client.config["column_mapping"]
    
    # 1 Pokemon Card and 1 Plastic Model/Figure to show genre adaptation
    listings = [
        {
            "管理ID_SKU": "DEMO-POKE-001",
            "商品名_JP": "ポケモンカード ピカチュウ プロモ",
            "Category": "Pokemon Cards",
            "Condition": "Used",
            "Brand": "Nintendo",
            "仕入URL": "https://jp.mercari.com/item/m12345678901",
            "出品価格_USD": "85.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1025/400/400",
            "担当者": "Final Demo",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "DEMO-FIG-002",
            "商品名_JP": "機動戦士ガンダム RX-78-2 プラモデル",
            "Category": "Plastic Models",
            "Condition": "New",
            "Brand": "Bandai",
            "仕入URL": "https://jp.mercari.com/item/m10987654321",
            "出品価格_USD": "120.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1062/400/400",
            "担当者": "Final Demo",
            "Listing_Status": "pending_ai"
        }
    ]

    rows_to_insert = []
    for item in listings:
        row_data = [""] * 57 
        mapping = {
            "管理ID_SKU": item["管理ID_SKU"],
            "出品日": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "eBayアカウント": "store_main",
            "販売形式": "FixedPrice",
            "商品名_JP": item["商品名_JP"],
            "Category": item["Category"],
            "Condition": item["Condition"],
            "Brand": item["Brand"],
            "出品価格_USD": item["出品価格_USD"],
            "仕入URL": item["仕入URL"],
            "画像URLs": item["画像URLs"],
            "担当者": item["担当者"],
            "Listing_Status": item["Listing_Status"]
        }
        
        for i in range(57):
            col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
            field_name = col_map.get(col_letter)
            if field_name in mapping:
                row_data[i] = mapping[field_name]
        rows_to_insert.append(row_data)
            
    try:
        client.api.append_range(tab, "A:BC", rows_to_insert)
        print(f"Successfully inserted {len(rows_to_insert)} Genre Demo listings into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting video test listings: {e}")

if __name__ == "__main__":
    insert_genre_demo_data()
