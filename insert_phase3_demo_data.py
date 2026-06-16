import json
import os
import sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_phase3_demo_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    col_map = client.config["column_mapping"]
    
    # 6 specific test cases representing all Phase 3 genres
    listings = [
        {
            "管理ID_SKU": "TEST-G-001",
            "商品名_JP": "ポケモンカード レックウザ デルタ種",
            "Category": "Pokemon Cards",
            "Brand": "Nintendo",
            "Model_Number": "N/A",
            "JAN_Code": "N/A",
            "Condition": "Used",
            "出品価格_USD": "85.00",
            "仕入URL": "https://jp.mercari.com/item/m11111111111",
            "画像URLs": "https://picsum.photos/id/1025/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-G-002",
            "商品名_JP": "初音ミク フィギュア 1/7スケール プレステージ",
            "Category": "Figures",
            "Brand": "Good Smile Company",
            "Model_Number": "Miku-001",
            "JAN_Code": "4571245298881",
            "Condition": "Used",
            "出品価格_USD": "120.00",
            "仕入URL": "https://jp.mercari.com/item/m22222222222",
            "画像URLs": "https://picsum.photos/id/1062/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-G-003",
            "商品名_JP": "タミヤ 1/24 ポルシェ 911 プラスチックモデルキット",
            "Category": "Vintage plastic models",
            "Brand": "Tamiya",
            "Model_Number": "24321",
            "JAN_Code": "4950344243211",
            "Condition": "New",
            "出品価格_USD": "55.00",
            "仕入URL": "https://jp.mercari.com/item/m33333333333",
            "画像URLs": "https://picsum.photos/id/1074/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-G-004",
            "商品名_JP": "ポピー 超合金 マジンガーZ ビンテージ玩具",
            "Category": "Vintage toys",
            "Brand": "Popy",
            "Model_Number": "GA-01",
            "JAN_Code": "N/A",
            "Condition": "Used",
            "出品価格_USD": "250.00",
            "仕入URL": "https://jp.mercari.com/item/m44444444444",
            "画像URLs": "https://picsum.photos/id/1084/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-G-005",
            "商品名_JP": "タミヤ 1/10 ホーネット RC バギー キット",
            "Category": "RC related",
            "Brand": "Tamiya",
            "Model_Number": "58336",
            "JAN_Code": "4950344583362",
            "Condition": "New",
            "出品価格_USD": "160.00",
            "仕入URL": "https://jp.mercari.com/item/m55555555555",
            "画像URLs": "https://picsum.photos/id/101/400/400",
            "Listing_Status": "pending_ai"
        },
        {
            "管理ID_SKU": "TEST-G-006",
            "商品名_JP": "任天堂 スーパーマリオブラザーズ ファミコン ソフト 箱説あり",
            "Category": "Game related",
            "Brand": "Nintendo",
            "Model_Number": "HVC-MA",
            "JAN_Code": "N/A",
            "Condition": "Used",
            "出品価格_USD": "75.00",
            "仕入URL": "https://jp.mercari.com/item/m66666666666",
            "画像URLs": "https://picsum.photos/id/201/400/400",
            "Listing_Status": "pending_ai"
        }
    ]

    rows_to_insert = []
    for item in listings:
        row_data = [""] * 60 # Ensure size matches sheet row layout
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
            "担当者": "Phase3 Demo Staff",
            "Listing_Status": item["Listing_Status"]
        }

        for i in range(57):
            col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
            field_name = col_map.get(col_letter)
            if field_name in mapping:
                row_data[i] = mapping[field_name]
        rows_to_insert.append(row_data)
            
    try:
        # Append data to Sheet
        client.api.append_range(tab, "A:BC", rows_to_insert)
        print(f"Successfully inserted {len(rows_to_insert)} Phase 3 Demo listings into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting Phase 3 demo listings: {e}")

if __name__ == "__main__":
    insert_phase3_demo_data()
