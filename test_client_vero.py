from modules.gsheets import GoogleSheetsClient
from modules.vero_checker import load_keyword_dictionary, scan_keywords

sheet_client = GoogleSheetsClient()
local_vero = load_keyword_dictionary()
sheet_vero = sheet_client.get_vero_keywords()
all_vero = local_vero + sheet_vero

# Test Title
title = 'Hatsune Miku MOTOGP Epoch Barbie Benefit Chevrolet Ironman'
# Test Description
description = 'This is a Lamborghini Nanoblock NARUTO Nendoroid NEON GENESIS EVANGELION Nike Playing Card Snoopy SONIC THE HEDGEHOG TETRIS Toyota.'

result = scan_keywords(title, description, all_vero)
print(f"VeRO Check Passed?: {result['passed']}")
print("Flagged Keywords:")
for kw in result['flagged_keywords']:
    print(f" - {kw}")
