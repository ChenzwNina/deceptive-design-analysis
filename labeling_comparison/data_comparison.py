import json
import pandas as pd
from collections import defaultdict

# Load the data from file
with open("all_label.json", "r") as f:
    data = json.load(f)

# Build index -> rater -> selected categories (including "no-dd")
index_votes = defaultdict(lambda: defaultdict(set))  # index -> rater -> set(categories)

for entry in data:
    for key, value in entry.items():
        index = ''.join(filter(str.isdigit, key))  # Extract index from "100luna" etc.
        rater = value["rater"]
        dark_pattern_type = value["value"]["dark_pattern_type"]

        if dark_pattern_type[2].get("no-dd", False):
            # Rater explicitly marked no dark pattern
            index_votes[index][rater] = {"no-dd"}
        else:
            # Collect selected categories with vote == 1
            for category, vote in dark_pattern_type[0].items():
                if vote == 1:
                    index_votes[index][rater].add(category)

# Analyze for consensus vs. disagreement
results = {}

for index, rater_map in index_votes.items():
    # Turn sets into immutable frozensets for comparison
    unique_sets = set(frozenset(categories) for categories in rater_map.values())

    if len(unique_sets) == 1:
        # All raters picked the exact same categories
        consensus = list(next(iter(unique_sets)))
        results[index] = {"consensus": consensus}
    else:
        # Raters differ in what they selected
        disagreement = {rater: list(cats) for rater, cats in rater_map.items()}
        results[index] = {"disagreement": disagreement}

# Convert to a DataFrame
df = pd.DataFrame([
    {"index": idx, "status": "consensus", "categories": val["consensus"]} if "consensus" in val
    else {"index": idx, "status": "disagreement", "details": val["disagreement"]}
    for idx, val in results.items()
])

# Optional: save to CSV
df.to_csv("rater_consensus_results.csv", index=False)

# Preview first few rows
print(df.head())
