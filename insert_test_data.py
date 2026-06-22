import json, os, sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_test_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    
    col_map = client.config["column_mapping"]
    
    run_id = datetime.now(timezone.utc).strftime("%m%d%H%M%S")
    
    listings = [
        {
            "管理ID_SKU": f"TEST-{run_id}-001",
            "商品名_JP": f"テストカード 1 {run_id}",
            "仕入URL": f"https://jp.mercari.com/item/m35656046994?rid={run_id}",
            "出品価格_USD": "9999.99",
            "Shipping_Policy": "DDP(1～50USD)Economy",
            "eBay_Title": f"テストカード 1 {run_id} Pokémon Card From Japan",
            "ChatGPT_Title": f"テストカード 1 {run_id} Pokémon Card From Japan"
        },
        {
            "管理ID_SKU": f"TEST-{run_id}-002",
            "商品名_JP": f"テストカード 2 {run_id}",
            "仕入URL": f"https://jp.mercari.com/item/m19206380831?rid={run_id}",
            "出品価格_USD": "9999.99",
            "Shipping_Policy": "DDP(101～200USD)Expedited",
            "eBay_Title": f"テストカード 2 {run_id} Pokemon Card Nintendo From Japan",
            "ChatGPT_Title": f"テストカード 2 {run_id} Pokemon Card Nintendo From Japan"
        },
        {
            "管理ID_SKU": f"TEST-{run_id}-003",
            "商品名_JP": f"テストカード 3 {run_id}",
            "仕入URL": f"https://jp.mercari.com/item/m93431796197?rid={run_id}",
            "出品価格_USD": "9999.99",
            "Shipping_Policy": "DDP(101～200USD)Expedited無在庫10日handling",
            "eBay_Title": f"テストカード 3 {run_id} Pokémon Card From Japan",
            "ChatGPT_Title": f"テストカード 3 {run_id} Pokémon Card From Japan"
        },
        {
            "管理ID_SKU": f"TEST-{run_id}-004",
            "商品名_JP": f"テストカード 4 {run_id}",
            "仕入URL": f"https://jp.mercari.com/item/m89746857993?rid={run_id}",
            "出品価格_USD": "9999.99",
            "Shipping_Policy": "DDP(101～200USD)Expedited荷物大南米除外",
            "eBay_Title": f"テストカード 4 {run_id} Pokémon Card Nintendo From Japan",
            "ChatGPT_Title": f"テストカード 4 {run_id} Pokémon Card Nintendo From Japan"
        },
        {
            "管理ID_SKU": f"TEST-{run_id}-005",
            "商品名_JP": f"テストカード 5 {run_id}",
            "仕入URL": f"https://jp.mercari.com/item/m31314525197?rid={run_id}",
            "出品価格_USD": "9999.99",
            "Shipping_Policy": "DDP(101～200USD)Expedited無在庫20日handling",
            "eBay_Title": f"テストカード 5 {run_id} Pokémon Card Nintendo From Japan",
            "ChatGPT_Title": f"テストカード 5 {run_id} Pokémon Card Nintendo From Japan"
        }
    ]

    rows_to_insert = []
    for item in listings:
        row_data = [""] * 55
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
        
        # Merge any other keys defined in item (e.g., eBay_Title, ChatGPT_Title)
        for k, v in item.items():
            mapping[k] = v
        
        for i in range(55):
            col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
            field_name = col_map.get(col_letter)
            if field_name in mapping:
                row_data[i] = mapping[field_name]
        rows_to_insert.append(row_data)
            
    try:
        client.api.append_range(tab, "A:BC", rows_to_insert)
        print(f"Successfully inserted {len(rows_to_insert)} TEST listings into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting TEST listings: {e}")

if __name__ == "__main__":
    insert_test_data()
