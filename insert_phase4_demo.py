import sys
import os

from modules.gsheets import GoogleSheetsClient

def insert_8_new_items():
    print("Connecting to Google Sheets...")
    client = GoogleSheetsClient()
    
    # 8 new items
    demo_items = [
        {
            "商品名_JP": "Vintage Tin Toy Robot 1960s Japan Wind Up Original Box",
            "Brand": "Unknown",
            "MPN": "Does not apply",
            "Item_Category": "Toys & Hobbies > Vintage & Antique Toys > Tin > Robots"
        },
        {
            "商品名_JP": "Hatsune Miku 1/7 Scale Figure Miku Symphony 2019 Ver.",
            "Brand": "Good Smile Company",
            "MPN": "4580416942639",
            "Item_Category": "Toys & Hobbies > Action Figures & Accessories > Action Figures"
        },
        {
            "商品名_JP": "Pokemon Card Pikachu Promo 001/S-P Full Art Holo Mint",
            "Brand": "Nintendo",
            "MPN": "Does not apply",
            "Item_Category": "Toys & Hobbies > Collectible Card Games > CCG Individual Cards"
        },
        {
            "商品名_JP": "Canon EOS 5D Mark IV DSLR Camera Body Only Tested Japan",
            "Brand": "Canon",
            "MPN": "1483C002",
            "Item_Category": "Cameras & Photo > Digital Cameras"
        },
        {
            "商品名_JP": "Canon EF 50mm f/1.4 USM Standard Prime Lens Near Mint",
            "Brand": "Canon",
            "MPN": "2515A003",
            "Item_Category": "Cameras & Photo > Lenses & Filters > Lenses"
        },
        {
            "商品名_JP": "Sony Cyber-shot DSC-RX100 VII Digital Camera Black",
            "Brand": "Sony",
            "MPN": "DSCRX100M7/B",
            "Item_Category": "Cameras & Photo > Digital Cameras"
        },
        {
            "商品名_JP": "Sony Alpha a7 III Mirrorless Digital Camera Body ILCE-7M3",
            "Brand": "Sony",
            "MPN": "ILCE-7M3",
            "Item_Category": "Cameras & Photo > Digital Cameras"
        },
        {
            "商品名_JP": "Fujifilm QuickSnap Flash 400 Disposable 35mm Camera 27 Exp",
            "Brand": "Fujifilm",
            "MPN": "1004126",
            "Item_Category": "Cameras & Photo > Film Photography > Film Cameras"
        }
    ]

    real_urls = [
        "https://i.ebayimg.com/images/g/HroAAOSwg1ZmfN31/s-l1600.jpg",
        "https://i.ebayimg.com/images/g/Jm0AAOSwfS1mfN3w/s-l1600.jpg",
        "https://i.ebayimg.com/images/g/QGoAAOSwb8BmfN3t/s-l1600.jpg"
    ]

    print("Clearing existing sheet data...")
    try:
        client.sheet.worksheet("Test_Inputs").clear()
        headers = ["SKU", "eBay_Title", "商品名_JP", "Brand", "MPN", "Item_Category", "Image_URLs", "ChatGPT_Title", "ChatGPT_Description", "Validation_Status", "Validation_Errors", "Staff_Name", "Date_Listed"]
        client.sheet.worksheet("Test_Inputs").append_row(headers)
    except Exception as e:
        print(f"Error clearing sheet: {e}")

    print("Inserting 8 new items...")
    
    for i, item in enumerate(demo_items):
        sku = f"TEST-DEMO-{i+6}" # Start from 6 so it matches the mock json keys TEST-DEMO-6 to 13
        
        row_data = [
            sku,
            item["商品名_JP"], # English title for test
            item["商品名_JP"],
            item["Brand"],
            item["MPN"],
            item["Item_Category"],
            "|".join(real_urls),
            "", "", "", "",
            "Taro (Demo)",
            "2026/07/04"
        ]
        
        client.sheet.worksheet("Test_Inputs").append_row(row_data)

    print("Done!")

if __name__ == "__main__":
    insert_8_new_items()
