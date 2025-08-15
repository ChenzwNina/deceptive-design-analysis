import json
import os
import pdb
import copy

class MajorityAnalyzer():
    def __init__(self, path, output_path, output_no_clear_majority):
        """
        Initialize with a json file path
        """
        with open(path) as f:
            self.data = json.load(f)
        label_cleaned, no_clear_majority_widget = self.iterate()

        with open(output_path, "w") as f2:
            json.dump(label_cleaned, f2, indent = 4)
        
        with open(output_no_clear_majority, "w") as f2:
            json.dump(no_clear_majority_widget, f2, indent = 4)
        
        print("Majority vote is done and files are saved!")
    
    def category_mapping(self):
        with open("category_mapping.json") as f:
            mapping = json.load(f)
        return mapping
    
    def check_low_level(self, index_key, original_value, low_level, majority_dict, no_clear_majority_dict):

        # Load category mapping from json
        mapping = self.category_mapping()
        original_copy = copy.deepcopy(original_value)
        majority_dict[index_key] = original_copy
        majority_dict[index_key]["pattern"][1]["low-level"] = []
        majority_dict[index_key]["pattern"][2]["meso-level"] = []
        majority_dict[index_key]["pattern"][3]["high-level"] = []

        for key, value in low_level.items():
            print("key:", key, "value:", value)
            if value >= 2:
                name = mapping[key]["name"]
                meso = mapping[key].get("meso-level", "")
                high = mapping[key]["high-level"]
                majority_dict[index_key]["pattern"][1]["low-level"].append(name)
                majority_dict[index_key]["pattern"][2]["meso-level"].append(meso)
                majority_dict[index_key]["pattern"][3]["high-level"].append(high)
    
    def check_meso_level(self, index_key, original_value, meso_level, majority_dict, no_clear_majority_dict):
        mapping = self.category_mapping()

        for key, value in meso_level.items():
            if key in mapping:

                if value >= 2:

                    meso = mapping[key]["name"]
                    high = mapping[key]["high-level"]
                    majority_dict[index_key]["pattern"][2]["meso-level"].append(meso)
                    majority_dict[index_key]["pattern"][3]["high-level"].append(high)

        if not majority_dict[index_key]["pattern"][1]["low-level"] and not majority_dict[index_key]["pattern"][2]["meso-level"] and not majority_dict[index_key]["pattern"][3]["high-level"]:
            
            # Remove the index from the majority dict if no category has passed majority
            majority_dict.pop(index_key, None)

            # Add it to no_clear_majority_dict
            no_clear_majority_dict[index_key] = copy.deepcopy(original_value)
            no_clear_majority_dict[index_key]["Reason"] = "Widget majority is not clear"
        else:
            majority_dict[index_key]["pattern"][2]["meso-level"] = list(set(majority_dict[index_key]["pattern"][2]["meso-level"]))
            majority_dict[index_key]["pattern"][3]["high-level"] = list(set(majority_dict[index_key]["pattern"][3]["high-level"]))


    
    def iterate(self):
        majority_dict = {}
        no_clear_majority_dict = {}
        for key, value in self.data.items():
            # print(key, value)
            dark_pattern_selection = value["pattern"][0]["dark pattern"]

            # Number of labelers is not equal to 3, add to no_clear_majority_dict, go to next widget
            labeler_number = len(dark_pattern_selection)
            if labeler_number != 3:
                no_clear_majority_dict[key] = copy.deepcopy(value)
                no_clear_majority_dict[key]["Reason"] = "Labeler number is not equal to 3"
                continue
            
            # 2 or more than 2 labelers think the widget does not have dd, add to majority_dict, go to next widget
            if not sum(bool(x) for x in dark_pattern_selection) >= 2:
                majority_dict[key] = value
                majority_dict[key]["pattern"][1]["low-level"] = []
                majority_dict[key]["pattern"][2]["meso-level"] = []
                majority_dict[key]["pattern"][3]["high-level"] = []
                continue

            # 2 or more than 2 labelers think the widget has dd, check any category has majority votes
            low_level, meso_level = value["pattern"][1]["low-level"], value["pattern"][2]["meso-level"]
            self.check_low_level(key, value, low_level, majority_dict, no_clear_majority_dict)
            self.check_meso_level(key, value, meso_level, majority_dict, no_clear_majority_dict)

        print(f"{len(majority_dict)} widgets pass majority votes")
        print(f"{len(no_clear_majority_dict)} widgets has not passed majority votes")
        return majority_dict, no_clear_majority_dict

round_number = 1
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "label_cleaning", f"round{round_number}/cleaned_label.json"))

folder_name = f"round{round_number}"

if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

analyzer = MajorityAnalyzer(path, f"{folder_name}/majority_label.json", f"{folder_name}/no_clear_majority.json")