# Amazon Brands and Exclusives
This repository contains code to reproduce the findings featured in our story, "[TK](https://themarkup.org/)" from our series, [TK](https://themarkup.org/series/).

Our methodology is described in "[How We TK](https://themarkup.org/)".

The the figures and tables from our analysis can be found in the `data` folder. <br>
Since our full dataset was too large to place in GitHub, we provide a subset in the `data-subsample` folder. <br>
To use the full dataset, please refer to the [Download data](#download-data).

## Installation
### Python
Make sure you have Python 3.6+ installed, we used [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to create a Python 3.8 virtual environment.

Then install the Python packages:<br>
`pip install -r requirements.txt`

## Notebooks
### 0-data-preprocessing.ipynb
This notebook parses Amazon search results, Amazon product pages, and produces the intermediary datasets used in ranking analysis and random forest classifiers.

### 1-data-analysis-search-results.ipynb
Bulk of the ranking analysis and stats in the data analysis

### 2-random-forest-analysis.ipynb
Feature engineering training set, finding optimal hyperparameters, and performing the ablation study on a random forest model. The most predictive feature is verified using three separate methods.

### 3-survey-results.ipynb
Visualizing the survey results from our national panel of 1000 adults. These visualizations show up in the "survey results" section of the data analysis.

### 4-limiations-product-page-changes.ipynb
Analysis of how often the buy box's default shipper and seller changes between Amazon and a third-party. This stat sends up in the limitations.


### utils.py
Contains convenient functions used in the notebooks.

### parsers.py
Contains parsers for search results and product pages.


## Data
This directory is where inputs, intermediaries and outputs are saved.

```
data
├── input
│   ├── best_sellers
│   ├── combined_queries_with_source.csv
│   ├── generic_search_terms
│   ├── search-private-label
│   ├── search-selenium
│   ├── search-selenium-our-brands-filter_
│   ├── selenium-products
│   ├── seller_central
│   └── spotcheck
├── intermediary # change this to output?
│   ├── amazon_private_label.csv.gz
│   ├── best_sellers.csv.gz
│   ├── generic_searches.csv.gz
│   ├── our_brands_api.csv.gz
│   ├── our_brands_filter.csv.gz
│   ├── pairwise_training_set_2021_5_10.csv.gz
│   ├── pairwise_training_set.csv.gz
│   ├── products.csv.gz
│   ├── products_with_meta.csv.gz
│   ├── searches.csv.gz
│   ├── spot_check
│   ├── top_search_asins.csv.gz
│   ├── top_searches.csv.gz
│   └── training_set.csv.gz
└── output # change this to viz?
    ├── figures
    └── tables

 ```
 
You can download the raw data files in `data/input` using this command:
`sh download_full_raw_data.sh`
 
### data/input/selenium-products (220 GB uncompressed)
You can download the raw data `selenium-products.tar.xz` (9 GB compressed) here.
 
### data/input/search-selenium/ (350 GB uncompressed)
You can download the raw data `search-selenium.tar.xz` (238 MB compressed) here.