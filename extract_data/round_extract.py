# Input index to filter by rounds
import json
import re
import os

def find_round(data, start_index, end_index):
    error_list = []
    selected_list = []
    for item in data[0:]:

        # Get index
        index_list = re.findall("[0-9]+", list(item.keys())[0])

        try:
            index = index_list[0]
            index_int = int(index)
        except:
            print("The index extracted is not a number or not extracted successfully")
            error_list.append(item)
        
        # If the widget index is within selection
        if index_int >= start_index and index_int <= end_index:
            selected_list.append(item)
        
    return selected_list, error_list

def save_to_json(round_number, selected_list, error_list):
    with open(f"extracted_data_{round_number}.json", "w") as f:
        json.dump(selected_list, f, indent=4)
    print(f"Round json saved to extracted_data_{round_number}.json")

    with open(f"not_valid.json", "w") as f1:
        json.dump(error_list, f1, indent=4)
    print("Not valid data saved to not_valid.json")

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "download_data_cloudflare", "kv_pairs.json"))
with open(path) as f:
    data = json.load(f)

# Extract data range
start_index = 0
end_index = 15

selected_list, error_list = find_round(data, start_index, end_index)
save_to_json(1, selected_list, error_list)



