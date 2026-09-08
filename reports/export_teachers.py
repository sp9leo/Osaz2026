"""
python export_teachers.py

Reads teachers_template.xlsx → writes teachers.json
"""
import sys
import json
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("pip install openpyxl")
    sys.exit(1)

BASE_DIR = Path(__file__).parent
XLSX = BASE_DIR / "teachers_template.xlsx"
JSON = BASE_DIR / "teachers.json"

wb = openpyxl.load_workbook(str(XLSX))
ws = wb["Učitelji"]

teachers = []
for row in ws.iter_rows(min_row=2, values_only=True):
    name, display, pin = row[0], row[1], row[2]
    if not name or not pin:
        continue
    teachers.append({
        "name": str(name).strip(),
        "display": str(display).strip() if display else str(name).strip(),
        "pin": str(int(pin)).strip(),
    })

config = {
    "admin_pin": "9999",
    "teachers": teachers,
}

with open(JSON, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f"Done: {len(teachers)} teachers -> {JSON.name}")
