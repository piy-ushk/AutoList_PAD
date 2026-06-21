import json, os, re, time, urllib.request, urllib.error


def load_api_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "api_keys.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_genre_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "genre_templates.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def match_genre(category_str, product_name_str):
    try:
        config = load_genre_config()
    except Exception:
        return "default"
    cat_lower = (category_str or "").lower().strip()
    name_lower = (product_name_str or "").lower().strip()
    
    # Pass 1: Match by Category
    for genre_key, genre_data in config.get("genres", {}).items():
        if genre_key == "default":
            continue
        for kw in genre_data.get("keywords", []):
            if kw in cat_lower:
                return genre_key
                
    # Pass 2: Match by Product Name
    for genre_key, genre_data in config.get("genres", {}).items():
        if genre_key == "default":
            continue
        for kw in genre_data.get("keywords", []):
            if kw in name_lower:
                return genre_key
                
    return "default"


SYSTEM_PROMPT = ("You are a professional eBay listing copywriter specializing in Japanese vintage collectibles, "
    "trading cards, and hobby products. You write clean, accurate, SEO-optimized eBay listings in English. "
    "You NEVER invent facts. You output valid JSON only, with no extra text.\n\n"
    'Output schema:\n{"title":"string (max 80 chars)","itemSpecifics":{"Card Name":"string",'
    '"Character":"string","Language":"Japanese","Manufacturer":"string","Card Type":"string",'
    '"Rarity":"string","Condition":"string","Set":"string","Year":"string","Grade":"string or N/A",'
    '"Features":"string"},"description":"string (HTML, 150-400 words)","rarity":"string",'
    '"features":"string (HTML <ul><li>)","background":"string"}')

USER_PROMPT_TEMPLATE = (
    "Generate an eBay listing for the following Japanese product:\n\n"
    "Product Name: {product_name}\nBrand: {brand}\n"
    "Model Number: {model}\nJAN Code: {jan}\nCondition: {condition}\n"
    "Category: {category}\nPrice (JPY): {price}\nNotes: {notes}\n\n"
    "Rules:\n1. Title under 80 characters\n"
    "2. Do NOT use trademarked names unless they are the actual product brand\n"
    "3. Do NOT include: replica, copy, fake, inspired, unauthorized, counterfeit\n"
    "4. Write as a collector to a collector\n"
    '5. Include "From Japan" naturally in title\n'
    "6. Output JSON only, no preamble"
)


class ChatGPTCaller:
    def __init__(self):
        self.config = load_api_config().get("openai", {})
        self.api_key = self.config.get("api_key", os.environ.get("OPENAI_API_KEY", ""))
        self.model = self.config.get("model", "gpt-4o")
        self.fallback_model = self.config.get("fallback_model", "gpt-4-turbo")
        self.max_tokens = self.config.get("max_tokens", 2000)
        self.temperature = self.config.get("temperature", 0.3)
        self.max_retries = self.config.get("max_retries", 3)
        self.retry_delay = self.config.get("retry_delay_seconds", 30)
        self.endpoint = "https://api.openai.com/v1/chat/completions"
        try:
            self.genre_config = load_genre_config()
        except Exception:
            self.genre_config = {"genres": {}}

    def build_user_prompt(self, product_data):
        # Deprecated: kept for backwards compatibility/tests
        return USER_PROMPT_TEMPLATE.format(
            product_name=product_data.get("商品名_JP", ""),
            brand=product_data.get("Brand", ""),
            model=product_data.get("Model_Number", ""),
            jan=product_data.get("JAN_Code", ""),
            condition=product_data.get("Condition", ""),
            category=product_data.get("Category", ""),
            price=product_data.get("想定仕入額_JPY", ""),
            notes=product_data.get("備考", ""),
        )

    def build_prompts(self, product_data):
        category = product_data.get("Category", "")
        name = product_data.get("商品名_JP", "")
        genre_key = match_genre(category, name)
        
        genres_section = self.genre_config.get("genres", {})
        genre_data = genres_section.get(genre_key, genres_section.get("default", {}))

        sys_specialization = genre_data.get("specialization", "Japanese vintage collectibles and hobby products")
        item_specifics_schema = genre_data.get("item_specifics_schema", "{}")
        
        system_prompt = (
            f"You are a professional eBay listing copywriter specializing in {sys_specialization}. "
            "You write clean, accurate, SEO-optimized eBay listings. You NEVER invent facts. "
            "You MUST output valid JSON only, with no extra text. Do not use Markdown formatting for the JSON output (no ```json).\n\n"
            "Output schema:\n"
            "{\n"
            '  "title": "string (max 80 chars, SEO optimized)",\n'
            f'  "itemSpecifics": {item_specifics_schema},\n'
            '  "background_bullets": ["string (English)", "string (Japanese translation)", ...],\n'
            '  "rarity_bullets": ["string (English)", "string (Japanese translation)", ...],\n'
            '  "description_bullets": ["string (English)", "string (Japanese translation)", ...],\n'
            '  "features_bullets": ["string (English)", "string (Japanese translation)", ...]\n'
            "}\n\n"
            "INSTRUCTIONS FOR BULLETS:\n"
            "- For 'background_bullets' (Product Development Background), write concise points about why the manufacturer made this product, mixing in expert knowledge. Provide each point in English, followed by its Japanese translation in the next array element.\n"
            "- For 'rarity_bullets' (Rarity), explain why it's hard to find. Provide English then Japanese translation.\n"
            "- For 'description_bullets' (Description) and 'features_bullets' (Features), highlight the main selling points. Provide English then Japanese translation.\n"
            "- Write to appeal to foreign collectors, showcasing deep specialized knowledge.\n"
        )

        genre_fields_txt = genre_data.get("genre_fields", "")
        if genre_key == "game_related":
            genre_fields_txt = genre_fields_txt.format(model=product_data.get("Model_Number", "N/A"))

        item_specifics_keys_str = ", ".join(genre_data.get("item_specifics_keys", []))
        
        user_prompt = (
            "Generate an eBay listing for the following Japanese product:\n\n"
            f"Product Name: {product_data.get('商品名_JP', '')}\n"
            f"Brand: {product_data.get('Brand', '')}\n"
            f"Model Number: {product_data.get('Model_Number', '')}\n"
            f"JAN Code: {product_data.get('JAN_Code', '')}\n"
            f"Condition: {product_data.get('Condition', '')}\n"
            f"Category: {product_data.get('Category', '')}\n"
            f"Price (JPY): {product_data.get('想定仕入額_JPY', '')}\n"
            f"Notes: {product_data.get('備考', '')}\n"
            f"{genre_fields_txt}\n"
            "Rules:\n"
            "1. Title under 80 characters. Space counts as 1 char. Include 'From Japan'.\n"
            "2. Do NOT use trademarked names unless they are the actual product brand.\n"
            "3. Do NOT include: replica, copy, fake, inspired, unauthorized, counterfeit.\n"
            "4. For itemSpecifics, provide values for: " + item_specifics_keys_str + ". If height/length/width are known, convert to cm and inches.\n"
            "5. Output JSON only, no preamble."
        )

        return system_prompt, user_prompt

    def _call_api(self, system_prompt, user_prompt):
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))

    def _send_request(self, system_prompt, user_prompt, retries=0):
        try:
            return self._call_api(system_prompt, user_prompt)
        except urllib.error.HTTPError as e:
            if e.code == 429 and retries < self.max_retries:
                time.sleep(self.retry_delay)
                return self._send_request(system_prompt, user_prompt, retries + 1)
            raise

    def generate_listing(self, product_data, system_prompt=None):
        if system_prompt:
            user_prompt = self.build_user_prompt(product_data)
            result = self._send_request(system_prompt, user_prompt)
        else:
            dyn_sys, dyn_user = self.build_prompts(product_data)
            result = self._send_request(dyn_sys, dyn_user)
        if "choices" not in result or not result["choices"]:
            raise ValueError("API response contained no choices")
        content = result["choices"][0].get("message", {}).get("content", "")
        parsed = _parse_json_response(content)
        if not _validate_output(parsed):
            raise ValueError("AI output failed validation")
            
        # Combine the AI output into the final HTML template
        title = parsed.get("title", product_data.get("商品名_JP", ""))
        condition = product_data.get("Condition", "Used")
        parsed["description"] = build_html_description(title, parsed, condition)
        
        # We store itemSpecifics as JSON string in the sheet so we can use it later
        parsed["ChatGPT_ItemSpecifics"] = json.dumps(parsed.get("itemSpecifics", {}), ensure_ascii=False)
        
        return parsed


def _parse_json_response(content):
    if not content:
        return {}
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:-1])
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        m = re.search(r'\{[\s\S]*\}', content)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    return {}


def _validate_output(ai_output):
    if not ai_output or not ai_output.get("title") or len(ai_output["title"]) > 80:
        return False
    specifics = ai_output.get("itemSpecifics", {})
    if not isinstance(specifics, dict) or len(specifics) < 3:
        return False
    return True


def validate_ai_output(ai_output):
    return _validate_output(ai_output)


def batch_generate(products):
    generator = ChatGPTCaller()
    results, failed = [], []
    for i, product in enumerate(products):
        try:
            results.append({"index": i, "product": product, "ai_output": generator.generate_listing(product)})
        except Exception as e:
            failed.append({"index": i, "product": product, "error": str(e)})
        if i < len(products) - 1:
            time.sleep(2)
    return results, failed


def build_html_description(title, ai_output, condition):
    def make_ol(bullets):
        if not bullets: return ""
        items = "".join(f"<li style='margin-bottom: 8px; line-height: 1.6;'>{b}</li>" for b in bullets)
        return f"<ul style='margin: 0; padding-left: 20px; list-style-type: disc;'>{items}</ul>"

    bg_html = make_ol(ai_output.get("background_bullets", []))
    rarity_html = make_ol(ai_output.get("rarity_bullets", []))
    desc_html = make_ol(ai_output.get("description_bullets", []))
    features_html = make_ol(ai_output.get("features_bullets", []))

    about_items = ""
    if bg_html: about_items += f"<h4 style='font-size:16px; margin: 15px 0 8px 0; color: #111820; border-bottom: 1px solid #e5e5e5; padding-bottom: 4px;'>Product Background / 経緯</h4>{bg_html}"
    if rarity_html: about_items += f"<h4 style='font-size:16px; margin: 15px 0 8px 0; color: #111820; border-bottom: 1px solid #e5e5e5; padding-bottom: 4px;'>Rarity / 希少性</h4>{rarity_html}"
    if desc_html: about_items += f"<h4 style='font-size:16px; margin: 15px 0 8px 0; color: #111820; border-bottom: 1px solid #e5e5e5; padding-bottom: 4px;'>Description / 商品詳細</h4>{desc_html}"
    if features_html: about_items += f"<h4 style='font-size:16px; margin: 15px 0 8px 0; color: #111820; border-bottom: 1px solid #e5e5e5; padding-bottom: 4px;'>Features / 特徴</h4>{features_html}"

    html = f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    .premium-desc-wrapper {{
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        color: #333;
        background-color: #f7f9fa;
        padding: 40px 20px;
        line-height: 1.6;
    }}
    .premium-desc-container {{
        max-width: 900px;
        margin: 0 auto;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        overflow: hidden;
        border: 1px solid #eaeaea;
    }}
    .premium-header {{
        background: linear-gradient(135deg, #0053a0 0%, #0064d2 100%);
        color: #ffffff;
        padding: 30px;
        text-align: center;
    }}
    .premium-header h1 {{
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .premium-header p {{
        margin: 10px 0 0 0;
        font-size: 16px;
        opacity: 0.9;
    }}
    .premium-section {{
        padding: 30px;
        border-bottom: 1px solid #f0f0f0;
    }}
    .premium-section:last-child {{
        border-bottom: none;
    }}
    .premium-section-title {{
        font-size: 20px;
        font-weight: 700;
        color: #0064d2;
        margin: 0 0 20px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .premium-section-title i {{
        font-size: 22px;
        width: 30px;
        text-align: center;
    }}
    .premium-content {{
        font-size: 15px;
        color: #444;
    }}
    .premium-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }}
    .info-box {{
        background: #f8fafd;
        border-left: 4px solid #0064d2;
        padding: 15px 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
    }}
    .warning-box {{
        background: #fffdf5;
        border: 1px solid #ffeb3b;
        border-left: 4px solid #ffc107;
        padding: 15px 20px;
        border-radius: 4px;
        font-size: 14px;
    }}
</style>

<div class="premium-desc-wrapper">
    <div class="premium-desc-container">
        <div class="premium-header">
            <h1>{title}</h1>
            <p>100% Authentic • Ships Directly from Japan</p>
        </div>

        <div class="premium-section">
            <h2 class="premium-section-title"><i class="fas fa-info-circle"></i> About This Item</h2>
            <div class="premium-content">
                {about_items}
            </div>
        </div>

        <div class="premium-grid">
            <div class="premium-section">
                <h2 class="premium-section-title"><i class="fas fa-camera"></i> Appearance</h2>
                <div class="info-box">
                    <p style="margin:0; font-weight: 600;">Please check the photos carefully.</p>
                    <p style="margin:5px 0 0 0; font-size:14px;">The item shown in the images is the exact item you will receive. Minor cosmetic wear may be present due to age.</p>
                </div>
            </div>

            <div class="premium-section">
                <h2 class="premium-section-title"><i class="fas fa-clipboard-check"></i> Condition</h2>
                <div class="info-box">
                    <p style="margin:0; font-weight: 600;">{condition}</p>
                    <p style="margin:5px 0 0 0; font-size:14px;">Our items are carefully inspected. If you have specific questions about the condition, please ask before purchasing.</p>
                </div>
            </div>
        </div>

        <div class="premium-section">
            <h2 class="premium-section-title"><i class="fas fa-plane-departure"></i> Shipping Details</h2>
            <div class="premium-content">
                <ul style="margin: 0; padding-left: 20px; list-style-type: disc;">
                    <li style="margin-bottom: 8px;">We always send the item with a <strong>tracking number</strong>. Please place an order without any concern on delivery.</li>
                    <li style="margin-bottom: 8px;">Shipping is only available to the address registered in eBay.</li>
                    <li style="margin-bottom: 8px;">Shipping operations are available from Monday to Friday (Closed on weekends).</li>
                    <li style="margin-bottom: 8px;">We do not mark merchandise values below value or mark items as "gifts" — International government regulations prohibit such behavior.</li>
                </ul>
            </div>
        </div>

        <div class="premium-section">
            <h2 class="premium-section-title"><i class="fas fa-exclamation-triangle"></i> International Buyers - Please Note:</h2>
            <div class="warning-box">
                <p style="margin:0 0 10px 0;">Import duties, taxes, and charges are <strong>not included</strong> in the item price or shipping cost. These charges are the buyer's responsibility.</p>
                <p style="margin:0;">Please check with your country's customs office to determine what these additional costs will be prior to bidding or buying. Thank you for your understanding.</p>
            </div>
        </div>
    </div>
</div>'''
    return html

