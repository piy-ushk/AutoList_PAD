import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.gsheets import GoogleSheetsClient

def reset_and_fix_for_validation():
    c = GoogleSheetsClient()
    h = c.api.read_range(c.tabs['listings'], 'A1:BC1')[0]
    rows = c.api.read_range(c.tabs['listings'], 'A2:BC7')
    for i, r in enumerate(rows):
        r.extend([''] * (len(h) - len(r)))
        # Reset statuses
        r[h.index('Listing_Status')] = 'pending_ai'
        r[h.index('Validation_Status')] = ''
        
        # Fix VeRO keywords in Title
        title = r[h.index('商品名_JP')]
        title = title.replace('Bullmark', 'Vintage Brand').replace('Pop-up', '3D')
        r[h.index('商品名_JP')] = title
        
        # Ensure they have unique URLs to avoid duplicates
        r[h.index('仕入URL')] = f'https://example.com/unique_{i}.jpg'

    c.api.write_range(c.tabs['listings'], 'A2:BC7', rows)
    print("Done resetting and fixing!")

if __name__ == "__main__":
    reset_and_fix_for_validation()
