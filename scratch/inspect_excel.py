import pandas as pd
import sys
import codecs
import glob

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

excel_files = glob.glob(r'client\*.xlsx')
if not excel_files:
    print("No excel file found!")
    sys.exit(1)

file_path = excel_files[0]
print(f"Reading file: {file_path}")

dfs = pd.read_excel(file_path, sheet_name=None)

for sheet_name, df in dfs.items():
    print(f"\n--- Sheet: {sheet_name} ---")
    print("Columns:", df.columns.tolist())
    print("First 3 rows:")
    print(df.head(3).to_string())
