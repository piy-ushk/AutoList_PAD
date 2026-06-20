import pandas as pd
import glob
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

file_path = glob.glob(r'client\*.xlsx')[0]
dfs = pd.read_excel(file_path, sheet_name=None)
for sheet_name, df in dfs.items():
    print(f'Sheet: {sheet_name}')
    for col in df.columns:
        cnt = df[col].dropna().astype(str).str.strip().ne('').sum()
        print(f'  {col}: {cnt} items')
