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
    
    # Check category string match first, then product name string match
    for genre_key, genre_data in config.get("genres", {}).items():
        if genre_key == "default":
            continue
        for kw in genre_data.get("keywords", []):
            if kw in cat_lower or kw in name_lower:
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

        # Construct System Prompt
        sys_specialization = genre_data.get("specialization", "Japanese vintage collectibles and hobby products")
        item_specifics_schema = genre_data.get("item_specifics_schema", "{}")
        
        system_prompt = (
            f"You are a professional eBay listing copywriter specializing in Japanese vintage collectibles, {sys_specialization}. "
            "You write clean, accurate, SEO-optimized eBay listings in English. You NEVER invent facts. You output valid JSON only, with no extra text.\n\n"
            "Output schema:\n"
            "{\n"
            '  "title": "string (max 80 chars)",\n'
            f'  "itemSpecifics": {item_specifics_schema},\n'
            '  "description": "string (HTML, 150-400 words)",\n'
            '  "rarity": "string",\n'
            '  "features": "string (HTML <ul><li>)",\n'
            '  "background": "string"\n'
            "}"
        )

        # Construct User Prompt
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
            "1. Title under 80 characters.\n"
            "2. Do NOT use trademarked names unless they are the actual product brand.\n"
            "3. Do NOT include: replica, copy, fake, inspired, unauthorized, counterfeit.\n"
            "4. Write as a collector to a collector.\n"
            "5. Include \"From Japan\" naturally in title.\n"
            f"6. For itemSpecifics, provide values for: {item_specifics_keys_str}.\n"
            "7. Output JSON only, no preamble."
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
    if not ai_output.get("description"):
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