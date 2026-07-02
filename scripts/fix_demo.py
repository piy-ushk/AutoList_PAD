import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.gsheets import GoogleSheetsClient

def fix_demo_validation_fields():
    c = GoogleSheetsClient()
    h = c.api.read_range(c.tabs['listings'], 'A1:BC1')[0]
    rows = c.api.read_range(c.tabs['listings'], 'A2:BC7')
    for i, r in enumerate(rows):
        r.extend([''] * (len(h) - len(r)))
        r[h.index('管理ID_SKU')] = f'TEST-DEMO-{i}'
        r[h.index('仕入URL')] = 'https://example.com'
        r[h.index('販売形式')] = 'Buy It Now'
        r[h.index('出品価格_USD')] = '100.00'
        r[h.index('担当者')] = 'DemoStaff'
        r[h.index('Listing_Status')] = 'pending_ai'
    c.api.write_range(c.tabs['listings'], 'A2:BC7', rows)
    print("Done fixing validation fields")

if __name__ == "__main__":
    fix_demo_validation_fields()
