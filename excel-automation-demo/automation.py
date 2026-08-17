from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "output.xlsx"

input_files = sorted(BASE_DIR.glob("input_*.xlsx"))

if not input_files:
    raise FileNotFoundError("No input_*.xlsx files were found.")

frames = [pd.read_excel(file) for file in input_files]
df = pd.concat(frames, ignore_index=True)

# Clean leading/trailing spaces in all text columns.
text_columns = df.select_dtypes(include="object").columns
df[text_columns] = df[text_columns].apply(lambda col: col.str.strip())

# Remove duplicate rows and sort by Order ID.
df = df.drop_duplicates()
df = df.sort_values(by="Order ID").reset_index(drop=True)

# Export one clean consolidated Excel file.
df.to_excel(OUTPUT_FILE, index=False)

print(f"Done: {len(input_files)} files combined.")
print(f"Final rows: {len(df)}")
print(f"Output: {OUTPUT_FILE}")
