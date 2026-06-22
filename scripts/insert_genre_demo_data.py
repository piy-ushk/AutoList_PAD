import json, os, sys, random
from datetime import datetime, timezone

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.gsheets import GoogleSheetsClient

def insert_genre_demo_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    col_map = client.config["column_mapping"]
    
    rand_id = str(random.randint(10000, 99999))
    run_id = datetime.now(timezone.utc).strftime("%m%d%H%M%S")
    
    listings = [
        {
            "管理ID_SKU": f"TEST-POKE-{run_id}-001",
            "商品名_JP": f"ポケモンカード ピカチュウ プロモ {run_id}",
            "Category": "Pokemon Cards",
            "Condition": "Used",
            "Brand": "Nintendo",
            "仕入URL": f"https://jp.mercari.com/item/m{rand_id}111",
            "出品価格_USD": "85.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1025/400/400",
            "担当者": "Final Demo",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": f"TEST-FIG-{run_id}-002",
            "商品名_JP": f"機動戦士ガンダム RX-78-2 プラモデル {run_id}",
            "Category": "Plastic Models",
            "Condition": "New",
            "Brand": "Bandai",
            "仕入URL": f"https://jp.mercari.com/item/m{rand_id}222",
            "出品価格_USD": "120.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1062/400/400",
            "担当者": "Final Demo",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": f"TEST-VERO-{run_id}-003",
            "商品名_JP": f"初音ミク フィギュア 1/7スケール {run_id}", # "初音ミク" triggers Patent Troll block
            "Category": "Figures",
            "Condition": "New",
            "Brand": "Good Smile Company",
            "仕入URL": f"https://jp.mercari.com/item/m{rand_id}333",
            "出品価格_USD": "150.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1074/400/400",
            "担当者": "Final Demo",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": f"TEST-DUP-{run_id}-004",
            "商品名_JP": f"ポケモンカード ピカチュウ プロモ {run_id}", # Duplicate of item 1
            "Category": "Pokemon Cards",
            "Condition": "Used",
            "Brand": "Nintendo",
            "仕入URL": f"https://jp.mercari.com/item/m{rand_id}111", # Duplicate URL
            "出品価格_USD": "85.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1025/400/400",
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
