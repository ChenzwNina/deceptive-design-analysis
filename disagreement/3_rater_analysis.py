import json
import os
from collections import defaultdict, Counter

def analyze_annotations(path):
    with open(path) as f:
        data = json.load(f)

    # Counts
    selected_by_one = defaultdict(list)            # category -> [widget_id]
    missed_by_one = defaultdict(list)              # category -> [widget_id]
    selected_by_annotator = defaultdict(Counter)   # category -> annotator -> count
    missed_by_annotator = defaultdict(Counter)     # category -> annotator -> count

    # NEW: widget lists per annotator
    selected_by_one_widgets = defaultdict(lambda: defaultdict(list))  # cat -> annotator -> [widget_id]
    missed_by_one_widgets = defaultdict(lambda: defaultdict(list))    # cat -> annotator -> [widget_id]

    # First pass: group rater selections by widget
    widget_annotations = defaultdict(dict)  # widget_id -> rater -> set(categories)

    for entry in data:
        assert len(entry) == 1
        full_key = list(entry.keys())[0]           # e.g., "100Leica"
        widget_id = ''.join(filter(str.isdigit, full_key))  # "100"
        rater = full_key[len(widget_id):]          # "Leica"
        content = entry[full_key]

        dpt = content["value"]["dark_pattern_type"]
        if dpt[2].get("not-sure"):
            continue                               # skip unsure
        elif dpt[2].get("no-dd"):
            selected = set()                       # explicit no-selection
        else:
            selected = {k for k, v in dpt[0].items() if v == 1}

        widget_annotations[widget_id][rater] = selected

    # Second pass: compute per-category vote patterns
    for widget_id, annots in widget_annotations.items():
        if len(annots) < 2:
            continue  # need at least 2 raters to say anything useful

        # category -> set(raters who selected it)
        category_votes = defaultdict(set)
        for rater, selected in annots.items():
            for cat in selected:
                category_votes[cat].add(rater)

        for cat, raters in category_votes.items():
            # Case A: exactly one annotator selected this category
            if len(raters) == 1:
                only_rater = next(iter(raters))
                selected_by_one[cat].append(widget_id)
                selected_by_annotator[cat][only_rater] += 1
                selected_by_one_widgets[cat][only_rater].append(widget_id)

            # Case B: exactly one annotator missed this category (2 of 3 selected)
            elif len(raters) == 2 and len(annots) == 3:
                missing = set(annots.keys()) - raters
                if len(missing) == 1:
                    missing_rater = next(iter(missing))
                    missed_by_one[cat].append(widget_id)
                    missed_by_annotator[cat][missing_rater] += 1
                    missed_by_one_widgets[cat][missing_rater].append(widget_id)

    return (
        selected_by_one,
        missed_by_one,
        selected_by_annotator,
        missed_by_annotator,
        selected_by_one_widgets,
        missed_by_one_widgets,
    )


# ========== Run / Print ==========

if __name__ == "__main__":
    round_number = 1
    path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", f"extract_data/3raters/round{round_number}/valid_data.json"
    ))

    (selected_by_one,
     missed_by_one,
     selected_by_annotator,
     missed_by_annotator,
     selected_by_one_widgets,
     missed_by_one_widgets) = analyze_annotations(path)

    all_cats = sorted(set(selected_by_one) | set(missed_by_one))
    for cat in all_cats:
        # Selected-by-one summary
        print(f"\nCategory: {cat}")
        print(f"  Selected by only 1 annotator in {len(selected_by_one[cat])} widgets")
        print(f"    Selected by annotators: {dict(selected_by_annotator[cat])}")
        for annot, wids in selected_by_one_widgets[cat].items():
            # show widget IDs as ints if you like
            try_ids = []
            for w in wids:
                try:
                    try_ids.append(int(w))
                except:
                    try_ids.append(w)
            print(f"    {{'{annot}': {sorted(try_ids)}}}")

        # Missed-by-one summary
        print(f"  Missed by only 1 annotator in {len(missed_by_one[cat])} widgets")
        print(f"    Missed by annotators: {dict(missed_by_annotator[cat])}")
        for annot, wids in missed_by_one_widgets[cat].items():
            try_ids = []
            for w in wids:
                try:
                    try_ids.append(int(w))
                except:
                    try_ids.append(w)
            print(f"    {{'{annot}': {sorted(try_ids)}}}")
