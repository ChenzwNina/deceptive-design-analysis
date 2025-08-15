# The script is to clean the data in a format that inter_rater_relaibility.py could run to count reliability
import json
import os
import re

labels = ["immortal-accounts-vote", "dead-end-vote", "no-way-back", "price-comparison-prevention-vote", "intermediate-currency-vote", "discount-framing-manipulation", "privacy-maze-vote", "extra-burden", "disguised-ad-vote", "sneak-into-basket-vote", "drip-pricing-vote", "reference-pricing-vote", "conflicting-information-vote", "information-without-context-vote", "false-hierarchy-vote", "visual-prominence-vote", "bundling-vote", "pressured-selling-vote", "bad-defaults-sum", "cuteness-vote", "positive-vote", "trick-questions-sum", "choice-overload-sum", "hidden-information-sum", "wrong-language-vote", "complex-language-vote", "feedward-ambiguity-sum", "nagging-sum", "forced-continuity-sum", "forced-registration-sum", "privacy-zukering-vote", "friend-spam-vote", "address-book-leeching-vote", "social-pyramid-vote", "pay-to-play-vote", "grinding-vote", "auto-play-vote", "high-demand-vote", "low-stock-vote", "endorsement-vote", "parasocial-vote", "activity-messages-vote", "countdown-timer-vote", "limited-time-vote", "confirmshaming-vote"]

def load_file(path):
    with open(path) as f:
        data = json.load(f)
        return data

def clean_existing_label(input_dict, labels):

    # If the categories not in the right labels, remove it
    new_dict = input_dict.copy()
    for key in new_dict.keys():
        if key not in labels:
            del input_dict[key]
    
    # If right label categories not in dict, add it and make number as 0
    for item in labels:
        if item not in new_dict.keys():
            input_dict[item] = 0
    
    for key, value in input_dict.copy().items():
        if value == 0:
            del input_dict[key]

def format_data(download_path, data, labels):
    total_label = {}
    for item in data:

        for key, value in item.items():
            widget_label = {}

            # Get index and rater
            index_list = re.findall("[0-9]+", key)
            index = index_list[0]
            index_int = int(index)
            rater = value["rater"]
            print("Current index: ", index_int, "Labeled by", rater)

            if str(index_int) not in total_label:
                print("Not in total_label")
                total_label[str(index_int)] = []
            
            if value["value"]["dark_pattern_type"] == "(none)":
                print(f"The widget index {index_int} has not been labeled by {rater}")
                continue
            
            # If DD is selected as none
            if value["value"]["dark_pattern_type"][2]["no-dd"]:
                widget_labels = {}
            else:
                widget_labels = value["value"]["dark_pattern_type"][0]
                clean_existing_label(widget_labels, labels)
                if not widget_labels:
                    print(f"The widget index {index_int} has not been labeled by {rater}")
                    continue
            total_label[str(index_int)].append(widget_labels)
    print("Label cleaning is finished")
    clean_out_not_qualified_data(download_path, total_label)
    

def clean_out_not_qualified_data(download_path, units):
    not_qualified = {}
    qualified = {}
    for index, value in units.items():
        if len(value) != 2:
            not_qualified[index] = value
        else:
            qualified[index] = value
    with open(f"{download_path}/rater_not_equal_to_2.json", "w") as f:
                json.dump(not_qualified, f, indent=4)
    
    with open(f"{download_path}/qualified.json", "w") as f:
                json.dump(qualified, f, indent=4)

round_number = 3
folder_name = f"round{round_number}/hanyu-luna"
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "extract_data", f"2raters/{folder_name}/valid_data.json"))
data  = load_file(path)

download_path = f"{folder_name}"
format_data(download_path, data, labels)

