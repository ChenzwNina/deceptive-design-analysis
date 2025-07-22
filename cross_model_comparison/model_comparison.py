import numpy as np
import pandas as pd

MODELS = ["grok-3-beta", "gpt-4.1", "deepseek-v3", "gemini-2.5-pro"]
FILE_PATH = "./majority_vote/majority_label.json"

def load_json_data(file_path=FILE_PATH):
    """
    Load data from a JSON file

    Parameters:
    file_path (str): The path to the JSON file.
    """
    data = pd.read_json(file_path)
    # print(data.head())
    return data.T

# 2.1 Compare the percentage and number of components labeled with dark patterns across the four models ("grok-3-beta", "gpt-4.1", "deepseek-v3", "gemini-2.5-pro”).
def compare_percentage_and_number(file_path=FILE_PATH):
    """
    Compare the percentage and number of components labeled with dark patterns across the four models.
    
    Parameters:
    file_path (str): The path to the data JSON file
    
    Returns:
    results (dict): A dictionary with model names as keys and a tuple of (percentage, number of components) as values.
    """
    data = load_json_data(file_path)
    results = {}

    def if_dark_pattern(lst):
        vote_lst = lst[0]['dark pattern']
        return sum(vote_lst) > len(vote_lst) // 2
    
    data['dark'] = data['pattern'].apply(if_dark_pattern)
    res = data.groupby('model')['dark'].agg([
        ('dark_count', lambda x: x.sum()),
        ('total', 'count'), 
        ('percentage', lambda x: (x.sum() / len(x)) * 100) 
    ])
    # print(res)
    for model in MODELS:
        if model not in res.index:
            print(f"Model {model} not found in the data.")
            continue
        results[model] = (res.loc[model, 'percentage'].item(), res.loc[model, 'dark_count'].item())
    print(results)
    return results

# 2.2 Compare the number of unique deceptive design types identified in each model.
# Analyze low-level and meso-level categories separately
def compare_unique_type_number(file_path=FILE_PATH):
    """
    Compare the number of unique deceptive design types identified in each model

    Returns:
    unique_types (dict): A dictionary with model names as keys and a dict of 
            levels as keys and number of unique deceptive design types as values
    """
    data = load_json_data(file_path)
    def dark_level_lst(lst):
        if 'low-level' not in lst[1] or 'meso-level' not in lst[2] or 'high-level' not in lst[3]:
            raise ValueError("Data structure has changed")
        return pd.Series({
            'low_level': lst[1]['low-level'],
            'meso_level': lst[2]['meso-level'],
            'high_level': lst[3]['high-level']
        })

    data[['low_level', 'meso_level', 'high_level']] = data['pattern'].apply(dark_level_lst)

    results = {}
    for model in MODELS:
        if model not in data['model'].unique():
            print(f"Model {model} not found in the data.")
            continue
        model_data = data[data['model'] == model]
        model_results = {}
        
        for level in ['low_level', 'meso_level', 'high_level']:
            # Flatten lists and count unique values
            unique_types = model_data[level].explode().nunique()
            model_results[level] = unique_types
        
        results[model] = model_results
    print(results)
    return results


# 2.3 Compare the average number of dark pattern types per component in each model.
# Count the total number of dark patterns, including both low-level patterns and meso-level patterns that lack associated low-level categories.

# 2.4 Assess whether the differences across models are statistically significant.

compare_percentage_and_number()
compare_unique_type_number()