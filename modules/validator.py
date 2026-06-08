import re


def check_required_fields(listing_data):
    required = ["管理ID_SKU", "Brand", "Category", "Condition", "ChatGPT_Title", "ChatGPT_Description", "仕入URL", "販売形式", "出品価格_USD"]
    missing = [c for c in required if not listing_data.get(c, "").strip()]
    return len(missing) == 0, missing


def check_ai_content(listing_data):
    ai_fields = ["ChatGPT_Title", "ChatGPT_Description", "ChatGPT_ItemSpecifics", "ChatGPT_Rarity", "ChatGPT_Features", "ChatGPT_Background"]
    missing = [f for f in ai_fields if not listing_data.get(f, "").strip()]
    has_any = len(missing) < 6
    return has_any, missing


def check_price(listing_data):
    price_val = listing_data.get("出品価格_USD", "")
    try:
        price = float(price_val)
        if price <= 0:
            return False, "Price must be greater than 0"
    except (ValueError, TypeError):
        return False, "Price is not a valid number"
    return True, ""


def check_title_length(listing_data):
    title = listing_data.get("ChatGPT_Title", listing_data.get("eBay_Title", ""))
    if len(title) > 80:
        return False, f"Title is {len(title)} characters (max 80)"
    return True, ""


def check_title_not_empty(listing_data):
    title = listing_data.get("ChatGPT_Title", listing_data.get("eBay_Title", ""))
    if not title.strip():
        return False, "Title is empty"
    return True, ""


def check_description_not_empty(listing_data):
    desc = listing_data.get("ChatGPT_Description", "")
    if not desc.strip():
        return False, "Description is empty"
    return True, ""


def check_images(listing_data):
    images = listing_data.get("画像URLs", "")
    if not images.strip():
        return False, "No image URLs set"
    return True, ""


def check_source_url(listing_data):
    url = listing_data.get("仕入URL", "")
    if not url.strip():
        return False, "Source URL is empty"
    if not re.match(r"^https?://", url):
        return False, "Source URL format is invalid"
    return True, ""


def check_assigned_staff(listing_data):
    staff = listing_data.get("担当者", "")
    if not staff.strip():
        return False, "No staff assigned"
    return True, ""


def run_all_validations(listing_data):
    checks = [
        ("AI Content", check_ai_content(listing_data)),
        ("Required Fields", check_required_fields(listing_data)),
        ("Price", check_price(listing_data)),
        ("Title Length", check_title_length(listing_data)),
        ("Title Not Empty", check_title_not_empty(listing_data)),
        ("Description", check_description_not_empty(listing_data)),
        ("Images", check_images(listing_data)),
        ("Source URL", check_source_url(listing_data)),
        ("Assigned Staff", check_assigned_staff(listing_data)),
    ]
    results = {"passed": True, "checks": [], "errors": []}
    for name, (passed, msg) in checks:
        results["checks"].append({"name": name, "passed": passed, "message": msg})
        if not passed:
            results["passed"] = False
            results["errors"].append(f"{name}: {msg}")
    return results