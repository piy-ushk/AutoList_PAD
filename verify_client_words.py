from modules.gsheets import GoogleSheetsClient
from modules.vero_checker import load_keyword_dictionary
import re

sheet_client = GoogleSheetsClient()
local_vero = load_keyword_dictionary()
sheet_vero = sheet_client.get_vero_keywords()
all_vero = local_vero + sheet_vero

test_words = ['MOTOGP', 'Hatsune Miku', 'Epoch', 'Barbie', 'Benefit', 'Chevrolet', 'Ironman', 'Lamborghini', 'Nanoblock', 'NARUTO', 'Nendoroid', 'NEON GENESIS EVANGELION', 'Nike', 'Playing Card', 'Snoopy', 'SONIC THE HEDGEHOG', 'TETRIS', 'Toyota']

print("--- VeRO Patent Troll Keywords Verification ---")
for word in test_words:
    found = False
    for entry in all_vero:
        keyword = entry.get("keyword", "").lower().strip()
        if not keyword: continue
        
        # We test by putting the word in a dummy sentence to simulate AI output
        dummy_sentence = f"This is a {word} item."
        dummy_sentence_lower = dummy_sentence.lower()
        
        match_type = entry.get("match_type", "contains")
        if match_type == "exact":
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            if re.search(r"\b" + pattern.pattern + r"\b", dummy_sentence_lower, re.IGNORECASE):
                found = True
                break
        elif match_type == "contains":
            if keyword in dummy_sentence_lower:
                found = True
                break
                
    if found:
        print(f"[BLOCKED] The term '{word}' is successfully recognized and will block the listing.")
    else:
        print(f"[WARNING] The term '{word}' is NOT recognized!")
