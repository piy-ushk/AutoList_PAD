import hashlib, re


def normalize_text(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower().strip())


def compute_hash(text):
    return hashlib.md5(normalize_text(text).encode("utf-8")).hexdigest()


def levenshtein_distance(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = curr
    return prev[-1]


def title_similarity(title_a, title_b):
    a, b = normalize_text(title_a), normalize_text(title_b)
    if not a and not b:
        return 1.0
    distance = levenshtein_distance(a, b)
    return max(0.0, 1.0 - distance / max(len(a), len(b))) if max(len(a), len(b)) > 0 else 1.0


def check_duplicate(new_listing, existing_listings):
    matches = []
    new_title = normalize_text(new_listing.get("ChatGPT_Title", new_listing.get("eBay_Title", "")))
    new_jan = normalize_text(new_listing.get("JAN_Code", ""))
    new_model = normalize_text(new_listing.get("Model_Number", ""))
    new_url = normalize_text(new_listing.get("仕入URL", ""))
    new_brand = normalize_text(new_listing.get("Brand", ""))

    for existing in existing_listings:
        existing_sku = existing.get("SKU", "")
        existing_jan = normalize_text(existing.get("JAN_Code", ""))
        existing_model = normalize_text(existing.get("Model_Number", ""))
        existing_url = normalize_text(existing.get("Source_URL", ""))
        existing_brand = normalize_text(existing.get("Brand", ""))
        existing_title = normalize_text(existing.get("Title_Hash", ""))

        if new_jan and existing_jan and new_jan == existing_jan:
            matches.append({"type": "JAN_Code", "priority": "HIGH", "existing_sku": existing_sku, "detail": f"JAN code match: {new_jan}"})

        if new_model and existing_model and new_model == existing_model:
            matches.append({"type": "Model_Number", "priority": "HIGH", "existing_sku": existing_sku, "detail": f"Model number match: {new_model}"})

        if new_url and existing_url and new_url == existing_url:
            matches.append({"type": "Source_URL", "priority": "HIGH", "existing_sku": existing_sku, "detail": f"Source URL match: {new_url}"})

        if new_title and existing_title and title_similarity(new_title, existing_title) > 0.8:
            matches.append({"type": "Title_Similarity", "priority": "MEDIUM", "existing_sku": existing_sku, "detail": f"Title similarity > 80%"})

        if new_brand and existing_brand and new_brand == existing_brand and new_title and existing_title and new_title in existing_title:
            matches.append({"type": "Brand_Title", "priority": "MEDIUM", "existing_sku": existing_sku, "detail": f"Brand + partial title match"})

    if matches:
        high = any(m["priority"] == "HIGH" for m in matches)
        return {"is_duplicate": True, "matches": matches, "priority": "HIGH" if high else "MEDIUM", "reason": "; ".join(m["detail"] for m in matches)}
    return {"is_duplicate": False, "matches": [], "priority": "NONE", "reason": ""}


def generate_fingerprint(listing):
    title = listing.get("ChatGPT_Title", listing.get("eBay_Title", ""))
    return {
        "SKU": listing.get("管理ID_SKU", listing.get("SKU", "")),
        "Title_Hash": compute_hash(title),
        "JAN_Code": listing.get("JAN_Code", ""),
        "Model_Number": listing.get("Model_Number", ""),
        "Brand": normalize_text(listing.get("Brand", "")),
        "Source_URL": listing.get("仕入URL", ""),
        "Image_Hash": listing.get("Image_Hash", ""),
        "Status": "active",
        "eBay_Item_ID": listing.get("eBay_Item_ID", ""),
    }