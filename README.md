# AutoList — eBay Listing Automation System Setup Instructions

## Requirements

- Windows PC
- Python 3.9 or higher (if not installed, download from https://www.python.org/downloads/)
- OpenAI API key (to use ChatGPT. Create one at https://platform.openai.com/api-keys)
- Google account (Gmail is fine)

---

## Step 1: Create api_keys.json

Copy `config/api_keys.json.template` and rename it to `config/api_keys.json`.

**Via Command Prompt / PowerShell:**
```bash
cd AutoList_PAD
copy config\api_keys.json.template config\api_keys.json
```

**Via File Explorer:**
Open the `config` folder, right-click `api_keys.json.template` -> Copy -> Right-click -> Paste -> Rename to `api_keys.json`.

Next, open `config/api_keys.json` with Notepad or an editor, and configure the following:

```json
{
  "openai": {
    "api_key": "sk-insert-your-actual-OpenAI-API-key-here",
    "model": "gpt-4o"
  },
  "google": {
    "access_token": "(Leave blank for now. Used in Step 4)"
  }
}
```

---

## Step 2: Set up Google Sheets

### 2-a. Create a Service Account in Google Cloud (One-time setup)

1. Go to https://console.cloud.google.com
2. Click the project selector in the top-left -> "New Project" -> Enter a project name and click create.
3. Go to "APIs & Services" -> "Library" -> Search for "Google Sheets API" and enable it.
4. Go to "Credentials" -> click "+ Create Credentials" -> Select "Service Account".
   - Name: `autolist` (or any name you prefer)
   - Role: "Editor"
   - Click "Done".
5. Click on the newly created service account -> Go to the "Keys" tab -> Click "Add Key" -> "Create new key" -> Select "JSON".
   - A JSON file will download automatically. Create a folder named `AutoList_PAD/credentials/` and save it there.
6. Open the downloaded JSON file, and edit `config/api_keys.json` to configure the key file path:

```json
{
  "openai": {
    "api_key": "sk-your-openai-key",
    "model": "gpt-4o"
  },
  "google": {
    "service_account_key_file": "credentials/your-downloaded-filename.json",
    "access_token": "(Leave blank)"
  }
}
```

### 2-b. Automatically Create the Google Sheet

```bash
python setup_sheets.py
```

If successful, you will see a message like this:
```
[SETUP] Created spreadsheet: https://docs.google.com/spreadsheets/d/1abc123def456...
[SETUP]   出品管理表: 55 cells written
[SETUP]   重複チェックDB: 10 cells written
...
```

The spreadsheet ID will be automatically written to `config/sheet_config.json`.

**If you encounter an error:**
- `[SETUP] ERROR: No Google access token configured.` -> Verify if you enabled the Google Sheets API in your Google Cloud Project.
- Alternatively, you can use the Service Account JSON method above, or create the spreadsheet manually:
  1. Create a new Google Sheet.
  2. Copy the spreadsheet ID (the long string of characters `XXXXXXXXX` in the URL: `https://docs.google.com/spreadsheets/d/XXXXXXXXX/edit`).
  3. Paste it into the `"spreadsheet_id"` field in `config/sheet_config.json`.
  4. Manually add the sheet tabs and column headers (refer to Section 5 of prompt.md).

### 2-c. Configure Spreadsheet Permissions

Open the created spreadsheet, click "Share" in the top-right -> Add the service account email address (looks like `autolist@XXXX.iam.gserviceaccount.com`) -> Set permission to "Editor".

---

## Step 3: Enter Listing Data

Open the "出品管理表" (Listing Management) tab in the Google Sheet. The headers in the first row are automatically filled.
Enter your product data starting from the second row.

**Minimum Required Columns:**

| Column | Column Name | Input Example | Description |
|---|---|---|---|
| A | 管理ID_SKU | `2026-06-01-1500` | Unique management ID (recommended: date-price) |
| E | 商品名_JP | `ポケモンカード リザードンVMAX` | Product name in Japanese |
| J | 仕入URL | `https://jp.mercari.com/item/...` | Sourcing URL such as Mercari (Required) |
| N | Category | `Pokemon Cards` | eBay category name |
| O | Condition | `Used` or `New` | Product condition |
| P | 出品価格_USD | `25.00` | Selling price in USD |
| AE | 担当者 | `山田太郎` | The name of the staff member in charge of this item |
| AI | Listing_Status | `pending_ai` | **Must be entered exactly as `pending_ai`** |

Other columns (Brand, JAN_Code, Image URLs, etc.) are optional, but filling them will increase detection accuracy.

---

## Step 4: Run the Script

```bash
python main.py
```

**How to Read the Execution Results:**

```
[2026-06-01 10:00:00] ============================================================
[2026-06-01 10:00:00] AutoList - eBay Listing Automation System
[2026-06-01 10:00:00] Step 1/5: Connecting to Google Sheets...
[2026-06-01 10:00:00]   Connected.
[2026-06-01 10:00:00] Step 2/5: Loading VeRO keyword dictionary...
[2026-06-01 10:00:00]   Loaded 52 keywords.
[2026-06-01 10:00:00] Step 3/5: Processing AI content generation...
[2026-06-01 10:00:00]   Found 2 rows.
[2026-06-01 10:00:00]   [1/2] Generating for SKU: 2026-06-01-1500
[2026-06-01 10:00:00]     OK: AI content generated.
[2026-06-01 10:00:00] Step 5/5: Preparing Monodas draft tasks...
[2026-06-01 10:00:00]   Saved 2 draft tasks to logs\monodas_task_batch.json.
[2026-06-01 10:00:00] Cycle complete.
```

When processing completes:
- The title and description generated by ChatGPT will be written to columns Y to AD of the spreadsheet.
- The `AI_Status` column will change to `ai_complete`.
- After verification, `Validation_Status` will change to `validated`.
- Data to be sent to Monodas will be saved to `logs/monodas_task_batch.json` (to be loaded by PAD to save drafts).

---

## Troubleshooting

**`OPENAI_API_KEY not configured` error occurs:**
-> Check if the correct API key is set in `api_key` under `config/api_keys.json`.

**`spreadsheet_id` is not set:**
-> Open `config/sheet_config.json` and make sure the actual spreadsheet ID is entered in `spreadsheet_id`.

**Rows are not being processed:**
-> Check if the `Listing_Status` in column `AI` of the spreadsheet is set to `pending_ai`.
-> Check if a name is entered in the `担当者` (Assignee/Staff) column (column `AE`).

---

## Overall Workflow

```
① Staff enters product data into the spreadsheet (Listing_Status = pending_ai)
② Run `python main.py`
③ → ChatGPT API automatically generates titles and descriptions
④ → Checks for VeRO prohibited keywords (stops if any are found)
⑤ → Checks for duplicate listings (stops if a duplicate is found)
⑥ → Outputs to logs/monodas_task_batch.json if all checks pass
⑦ Power Automate Desktop reads this JSON and saves drafts in Monodas
⑧ Run `python sync_results.py` (or `2_run_sync_results.bat`) to update the spreadsheet with eBay IDs and clear logs
⑨ Administrator checks and approves the drafts in eBay Seller Hub
⑩ After publishing, Monodas automatically monitors stock, prices, and handles auto-termination
```