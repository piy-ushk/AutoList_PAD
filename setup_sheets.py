"""
AutoList - Google Spreadsheet Initializer

Creates the spreadsheet with all required tabs, headers, and default data.
Run once after configuring API keys.

Usage:
    python setup_sheets.py
"""

import json, os, urllib.request, urllib.error

SHEET_TITLE = "AutoList - eBay Listing Management"

TABS = {
    "出品管理表": ["管理ID_SKU", "出品日", "eBayアカウント", "販売形式", "商品名_JP",
                   "eBay_Title", "eBay_Item_ID", "eBay_Listing_URL", "仕入先", "仕入URL",
                   "JAN_Code", "Model_Number", "Brand", "Category", "Condition",
                   "出品価格_USD", "想定仕入額_JPY", "実際仕入額_JPY", "想定送料_JPY", "実送料_JPY",
                   "Shipping_Policy", "Handling_Time", "南米除外", "画像URLs",
                   "ChatGPT_Title", "ChatGPT_Description", "ChatGPT_ItemSpecifics",
                   "ChatGPT_Rarity", "ChatGPT_Features", "ChatGPT_Background",
                   "担当者", "AI_Status", "Validation_Status", "VeRO_Flags", "Listing_Status",
                   "owner_approved", "Rejection_Reason", "Error_Status", "Error_Field",
                   "Error_Timestamp", "売れた日", "購入者ID", "追跡番号", "発送日", "到着確認",
                   "eBay手数料_JPY", "広告費_JPY", "利益_JPY", "利益率", "キャンセル有無",
                   "キャンセル理由", "フィードバック送信", "サンクスレター", "備考"],
    "重複チェックDB": ["SKU", "Title_Hash", "JAN_Code", "Model_Number", "Brand",
                       "Source_URL", "Image_Hash", "Status", "Listed_Date", "eBay_Item_ID"],
    "禁止用語辞書": ["Keyword", "Category", "Match_Type", "Action", "Replacement", "Notes"],
    "エラーログ": ["Timestamp", "SKU", "Error_Type", "Error_Field", "Error_Message",
                   "PAD_Step", "Screenshot_Path", "Resolved", "Resolution_Notes"],
    "スタッフ管理": ["Staff_ID", "Name", "Role", "Email", "eBay_Account",
                    "Active", "Listings_Today", "Listings_Total", "Error_Rate"],
    "シッピングポリシー一覧": ["Template_Name", "Usage_Type", "Price_Range", "Handling_Days",
                           "Shipping_Method", "SA_Exclusion", "Notes"],
}

VERO_SAMPLE = [
    ["Pokémon", "VeRO", "contains", "block", "", "Trademarked franchise"],
    ["Pikachu", "VeRO", "contains", "block", "", "Pokémon character"],
    ["Nintendo", "VeRO", "contains", "block", "", ""],
    ["Disney", "VeRO", "contains", "block", "", ""],
    ["Marvel", "VeRO", "contains", "block", "", ""],
    ["LEGO", "VeRO", "contains", "block", "", ""],
    ["Bandai", "VeRO", "contains", "block", "", ""],
    ["Nike", "VeRO", "contains", "block", "", ""],
    ["Adidas", "VeRO", "contains", "block", "", ""],
    ["Apple", "VeRO", "contains", "block", "", ""],
    ["Sony", "VeRO", "contains", "block", "", ""],
    ["replica", "NG_Word", "contains", "block", "", "Prohibited term"],
    ["fake", "NG_Word", "contains", "block", "", "Prohibited term"],
    ["counterfeit", "NG_Word", "contains", "block", "", "Prohibited term"],
]


def log(message):
    print(f"[SETUP] {message}", flush=True)


def get_access_token():
    config_path = os.path.join(os.path.dirname(__file__), "config", "api_keys.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f).get("google", {}).get("access_token", "")
    except FileNotFoundError:
        return ""


def get_sheet_id():
    config_path = os.path.join(os.path.dirname(__file__), "config", "sheet_config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f).get("spreadsheet_id", "")


def create_spreadsheet():
    base = "https://sheets.googleapis.com/v4/spreadsheets"
    token = get_access_token()
    if not token:
        log("ERROR: No Google access token configured.")
        log("Set up a service account and get the token in config/api_keys.json")
        return ""

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    sheets = [{"properties": {"title": name}} for name in TABS]
    body = json.dumps({"properties": {"title": SHEET_TITLE}, "sheets": sheets}).encode("utf-8")
    req = urllib.request.Request(base, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            sid = result.get("spreadsheetId", "")
            log(f"Created spreadsheet: https://docs.google.com/spreadsheets/d/{sid}")
            return sid
    except urllib.error.HTTPError as e:
        log(f"API error: {e.read().decode()}")
    except Exception as e:
        log(f"Error: {e}")
    return ""


def setup_spreadsheet():
    log("AutoList - Google Spreadsheet Initializer")
    spreadsheet_id = get_sheet_id()
    if not spreadsheet_id or spreadsheet_id == "YOUR_GOOGLE_SHEET_ID_HERE":
        log("No spreadsheet ID in config. Creating...")
        spreadsheet_id = create_spreadsheet()
        if not spreadsheet_id:
            log("Failed to create spreadsheet.")
            return
        log(f"Update config/sheet_config.json with id: {spreadsheet_id}")

    base = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values"
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for tab_name, cols in TABS.items():
        if tab_name == "禁止用語辞書":
            data = [cols] + VERO_SAMPLE
        else:
            data = [cols]
        range_spec = f"A1:{chr(64 + len(cols))}{len(data)}"
        url = f"{base}/'{tab_name}'!{range_spec}?valueInputOption=USER_ENTERED"
        body = json.dumps({"range": f"'{tab_name}'!{range_spec}", "majorDimension": "ROWS", "values": data}).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers, method="PUT")
        try:
            with urllib.request.urlopen(req) as resp:
                r = json.loads(resp.read().decode("utf-8"))
                log(f"  {tab_name}: {r.get('updatedCells', 0)} cells written")
        except urllib.error.HTTPError as e:
            log(f"  {tab_name}: FAILED - {e.read().decode()}")
        except Exception as e:
            log(f"  {tab_name}: FAILED - {e}")

    log("")
    log("Setup complete. Next steps:")
    log("  1. Add full VeRO dictionary from パテントロール用語集_VERO資料.xlsx")
    log("  2. Add shipping policies to シッピングポリシー一覧")
    log("  3. Add staff to スタッフ管理")
    log("  4. Run: python main.py")


if __name__ == "__main__":
    setup_spreadsheet()