import os
import re

MAIN_PY_PATH = os.path.join(os.path.dirname(__file__), '..', 'main.py')

def switch_mode(enable_test_mode):
    with open(MAIN_PY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if enable_test_mode:
        new_content = re.sub(r'ONLY_PROCESS_TEST_CARDS\s*=\s*(True|False)', 'ONLY_PROCESS_TEST_CARDS = True', content)
    else:
        new_content = re.sub(r'ONLY_PROCESS_TEST_CARDS\s*=\s*(True|False)', 'ONLY_PROCESS_TEST_CARDS = False', content)
        
    with open(MAIN_PY_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

def check_current_mode():
    with open(MAIN_PY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'ONLY_PROCESS_TEST_CARDS\s*=\s*(True|False)', content)
    if match:
        return match.group(1) == 'True'
    return False

def main():
    print("==========================================")
    print("AutoList - Switch Mode (動作モード切替)")
    print("==========================================")
    
    is_demo = check_current_mode()
    
    if is_demo:
        print("Current Mode: [DEMO MODE] (Processing ONLY 'TEST-' SKUs)")
    else:
        print("Current Mode: [LIVE MODE] (Processing ALL SKUs normally)")
        
    print("\nSelect the mode you want to switch to:")
    print("1. DEMO MODE (Safe UAT testing - process only 'TEST-' items)")
    print("2. LIVE MODE (Process all actual data)")
    print("3. CANCEL")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == '1':
        switch_mode(True)
        print("\n[SUCCESS] Switched to DEMO MODE (ONLY_PROCESS_TEST_CARDS = True)!")
    elif choice == '2':
        switch_mode(False)
        print("\n[SUCCESS] Switched to LIVE MODE (ONLY_PROCESS_TEST_CARDS = False)!")
    elif choice == '3':
        print("\nCancelled.")
    else:
        print("\nInvalid choice. Cancelled.")

if __name__ == "__main__":
    main()
