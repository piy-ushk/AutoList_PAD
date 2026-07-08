import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def insert_camera_demo():
    client = GoogleSheetsClient()
    
    print("Clearing existing sheet data...")
    client.api.write_range(client.tabs['listings'], 'A2:BC1000', [[''] * 55 for _ in range(999)])
    
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
            "仕入URL": "https://jp.mercari.com/item/m12345678901",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m12345678901_1.jpg"
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
            "仕入URL": "https://jp.mercari.com/item/m12345678902",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m12345678902_1.jpg"
        }
    ]

    print(f"Inserting {len(demo_items)} camera items...")
    
    rows_to_insert = []
    for item in demo_items:
        row = [''] * len(headers)
        for i, header in enumerate(headers):
            if header in item:
                row[i] = item[header]
        row[headers.index('出品価格_USD')] = '299.00'
        row[headers.index('担当者')] = 'AI Agent'
        row[headers.index('Status')] = 'pending_ai'
        rows_to_insert.append(row)
        
    client.api.write_range(client.tabs['listings'], f'A2:BC{len(rows_to_insert)+1}', rows_to_insert)
    print("Done! You can now run main.py to process these camera items.")

if __name__ == "__main__":
    insert_camera_demo()
