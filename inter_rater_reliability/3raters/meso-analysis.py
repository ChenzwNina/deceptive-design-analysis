import json
import os
import pdb

def load_file(path):
    with open(path) as f:
        data = json.load(f)
    return data

def format_data(data, output_path):
    new_dict_meso = {}
    new_dict_high = {}
    for key, value in data.items():
        new_list_meso = []
        new_list_high = []
        for i in value:
            meso_level, high_level = mapping_data(i)
            new_list_meso.append(meso_level)
            new_list_high.append(high_level)
        new_dict_meso[key] = new_list_meso
        new_dict_high[key] = new_list_high
    output_data(new_dict_meso, new_dict_high, output_path)

def output_data(new_dict_meso, new_dict_high, output_path):
    # pdb.set_trace()
    meso_folder = f"{output_path}/meso"
    high_folder = f"{output_path}/high"
    if not os.path.isdir(meso_folder):
        os.makedirs(meso_folder)
    if not os.path.isdir(high_folder):
        os.makedirs(high_folder)

    with open(f"{meso_folder}/qualified.json", "w") as f:
        json.dump(new_dict_meso, f, indent=4)
    
    with open(f"{high_folder}/qualified.json", "w") as f:
        json.dump(new_dict_high, f, indent=4)


def mapping_data(item):
    new_dict_meso = {}
    new_dict_high = {}
    if not item:
        return item, item
    else:
        for key, value in item.items():
            meso_category, high_category = map_category(key)
            if meso_category not in new_dict_meso:
                new_dict_meso[meso_category] = value
            else:
                new_dict_meso[meso_category] += 1
            if high_category not in new_dict_high:
                new_dict_high[high_category] = value
            else:
                new_dict_high[high_category] += 1
        return new_dict_meso, new_dict_high


def map_category(key):
    if key in ["immortal-accounts-vote", "dead-end-vote", "no-way-back"]:
        meso_category = "roach-motel"
        high_category = "obstruction"
    elif key in ["price-comparison-prevention-vote", "intermediate-currency-vote", "discount-framing-manipulation"]:
        meso_category = "creating-barriers"
        high_category = "obstruction"
    elif key in  ["privacy-maze-vote", "extra-burden", "disguised-ad-vote"]:
        meso_category = "adding-steps"
        high_category = "obstruction"
    elif key in ["disguised-ad-vote"]:
        meso_category = "bait-and-switch"
        high_category = "sneaking"
    elif key in ["sneak-into-basket-vote", "drip-pricing-vote", "reference-pricing-vote"]:
        meso_category = "hiding-information"
        high_category = "sneaking"
    elif key in ["conflicting-information-vote", "information-without-context-vote"]:
        meso_category = "contextualizing"
        high_category = "sneaking"
    elif key in ["false-hierarchy-vote", "visual-prominence-vote", "bundling-vote", "pressured-selling-vote"]:
        meso_category = "manipulating-choice"
        high_category = "interface-interference"
    elif key in ["bad-defaults-sum"]:
        meso_category = "bad-defaults"
        high_category = "interface-interference"
    elif key in [ "cuteness-vote", "positive-vote"]:
        meso_category = "emotional"
        high_category = "interface-interference"
    elif key in ["trick-questions-sum"]:
        meso_category = "trick-questions"
        high_category = "interface-interference"
    elif key in ["choice-overload-sum"]:
        meso_category = "choice-overload"
        high_category = "interface-interference"
    elif key in ["hidden-information-sum"]:
        meso_category = "hidden-info"
        high_category = "interface-interference"    
    elif key in ["wrong-language-vote", "complex-language-vote"]:
        meso_category = "language-inaccessibility"
        high_category = "interface-interference"  
    elif key in ["feedward-ambiguity-sum"]:
        meso_category = "feedward-ambiguity"
        high_category = "interface-interference"
    elif key in ["nagging-sum"]:
        meso_category = "nagging"
        high_category = "forced-action"
    elif key in ["forced-continuity-sum"]:
        meso_category = "forced-continuity"
        high_category = "forced-action"  
    elif key in ["forced-registration-sum"]:
        meso_category = "forced-registration"
        high_category = "forced-action"   
    elif key in ["privacy-zukering-vote", "friend-spam-vote", "address-book-leeching-vote", "social-pyramid-vote"]:
        meso_category = "forced-communication"
        high_category = "forced-action"  
    elif key in ["pay-to-play-vote", "grinding-vote"]:
        meso_category = "gamification"
        high_category = "forced-action"
    elif key in ["auto-play-vote"]:
        meso_category = "attention-capture"
        high_category = "forced-action"  
    elif key in ["high-demand-vote"]:
        meso_category = "scarcity"
        high_category = "social-engineering" 
    elif key in ["low-stock-vote", "endorsement-vote", "parasocial-vote"]:
        meso_category = "social-proof"
        high_category = "social-engineering"    
    elif key in ["activity-messages-vote", "countdown-timer-vote", "limited-time-vote"]:
        meso_category = "urgency"
        high_category = "social-engineering" 
    elif key in ["confirmshaming-vote"]:
        meso_category = "confirmshaming"
        high_category = "social-engineering"
    else:
        print("error: unrecognized category: ", key)
    return meso_category, high_category




round_number = "round1"
input_file = f"{round_number}/qualified.json"
output_file = f"meso_analysis-{round_number}"
data = load_file(input_file)

format_data(data, output_file)