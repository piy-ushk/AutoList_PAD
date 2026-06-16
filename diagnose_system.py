import os
import sys
import json

def log_test(name, success, message=""):
    status = "[ OK ]" if success else "[FAIL]"
    print(f"{status} {name}")
    if not success and message:
        print(f"       -> {message}")
    return success

def run_diagnostics():
    print("=" * 60)
    print("AutoList - System Self-Diagnostic Tool")
    print("=" * 60)
    
    all_ok = True
    
    # 1. Check Python Libraries
    print("\n--- 1. Python Libraries Check ---")
    libs = [
        ("Pillow (PIL)", "PIL.Image"),
        ("imagehash", "imagehash"),
        ("requests", "requests")
    ]
    for lib_name, import_path in libs:
        try:
            __import__(import_path)
            log_test(lib_name, True)
        except ImportError as e:
            all_ok = log_test(lib_name, False, f"Library not installed. Run: pip install {lib_name.split(' ')[0]}")
            
    # 2. Check Configuration Files
    print("\n--- 2. Configuration Files Check ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, "config")
    
    configs = [
        "api_keys.json",
        "sheet_config.json",
        "selectors_config.json",
        "genre_templates.json",
        "vero_keywords.json"
    ]
    for config_file in configs:
        path = os.path.join(config_dir, config_file)
        if not os.path.exists(path):
            all_ok = log_test(config_file, False, f"Missing file at {path}")
            continue
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            log_test(config_file, True)
            
            # Subcheck specific configurations
            if config_file == "api_keys.json":
                openai_key = data.get("openai", {}).get("api_key", "")
                if not openai_key or openai_key.startswith("sk-YOUR"):
                    all_ok = log_test("  OpenAI API Key status", False, "API key is empty or default placeholder in api_keys.json") & all_ok
                else:
                    log_test("  OpenAI API Key status", True)
                    
                sheet_id = data.get("google", {}).get("spreadsheet_id", "")
                if not sheet_id or "YOUR_" in sheet_id:
                    all_ok = log_test("  Spreadsheet ID status", False, "Spreadsheet ID is missing or placeholder in api_keys.json") & all_ok
                else:
                    log_test("  Spreadsheet ID status", True)
        except json.JSONDecodeError as e:
            all_ok = log_test(config_file, False, f"Invalid JSON syntax: {e}") & all_ok
            
    # 3. Check Credentials Folder
    print("\n--- 3. Credentials Folder Check ---")
    cred_dir = os.path.join(base_dir, "credentials")
    sa_file = os.path.join(cred_dir, "service-account.json")
    
    if not os.path.exists(cred_dir):
        all_ok = log_test("Credentials Directory", False, "Missing credentials directory. Please create it.")
    else:
        log_test("Credentials Directory", True)
        if not os.path.exists(sa_file):
            all_ok = log_test("service-account.json", False, "Missing service-account.json in credentials/ directory.")
        else:
            log_test("service-account.json", True)

    # 4. Check API Connectivity
    print("\n--- 4. Active API Connectivity Check ---")
    
    # 4a. Google Sheets Connection
    sheets_ok = False
    try:
        sys.path.insert(0, base_dir)
        from modules.gsheets import GoogleSheetsClient
        client = GoogleSheetsClient()
        tab_name = client.tabs.get("listings", "出品管理表")
        # Try reading a tiny range
        client.api.read_range(tab_name, "A1:A2")
        log_test("Google Sheets API Connection", True)
        sheets_ok = True
    except Exception as e:
        all_ok = log_test("Google Sheets API Connection", False, f"Failed to connect: {e}")

    # 4b. OpenAI Connection
    if sheets_ok:
        try:
            from modules.chatgpt import ChatGPTCaller
            caller = ChatGPTCaller()
            if not caller.api_key or caller.api_key.startswith("sk-YOUR"):
                log_test("OpenAI API Connection", False, "Skipped: OpenAI API key is not set.")
            else:
                # Do a tiny test completion
                import urllib.request
                import urllib.error
                payload = {
                    "model": caller.model,
                    "messages": [{"role": "user", "content": "Ping"}],
                    "max_tokens": 5
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {caller.api_key}"
                }
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(caller.endpoint, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=10) as response:
                    res = json.loads(response.read().decode("utf-8"))
                    if "choices" in res:
                        log_test("OpenAI API Connection", True)
                    else:
                        all_ok = log_test("OpenAI API Connection", False, "Invalid API response structure.")
        except Exception as e:
            all_ok = log_test("OpenAI API Connection", False, f"Failed to connect to OpenAI: {e}")

    print("\n" + "=" * 60)
    if all_ok:
        print("DIAGNOSTICS SUCCESSFUL: System is configured correctly!")
    else:
        print("DIAGNOSTICS FAILED: Please fix the errors listed above before running.")
    print("=" * 60)
    return all_ok

if __name__ == "__main__":
    sys.exit(0 if run_diagnostics() else 1)
