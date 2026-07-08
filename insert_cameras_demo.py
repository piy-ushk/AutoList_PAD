import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def insert_camera_demo():
    client = GoogleSheetsClient()
    headers = client.api.read_range(client.tabs['listings'], 'A1:BC1')[0]
    
    demo_items = [
        {
            "SKU": "TEST-DEMO-CAM-1",
            "商品名_JP": "Ilford Sprite 35-II Reusable 35mm Film Camera Black",
            "Brand": "Ilford",
            "Model_Number": "Sprite 35-II",
            "Condition": "Used",
            "Category": "disposable_camera",
            "仕入れ値_JPY": "4500",
            "備考": "Good working condition.",
            "仕入URL": "https://jp.mercari.com/item/m24806593561",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m24806593561_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-CAM-2",
            "商品名_JP": "Pentax K-70 Digital SLR Camera Body Black Tested",
            "Brand": "Pentax",
            "Model_Number": "K-70",
            "Condition": "Used",
            "Category": "Digital SLR Cameras",
            "仕入れ値_JPY": "35000",
            "備考": "Tested and working.",
            "仕入URL": "https://jp.mercari.com/item/m59123840515",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m59123840515_1.jpg"
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
