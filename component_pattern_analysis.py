import json
from collections import defaultdict
import pandas as pd

with open("majority_vote/majority_label.json", "r") as f:
    data = json.load(f)

component_pattern_counts = defaultdict(lambda: defaultdict(int))

for idx, item in data.items():
    component_id = item["component"]
    dark_votes = item["pattern"][0]["dark pattern"]

    if sum(dark_votes) >= 2:
        low_level_patterns = item["pattern"][1].get("low-level", [])
        for pattern in low_level_patterns:
            component_pattern_counts[component_id][pattern] += 1

rows = []

for component_id, patterns in component_pattern_counts.items():
    for pattern, count in patterns.items():
        rows.append({
            "Component Type ID": component_id,
            "Low-level Dark Pattern": pattern,
            "Count": count
        })

df = pd.DataFrame(rows)

df = df.sort_values(by=["Component Type ID", "Count"], ascending=[True, False])

print(df)


