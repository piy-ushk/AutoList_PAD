import json
import os
import re


def load_keyword_dictionary():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "vero_keywords.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("keywords", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def strip_html(html_text):
    clean = re.compile("<.*?>")
    text = re.sub(clean, "", html_text)
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("&nbsp;", " ")
    return text


def normalize_text(text):
    if not text:
        return ""
    return text.lower().strip()


def scan_keywords(title, description, keyword_dict):
    text = normalize_text(title)
    desc_text = normalize_text(strip_html(description))
    combined = text + " " + desc_text

    flags = []
    auto_replacements = {}

    for entry in keyword_dict:
        keyword = normalize_text(entry.get("keyword", ""))
        if not keyword:
            continue

        match_type = entry.get("match_type", "contains")
        action = entry.get("action", "block")
        found = False

        if match_type == "exact":
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            if re.search(r"\b" + pattern.pattern + r"\b", combined, re.IGNORECASE):
                found = True
        elif match_type == "contains":
            if keyword in combined:
                found = True
        elif match_type == "regex":
            regex_pattern = entry.get("pattern", entry.get("regex", ""))
            if regex_pattern:
                try:
                    if re.search(regex_pattern, combined, re.IGNORECASE):
                        found = True
                except re.error:
                    if keyword in combined:
                        found = True

        if found:
            flags.append(entry)
            if action == "auto_replace" and entry.get("replacement"):
                auto_replacements[keyword] = entry.get("replacement")
            if action == "block":
                break

    return {
        "passed": len(flags) == 0,
        "flags": flags,
        "flagged_keywords": [f.get("keyword", "") for f in flags],
        "auto_replacements": auto_replacements,
    }


def auto_replace(text, replacements):
    modified = text
    replacements_made = []

    for keyword, replacement in replacements.items():
        if not replacement:
            continue
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        if pattern.search(modified):
            modified = pattern.sub(replacement, modified)
            replacements_made.append(f"{keyword} -> {replacement}")

    return modified, replacements_made


def check_hard_banned_words(title):
    hard_banned = ["replica", "fake", "counterfeit", "inspired", "unauthorized", "knockoff"]
    title_lower = normalize_text(title)
    for word in hard_banned:
        pattern = re.compile(r"\b" + re.escape(word) + r"\b")
        if pattern.search(title_lower):
            return False, word
    return True, ""


def run_vero_check(title, description, keyword_dict):
    hard_pass, hard_word = check_hard_banned_words(title)
    if not hard_pass:
        return {
            "passed": False,
            "reason": "hard_banned_word",
            "flagged_word": hard_word,
            "flags": [{"keyword": hard_word, "category": "NG_Word"}],
        }

    result = scan_keywords(title, description, keyword_dict)

    if not result["passed"] and result.get("auto_replacements"):
        modified_title, title_replacements = auto_replace(title, result["auto_replacements"])
        modified_desc, desc_replacements = auto_replace(description, result["auto_replacements"])
        recheck = scan_keywords(modified_title, modified_desc, keyword_dict)

        result["auto_replaced_title"] = modified_title if title_replacements else title
        result["auto_replaced_description"] = modified_desc if desc_replacements else description
        result["title_replacements_made"] = title_replacements
        result["desc_replacements_made"] = desc_replacements
        result["passed"] = recheck["passed"]
        if not recheck["passed"]:
            result["flags"] = recheck["flags"]
            result["flagged_keywords"] = recheck["flagged_keywords"]

    return result