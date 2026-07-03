import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.gsheets import GoogleSheetsClient

def insert_all_genres_demo_data():
    client = GoogleSheetsClient()
    
    # We will clear the existing rows to just generate these new 6 rows
    print("Clearing existing sheet data...")
    client.api.write_range(client.tabs['listings'], 'A2:BC1000', [[''] * 55 for _ in range(999)])
    
    headers = client.api.read_range(client.tabs['listings'], 'A1:BC1')[0]
    
    demo_items = [
        {
            "商品名_JP": "Tamiya 1/12 Scale Tyrrell P34 Six Wheeler Vintage Plastic Model Kit Unassembled",
            "Brand": "Tamiya",
            "Model_Number": "1/12 Scale",
            "Condition": "New",
            "Category": "Vintage Plastic Model",
            "想定仕入額_JPY": "12000",
            "備考": "Box has slight wear due to age, but all parts are sealed in original plastic bags. Includes original decals."
        },
        {
            "商品名_JP": "Vintage Brand Ultra Seven Sofubi Soft Vinyl Figure Vintage 1970s Japan",
            "Brand": "Vintage Brand",
            "Model_Number": "Ultra Seven",
            "Condition": "Used",
            "Category": "Vintage Toy",
            "想定仕入額_JPY": "35000",
            "備考": "Paint fading on the boots and gloves. No cracks. Rare early production mold with silver paint variations."
        },
        {
            "商品名_JP": "Yokomo YD-2Z RWD Drift Car Chassis Kit 1/10 RC Radio Control",
            "Brand": "Yokomo",
            "Model_Number": "YD-2Z",
            "Condition": "New",
            "Category": "RC Related",
            "想定仕入額_JPY": "25000",
            "備考": "Unassembled kit. Does not include electronics or body."
        },
        {
            "商品名_JP": "Nintendo Super Famicom Console Boxed CIB Tested Working SFC",
            "Brand": "Nintendo",
            "Model_Number": "SHVC-001",
            "Condition": "Used",
            "Category": "Game Related",
            "想定仕入額_JPY": "8000",
            "備考": "Console is yellowed due to age. Includes 2 controllers, AC adapter, and AV cable. Original box has some corner damage."
        },
        {
            "商品名_JP": "Vintage Alice in Wonderland Japanese 3D Picture Book 1980s",
            "Brand": "N/A",
            "Model_Number": "N/A",
            "Condition": "Used",
            "Category": "Picture Book",
            "想定仕入額_JPY": "4500",
            "備考": "Some pop-up mechanics are slightly bent but fully functional. No torn pages. Japanese text."
        },
        {
            "商品名_JP": "おやこでいっしょにアンパンマンシアター",
            "Brand": "Bandai",
            "Model_Number": "Anpanman Theater",
            "Condition": "Used",
            "Category": "Animation Merch",
            "想定仕入額_JPY": "5000",
            "備考": "Works perfectly. Slight scratches on the body but does not affect projection."
        },
        {
            "商品名_JP": "ポケモンカード ピカチュウ プロモ",
            "Brand": "Nintendo",
            "Model_Number": "Pikachu Promo",
            "Condition": "Used",
            "Category": "Pokemon Cards",
            "想定仕入額_JPY": "12000",
            "備考": "Near mint condition. Stored in a protective sleeve."
        },
        {
            "商品名_JP": "Canon EOS 5D Mark IV DSLR Camera Body Only",
            "Brand": "Canon",
            "Model_Number": "EOS 5D Mark IV",
            "Condition": "Used",
            "Category": "Digital Cameras",
            "想定仕入額_JPY": "120000",
            "備考": "Excellent condition. Minimal signs of use. Shutter count around 20,000. Includes battery, charger, and strap."
        },
        {
            "商品名_JP": "初音ミク フィギュア 1/7スケール",
            "Brand": "Good Smile Company",
            "Model_Number": "1/7 Scale",
            "Condition": "New",
            "Category": "Figures",
            "想定仕入額_JPY": "15000",
            "備考": "Brand new in sealed box."
        }
    ]

    real_urls = [
        "https://jp.mercari.com/item/m61126572832",
        "https://jp.mercari.com/item/m97579951845",
        "https://jp.mercari.com/item/m38644870547",
        "https://jp.mercari.com/item/m80279095083",
        "https://jp.mercari.com/item/m55203513386",
        "https://jp.mercari.com/item/m30599064139",
        "https://jp.mercari.com/item/m28494770278",
        "https://jp.mercari.com/item/m91481634727",
        "https://jp.mercari.com/item/m78656521379"
    ]
    real_images = [
        "https://static.mercdn.net/item/detail/orig/photos/m61126572832_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m97579951845_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m38644870547_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m80279095083_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m55203513386_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m30599064139_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m28494770278_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m91481634727_1.jpg",
        "https://static.mercdn.net/item/detail/orig/photos/m78656521379_1.jpg"
    ]

    rows_to_insert = []
    for i, item in enumerate(demo_items):
        row = [''] * len(headers)
        row[headers.index('Listing_Status')] = 'pending_ai'
        
        item['管理ID_SKU'] = f'TEST-DEMO-{i}'
        item['仕入URL'] = real_urls[i]
        item['画像URLs'] = real_images[i]
        item['販売形式'] = 'Buy It Now'
        item['出品価格_USD'] = '150.00'
        item['担当者'] = 'DemoStaff'
        item['在庫_Quantity'] = '0'
        item['Shipping_Policy'] = 'DDP(101～200USD)Expedited'
        item['Return_Policy'] = 'Returns Accepted'

        for key, val in item.items():
            if key in headers:
                row[headers.index(key)] = str(val)
        rows_to_insert.append(row)

    print(f"Inserting {len(rows_to_insert)} items...")
    range_name = f"A2:BC{1 + len(rows_to_insert)}"
    client.api.write_range(client.tabs['listings'], range_name, rows_to_insert)
    print("Done!")

if __name__ == "__main__":
    insert_all_genres_demo_data()
