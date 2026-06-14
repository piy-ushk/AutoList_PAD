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

    def _execute_request(self, req):
        import time
        max_retries = 5
        delay = 2
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req) as response:
                    return response.read()
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise e

    def read_range(self, tab_name, range_spec):
        import urllib.parse
        range_name = f"'{tab_name}'!{range_spec}"
        url = f"{self.base_url}/{self.spreadsheet_id}/values/{urllib.parse.quote(range_name)}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        req = urllib.request.Request(url, headers=headers)
        res_data = self._execute_request(req)
        data = json.loads(res_data.decode("utf-8"))
        return data.get("values", [])

    def write_range(self, tab_name, range_spec, data):
        import urllib.parse
        range_name = f"'{tab_name}'!{range_spec}"
        url = f"{self.base_url}/{self.spreadsheet_id}/values/{urllib.parse.quote(range_name)}?valueInputOption=USER_ENTERED"
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        body = json.dumps({"range": range_name, "majorDimension": "ROWS", "values": data})
        req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers, method="PUT")
        res_data = self._execute_request(req)
        return json.loads(res_data.decode("utf-8"))

    def append_range(self, tab_name, range_spec, data):
        import urllib.parse
        range_name = f"'{tab_name}'!{range_spec}"
        url = f"{self.base_url}/{self.spreadsheet_id}/values/{urllib.parse.quote(range_name)}:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS"
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        body = json.dumps({"range": range_name, "majorDimension": "ROWS", "values": data})
        req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers, method="POST")
        res_data = self._execute_request(req)
        return json.loads(res_data.decode("utf-8"))

    def batch_write_ranges(self, data_list):
        url = f"{self.base_url}/{self.spreadsheet_id}/values:batchUpdate"
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        body = json.dumps({"valueInputOption": "USER_ENTERED", "data": data_list})
        req = urllib.request.Request(url, data=body.encode("utf-8"), headers=headers, method="POST")
        res_data = self._execute_request(req)
        return json.loads(res_data.decode("utf-8"))


class GoogleSheetsClient:
    def __init__(self):
        self.config = load_sheet_config()
        self.tabs = self.config["tabs"]
        try:
            api_config = load_api_config()
            self.spreadsheet_id = api_config.get("google", {}).get("spreadsheet_id", "")
            if not self.spreadsheet_id or self.spreadsheet_id.strip() == "YOUR_SPREADSHEET_ID":
                self.spreadsheet_id = self.config.get("spreadsheet_id", "")
        except Exception:
            api_config = {}
            self.spreadsheet_id = self.config.get("spreadsheet_id", "")

        try:
            token = api_config.get("google", {}).get("access_token", "")
            if not token or not token.strip() or "token" in token.lower():
                key_file = api_config.get("google", {}).get("service_account_key_file", "")
                if key_file:
                    proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    full_path = key_file if os.path.isabs(key_file) else os.path.join(proj_root, key_file)
                    if os.path.exists(full_path):
                        from google.oauth2 import service_account
                        from google.auth.transport.requests import Request
                        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                        creds = service_account.Credentials.from_service_account_file(full_path, scopes=scopes)
                        creds.refresh(Request())
                        token = creds.token
            self.access_token = token
        except Exception as e:
            print(f"Error loading service account access token: {e}")
            self.access_token = ""
        self.api = SheetAPI(self.spreadsheet_id, self.access_token)

    def get_all_rows(self):
        tab = self.tabs["listings"]
        values = self.api.read_range(tab, "A:BC")
        if not values or len(values) < 2:
            return []
        
        col_map = self.config["column_mapping"]
        rows = []
        for row_idx, row in enumerate(values[1:], start=1):
            row_data = {}
            # Iterate through all configured columns
            for i in range(55):  # 55 columns for A to BC
                col_letter = chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))
                field_name = col_map.get(col_letter)
                if field_name:
                    row_data[field_name] = row[i] if i < len(row) else ""
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

    def batch_update_cells(self, sheet_row, updates):
        col_map = self.config["column_mapping"]
        header_map = {v: k for k, v in col_map.items()}
        tab = self.tabs["listings"]
        data_list = []
        for field_name, value in updates:
            sheet_col_letter = header_map.get(field_name)
            if sheet_col_letter:
                range_spec = f"'{tab}'!{sheet_col_letter}{sheet_row}:{sheet_col_letter}{sheet_row}"
                data_list.append({"range": range_spec, "values": [[str(value)]]})
        if not data_list:
            return False
        try:
            self.api.batch_write_ranges(data_list)
            return True
        except Exception:
            return False

    def write_ai_content(self, sheet_row, ai_data):
        updates = [
            ("eBay_Title", ai_data.get("title", "")),
            ("ChatGPT_Title", ai_data.get("title", "")),
            ("ChatGPT_ItemSpecifics", json.dumps(ai_data.get("itemSpecifics", {}), ensure_ascii=False)),
            ("ChatGPT_Description", ai_data.get("description", "")),
            ("ChatGPT_Rarity", ai_data.get("rarity", "")),
            ("ChatGPT_Features", ai_data.get("features", "")),
            ("ChatGPT_Background", ai_data.get("background", "")),
            ("AI_Status", "ai_complete")
        ]
        return self.batch_update_cells(sheet_row, updates)

    def mark_draft_saved(self, sheet_row, item_id, listing_url):
        updates = [
            ("eBay_Item_ID", item_id),
            ("eBay_Listing_URL", listing_url),
            ("Listing_Status", "draft_saved"),
            ("Error_Status", "")
        ]
        return self.batch_update_cells(sheet_row, updates)

    def mark_error(self, sheet_row, error_message, error_field=None):
        updates = [
            ("Listing_Status", "error"),
            ("Error_Status", error_message),
            ("Error_Timestamp", datetime.now(timezone.utc).isoformat())
        ]
        if error_field:
            updates.append(("Error_Field", error_field))
        return self.batch_update_cells(sheet_row, updates)

    def update_validation_status(self, sheet_row, status, flags=None):
        updates = [("Validation_Status", status)]
        if flags:
            updates.append(("VeRO_Flags", ", ".join(flags)))
        return self.batch_update_cells(sheet_row, updates)

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
            values = self.api.read_range(tab, "A:K")
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
                        "Image_PHash": row[10] if len(row) > 10 else "",
                    })
            return entries
        except Exception:
            return []

    def append_duplicate_entry(self, listing):
        tab = self.tabs["duplicate_db"]
        from modules.duplicate_checker import generate_fingerprint
        fp = generate_fingerprint(listing)
        row_data = [
            fp["SKU"],
            fp["Title_Hash"],
            fp["JAN_Code"],
            fp["Model_Number"],
            fp["Brand"],
            fp["Source_URL"],
            fp["Image_Hash"],
            fp["Status"],
            datetime.now(timezone.utc).isoformat(),
            fp["eBay_Item_ID"],
            fp["Image_PHash"],
        ]
        self.api.append_range(tab, "A:K", [row_data])
        return True

    def update_staff_metrics(self, staff_name, is_success, error_type=None):
        if not staff_name:
            return False
        tab = self.tabs.get("staff", "スタッフ管理")
        try:
            values = self.api.read_range(tab, "A:J")
            if not values or len(values) < 2:
                return False
            for i, row in enumerate(values[1:], start=2):
                if len(row) > 1 and row[1].strip() == staff_name.strip():
                    try:
                        today = int(row[6]) if len(row) > 6 and row[6].strip() else 0
                        total = int(row[7]) if len(row) > 7 and row[7].strip() else 0
                        errors = int(row[8]) if len(row) > 8 and row[8].strip() else 0
                    except Exception:
                        today, total, errors = 0, 0, 0
                    if is_success:
                        today += 1
                        total += 1
                    else:
                        errors += 1
                    self.api.write_range(tab, f"G{i}:I{i}", [[str(today), str(total), str(errors)]])
                    return True
        except Exception:
            pass
        return False

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