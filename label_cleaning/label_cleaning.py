# Generate summary
# Cleaning data
import json
import re
import os

class DataAnalyzer():
    def __init__(self, path, output_path, output_path_problematic):
        """
        Initialize with a json file path
        """
        with open(path) as f:
            self.data = json.load(f)
        label_vote, problematic_widget = self.iterate()

        with open(output_path, "w") as f2:
            json.dump(label_vote, f2, indent = 4)
        
        with open(output_path_problematic, "w") as f2:
            json.dump(problematic_widget, f2, indent = 4)
        
        print("Labels are cleaned and files are saved!")

        
    def get_component(self):
        with open("widget_data.json") as f:
            data = json.load(f)
        return data
    
    def read_through_component(self, index_int, component_mapping):
        description_number = component_mapping[index_int]["Description_number"]
        model = component_mapping[index_int]["Model"]
        condition = component_mapping[index_int]["Condition"]
        return description_number, model, condition
    
    def merge_categories(self, current, existing, level, index_int, existing_index):
        
        if level == "dark pattern":
            existing["dark pattern"].append(current["dark pattern"][0])
        else: 
            for key, value in current[f"{level}"].items():
                if key in existing[f"{level}"]:
                    existing[f"{level}"][key] += 1 # Add number of votes to existing categories
                else:
                    existing[f"{level}"][key] = 1   # Add new key-value pair
        

    # Cleaning data
    def iterate(self):
        print("Total number of widgets", len(self.data))
        existing_index = {}
        problematic_index = {}
        for item in self.data:

            widget_label = {}

            # Get index
            index_list = re.findall("[0-9]+", list(item.keys())[0])

            index = index_list[0]
            index_int = int(index)

            # All deceptive designs for the widget


            problematic_widget, deceptive_design_dict = self.get_deceptive_design(item, index_int)

            # Labeler name
            labeler_name = list(item.values())[0]["rater"]

            # Widget index

            # If the widget is not marked as no dark pattern, but there is no selection, save it separately
            if problematic_widget == True:
                problematic_index[index_int] = labeler_name
                continue # Go to next widget

            # If index already exists, add labelers' name and new deceptive design to existing index info
            if index_int in existing_index:

                # Add labeler's name to labeler if the name does not exist
                if labeler_name not in existing_index[index_int]["labeler"]:
                    existing_index[index_int]["labeler"].append(labeler_name)

                # Merge number of instances for each deceptive design and new categories into existing framework
                levels = {0: "dark pattern", 1: "low-level", 2: "meso-level", 3: "high-level"}
                for key, value in levels.items():
                    existing = existing_index[index_int]["pattern"][key]
                    current = deceptive_design_dict[key]
                    self.merge_categories(current, existing, value, index_int, existing_index)
                

            # Else create a new dict to save the info
            else:
                # Get widget index and component mapping
                component_mapping = self.get_component()
                description_number, model, condition = self.read_through_component(index_int, component_mapping)

                # Save widget info to the dict
                widget_label["component"] = description_number # Component type
                widget_label["model"] = model # LLM model
                widget_label["condition"] = condition # Condition
                widget_label["pattern"] = deceptive_design_dict # Widget selected deceptive designs
                widget_label["labeler"] = [labeler_name]
                existing_index[index_int] = widget_label
            
            # print("Full list", existing_index)
        
        return existing_index, problematic_index
    
    def get_deceptive_design(self, item, index_int):
        deceptive_design_list = []
        problematic_widget = False
        dark_pattern_or_no = {}
        low_level_dict = {}
        meso_level_dict = {}
        high_level_dict = {}
        problematic_dict = {}
        dark_pattern_or_no_list = []

        # If there is no dark pattern selected, ignore all selection, save empty low and meso levels

        if list(item.values())[0]["value"]["dark_pattern_type"] == "(none)":
            problematic_widget = True
            low_level_type = {}
            meso_level_type = {}
            high_level_type = {}
        else:
            if not list(item.values())[0]["value"]["dark_pattern_type"][2]["no-dd"]:
                
                # Get low level and meso types
                low_level_total, meso_level_total = list(item.values())[0]["value"]["dark_pattern_type"][:2]

                # Get dict version for low-level, meso-level and high-level deceptive designs
                dark_pattern_or_no_list, low_level_type, meso_level_type, high_level_type = self.count_level(low_level_total, meso_level_total)
                problematic_widget = not(len(list(low_level_type.items())) or (len(list(meso_level_type.items()))))          

            else:
                low_level_type = {}
                meso_level_type = {}
                high_level_type = {}
                dark_pattern_or_no_list.append(False)


        # Clean format
        dark_pattern_or_no["dark pattern"] = dark_pattern_or_no_list
        low_level_dict["low-level"] = low_level_type
        # low_level_dict["low-level-instance"] = low_level_instance
        meso_level_dict["meso-level"] = meso_level_type
        # meso_level_dict["meso-level-instance"] = meso_level_instance
        high_level_dict["high-level"] = high_level_type
        # high_level_dict["high-level-instance"] = high_level_instance
        

        # # Append level categories to list
        deceptive_design_list.extend([dark_pattern_or_no,low_level_dict,meso_level_dict,high_level_dict])
        return problematic_widget, deceptive_design_list

    
    def count_level(self, low_level_total, meso_level_total):

        # Empty list to save deceptive design types
        low_level_type_dict = {}
        meso_level_type_dict = {}
        high_level_type_dict = {}

        # Empty dict to save number of instances for each deceptive design
        low_level_instance_dict = {}
        meso_level_instance_dict = {}
        high_level_instance_dict = {}


        for key in low_level_total.copy().keys():
            value = low_level_total[key]
            if "sum" in key:
                meso_level_total[key] = value

            elif value > 0:
                low_level_instance_dict[key] = value
                low_level_type_dict[key] = 1

        high_level_categories = ["obstruction-sum", "sneaking-sum", "interface-interference-sum", "forced-action-sum", "social-engineering-sum"]
        
        for key, value in meso_level_total.items():
            if value != 0 and key in high_level_categories:
                high_level_instance_dict[key] = value
                high_level_type_dict[key] = 1
            elif value != 0 and key not in high_level_categories:
                meso_level_instance_dict[key] = value
                meso_level_type_dict[key] = 1

        dark_pattern_or_no_list = [True]

        return dark_pattern_or_no_list, low_level_type_dict, meso_level_type_dict, high_level_type_dict

round_number = 1
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "extract_data", f"3raters/round{round_number}/valid_data.json"))

folder_name = f"round{round_number}"

if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

analyzer = DataAnalyzer(path, f"{folder_name}/cleaned_label.json", f"{folder_name}/no_label_widget.json")