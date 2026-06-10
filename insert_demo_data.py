import json, os, sys
from datetime import datetime, timezone

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.gsheets import GoogleSheetsClient

def insert_demo_data():
    client = GoogleSheetsClient()
    tab = client.tabs["listings"]
    
    # We will append a row to the end. 
    # Let's map it based on the columns
    col_map = client.config["column_mapping"]
    
    # Define 33 real active Pokemon card listings for testing
    listings = [
        {
            "管理ID_SKU": "PKMN-101",
            "商品名_JP": "メガドラミドロsar",
            "仕入URL": "https://jp.mercari.com/item/m49140879745",
            "出品価格_USD": "45"
        },
        {
            "管理ID_SKU": "PKMN-102",
            "商品名_JP": "ポケモンカード(メガズルズキンex)のSAR",
            "仕入URL": "https://jp.mercari.com/item/m74706408254",
            "出品価格_USD": "60"
        },
        {
            "管理ID_SKU": "PKMN-103",
            "商品名_JP": "ポケモンカード ニャースVMAX プロモ 029/S-P 0065",
            "仕入URL": "https://jp.mercari.com/item/m19660951690",
            "出品価格_USD": "25"
        },
        {
            "管理ID_SKU": "PKMN-104",
            "商品名_JP": "メイのはげまし SR MEGA 拡張パック ムニキスゼロ 107/080",
            "仕入URL": "https://jp.mercari.com/item/m98870121706",
            "出品価格_USD": "80"
        },
        {
            "管理ID_SKU": "PKMN-105",
            "商品名_JP": "ポケモンカード　テツノイバラex RR 100枚 まとめ売り　② 最終値下げ",
            "仕入URL": "https://jp.mercari.com/item/m49241683507",
            "出品価格_USD": "120"
        },
        {
            "管理ID_SKU": "PKMN-106",
            "商品名_JP": "レシラムex SR SV11W ホワイトフレア 160/086",
            "仕入URL": "https://jp.mercari.com/item/m28575759382",
            "出品価格_USD": "35"
        },
        {
            "管理ID_SKU": "PKMN-107",
            "商品名_JP": "ポケモンカードサンダー",
            "仕入URL": "https://jp.mercari.com/item/m59859082962",
            "出品価格_USD": "15"
        },
        {
            "管理ID_SKU": "PKMN-108",
            "商品名_JP": "リザードンEX XYA メガバトルデッキ60 MリザードンEX 001/021",
            "仕入URL": "https://jp.mercari.com/item/m86789948362",
            "出品価格_USD": "110"
        },
        {
            "管理ID_SKU": "PKMN-109",
            "商品名_JP": "ポケモンカード レックウザ 127/193",
            "仕入URL": "https://jp.mercari.com/item/m10942066448",
            "出品価格_USD": "12"
        },
        {
            "管理ID_SKU": "PKMN-110",
            "商品名_JP": "ロケット団のミュウツーex SAR スカーレット&バイオレット 拡張パック ロ…",
            "仕入URL": "https://jp.mercari.com/item/m32049021489",
            "出品価格_USD": "95"
        },
        {
            "管理ID_SKU": "PKMN-111",
            "商品名_JP": "PSA10 ピカチュウVMAX: プロモ P [S-P 265]",
            "仕入URL": "https://jp.mercari.com/item/m67205305005",
            "出品価格_USD": "250"
        },
        {
            "管理ID_SKU": "PKMN-112",
            "商品名_JP": "カスミの元気 SR 108/081 トサキント AR トリデプス AR",
            "仕入URL": "https://jp.mercari.com/item/m73847299723",
            "出品価格_USD": "40"
        },
        {
            "管理ID_SKU": "PKMN-113",
            "商品名_JP": "と*ん様 【新品未開封】ポケモンカード スペシャルBOX フクオカ",
            "仕入URL": "https://jp.mercari.com/item/m60626865040",
            "出品価格_USD": "300"
        },
        {
            "管理ID_SKU": "PKMN-114",
            "商品名_JP": "ポケモンセンター スペシャルBOX 3種セット",
            "仕入URL": "https://jp.mercari.com/item/m91536769958",
            "出品価格_USD": "850"
        },
        {
            "管理ID_SKU": "PKMN-115",
            "商品名_JP": "ポケモンカード カルボウ 010/087 Cエラー品",
            "仕入URL": "https://jp.mercari.com/item/m99588938416",
            "出品価格_USD": "75"
        },
        {
            "管理ID_SKU": "PKMN-116",
            "商品名_JP": "【BOX】 MEGA 拡張パック ムニキスゼロ",
            "仕入URL": "https://jp.mercari.com/item/m63328084822",
            "出品価格_USD": "120"
        },
        {
            "管理ID_SKU": "PKMN-117",
            "商品名_JP": "K*U様 ポケモンカードスカーレット&バイオレットスペシャルＢＯＸポケモンセンタ",
            "仕入URL": "https://jp.mercari.com/item/m64099208433",
            "出品価格_USD": "180"
        },
        {
            "管理ID_SKU": "PKMN-118",
            "商品名_JP": "【最終値下げ】ポケモン ゴールドカード 大量セット",
            "仕入URL": "https://jp.mercari.com/item/m45017716792",
            "出品価格_USD": "90"
        },
        {
            "管理ID_SKU": "PKMN-119",
            "商品名_JP": "【パック】 スカーレット&バイオレット 拡張パック ステラミラクル",
            "仕入URL": "https://jp.mercari.com/item/m35563805007",
            "出品価格_USD": "10"
        },
        {
            "管理ID_SKU": "PKMN-120",
            "商品名_JP": "ポケモンカード メガガルーラex ソウブレイズex 2枚セット",
            "仕入URL": "https://jp.mercari.com/item/m86051157665",
            "出品価格_USD": "15"
        },
        {
            "管理ID_SKU": "PKMN-121",
            "商品名_JP": "ポケモンカード ザルード メガダークライEX 2枚セット",
            "仕入URL": "https://jp.mercari.com/item/m98817547383",
            "出品価格_USD": "15"
        },
        {
            "管理ID_SKU": "PKMN-122",
            "商品名_JP": "ポケモンカード　SV1V 拡張パック　バイオレットex まとめ売り 15枚セット",
            "仕入URL": "https://jp.mercari.com/item/m74650915532",
            "出品価格_USD": "25"
        },
        {
            "管理ID_SKU": "PKMN-123",
            "商品名_JP": "ポケモンカードゲーム スタートデッキ100",
            "仕入URL": "https://jp.mercari.com/item/m98918135060",
            "出品価格_USD": "35"
        },
        {
            "管理ID_SKU": "PKMN-124",
            "商品名_JP": "ぬ*ぬ様 ポケカ　れんげきウーラオス2枚セット",
            "仕入URL": "https://jp.mercari.com/item/m86119012823",
            "出品価格_USD": "12"
        },
        {
            "管理ID_SKU": "PKMN-125",
            "商品名_JP": "「みんなでぼうけん ピカチュウ」プロモ2枚",
            "仕入URL": "https://jp.mercari.com/item/m78246943761",
            "出品価格_USD": "20"
        },
        {
            "管理ID_SKU": "PKMN-126",
            "商品名_JP": "メガゼラオラEX トレーディングカード",
            "仕入URL": "https://jp.mercari.com/item/m98218938574",
            "出品価格_USD": "18"
        },
        {
            "管理ID_SKU": "PKMN-127",
            "商品名_JP": "ポケモンカードゲーム スペシャルBOX ポケモンセンターフクオカ シュリンク付き",
            "仕入URL": "https://jp.mercari.com/item/m86094490146",
            "出品価格_USD": "320"
        },
        {
            "管理ID_SKU": "PKMN-128",
            "商品名_JP": "【BOX】シュリンク付き MEGA ハイクラスパック MEGAドリームex",
            "仕入URL": "https://jp.mercari.com/item/m99719288116",
            "出品価格_USD": "140"
        },
        {
            "管理ID_SKU": "PKMN-129",
            "商品名_JP": "【新品未開封】ポケモンカード「レイジングサーフ」30パック(1BOX分)",
            "仕入URL": "https://jp.mercari.com/item/m74358786718",
            "出品価格_USD": "50"
        },
        {
            "管理ID_SKU": "PKMN-130",
            "商品名_JP": "ソード&シールド Ultra-Premium Collection Chari…",
            "仕入URL": "https://jp.mercari.com/item/m14165263592",
            "出品価格_USD": "220"
        },
        {
            "管理ID_SKU": "PKMN-131",
            "商品名_JP": "ポケモンカード ハイクラスパック MEGAドリームexシュリンク付き BOX",
            "仕入URL": "https://jp.mercari.com/item/m95078456943",
            "出品価格_USD": "130"
        },
        {
            "管理ID_SKU": "PKMN-132",
            "商品名_JP": "モルペコex SAR M 115/081 & メガカイリューex MA",
            "仕入URL": "https://jp.mercari.com/item/m63303881159",
            "出品価格_USD": "55"
        },
        {
            "管理ID_SKU": "PKMN-133",
            "商品名_JP": "ポケモンカード ドラパルトex なかよしポフィン　まとめ売り",
            "仕入URL": "https://jp.mercari.com/item/m37770158938",
            "出品価格_USD": "22"
        }
    ]

    rows_to_insert = []
    for item in listings:
        row_data = [""] * 54
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
            "画像URLs": "https://upload.wikimedia.org/wikipedia/en/a/a6/Pok%C3%A9mon_Pikachu_art.png",
            "担当者": "Test Staff",
            "Listing_Status": "pending_ai"
        }
        
        # map to index
        for i in range(54):
            col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
            field_name = col_map.get(col_letter)
            if field_name in mapping:
                row_data[i] = mapping[field_name]
        rows_to_insert.append(row_data)
            
    try:
        client.api.append_range(tab, "A:BB", rows_to_insert)
        print(f"Successfully inserted {len(rows_to_insert)} real Pokemon card listings into the Google Sheet!")
    except Exception as e:
        print(f"Error inserting real listings: {e}")

if __name__ == "__main__":
    insert_demo_data()
