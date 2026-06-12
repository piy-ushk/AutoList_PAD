import re


def select_shipping_policy(price_usd, handling_days, sa_exclusion=False, stock_type="DROP"):
    if isinstance(handling_days, str):
        handling_days = int(re.sub(r"[^0-9]", "", handling_days) or "10")
    if isinstance(sa_exclusion, str):
        sa_exclusion = sa_exclusion.strip().upper() == "YES"
    if isinstance(stock_type, str):
        stock_type = "STOCK" if "在庫" in stock_type or stock_type.lower() == "stock" else "DROP"

    brackets = [50, 100, 200, 300, 400, 500, 600, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500]
    price_range, prev_b = "2501+", 0
    for b in brackets:
        if price_usd <= b:
            price_range = f"1-{b}" if price_usd <= 50 else f"{prev_b + 1}-{b}"
            break
        prev_b = b
    method = "ECO" if price_usd <= 100 else "EXP"
    sa_suffix = "_SAOFF" if sa_exclusion else ""
    return f"{stock_type}_{handling_days}D_{price_range}_{method}{sa_suffix}"


def parse_policy_name(policy_name):
    m = re.match(r"^(DROP|STOCK)_(\d+)D_(\d+\+?)-(\d+\+?)_(ECO|EXP)(?:_SAOFF)?$", policy_name)
    if not m:
        return None
    return {"stock_type": m.group(1), "handling_days": int(m.group(2)),
            "price_range_min": m.group(3), "price_range_max": m.group(4),
            "shipping_method": m.group(5), "sa_exclusion": "_SAOFF" in policy_name}


def find_best_policy(price_usd, handling_days, sa_exclusion, stock_type, available_policies):
    target = select_shipping_policy(price_usd, handling_days, sa_exclusion, stock_type)
    exact = [p for p in available_policies if p.get("Template_Name", "") == target]
    if exact:
        return exact[0].get("Template_Name", target)

    target_p = parse_policy_name(target)
    if not target_p:
        return target

    best, best_score = None, -1
    for policy in available_policies:
        name = policy.get("Template_Name", "")
        p = parse_policy_name(name)
        if not p:
            continue
        score = sum([40 if p["stock_type"] == target_p["stock_type"] else 0,
                     30 if p["handling_days"] == target_p["handling_days"] else 0,
                     20 if p["shipping_method"] == target_p["shipping_method"] else 0,
                     10 if p["sa_exclusion"] == target_p["sa_exclusion"] else 0])
        if score > best_score:
            best_score, best = score, name
    return best if best else target


def generate_all_templates():
    templates = []
    for stock in ["DROP", "STOCK"]:
        for days in [3, 5, 7, 10, 15, 20, 30]:
            for pr_min, pr_max in [(1, 50), (51, 100), (101, 200), (201, 300), (301, 400),
                                   (401, 500), (501, 600), (601, 700), (701, 900),
                                   (901, 1100), (1101, 1300), (1301, 1500), (1501, 1700),
                                   (1701, 1900), (1901, 2100), (2101, 2300), (2301, 2500)]:
                method = "ECO" if pr_max <= 100 else "EXP"
                for sa in [False, True]:
                    sa_s = "_SAOFF" if sa else ""
                    name = f"{stock}_{days}D_{pr_min}-{pr_max}_{method}{sa_s}"
                    templates.append({"Template_Name": name, "Usage_Type": stock, "Price_Range": f"{pr_min}-{pr_max}",
                                      "Handling_Days": str(days), "Shipping_Method": method, "SA_Exclusion": "YES" if sa else "NO"})
    return templates