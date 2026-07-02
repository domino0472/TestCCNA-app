import json

with open("baza_pytan.json", "r", encoding="utf-8") as f:
    qs = json.load(f)

for q in qs:
    if q["id"] == 13:
        print(json.dumps(q, indent=2))
        break
