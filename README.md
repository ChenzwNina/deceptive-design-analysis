# Data Cleaning for Dark Pattern Labeling
## Folder: download_data_cloudflare
Step 1: download data from cloudflare
- `download_kv.py`: download labeling data from Cloudflare. Output file `kv_pairs.json`.
  
## Folder: extract_data
Step 2: extract data from downloaded data (for consistency comparison only)
`round_extract.py`: input is `kv_pairs.json`, start index, end index, rater name in this round to extract partial data from the downloaded data. Output file is a folder whose name is based on the input round number. In the folder, there are 3 files.
- `valid_data.json`: The file saves mapping between widget index and widget information, including model, component type, and condition. Each widget has labeled by 3 raters.
- `rechecked_data.json`: The file contains information about widgets that miss labels from raters and with unsure labels.
- `rater_not_valid.json`: The file contains data by raters that do not belong to this round.
  
## Folder: label_cleaning
Step 3: clean labels
- `label_cleaning.py`: input is `alid_data.json`, output are `cleaned_label.json` and `no_label_widget.json`. `cleaned_label.json` contains indexed, cleaned data: votes plus component details (model, component type, etc.). `no_label_widget.json` lists widgets with no categories selected and no “no dark pattern” flag—this file should be empty.
  
## Folder: majority_vote
Step 4: do majority votes
- `majority_vote.py`: input is `cleaned_label.json`, output is `majority_label.json` and `no_clear_majority.json`. The code processes the data in cleaned_label.json, filtering out widgets that do not have exactly 3 votes (i.e., fewer or more than 3). For the remaining widgets, it takes the majority vote: any category with votes from 2 or more labelers is included in `majority_label.json`.

## Folder: inter_rater_reliability
- The folder is used to count inter-rater reliability with Krippendorff's Alpha and Jaccard distance.
- `reliability_data_cleaning.py` cleans data to follow a format that could be processed by `inter_rater_reliability.py`. The output file is `qualified.json` and `rater_not_equal_to_3.json ` which contains widgets that have less than 3 raters.
- `inter_rater_reliability.py ` computes the alpha.

For further analysis, `majority_label.json` should be used as the sample data file.
