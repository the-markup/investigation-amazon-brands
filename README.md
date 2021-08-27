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
│   ├── combined_queries_with_source.csv
│   ├── best_sellers
│   ├── generic_search_terms
│   ├── search-private-label
│   ├── search-selenium
│   ├── search-selenium-our-brands-filter_
│   ├── selenium-products
│   ├── seller_central
│   └── spotcheck
└── output # change this to viz?
    ├── datasets
    │   ├── amazon_private_label.csv.xz
    │   ├── products.csv.xz
    │   ├── searches.csv.xz
    │   ├── pairwise_training_set.csv.gz
    │   └── training_set.csv.gz
    ├── figures
    └── tables
 ```
 
`data/output/datasets/amazon_private_label.csv.xz` is our dataset of Amazon brands, exclusives, and proprietary electronics (N=137,428).

`data/output/datasets/searches.csv.xz` parsed search result pages from top and generic searchs (N=187,534 product positions). You can filter this by `search_term` for each of these subsets from `data/input/combined_queries_with_source.csv`.

`data/output/datasets/products.csv.xz` parsed product pages from the searches above (N=157,405 product pages). 
`training_set.csv.gz` metadata used to train random forests. Additionally feature engineering is conducted in `notebooks/2-random-forest-analysis.ipynb`

## Download Data
You can download the raw data files in `data/input` using this command:
`sh download_full_raw_data.sh`

Note this is not necessary to run notebooks and see full results.
 
### data/input/selenium-products (220 GB uncompressed)
Product pages collected in February 2021. You can download the raw data `selenium-products.tar.xz` (9 GB compressed) here.
 
### data/input/search-selenium/ (350 GB uncompressed)
Search results collected in January 2021. You can download the raw data `search-selenium.tar.xz` (238 MB compressed) here.