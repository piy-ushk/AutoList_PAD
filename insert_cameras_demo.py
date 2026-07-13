import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def insert_camera_demo():
    client = GoogleSheetsClient()
    headers = client.api.read_range(client.tabs['listings'], 'A1:BC1')[0]
    
    demo_items = [
        {
            "SKU": "TEST-DEMO-4",
            "商品名_JP": "Pokemon Card Charizard VMAX SSR 308/190 Shiny Star V Japanese Mint",
            "Brand": "Nintendo",
            "Model_Number": "Does not apply",
            "Condition": "Used",
            "Category": "Toys & Hobbies > Collectible Card Games > CCG Individual Cards",
            "仕入れ値_JPY": "5000",
            "備考": "Collector item.",
            "仕入URL": "https://jp.mercari.com/item/m77535112834",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m77535112834_1.jpg"
        }
    ]

    print(f"Inserting {len(demo_items)} camera items...")
    
    rows_to_insert = []
    for item in demo_items:
        row = [''] * len(headers)
        row[headers.index('Listing_Status')] = 'pending_ai'
        
        item['管理ID_SKU'] = item['SKU']
        item['販売形式'] = 'Buy It Now'
        item['出品価格_USD'] = '299.00'
        item['担当者'] = 'AI Agent'
        item['在庫_Quantity'] = '0'
        item['Shipping_Policy'] = 'DDP(101～200USD)Expedited'
        item['Return_Policy'] = 'Returns Accepted'
        item['Item_Condition'] = item['Condition']
        item['状態詳細'] = item['Condition']
        item['Handling_Time'] = "10日"
        item['自動価格調整'] = "NO"

        for key, val in item.items():
            if key in headers:
                row[headers.index(key)] = str(val)
                
        rows_to_insert.append(row)
        
    client.api.write_range(client.tabs['listings'], f'A2:BC{len(rows_to_insert)+1}', rows_to_insert)
    print("Done! You can now run main.py to process these camera items.")

if __name__ == "__main__":
    insert_camera_demo()
