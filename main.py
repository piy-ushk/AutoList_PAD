import json, os, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.gsheets import GoogleSheetsClient, load_sheet_config
from modules.chatgpt import ChatGPTCaller, validate_ai_output
from modules.vero_checker import run_vero_check, load_keyword_dictionary
from modules.duplicate_checker import check_duplicate, generate_fingerprint
from modules.shipping import select_shipping_policy
from modules.error_handler import ErrorHandler, ErrorCode
from modules.validator import run_all_validations


def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}", flush=True)


def print_banner():
    log("=" * 60)
    log("AutoList - eBay Listing Automation System")
    log("Main Orchestrator v1.0")
    log("=" * 60)


def init_sheets():
    log("Step 1/5: Connecting to Google Sheets...")
    try:
        client = GoogleSheetsClient()
        log("  Connected.")
        return client
    except Exception as e:
        log(f"  FATAL: Cannot connect: {e}")
        sys.exit(1)


def init_vero_dictionary(sheet_client):
    log("Step 2/5: Loading VeRO keyword dictionary...")
    keywords = sheet_client.get_vero_keywords()
    if not keywords:
        log("  WARNING: Could not load from Sheets, falling back to local config.")
        keywords = load_keyword_dictionary()
    log(f"  Loaded {len(keywords)} keywords.")
    return keywords


def process_ai_generation(sheet_client, error_handler):
    log("Step 3/5: Processing AI content generation...")
    rows = sheet_client.get_pending_ai_rows()
    if not rows:
        log("  No rows pending.")
        return

    log(f"  Found {len(rows)} rows.")
    chatgpt = ChatGPTCaller()
    if not chatgpt.api_key or chatgpt.api_key.startswith("sk-YOUR"):
        log("  WARNING: OpenAI API key not configured. Skipping.")
        return

    success, errors = 0, 0
    for i, row in enumerate(rows):
        sku = row.get("管理ID_SKU", f"row_{row['_sheet_row']}")
        sheet_row = row["_sheet_row"]
        log(f"  [{i+1}/{len(rows)}] Generating for SKU: {sku}")
        try:
            output = chatgpt.generate_listing(row)
            if validate_ai_output(output):
                sheet_client.write_ai_content(sheet_row, output)
                success += 1
            else:
                raise ValueError("AI output failed validation")
        except Exception as e:
            error_handler.log_chatgpt_error(sku, str(e))
            sheet_client.update_cell(sheet_row, "AI_Status", "ai_error")
            errors += 1
            log(f"    ERROR: {e}")
        if i < len(rows) - 1:
            time.sleep(2)
    log(f"  Complete: {success} success, {errors} failed.")


import time


def process_validation(sheet_client, error_handler):
    log("Step 4/5: Running validation...")
    rows = sheet_client.get_ai_complete_rows()
    if not rows:
        log("  No rows to validate.")
        return

    log(f"  Found {len(rows)} rows.")
    duplicates = sheet_client.get_duplicate_db_entries()
    vero_kw = sheet_client.get_vero_keywords() or load_keyword_dictionary()
    validated, blocked = 0, 0

    for row in rows:
        sku = row.get("管理ID_SKU", f"row_{row['_sheet_row']}")
        sheet_row = row["_sheet_row"]
        staff_name = row.get("担当者", "")
        log(f"  Validating SKU: {sku}")

        vr = run_all_validations(row)
        if not vr["passed"]:
            sheet_client.update_validation_status(sheet_row, "format_error")
            error_handler.log_error(sku=sku, error_code=ErrorCode.E014, error_message="; ".join(vr["errors"]), pad_step="Validate_Row")
            blocked += 1
            if staff_name: sheet_client.update_staff_metrics(staff_name, is_success=False)
            continue

        title = row.get("ChatGPT_Title", "")
        desc = row.get("ChatGPT_Description", "")
        vero = run_vero_check(title, desc, vero_kw)
        if not vero["passed"]:
            flagged = vero.get("flagged_keywords", [])
            sheet_client.update_validation_status(sheet_row, "vero_flagged", flagged)
            error_handler.log_vero_error(sku, flagged)
            blocked += 1
            if staff_name: sheet_client.update_staff_metrics(staff_name, is_success=False)
            log(f"    BLOCKED: VeRO: {', '.join(flagged)}")
            continue

        dup = check_duplicate(row, duplicates)
        if dup["is_duplicate"]:
            sheet_client.update_validation_status(sheet_row, "duplicate_suspected")
            error_handler.log_duplicate_error(sku, dup["reason"])
            blocked += 1
            if staff_name: sheet_client.update_staff_metrics(staff_name, is_success=False)
            log(f"    BLOCKED: Duplicate: {dup['reason']}")
            continue

        sheet_client.update_validation_status(sheet_row, "validated")
        sheet_client.append_duplicate_entry(row)
        validated += 1
        if staff_name: sheet_client.update_staff_metrics(staff_name, is_success=True)
        log(f"    OK.")
    log(f"  Complete: {validated} passed, {blocked} blocked.")


def process_monodas_drafts(sheet_client):
    log("Step 5/5: Preparing Monodas draft tasks...")
    rows = sheet_client.get_validated_rows()
    if not rows:
        log("  No rows ready.")
        return
    log(f"  Found {len(rows)} rows.")
    tasks = []
    for row in rows:
        policy = select_shipping_policy(
            price_usd=float(row.get("出品価格_USD", 0)),
            handling_days=row.get("Handling_Time", "10日"),
            sa_exclusion=row.get("南米除外", "NO"),
            stock_type="DROP",
        )
        tasks.append({
            "sheet_row": row["_sheet_row"],
            "sku": row.get("管理ID_SKU", ""),
            "title": row.get("ChatGPT_Title", ""),
            "category": row.get("Category", ""),
            "condition": row.get("Condition", ""),
            "price_usd": row.get("出品価格_USD", ""),
            "description": row.get("ChatGPT_Description", ""),
            "source_url": row.get("仕入URL", ""),
            "image_urls": row.get("画像URLs", ""),
            "shipping_policy": policy,
            "handling_time": row.get("Handling_Time", "10日"),
            "item_specifics": row.get("ChatGPT_ItemSpecifics", "{}"),
        })
    path = os.path.join(os.path.dirname(__file__), "logs", "monodas_task_batch.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    log(f"  Saved {len(tasks)} draft tasks to {path}.")
    log("  PAD reads this file to fill Monodas forms (draft only).")


def process_monodas_results(sheet_client):
    log("Step 0/5: Checking for Monodas listing results to sync...")
    path = os.path.join(os.path.dirname(__file__), "logs", "monodas_results.json")
    if not os.path.exists(path):
        log("  No results file found to sync.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        log(f"  ERROR: Could not read results file: {e}")
        return

    # Handle both a single object and a list of objects
    if not isinstance(results, list):
        results = [results]

    log(f"  Found {len(results)} results to sync.")
    success_count = 0
    for res in results:
        sheet_row = res.get("sheet_row")
        item_id = res.get("ebay_item_id")
        if not sheet_row or not item_id:
            continue

        # Construct standard eBay URL
        listing_url = f"https://www.ebay.com/itm/{item_id}"

        try:
            sheet_client.mark_draft_saved(sheet_row, item_id, listing_url)
            success_count += 1
            log(f"    Row {sheet_row} synced: eBay ID {item_id}")
        except Exception as e:
            log(f"    ERROR syncing row {sheet_row}: {e}")

    try:
        os.remove(path)
        log(f"  Sync complete. Processed {success_count} entries. Results file deleted.")
    except Exception as e:
        log(f"  WARNING: Could not delete results file: {e}")


def main():
    print_banner()
    try:
        sheet = init_sheets()
        process_monodas_results(sheet)
        err = ErrorHandler(sheet_logger=sheet)
        init_vero_dictionary(sheet)
        process_ai_generation(sheet, err)
        process_validation(sheet, err)
        process_monodas_drafts(sheet)
        log("Cycle complete.")
        return 0
    except Exception as e:
        log(f"FATAL: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())