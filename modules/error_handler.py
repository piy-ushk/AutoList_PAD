import json, os, time, sys, traceback
from datetime import datetime, timezone
from enum import Enum


class ErrorCode(Enum):
    E001 = ("E001", "Google Sheet read failure", "HIGH")
    E002 = ("E002", "ChatGPT API call failure", "HIGH")
    E003 = ("E003", "ChatGPT JSON parse failure", "MEDIUM")
    E004 = ("E004", "VeRO keyword detected", "MEDIUM")
    E005 = ("E005", "Duplicate listing detected", "MEDIUM")
    E006 = ("E006", "Monodas login failure", "HIGH")
    E007 = ("E007", "Monodas form field not found", "HIGH")
    E008 = ("E008", "Monodas Draft save failure", "HIGH")
    E009 = ("E009", "eBay Item ID capture failure", "HIGH")
    E010 = ("E010", "Image upload failure", "MEDIUM")
    E011 = ("E011", "Google Sheet write failure", "HIGH")
    E012 = ("E012", "Item Specifics field missing", "LOW")
    E013 = ("E013", "Title exceeds 80 characters", "MEDIUM")
    E014 = ("E014", "Required field empty", "MEDIUM")
    E015 = ("E015", "Monodas session expired", "MEDIUM")

    @property
    def code(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @property
    def severity(self):
        return self.value[2]

    @classmethod
    def from_code(cls, code_str):
        for code in cls:
            if code.code == code_str:
                return code
        return None


RECOVERABLE_ERRORS = {ErrorCode.E015, ErrorCode.E002}
UNRECOVERABLE_ERRORS = {
    ErrorCode.E007, ErrorCode.E008, ErrorCode.E009,
    ErrorCode.E006, ErrorCode.E001, ErrorCode.E011,
}


class ErrorHandler:
    def __init__(self, sheet_logger=None):
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        self.screenshot_dir = os.path.join(self.log_dir, "error_screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(os.path.join(self.log_dir, "run_logs"), exist_ok=True)
        self.sheet_logger = sheet_logger

    def set_sheet_logger(self, sheet_logger):
        self.sheet_logger = sheet_logger

    def _make_screenshot_filename(self, sku):
        safe_sku = sku.replace('/', '_').replace('\\', '_')
        return f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{safe_sku}.png"

    def capture_screenshot(self, sku):
        screen_path = os.path.join(self.screenshot_dir, self._make_screenshot_filename(sku))
        try:
            import subprocess
            subprocess.run([
                "powershell", "-Command",
                "Add-Type -AssemblyName System.Windows.Forms; "
                f"[System.Windows.Forms.SendKeys]::SendWait('{{PRTSC}}')"
            ], capture_output=True, timeout=10)
        except Exception:
            return ""
        return screen_path

    def log_error(self, sku, error_code, error_message, error_field=None, pad_step=None, screenshot_path=None):
        error_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sku": sku,
            "error_code": error_code.code,
            "error_type": error_code.description,
            "error_field": error_field or "",
            "error_message": error_message,
            "pad_step": pad_step or "",
            "severity": error_code.severity,
            "screenshot_path": screenshot_path or "",
        }
        log_json_path = os.path.join(self.log_dir, "run_logs", f"error_{error_code.code}_{sku}.json")
        with open(log_json_path, "w", encoding="utf-8") as f:
            json.dump(error_data, f, ensure_ascii=False, indent=2)
        if self.sheet_logger:
            try:
                self.sheet_logger.log_error(
                    sku=sku,
                    error_type=error_code.description,
                    error_field=error_field or "",
                    error_message=error_message,
                    pad_step=pad_step or "",
                    screenshot_path=screenshot_path or "",
                )
            except Exception:
                pass
        return error_data

    def log_chatgpt_error(self, sku, error_message):
        self.log_error(sku=sku, error_code=ErrorCode.E002, error_message=error_message, pad_step="Generate_AI_Content")

    def log_json_parse_error(self, sku, error_message):
        self.log_error(sku=sku, error_code=ErrorCode.E003, error_message=error_message, pad_step="Generate_AI_Content")

    def log_vero_error(self, sku, vero_keywords):
        self.log_error(
            sku=sku, error_code=ErrorCode.E004,
            error_message=f"VeRO keywords found: {', '.join(vero_keywords)}",
            pad_step="Validate_Row",
        )

    def log_duplicate_error(self, sku, error_message):
        self.log_error(sku=sku, error_code=ErrorCode.E005, error_message=error_message, pad_step="Validate_Row")

    def log_monodas_draft_error(self, sku, error_message):
        self.log_error(sku=sku, error_code=ErrorCode.E008, error_message=error_message, pad_step="Save_Draft_To_Monodas")

    def log_item_id_error(self, sku, error_message):
        self.log_error(sku=sku, error_code=ErrorCode.E009, error_message=error_message, pad_step="Save_Draft_To_Monodas")

    def retry_with_backoff(self, func, *args, **kwargs):
        backoff_times = [5, 15, 45]
        for attempt, delay in enumerate(backoff_times):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < len(backoff_times) - 1:
                    time.sleep(delay)
                else:
                    raise e
        return None