import pandas as pd
import glob
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
file_path = glob.glob(r'client\*.xlsx')[0]
dfs = pd.read_excel(file_path, sheet_name=None)
df = dfs['パテントトロール']
print("--- PT Sheet ---")
if '2-D artwork' in df.columns:
    print(df['2-D artwork'].head(20).tolist())
else:
    print("Column not found")
