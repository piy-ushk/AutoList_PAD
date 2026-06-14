import json, os, sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_video_test_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    col_map = client.config["column_mapping"]
    
    # Define 4 specific test cases to demonstrate all Phase 2 features in a video
    listings = [
        {
            "管理ID_SKU": "TEST-V-001",
            "商品名_JP": "ポケモンカード ピカチュウ 通常商品",
            "仕入URL": "https://jp.mercari.com/item/m80539733708",
            "出品価格_USD": "45.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1025/400/400", # Dog image
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-V-002",
            "商品名_JP": "ポケモンカード リザードン 高額商品",
            "仕入URL": "https://jp.mercari.com/item/m65587432790",
            "出品価格_USD": "350.00", # > $300 (High-Value Threshold)
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1062/400/400", # Aurora image
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-V-003",
            "商品名_JP": "ポケモンカード ミュウ レプリカ警告品",
            "仕入URL": "https://jp.mercari.com/item/m85975277992",
            "出品価格_USD": "25.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1074/400/400", # Cat image
            "Listing_Status": "pending_validation",
            "AI_Status": "ai_complete",
            "eBay_Title": "TEST Pokemon Card Mew Replica Banned Word",
            "ChatGPT_Title": "TEST Pokemon Card Mew Replica Banned Word",
            "ChatGPT_Description": "This is a replica card for display purposes.",
            "ChatGPT_ItemSpecifics": "{}"
        },
        {
            "管理ID_SKU": "TEST-V-004",
            "商品名_JP": "ポケモンカード ピカチュウ 重複商品", # Same product as TEST-V-001
            "仕入URL": "https://jp.mercari.com/item/m56059963187",
            "出品価格_USD": "42.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1025/300/300", # Visually identical to TEST-V-001 (different dimensions to test PHash)
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-V-005",
            "商品名_JP": "ポケモンカード イーブイ カスタム予約品",
            "仕入URL": "https://jp.mercari.com/item/m80092174003",
            "出品価格_USD": "55.00",
            "Shipping_Policy": "STOCK_3D_1-50_ECO",
            "画像URLs": "https://picsum.photos/id/1084/400/400",
            "Listing_Status": "pending_ai",
            "Schedule_Time": "2026/06/25" # Demonstrate custom future date input
        }
    ]

    rows_to_insert = []
    for item in listings:
        row_data = [""] * 57 # Ensure size up to BC column if needed
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
            "仕入URL": item["仕入URL"],
            "画像URLs": item["画像URLs"],
            "担当者": "Video Demo Staff",
            "Listing_Status": item["Listing_Status"]
        }
        
        # Merge any other keys defined in item (e.g., eBay_Title, ChatGPT_Title, AI_Status)
        for k, v in item.items():
            mapping[k] = v

        for i in range(57):
            col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
            field_name = col_map.get(col_letter)
            if field_name in mapping:
                row_data[i] = mapping[field_name]
        rows_to_insert.append(row_data)
            
    try:
        client.api.append_range(tab, "A:BC", rows_to_insert)
        print(f"Successfully inserted {len(rows_to_insert)} Video Demo listings into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting video test listings: {e}")

if __name__ == "__main__":
    insert_video_test_data()
