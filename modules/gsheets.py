import json, os, urllib.request, urllib.error
from datetime import datetime, timezone


def load_sheet_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "sheet_config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_api_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "api_keys.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"google": {"access_token": "", "spreadsheet_id": ""}}


class SheetAPI:
    def __init__(self, spreadsheet_id, access_token):
        self.base_url = "https://sheets.googleapis.com/v4/spreadsheets"
        self.spreadsheet_id = spreadsheet_id
        self.access_token = access_token

    def read_range(self, tab_name, range_spec):
        range_name = f"'{tab_name}'!{range_spec}"
        url = f"{self.base_url}/{self.spreadsheet_id}/values/{range_name}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("values", [])

    def write_range(self, tab_name, range_spec, data):
        range_name = f"'{tab_name}'!{range_spec}"
        url = f"{self.base_url}/{self.spreadsheet_id}/values/{range_name}?valueInputOption=USER_ENTERED"
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        body = json.dumps({"range": range_name, "majorDimension": "ROWS", "values": data})
        req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers, method="PUT")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))

    def append_range(self, tab_name, range_spec, data):
        range_name = f"'{tab_name}'!{range_spec}"
        url = f"{self.base_url}/{self.spreadsheet_id}/values/{range_name}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS"
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        body = json.dumps({"range": range_name, "majorDimension": "ROWS", "values": data})
        req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))


class GoogleSheetsClient:
    def __init__(self):
        self.config = load_sheet_config()
        self.spreadsheet_id = self.config["spreadsheet_id"]
        self.tabs = self.config["tabs"]
        try:
            api_config = load_api_config()
            self.access_token = api_config.get("google", {}).get("access_token", "")
        except (FileNotFoundError, json.JSONDecodeError):
            self.access_token = ""
        self.api = SheetAPI(self.spreadsheet_id, self.access_token)

    def get_all_rows(self):
        tab = self.tabs["listings"]
        values = self.api.read_range(tab, "A:BB")
        if not values or len(values) < 2:
            return []
        headers = [h.strip() for h in values[0]]
        rows = []
        for row_idx, row in enumerate(values[1:], start=1):
            row_data = {}
            for col_idx, header in enumerate(headers):
                row_data[header] = row[col_idx] if col_idx < len(row) else ""
            row_data["_sheet_row"] = row_idx + 1
            rows.append(row_data)
        return rows

    def get_pending_ai_rows(self):
        rows = self.get_all_rows()
        return [r for r in rows if r.get("Listing_Status", "").strip() == "pending_ai"]

    def get_ai_complete_rows(self):
        rows = self.get_all_rows()
        return [r for r in rows if r.get("AI_Status", "").strip() == "ai_complete"]

    def get_validated_rows(self):
        rows = self.get_all_rows()
        return [r for r in rows if r.get("Validation_Status", "").strip() == "validated"]

    def get_draft_saved_rows(self):
        rows = self.get_all_rows()
        return [r for r in rows if r.get("Listing_Status", "").strip() == "draft_saved"]

    def get_approved_rows(self):
        rows = self.get_all_rows()
        return [r for r in rows if r.get("Listing_Status", "").strip() == "draft_saved" and r.get("owner_approved", "").strip().upper() == "YES"]

    def update_cell(self, sheet_row, field_name, value):
        col_map = self.config["column_mapping"]
        header_map = {v: k for k, v in col_map.items()}
        sheet_col_letter = header_map.get(field_name)
        if not sheet_col_letter:
            return False
        tab = self.tabs["listings"]
        range_spec = f"{sheet_col_letter}{sheet_row}:{sheet_col_letter}{sheet_row}"
        try:
            self.api.write_range(tab, range_spec, [[str(value)]])
            return True
        except Exception:
            return False

    def write_ai_content(self, sheet_row, ai_data):
        fields = [
            ("ChatGPT_Title", ai_data.get("title", "")),
            ("ChatGPT_ItemSpecifics", json.dumps(ai_data.get("itemSpecifics", {}), ensure_ascii=False)),
            ("ChatGPT_Description", ai_data.get("description", "")),
            ("ChatGPT_Rarity", ai_data.get("rarity", "")),
            ("ChatGPT_Features", ai_data.get("features", "")),
            ("ChatGPT_Background", ai_data.get("background", "")),
        ]
        for field_name, value in fields:
            self.update_cell(sheet_row, field_name, value)
        self.update_cell(sheet_row, "AI_Status", "ai_complete")
        return True

    def mark_draft_saved(self, sheet_row, item_id, listing_url):
        self.update_cell(sheet_row, "eBay_Item_ID", item_id)
        self.update_cell(sheet_row, "eBay_Listing_URL", listing_url)
        self.update_cell(sheet_row, "Listing_Status", "draft_saved")
        self.update_cell(sheet_row, "Error_Status", "")
        return True

    def mark_error(self, sheet_row, error_message, error_field=None):
        self.update_cell(sheet_row, "Listing_Status", "error")
        self.update_cell(sheet_row, "Error_Status", error_message)
        self.update_cell(sheet_row, "Error_Timestamp", datetime.now(timezone.utc).isoformat())
        if error_field:
            self.update_cell(sheet_row, "Error_Field", error_field)
        return True

    def update_validation_status(self, sheet_row, status, flags=None):
        self.update_cell(sheet_row, "Validation_Status", status)
        if flags:
            self.update_cell(sheet_row, "VeRO_Flags", ", ".join(flags))
        return True

    def update_listing_status(self, sheet_row, status):
        self.update_cell(sheet_row, "Listing_Status", status)
        return True

    def get_vero_keywords(self):
        tab = self.tabs["vero_dict"]
        try:
            values = self.api.read_range(tab, "A:F")
            if not values or len(values) < 2:
                return []
            keywords = []
            for row in values[1:]:
                if len(row) >= 4 and row[0].strip():
                    keywords.append({
                        "keyword": row[0].strip(),
                        "category": row[1].strip() if len(row) > 1 else "VeRO",
                        "match_type": row[2].strip() if len(row) > 2 else "contains",
                        "action": row[3].strip() if len(row) > 3 else "block",
                        "replacement": row[4].strip() if len(row) > 4 else "",
                        "notes": row[5].strip() if len(row) > 5 else "",
                    })
            return keywords
        except Exception:
            return []

    def get_duplicate_db_entries(self):
        tab = self.tabs["duplicate_db"]
        try:
            values = self.api.read_range(tab, "A:J")
            if not values or len(values) < 2:
                return []
            entries = []
            for row in values[1:]:
                if len(row) >= 1:
                    entries.append({
                        "SKU": row[0] if len(row) > 0 else "",
                        "Title_Hash": row[1] if len(row) > 1 else "",
                        "JAN_Code": row[2] if len(row) > 2 else "",
                        "Model_Number": row[3] if len(row) > 3 else "",
                        "Brand": row[4] if len(row) > 4 else "",
                        "Source_URL": row[5] if len(row) > 5 else "",
                        "Image_Hash": row[6] if len(row) > 6 else "",
                        "Status": row[7] if len(row) > 7 else "",
                        "Listed_Date": row[8] if len(row) > 8 else "",
                        "eBay_Item_ID": row[9] if len(row) > 9 else "",
                    })
            return entries
        except Exception:
            return []

    def append_duplicate_entry(self, listing):
        tab = self.tabs["duplicate_db"]
        row_data = [
            listing.get("管理ID_SKU", listing.get("SKU", "")),
            listing.get("Title_Hash", ""),
            listing.get("JAN_Code", ""),
            listing.get("Model_Number", ""),
            listing.get("Brand", ""),
            listing.get("仕入URL", listing.get("Source_URL", "")),
            listing.get("Image_Hash", ""),
            "active",
            datetime.now(timezone.utc).isoformat(),
            listing.get("eBay_Item_ID", ""),
        ]
        self.api.append_range(tab, "A:J", [row_data])
        return True

    def log_error(self, sku, error_type, error_field, error_message, pad_step, screenshot_path=""):
        tab = self.tabs["error_log"]
        row_data = [
            datetime.now(timezone.utc).isoformat(),
            sku, error_type, error_field, error_message, pad_step, screenshot_path, "NO", "",
        ]
        self.api.append_range(tab, "A:I", [row_data])
        return True

    def get_staff_list(self):
        tab = self.tabs["staff"]
        try:
            values = self.api.read_range(tab, "A:I")
            if not values or len(values) < 2:
                return []
            staff = []
            for row in values[1:]:
                if len(row) >= 6:
                    staff.append({
                        "Staff_ID": row[0] if len(row) > 0 else "",
                        "Name": row[1] if len(row) > 1 else "",
                        "Role": row[2] if len(row) > 2 else "",
                        "Email": row[3] if len(row) > 3 else "",
                        "eBay_Account": row[4] if len(row) > 4 else "",
                        "Active": row[5] if len(row) > 5 else "",
                    })
            return staff
        except Exception:
            return []

    def get_shipping_policies(self):
        tab = self.tabs["shipping"]
        try:
            values = self.api.read_range(tab, "A:G")
            if not values or len(values) < 2:
                return []
            policies = []
            for row in values[1:]:
                if len(row) >= 5:
                    policies.append({
                        "Template_Name": row[0] if len(row) > 0 else "",
                        "Usage_Type": row[1] if len(row) > 1 else "",
                        "Price_Range": row[2] if len(row) > 2 else "",
                        "Handling_Days": row[3] if len(row) > 3 else "",
                        "Shipping_Method": row[4] if len(row) > 4 else "",
                        "SA_Exclusion": row[5] if len(row) > 5 else "NO",
                        "Notes": row[6] if len(row) > 6 else "",
                    })
            return policies
        except Exception:
            return []