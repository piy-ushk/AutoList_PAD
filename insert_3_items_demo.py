import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def insert_final_demo():
    client = GoogleSheetsClient()
    
    print("Clearing existing sheet data...")
    client.api.write_range(client.tabs['listings'], 'A2:BC1000', [[''] * 55 for _ in range(999)])
    
    headers = client.api.read_range(client.tabs['listings'], 'A1:BC1')[0]
    
    demo_items = [
        {
            "SKU": "TEST-DEMO-3-1",
            "商品名_JP": "Vintage Alice in Wonderland Japanese 3D Picture Book 1980s",
            "Brand": "N/A",
            "Model_Number": "N/A",
            "Condition": "Used",
            "Category": "Picture Book",
            "仕入れ値_JPY": "4500",
            "備考": "Some pop-up mechanics are slightly bent.",
            "仕入URL": "https://jp.mercari.com/item/m45040687729",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m45040687729_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-3-2",
            "商品名_JP": "Nintendo Super Famicom Console Boxed CIB Tested Working SFC",
            "Brand": "Nintendo",
            "Model_Number": "SHVC-001",
            "Condition": "Used",
            "Category": "Game Related",
            "仕入れ値_JPY": "8000",
            "備考": "Console is yellowed due to age.",
            "仕入URL": "https://jp.mercari.com/item/m44906231946",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m44906231946_1.jpg"
        },
         {
            "SKU": "TEST-DEMO-8",
            "商品名_JP": "Nikon 1 J1 Mirrorless Digital Camera Body White Tested",
            "Brand": "Nikon",
            "Model_Number": "J1",
            "Condition": "Used",
            "Category": "Cameras & Photo > Digital Cameras",
            "仕入れ値_JPY": "10000",
            "備考": "Mirrorless body.",
            "仕入URL": "https://jp.mercari.com/item/m47275046421",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m47275046421_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-3-3",
            "商品名_JP": "Vintage Brand Ultra Seven Sofubi Soft Vinyl Figure Vintage 1970s Japan",
            "Brand": "Vintage Brand",
            "Model_Number": "Ultra Seven",
            "Condition": "Used",
            "Category": "Vintage Toy",
            "仕入れ値_JPY": "35000",
            "備考": "Paint fading on the boots and gloves.",
            "仕入URL": "https://jp.mercari.com/item/m91233202436",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m91233202436_1.jpg"
        }
    ]

    rows_to_insert = []
    for item in demo_items:
        row = [''] * len(headers)
        row[headers.index('Listing_Status')] = 'pending_ai'
        
        item['管理ID_SKU'] = item['SKU']
        item['販売形式'] = 'Buy It Now'
        item['出品価格_USD'] = '999.00'
        item['担当者'] = 'DemoStaff'
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

    print(f"Inserting {len(rows_to_insert)} items...")
    range_name = f"A2:BC{1 + len(rows_to_insert)}"
    client.api.write_range(client.tabs['listings'], range_name, rows_to_insert)
    print("Done! You can now run main.py to process these 14 demo items.")

if __name__ == "__main__":
    insert_final_demo()
