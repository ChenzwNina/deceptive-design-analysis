# Input index to filter by rounds
import json
import re
import os

def find_round(data, start_index, end_index, rater_name):
    error_list = []
    selected_list = []
    double_check_dict = {}
    double_check_no_label = []
    double_check_unsure = []
    double_check_index = []
    for item in data:
        for key, value in item.items():

            # Get index and rater
            index_list = re.findall("[0-9]+", key)
            rater = value["rater"]
            index = index_list[0]
            index_int = int(index)

            # If the widget index is not within selection, continue to next item
            if index_int < start_index or index_int > end_index:
                continue

            if value["rater"] not in rater_name:
                print(f"Rater {rater} does not belong to rater list for widget {index_int}")
                error_list.append(item)
                continue

            if value["value"]["dark_pattern_type"] == "(none)":
                print(f"The widget index {index_int} has not been labeled by {rater}")
                comment = f"The widget index {index_int} has not been labeled by {rater}"
                double_check_no_label.append(comment)
                if key not in double_check_index:
                    double_check_index.append(index_int)
                continue

            if value["value"]["dark_pattern_type"][2]["not-sure"]:
                print(f"{rater} marked widget index {index_int} as unsure. Double-check list is created.")
                comment = f"{rater} marked widget index {index_int} as unsure. Double-check list is created."
                double_check_unsure.append(comment)
                if key not in double_check_index:
                    double_check_index.append(index_int)
                continue
            if all(v == 0 for v in value["value"]["dark_pattern_type"][0].values()) and value["value"]["dark_pattern_type"][2]["no-dd"] is False:
                print(f"The widget index {index_int} has not been labeled by {rater}")
                comment = f"The widget index {index_int} has not been labeled by {rater}"
                double_check_no_label.append(comment)
                if key not in double_check_index:
                    double_check_index.append(index_int)
                continue


            
            # If it satisfies all requirements, append it to selected_list
            selected_list.append(item)


    double_check_dict["missing label"] = double_check_no_label
    double_check_dict["unsure"] = double_check_unsure
    selected_list, double_check_index, double_check_dict = check_number_of_labeler(selected_list, double_check_index, double_check_dict, rater_name)
    new_selected_list = clean_missing_unsure_data(selected_list, double_check_index)

    return new_selected_list, error_list, double_check_dict

def check_number_of_labeler(selected_list, double_check_index, double_check_dict, rater_name):
    index_dict = {}

    for d in selected_list:
        for k, value in d.items():
            index = int(re.findall("[0-9]+", k)[0])
            if index in index_dict:
                index_dict[index].append(value["rater"])
            else:
                index_dict[index] = []
                index_dict[index].append(value["rater"])
    
    for k, value in index_dict.items():
        if len(value) < 2:
            missing = set(rater_name) - set(value)
            missing_str = ", ".join(sorted(missing))
            if k not in double_check_index:
                double_check_index.append(k)
                double_check_dict["missing label"].append(f"The widget index {k} has not been labeled by {missing_str}")

    return selected_list, double_check_index, double_check_dict


def clean_missing_unsure_data(selected_list, double_check_index):
    print(f"Widgets that need to be dropped {double_check_index}")
    double_check_index = set(double_check_index)          # fast lookup
    keep = []

    for d in selected_list:                               # iterate list-elements
        drop_this = False
        for k in d.keys():                                # examine each key
            index = int(re.findall("[0-9]+", k)[0])              # leading digits
            if index in double_check_index:
                drop_this = True
                # print(f"Widget {index} is dropped.")
                break
        if not drop_this:
            keep.append(d)

    return keep

def save_to_json(folder_name, selected_list, error_list, double_check_dict):
    with open(f"{folder_name}/valid_data.json", "w") as f:
        json.dump(selected_list, f, indent=4)
    print(f"Round json saved to valid_data.json")

    with open(f"{folder_name}/rater_not_valid.json", "w") as f1:
        json.dump(error_list, f1, indent=4)
    print("Data saved to rater_not_valid.json")

    with open(f"{folder_name}/rechecked_data.json", "w") as f2:
        json.dump(double_check_dict, f2, indent=4)
    print("Data saved to rechecked_data.json")

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "download_data_cloudflare", "kv_pairs.json"))
with open(path) as f:
    data = json.load(f)


# Extract data range
start_index = 524
end_index = 696
rater_name = ["luna", "Hanyu"]
round_number = 3

folder_name = f"round{round_number}/hanyu-luna"
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)
    
selected_list, error_list, double_check_dict = find_round(data, start_index, end_index, rater_name)
save_to_json(folder_name, selected_list, error_list, double_check_dict)



