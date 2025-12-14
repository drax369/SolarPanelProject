import json
import pandas as pd
from pathlib import Path

SITE_SUM_PATH = Path("outputs/site_summaries.json")
OUT_EXCEL_PATH = Path("outputs/output_results.xlsx")

def main():
    if not SITE_SUM_PATH.exists():
        print("site_summaries.json not found:", SITE_SUM_PATH.resolve())
        return

    with SITE_SUM_PATH.open("r", encoding="utf-8") as f:
        site_records = json.load(f)

    # convert to DataFrame
    df = pd.DataFrame(site_records)

    # write to Excel
    df.to_excel(OUT_EXCEL_PATH, index=False, sheet_name="Results")

    print("Wrote results to:", OUT_EXCEL_PATH.resolve())
    print(f"Total records: {len(df)}")

if __name__ == "__main__":
    main()
