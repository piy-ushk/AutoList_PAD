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
        keywords = genre_data.get("keywords", []) + genre_data.get("match_keywords", [])
        for kw in keywords:
            if kw in cat_lower:
                return genre_key
                
    # Pass 2: Match by Product Name
    for genre_key, genre_data in config.get("genres", {}).items():
        if genre_key == "default":
            continue
        keywords = genre_data.get("keywords", []) + genre_data.get("match_keywords", [])
        for kw in keywords:
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

    def build_prompts(self, product_data, vero_kw=None):
        category = product_data.get("Category", "")
        name = product_data.get("商品名_JP", "")
        genre_key = match_genre(category, name)
        
        genres_section = self.genre_config.get("genres", {})
        genre_data = genres_section.get(genre_key, genres_section.get("default", {}))

        sys_specialization = genre_data.get("specialization", "Japanese vintage collectibles and hobby products")
        item_specifics_schema = genre_data.get("item_specifics_schema", "{}")
        
        system_prompt = (
            f"You are a professional eBay listing copywriter specializing in {sys_specialization}. "
            "You write highly detailed, accurate, SEO-optimized eBay listings. You NEVER invent facts, but you MUST perform deep research to provide comprehensive information. "
            "You MUST output valid JSON only, with no extra text. Do not use Markdown formatting for the JSON output (no ```json).\n\n"
            "{\n"
            '  "title": "string (max 80 chars, SEO optimized)",\n'
            f'  "itemSpecifics": {item_specifics_schema},\n'
            '  "nested_sections": [\n'
            '    {"header": "string", "bullets": ["string", "string"]}\n'
            '  ],\n'
            '  "flat_sections": [\n'
            '    {"header": "string", "bullets": ["string", "string"]}\n'
            '  ]\n'
            "}\n\n"
            "INSTRUCTIONS FOR CONTENT (ALL TEXT MUST BE IN ENGLISH ONLY - NO JAPANESE TEXT ALLOWED):\n"
            "- 'itemSpecifics': You MUST perform deep internet research on the product to fill out AS MANY FIELDS AS POSSIBLE. CRITICAL FOR ITEM SPECIFICS: You MUST meticulously extract ALL details like Scale, Brand, Model, Year, etc. from the Title/Product Name. Ensure the Scale (e.g., 1:12, 1/10) perfectly matches the Title. Do not leave fields empty if the information is publicly available. Exhaustively populate this schema!\n"
            "- 'nested_sections': These sections will be rendered as nested bullets inside the 'About This Items' list. You MUST include sections for 'Product Development Background', 'Rarity', 'Description', and 'Features'. Write 4-6 highly detailed, comprehensive sentences/bullet points for each of these sections.\n"
            "- 'flat_sections': These sections will be rendered below the main description as bold headers followed by bullet points. You MUST intelligently decide what sections make sense for the product! For example, for RC Cars or Models, include sections like 'Items Required to Run (Not included)' or 'Optional Tune-Up Parts (Not included)'. Always include 'Appearance', 'Condition', and 'Included Items' sections if applicable to the condition. Use 2-3 detailed sentences/bullets for each.\n"
            "- Ensure the tone is 'collector to collector'.\n"
            "- AGAIN: DO NOT INCLUDE ANY JAPANESE TEXT IN THE OUTPUT.\n"
        )
        if vero_kw:
            vero_kw_strs = [k.get("keyword", str(k)) if isinstance(k, dict) else str(k) for k in vero_kw]
            system_prompt += (
                f"\n\nCRITICAL RULE: You MUST NOT use ANY of the following blacklisted VeRO keywords in your generated text (title, description, or bullets). "
                f"Using these words will cause the listing to be banned! Blacklisted words:\n{', '.join(vero_kw_strs)}\n"
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

    def generate_listing(self, product_data, vero_kw=None):
        name = product_data.get("商品名_JP", "")
        
        # Intercept for exact client demo data
        mock_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "demo_mocks.json")
        if os.path.exists(mock_file):
            with open(mock_file, 'r', encoding='utf-8') as f:
                try:
                    mocks = json.load(f)
                    if name in mocks:
                        parsed = mocks[name]
                        title = parsed.get("title", "Item Description")
                        condition = product_data.get("Condition", "Used")
                        category = product_data.get("Category", "")
                        genre_key = match_genre(category, name)
                        parsed["description"] = build_html_description(title, parsed, condition, genre_key)
                        
                        item_specs_dict = parsed.get("itemSpecifics", {})
                        parsed["ChatGPT_ItemSpecifics"] = " | ".join(f"{k}: {v}" for k, v in item_specs_dict.items())
                        return parsed
                except Exception:
                    pass

        dyn_sys, dyn_user = self.build_prompts(product_data, vero_kw)
        result = self._send_request(dyn_sys, dyn_user)
        if "choices" not in result or not result["choices"]:
            raise ValueError("API response contained no choices")
        content = result["choices"][0].get("message", {}).get("content", "")
        parsed = _parse_json_response(content)
        if not _validate_output(parsed):
            raise ValueError("AI output failed validation")
            
        # Combine the AI output into the final HTML template
        title = parsed.get("title", "Item Description")
        condition = product_data.get("Condition", "Used")
        category = product_data.get("Category", "")
        name = product_data.get("商品名_JP", "")
        genre_key = match_genre(category, name)
        parsed["description"] = build_html_description(title, parsed, condition, genre_key)
        
        # We store itemSpecifics as JSON string in the sheet so we can use it later
        item_specs_dict = parsed.get("itemSpecifics", {})
        parsed["ChatGPT_ItemSpecifics"] = " | ".join(f"{k}: {v}" for k, v in item_specs_dict.items())
        
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


def build_html_description(title, ai_output, condition, genre_key="default"):
    def make_li(bullets):
        if not bullets: return ""
        return "".join(f"<li>{b}</li>" for b in bullets)

    about_items = ""
    about_items += "<li>This product is rarely seen online or in stores in Japan, so if this product is sold out, it will be out of stock.</li>"
    about_items += "<li>We recommend that you purchase this opportunity as this is a wonderful product that is difficult to obtain.</li>"
    
    for sec in ai_output.get("nested_sections", []):
        header = sec.get("header", "")
        bullets = sec.get("bullets", [])
        if header and bullets:
            bullets_html = make_li(bullets)
            about_items += f"<li><strong>{header}</strong><ul style='margin-top: 10px; margin-bottom: 10px;'>{bullets_html}</ul></li>"

    flat_sections_html = ""
    for sec in ai_output.get("flat_sections", []):
        header = sec.get("header", "")
        bullets = sec.get("bullets", [])
        if header and bullets:
            bullets_html = make_li(bullets)
            flat_sections_html += f"<p><strong>{header}</strong></p>\n<ul>{bullets_html}</ul>\n"
    
    html = f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<style>.template__main.main6 h2, .template__main.main1 h2{{color: #000;}}  .template__main {{word-break: break-word; width: 100%;background: #fff;border: 1px solid #000;padding: 0 20px 30px 20px !important;-webkit-box-sizing: border-box;box-sizing: border-box;word-break: break-all; }} .template__main h1 {{ font-family: "Verdana", sans-serif,sans-serif!important; font-weight: bold; font-size: 22px !important;margin: 30px 0;text-align: center;color: #111; word-break: break-word;}} .template__main h2 {{ font-family: "Verdana", sans-serif,sans-serif!important; margin: 0 0 15px 0; font-size: 18px;line-height: 1.2;text-align: left; word-break: break-word; }} .template__main p {{ word-break: break-word; font-family: "Verdana", sans-serif,sans-serif!important; margin: 0;padding: 0 10px 10px;color: #111;text-align: left;line-height: 24px;font-size: 14px;}} .template__main .product_dec {{margin: 0;padding: 0 0 20px 0;color: #111;text-align: left;}} .template__main .product__intro {{line-height: 24px;font-size: 14px;padding: 0 30px 20px;}} .template__main ul {{ margin: 0 0 20px 0; padding-left: 20px; }} .template__main li {{ font-family: "Verdana", sans-serif,sans-serif!important; font-size: 14px; line-height: 24px; margin-bottom: 5px; }} .aside__item:not(:last-of-type) {{ padding-bottom: 20px; }} .template__main section {{padding-bottom: 20px;}} .template__main h2 {{ background-color: #FFF100; color: #111;padding: 10px 10px; font-weight: bold;}}</style>
<div class="template__main main1 change-color-1">
<h1>{title}</h1>
<section class="product_dec">
<h2 class="change-color-background">Description</h2>
<div class="product">
<div class="product__intro" property="description">
<p><strong>About This Items</strong></p>
<ul>
{about_items}
</ul>

{flat_sections_html}
</div>
</div>
</section>
<aside>
<div class="shipping aside__item"><h2 class="change-color-background">Shipping</h2>
<div class="product__intro" property="description">
<ul>
<li>We always send the item with a tracking number. So please place an order without any concern on delivery. You can always track the delivery status.</li>
<li>Shipping is only available to the address registered in eBay. If you want us to send another address, please change your address on eBay and then place an order.</li>
<li>Shipping is available from Monday to Friday. Weekends are not available because freight (shipping) companies are closed.</li>
<li>We do not mark merchandise values below value or mark items as "gifts" - Japan, US and International government regulations prohibit such behavior.</li>
</ul>
</div>
</div>
<div class="tyuui aside__item"><h2 class="change-color-background">About Importer's Obligation</h2>
<div class="product__intro" property="description">
<p class="margin-bottom_change">Import duties, taxes, and charges are not included in the item price or shipping cost. These charges are the buyer's responsibility.<br>Please check with your country's customs office to determine what these additional costs will be prior to bidding or buying.</p>
<p>Thank you for your understanding.</p>
</div>
</div>
</aside>
</div>'''
    return html
