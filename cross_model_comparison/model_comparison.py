import numpy as np
import pandas as pd

def load_json_data(file_path="./majority_vote/majority_label.json"):
    """
    Load data from a JSON file

    Parameters:
    file_path (str): The path to the JSON file.
    """
    data = pd.read_json(file_path)
    # print(data.head())
    return data.T

# 2.1 Compare the percentage and number of components labeled with dark patterns across the four models ("grok-3-beta", "gpt-4.1", "deepseek-v3", "gemini-2.5-pro”).
def compare_percentage_and_number(file_path="./majority_vote/majority_label.json"):
    """
    Compare the percentage and number of components labeled with dark patterns across the four models.
    
    Parameters:
    file_path (str): The path to the data JSON file
    
    Returns:
    results (dict): A dictionary with model names as keys and a tuple of (percentage, number of components) as values.
    """
    data = load_json_data(file_path)
    models = ["grok-3-beta", "gpt-4.1", "deepseek-v3", "gemini-2.5-pro"]
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
    for model in models:
        if model not in res.index:
            print(f"Model {model} not found in the data.")
            continue
        results[model] = (res.loc[model, 'percentage'], res.loc[model, 'dark_count'])
    print(results)
    return results

# 2.2 Compare the number of unique deceptive design types identified in each model.
# Analyze low-level and meso-level categories separately

# 2.3 Compare the average number of dark pattern types per component in each model.
# Count the total number of dark patterns, including both low-level patterns and meso-level patterns that lack associated low-level categories.

# 2.4 Assess whether the differences across models are statistically significant.

compare_percentage_and_number()