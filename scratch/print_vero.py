import pandas as pd
import glob
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
file_path = glob.glob(r'client\*.xlsx')[0]
dfs = pd.read_excel(file_path, sheet_name=None)
df = dfs['VeRO']
print("--- VeRO Sheet ---")
for col in df.columns:
    print(f"\nCol: {col}")
    vals = df[col].dropna().astype(str).tolist()
    print(vals)
