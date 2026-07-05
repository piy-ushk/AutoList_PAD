import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient

def insert_phase4_only():
    client = GoogleSheetsClient()
    
    print("Clearing existing sheet data...")
    client.api.write_range(client.tabs['listings'], 'A2:BC1000', [[''] * 55 for _ in range(999)])
    
    headers = client.api.read_range(client.tabs['listings'], 'A1:BC1')[0]
    
    demo_items = [
        {
            "SKU": "TEST-DEMO-0",
            "商品名_JP": "Tamiya 1/12 Scale Tyrrell P34 Six Wheeler Vintage Plastic Model Kit Unassembled",
            "Brand": "Tamiya",
            "Model_Number": "1/12 Scale",
            "Condition": "New",
            "Category": "Vintage Plastic Model",
            "想定仕入額_JPY": "12000",
            "備考": "Box has slight wear due to age."
        },
        {
            "SKU": "TEST-DEMO-1",
            "商品名_JP": "Vintage Brand Ultra Seven Sofubi Soft Vinyl Figure Vintage 1970s Japan",
            "Brand": "Vintage Brand",
            "Model_Number": "Ultra Seven",
            "Condition": "Used",
            "Category": "Vintage Toy",
            "想定仕入額_JPY": "35000",
            "備考": "Paint fading on the boots and gloves."
        },
        {
            "SKU": "TEST-DEMO-6",
            "商品名_JP": "Vintage Tin Toy Robot 1960s Japan Wind Up Original Box",
            "Brand": "Unknown",
            "Model_Number": "Does not apply",
            "Condition": "Used",
            "Category": "Toys & Hobbies > Vintage & Antique Toys > Tin > Robots",
            "想定仕入額_JPY": "8000",
            "備考": "Vintage item."
        },
        {
            "SKU": "TEST-DEMO-7",
            "商品名_JP": "Hatsune Miku 1/7 Scale Figure Miku Symphony 2019 Ver.",
            "Brand": "Good Smile Company",
            "Model_Number": "4580416942639",
            "Condition": "New",
            "Category": "Toys & Hobbies > Action Figures & Accessories > Action Figures",
            "想定仕入額_JPY": "12000",
            "備考": "New item."
        },
        {
            "SKU": "TEST-DEMO-8",
            "商品名_JP": "Pokemon Card Pikachu Promo 001/S-P Full Art Holo Mint",
            "Brand": "Nintendo",
            "Model_Number": "Does not apply",
            "Condition": "Used",
            "Category": "Toys & Hobbies > Collectible Card Games > CCG Individual Cards",
            "想定仕入額_JPY": "5000",
            "備考": "Collector item."
        },
        {
            "SKU": "TEST-DEMO-9",
            "商品名_JP": "Canon EOS 5D Mark IV DSLR Camera Body Only Tested Japan",
            "Brand": "Canon",
            "Model_Number": "1483C002",
            "Condition": "Used",
            "Category": "Cameras & Photo > Digital Cameras",
            "想定仕入額_JPY": "80000",
            "備考": "Working perfectly."
        },
        {
            "SKU": "TEST-DEMO-10",
            "商品名_JP": "Canon EF 50mm f/1.4 USM Standard Prime Lens Near Mint",
            "Brand": "Canon",
            "Model_Number": "2515A003",
            "Condition": "Used",
            "Category": "Cameras & Photo > Lenses & Filters > Lenses",
            "想定仕入額_JPY": "25000",
            "備考": "Excellent lens."
        },
        {
            "SKU": "TEST-DEMO-11",
            "商品名_JP": "Sony Cyber-shot DSC-RX100 VII Digital Camera Black",
            "Brand": "Sony",
            "Model_Number": "DSCRX100M7/B",
            "Condition": "Used",
            "Category": "Cameras & Photo > Digital Cameras",
            "想定仕入額_JPY": "90000",
            "備考": "Compact camera."
        },
        {
            "SKU": "TEST-DEMO-12",
            "商品名_JP": "Sony Alpha a7 III Mirrorless Digital Camera Body ILCE-7M3",
            "Brand": "Sony",
            "Model_Number": "ILCE-7M3",
            "Condition": "Used",
            "Category": "Cameras & Photo > Digital Cameras",
            "想定仕入額_JPY": "150000",
            "備考": "Mirrorless body."
        },
        {
            "SKU": "TEST-DEMO-13",
            "商品名_JP": "Fujifilm QuickSnap Flash 400 Disposable 35mm Camera 27 Exp",
            "Brand": "Fujifilm",
            "Model_Number": "1004126",
            "Condition": "New",
            "Category": "Cameras & Photo > Film Photography > Film Cameras",
            "想定仕入額_JPY": "1500",
            "備考": "Disposable camera."
        }
    ]

    real_urls = [
        "https://jp.mercari.com/item/m61126572832",
        "https://jp.mercari.com/item/m97579951845",
        "https://jp.mercari.com/item/m16631865308",
        "https://jp.mercari.com/item/m46147863763",
        "https://jp.mercari.com/item/m22102102495",
        "https://jp.mercari.com/item/m19720844735",
        "https://jp.mercari.com/item/m10660684954",
        "https://jp.mercari.com/item/m31380758159",
        "https://jp.mercari.com/item/m53171841093",
        "https://jp.mercari.com/item/m80474522380"
    ]
    real_images = [
        "https://static.mercdn.net/item/detail/orig/photos/m61126572832_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m97579951845_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m16631865308_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m46147863763_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m22102102495_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m19720844735_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m10660684954_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m31380758159_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m53171841093_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m80474522380_1.jpg"
    ]

    rows_to_insert = []
    for i, item in enumerate(demo_items):
        row = [''] * len(headers)
        row[headers.index('Listing_Status')] = 'pending_ai'
        
        item['管理ID_SKU'] = item['SKU']
        item['仕入URL'] = real_urls[i % len(real_urls)]
        item['画像URLs'] = real_images[i % len(real_images)]
        item['販売形式'] = 'Buy It Now'
        item['出品価格_USD'] = '999.00'
        item['担当者'] = 'DemoStaff'
        item['在庫_Quantity'] = '0'
        item['Shipping_Policy'] = 'DDP(101～200USD)Expedited'
        item['Return_Policy'] = 'Returns Accepted'
        item['Item_Condition'] = item['Condition']
        item['状態'] = item['Condition']

        for key, val in item.items():
            if key in headers:
                row[headers.index(key)] = str(val)
        rows_to_insert.append(row)

    print(f"Inserting {len(rows_to_insert)} items...")
    range_name = f"A2:BC{1 + len(rows_to_insert)}"
    client.api.write_range(client.tabs['listings'], range_name, rows_to_insert)
    print("Done!")

if __name__ == "__main__":
    insert_phase4_only()
