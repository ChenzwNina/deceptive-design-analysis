# Data Cleaning for Dark Pattern Labeling
## Folder: download_data_cloudflare
Step 1: download data from cloudflare
- `download_kv.py`: download labeling data from Cloudflare. Output file `kv_pairs.json`.
## Folder: extract_data
Step 2: extract data from downloaded data (for consistency comparison only)
- `widget_data.json`: The file saves mapping between widget index and widget information, including model, component type, and condition.
- `round_extract.py`: input is `kv_pairs.json`, start index, and end index to extract partial data from the downloaded data. Output file is `extracted_data_{x}.json` and `not_valid.json`. `extracted_data_{x}.json`includes widgets with index between input start and end index. `not_valid.json` is a file to save invalid data format.
## Folder: label_cleaning
Step 3: clean labels
- `label_cleaning.py`: input is `kv_pairs.json` or `extracted_data_{x}.json`, output are `cleaned_label.json` and `no_label_widget.json`. `cleaned_label.json` is the cleaned data with component information and labeling votes organized by index. `no_label_widget.json` contains widgets where labelers did not select any categories and also did not mark them as having no dark patterns, which needs a second look.
## Folder: majority_vote
Step 4: do majority votes
- `majority_vote.py`: input is `cleaned_label.json`, output is `majority_label.json` and `no_clear_majority.json`. The code processes the data in cleaned_label.json, filtering out widgets that do not have exactly 3 votes (i.e., fewer or more than 3). For the remaining widgets, it takes the majority vote: any category with votes from 2 or more labelers is included in `majority_label.json`.

For further analysis, `majority_label.json` should be used as the sample data file.
