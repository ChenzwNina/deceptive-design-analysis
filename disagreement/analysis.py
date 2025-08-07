import json
import os
from collections import defaultdict, Counter

def analyze_annotations(path):
    with open(path) as f:
        data = json.load(f)

    selected_by_one = defaultdict(list)       # category -> [widget_id]
    missed_by_one = defaultdict(list)         # category -> [widget_id]
    missed_by_annotator = defaultdict(Counter)  # category -> annotator -> count
    selected_by_annotator = defaultdict(Counter)  # category -> annotator -> count (NEW)


    widget_annotations = defaultdict(dict)

    for entry in data:
        assert len(entry) == 1
        full_key = list(entry.keys())[0]  # e.g., "100Leica"
        widget_id = ''.join(filter(str.isdigit, full_key))
        rater = full_key[len(widget_id):]
        content = entry[full_key]

        # Extract selected categories
        selections = content["value"]["dark_pattern_type"]
        if selections[2].get("not-sure"):
            continue  # skip uncertain label
        elif selections[2].get("no-dd"):
            selected = set()
        else:
            selected = {k for k, v in selections[0].items() if v == 1}

        widget_annotations[widget_id][rater] = selected

    for widget_id, annots in widget_annotations.items():
        if len(annots) < 2:
            continue

        category_votes = defaultdict(set)
        for rater, selected in annots.items():
            for cat in selected:
                category_votes[cat].add(rater)

        for category, raters in category_votes.items():
            if len(raters) == 1:
                selected_by_one[category].append(widget_id)
                only_rater = list(raters)[0]
                selected_by_annotator[category][only_rater] += 1  # NEW
            elif len(raters) == 2 and len(annots) == 3:
                missing = set(annots.keys()) - raters
                if len(missing) == 1:
                    missed_by_one[category].append(widget_id)
                    missed_by_annotator[category][list(missing)[0]] += 1

    return selected_by_one, missed_by_one, missed_by_annotator, selected_by_annotator


# ========== Run Analysis ==========
round_number = 2
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", f"extract_data/3raters/round{round_number}/valid_data.json"))

if __name__ == "__main__":
    selected_by_one, missed_by_one, missed_by_annotator, selected_by_annotator = analyze_annotations(path)

    # Print summaries
    for cat in sorted(set(selected_by_one) | set(missed_by_one)):
        print(f"\nCategory: {cat}")
        print(f"  Selected by only 1 annotator in {len(selected_by_one[cat])} widgets")
        print(f"    Selected by annotators: {dict(selected_by_annotator[cat])}")  # NEW
        print(f"  Missed by only 1 annotator in {len(missed_by_one[cat])} widgets")
        print(f"    Missed by annotators: {dict(missed_by_annotator[cat])}")

