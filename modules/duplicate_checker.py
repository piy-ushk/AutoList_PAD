import hashlib, re, requests
from PIL import Image
import imagehash
from io import BytesIO


def normalize_text(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower().strip())


def compute_hash(text):
    return hashlib.md5(normalize_text(text).encode("utf-8")).hexdigest()


def compute_phash(image_urls):
    if not image_urls:
        return ""
    # Extract the first valid URL
    urls = [u.strip() for u in image_urls.replace(",", "\n").split("\n") if u.strip().startswith("http")]
    if not urls:
        return ""
    first_url = urls[0]
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        response = requests.get(first_url, headers=headers, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return str(imagehash.phash(img))
    except Exception as e:
        print(f"    WARNING: Failed to compute PHash for {first_url}: {e}")
        return ""


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
    new_title = normalize_text(new_listing.get("eBay_Title", "").strip() or new_listing.get("ChatGPT_Title", "").strip())
    new_jan = normalize_text(new_listing.get("JAN_Code", ""))
    new_model = normalize_text(new_listing.get("Model_Number", ""))
    new_url = normalize_text(new_listing.get("仕入URL", ""))
    new_brand = normalize_text(new_listing.get("Brand", ""))
    
    # Check if we computed a phash for the new listing earlier (or compute it now if missing)
    new_phash = new_listing.get("Image_PHash", "")
    if not new_phash and new_listing.get("画像URLs"):
        new_phash = compute_phash(new_listing.get("画像URLs", ""))

    IGNORE_VALUES = {"n/a", "na", "none", "nan", "", "-"}

    for existing in existing_listings:
        existing_sku = existing.get("SKU", "")
        existing_jan = normalize_text(existing.get("JAN_Code", ""))
        existing_model = normalize_text(existing.get("Model_Number", ""))
        existing_url = normalize_text(existing.get("Source_URL", ""))
        existing_brand = normalize_text(existing.get("Brand", ""))
        existing_title = normalize_text(existing.get("Title_Hash", ""))
        existing_phash = existing.get("Image_PHash", "")

        if new_jan and existing_jan and new_jan not in IGNORE_VALUES and existing_jan not in IGNORE_VALUES and new_jan == existing_jan:
            matches.append({"type": "JAN_Code", "priority": "HIGH", "existing_sku": existing_sku, "detail": f"JAN code match: {new_jan}"})

        if new_model and existing_model and new_model not in IGNORE_VALUES and existing_model not in IGNORE_VALUES and new_model == existing_model:
            matches.append({"type": "Model_Number", "priority": "HIGH", "existing_sku": existing_sku, "detail": f"Model number match: {new_model}"})

        if new_url and existing_url and new_url not in IGNORE_VALUES and existing_url and new_url == existing_url:
            matches.append({"type": "Source_URL", "priority": "HIGH", "existing_sku": existing_sku, "detail": f"Source URL match: {new_url}"})

        if new_title and existing_title:
            sim = title_similarity(new_title, existing_title)
            if sim > 0.8:
                priority = "HIGH" if sim == 1.0 else "MEDIUM"
                matches.append({"type": "Title_Similarity", "priority": priority, "existing_sku": existing_sku, "detail": f"Title similarity {sim*100:.1f}%"})

        if new_brand and existing_brand and new_brand == existing_brand and new_title and existing_title and new_title in existing_title:
            matches.append({"type": "Brand_Title", "priority": "MEDIUM", "existing_sku": existing_sku, "detail": f"Brand + partial title match"})

        if new_phash and existing_phash:
            try:
                hash1 = imagehash.hex_to_hash(new_phash)
                hash2 = imagehash.hex_to_hash(existing_phash)
                diff = hash1 - hash2
                if diff <= 5:  # High similarity
                    matches.append({"type": "Image_PHash", "priority": "HIGH", "existing_sku": existing_sku, "detail": f"Image PHash match (diff={diff})"})
            except Exception:
                pass

    if matches:
        high = any(m["priority"] == "HIGH" for m in matches)
        return {"is_duplicate": True, "matches": matches, "priority": "HIGH" if high else "MEDIUM", "reason": "; ".join(m["detail"] for m in matches)}
    return {"is_duplicate": False, "matches": [], "priority": "NONE", "reason": ""}


def generate_fingerprint(listing):
    title = listing.get("eBay_Title", "").strip() or listing.get("ChatGPT_Title", "").strip()
    image_urls = listing.get("画像URLs", "")
    image_hash = compute_hash(image_urls) if image_urls else listing.get("Image_Hash", "")
    image_phash = compute_phash(image_urls) if image_urls else listing.get("Image_PHash", "")
    return {
        "SKU": listing.get("管理ID_SKU", listing.get("SKU", "")),
        "Title_Hash": title,
        "JAN_Code": listing.get("JAN_Code", ""),
        "Model_Number": listing.get("Model_Number", ""),
        "Brand": normalize_text(listing.get("Brand", "")),
        "Source_URL": listing.get("仕入URL", listing.get("Source_URL", "")),
        "Image_Hash": image_hash,
        "Image_PHash": image_phash,
        "Status": "active",
        "eBay_Item_ID": listing.get("eBay_Item_ID", ""),
    }