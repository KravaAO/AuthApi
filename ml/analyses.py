import os
import glob
import pandas as pd
import json
from dateutil.parser import parse as date_parse

def guess_type(values):
    numbers, dates, bools = 0, 0, 0
    for val in values:
        val = str(val).strip()
        try:
            float(val.replace(",", "").replace(" ", "").replace("₴", "").replace("$", ""))
            numbers += 1
        except:
            pass
        try:
            date_parse(val, fuzzy=False)
            dates += 1
        except:
            pass
        if val.lower() in ["yes", "no", "true", "false", "так", "ні"]:
            bools += 1

    total = len(values)
    if total == 0:
        return "unknown"
    if numbers / total > 0.8:
        return "number"
    elif dates / total > 0.8:
        return "date"
    elif bools / total > 0.8:
        return "boolean"
    elif total > len(set(values)) * 2:
        return "category"
    else:
        return "text"

def collect_columns_from_csv(folder_path, max_files=10000):
    csv_files = glob.glob(os.path.join(folder_path, '**', '*.csv'), recursive=True)
    csv_files = csv_files[:max_files]
    column_data = []

    for path in csv_files:
        try:
            df = pd.read_csv(path, dtype=str, nrows=50)
            for col in df.columns:
                values = df[col].dropna().tolist()
                if len(values) >= 5:
                    col_type = guess_type(values)
                    column_data.append({
                        "column_name": col,
                        "values": values[:10],
                        "type": col_type,
                        "source": os.path.basename(path)
                    })
        except Exception as e:
            continue

    return column_data

if __name__ == "__main__":
    # Шлях до папки з розпакованими CSV
    folder = "unzipped"
    output = "column_dataset_large.json"

    dataset = collect_columns_from_csv(folder, max_files=10000)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(dataset)} labeled columns to {output}")
