import pandas as pd
import sys

file_path = r'client\パテントロール用語集・VERO資料.xlsx'
dfs = pd.read_excel(file_path, sheet_name=None)

for sheet_name in ['パテントトロール', 'VeRO']:
    df = dfs[sheet_name]
    for row_idx, row in df.iterrows():
        for col_idx, val in enumerate(row):
            val_str = str(val).lower()
            if 'アイテム' in val_str or 'global' in val_str:
                print(f"Sheet '{sheet_name}', Row {row_idx}, Col {col_idx}: {val}")
