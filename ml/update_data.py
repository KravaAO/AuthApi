import json
from dateutil.parser import parse as date_parse

# Завантаження існуючого датасету
with open("column_dataset_large.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Функція перевірки, чи є колонка датою
def is_date_column(values):
    success = 0
    for val in values:
        try:
            parse(val.strip(), fuzzy=False)
            success += 1
        except:
            pass
    return success / len(values) > 0.8

# Список додаткових прикладів дат
extra_date_examples = [
    ["01/01/2020", "15/03/2021", "20/08/2022", "30/12/2023"],
    ["2020-01-01", "2021-02-02", "2022-03-03", "2023-04-04"],
    ["Jan 1, 2020", "Feb 2, 2021", "Mar 3, 2022", "Apr 4, 2023"],
    ["01.01.2020", "02.02.2021", "03.03.2022", "04.04.2023"],
    ["2020/01/01", "2021/02/02", "2022/03/03", "2023/04/04"],
    ["1st Jan 2020", "2nd Feb 2021", "3rd Mar 2022", "4th Apr 2023"],
    ["Monday, January 1, 2020", "Tuesday, February 2, 2021"],
    ["2020", "2021", "2022", "2023"]
]

# Створюємо нові записи для JSON
for i, values in enumerate(extra_date_examples):
    data.append({
        "column_name": f"extra_date_{i+1}",
        "values": values,
        "type": "date",
        "source": "synthetic"
    })

# Зберігаємо оновлений JSON
extended_path = "column_dataset_large_extended.json"
with open(extended_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

extended_path
