import json, os, sys, random
from datetime import datetime, timezone

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.gsheets import GoogleSheetsClient

def insert_demo3_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    col_map = client.config["column_mapping"]
    
    rand_id = str(random.randint(10000, 99999))
    run_id = datetime.now(timezone.utc).strftime("%m%d%H%M%S")
    
    listings = [
        {
            "管理ID_SKU": f"TEST-DEMO3-POKE-{run_id}",
            "商品名_JP": f"ポケモンカード ピカチュウ プロモ {run_id}",
            "Category": "Pokemon Cards",
            "Condition": "Used",
            "Brand": "Nintendo",
            "仕入URL": f"https://jp.mercari.com/item/m86121666040?rid={run_id}",
            "出品価格_USD": "85.00",
            "Shipping_Policy": "DDP(1～50USD)Economy",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m86121666040_1.jpg",
            "担当者": "Final Demo",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": f"TEST-DEMO3-CAM-{run_id}",
            "商品名_JP": f"Nikon D850 ボディ デジタル一眼レフ {run_id}",
            "Category": "Digital SLR Cameras",
            "Condition": "Used",
            "Brand": "Nikon",
            "仕入URL": f"https://jp.mercari.com/item/m35415760638?rid={run_id}",
            "出品価格_USD": "1800.00",
            "Shipping_Policy": "DDP(101～200USD)Expedited",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m35415760638_1.jpg",
            "担当者": "Final Demo",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": f"TEST-DEMO3-FIG-{run_id}",
            "商品名_JP": f"S.H.Figuarts ドラゴンボール アクションフィギュア {run_id}",
            "Category": "Figure",
            "Condition": "New",
            "Brand": "Bandai",
            "仕入URL": f"https://jp.mercari.com/item/m30863459484?rid={run_id}",
            "出品価格_USD": "85.00",
            "Shipping_Policy": "DDP(1～50USD)Economy",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m30863459484_1.jpg",
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
            "eBayアカウント": item.get("eBayアカウント", "store_main"),
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
        print(f"Successfully inserted {len(rows_to_insert)} Final Demo listings into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting final demo listings: {e}")

if __name__ == "__main__":
    insert_demo3_data()
