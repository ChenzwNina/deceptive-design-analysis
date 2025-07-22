import json
import pandas as pd
from collections import defaultdict

with open("majority_vote/majority_label.json", "r") as f:
    data = json.load(f)

total_count = defaultdict(int)
dark_count = defaultdict(int)

for idx, item in data.items():
    component_type = item["component"]
    dark_votes = item["pattern"][0]["dark pattern"]

    total_count[component_type] += 1

    if sum(dark_votes) >= 2:
        dark_count[component_type] += 1

results = []

for comp_id in sorted(total_count.keys()):
    total = total_count[comp_id]
    dark = dark_count.get(comp_id, 0)
    percentage = round(dark / total * 100, 2)
    results.append({
        "Component Type ID": comp_id,
        "Total Count": total,
        "With Dark Pattern": dark,
        "Percentage": f"{percentage} %"
    })

df = pd.DataFrame(results)
print(df)
