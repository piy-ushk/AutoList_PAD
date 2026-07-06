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
        # From Phase 4
        {
            "SKU": "TEST-DEMO-0",
            "商品名_JP": "Tamiya 1/12 Scale Tyrrell P34 Six Wheeler Vintage Plastic Model Kit Unassembled",
            "Brand": "Tamiya",
            "Model_Number": "1/12 Scale",
            "Condition": "New",
            "Category": "Vintage Plastic Model",
            "仕入れ値_JPY": "12000",
            "備考": "Box has slight wear due to age.",
            "仕入URL": "https://jp.mercari.com/item/m61126572832",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m61126572832_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-1",
            "商品名_JP": "Vintage Brand Ultra Seven Sofubi Soft Vinyl Figure Vintage 1970s Japan",
            "Brand": "Vintage Brand",
            "Model_Number": "Ultra Seven",
            "Condition": "Used",
            "Category": "Vintage Toy",
            "仕入れ値_JPY": "35000",
            "備考": "Paint fading on the boots and gloves.",
            "仕入URL": "https://jp.mercari.com/item/m97579951845",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m97579951845_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-2",
            "商品名_JP": "Vintage Tin Toy Robot 1960s Japan Wind Up Original Box",
            "Brand": "Unknown",
            "Model_Number": "Does not apply",
            "Condition": "Used",
            "Category": "Toys & Hobbies > Vintage & Antique Toys > Tin > Robots",
            "仕入れ値_JPY": "8000",
            "備考": "Vintage item.",
            "仕入URL": "https://jp.mercari.com/item/m16631865308",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m16631865308_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-3",
            "商品名_JP": "Re Zero Starting Life in Another World Rem Coreful Figure Taito Japan New",
            "Brand": "Taito",
            "Model_Number": "Does not apply",
            "Condition": "New",
            "Category": "Toys & Hobbies > Action Figures & Accessories > Action Figures",
            "仕入れ値_JPY": "12000",
            "備考": "New item.",
            "仕入URL": "https://jp.mercari.com/item/m32979305678",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m32979305678_1.jpg"
        },
        # Updated ones from insert_3_demos
        {
            "SKU": "TEST-DEMO-4",
            "商品名_JP": "Pokemon Card Pikachu Promo 001/S-P Full Art Holo Mint",
            "Brand": "Nintendo",
            "Model_Number": "Does not apply",
            "Condition": "Used",
            "Category": "Toys & Hobbies > Collectible Card Games > CCG Individual Cards",
            "仕入れ値_JPY": "5000",
            "備考": "Collector item.",
            "仕入URL": "https://jp.mercari.com/item/m72293528805",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m72293528805_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-5",
            "商品名_JP": "Pentax K-70 Digital SLR Camera Body Black Tested",
            "Brand": "Pentax",
            "Model_Number": "K-70",
            "Condition": "Used",
            "Category": "Cameras & Photo > Digital Cameras",
            "仕入れ値_JPY": "80000",
            "備考": "Working perfectly.",
            "仕入URL": "https://jp.mercari.com/item/m59123840515",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m59123840515_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-6",
            "商品名_JP": "Sigma 18-35mm f/1.8 DC HSM Art Lens for Nikon Mount",
            "Brand": "Sigma",
            "Model_Number": "Does not apply",
            "Condition": "Used",
            "Category": "Cameras & Photo > Lenses & Filters > Lenses",
            "仕入れ値_JPY": "25000",
            "備考": "Excellent lens.",
            "仕入URL": "https://jp.mercari.com/item/m93472250105",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m93472250105_1.jpg"
        },
        # Remaining Phase 4
        {
            "SKU": "TEST-DEMO-7",
            "商品名_JP": "Nikon Coolpix S210 Digital Compact Camera Black Tested",
            "Brand": "Nikon",
            "Model_Number": "Coolpix S210",
            "Condition": "Used",
            "Category": "Cameras & Photo > Digital Cameras",
            "仕入れ値_JPY": "5000",
            "備考": "Compact camera.",
            "仕入URL": "https://jp.mercari.com/item/m91052090495",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m91052090495_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-8",
            "商品名_JP": "Nikon 1 J1 Mirrorless Digital Camera Body Black Tested",
            "Brand": "Nikon",
            "Model_Number": "J1",
            "Condition": "Used",
            "Category": "Cameras & Photo > Digital Cameras",
            "仕入れ値_JPY": "10000",
            "備考": "Mirrorless body.",
            "仕入URL": "https://jp.mercari.com/item/m16035508401",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m16035508401_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-9",
            "商品名_JP": "Kodak FunSaver 35mm Single Use Camera 27 Exp",
            "Brand": "Kodak",
            "Model_Number": "Does not apply",
            "Condition": "New",
            "Category": "Cameras & Photo > Film Photography > Film Cameras",
            "仕入れ値_JPY": "1500",
            "備考": "Disposable camera.",
            "仕入URL": "https://jp.mercari.com/item/m31235321067",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m31235321067_1.jpg"
        },
        # From insert_all_genres_demo.py
        {
            "SKU": "TEST-DEMO-10",
            "商品名_JP": "Yokomo YD-2Z RWD Drift Car Chassis Kit 1/10 RC Radio Control",
            "Brand": "Yokomo",
            "Model_Number": "YD-2Z",
            "Condition": "New",
            "Category": "RC Related",
            "仕入れ値_JPY": "25000",
            "備考": "Unassembled kit.",
            "仕入URL": "https://jp.mercari.com/item/m38644870547",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m38644870547_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-11",
            "商品名_JP": "Nintendo Super Famicom Console Boxed CIB Tested Working SFC",
            "Brand": "Nintendo",
            "Model_Number": "SHVC-001",
            "Condition": "Used",
            "Category": "Game Related",
            "仕入れ値_JPY": "8000",
            "備考": "Console is yellowed due to age.",
            "仕入URL": "https://jp.mercari.com/item/m80279095083",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m80279095083_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-12",
            "商品名_JP": "Vintage Alice in Wonderland Japanese 3D Picture Book 1980s",
            "Brand": "N/A",
            "Model_Number": "N/A",
            "Condition": "Used",
            "Category": "Picture Book",
            "仕入れ値_JPY": "4500",
            "備考": "Some pop-up mechanics are slightly bent.",
            "仕入URL": "https://jp.mercari.com/item/m55203513386",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m55203513386_1.jpg"
        },
        {
            "SKU": "TEST-DEMO-13",
            "商品名_JP": "アンパンマン ホームシアター",
            "Brand": "Bandai",
            "Model_Number": "Anpanman Theater",
            "Condition": "Used",
            "Category": "Animation Merch",
            "仕入れ値_JPY": "5000",
            "備考": "Works perfectly.",
            "仕入URL": "https://jp.mercari.com/item/m42074830308",
            "画像URLs": "https://static.mercdn.net/item/detail/orig/photos/m42074830308_1.jpg"
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
