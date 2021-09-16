# Amazon Brands and Exclusives
This repository contains code to reproduce the findings featured in the methodology attached.

Data that we collected and analyzed are in the `data` folder.<br>
To use the full input dataset (which is not hosted here), please refer to the [Download data](#download-data).<br>

Jupyter notebooks used for data preprocessing and analysis are avialble in the `notebooks` folder.<br>
Descriptions for each notebook are outlined in the [Notebooks](#notebooks) section below.

## Installation
### Python
Make sure you have Python 3.6+ installed, we used [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to create a Python 3.8 virtual environment.

Then install the Python packages:<br>
`pip install -r requirements.txt`

## Notebooks
These notebooks are intended to be run sequentially, but they are not dependent on one another.
If you want quick overview of the methodology you only need to concern yourself with the notebooks with an asterix(*).

### 0-data-preprocessing.ipynb
This notebook parses Amazon search results, Amazon product pages, and produces the intermediary datasets (`data/output/datasets/`) used in ranking analysis and random forest classifiers.

### 1-data-analysis-search-results.ipynb *
Bulk of the ranking analysis and stats in the data analysis

### 2-random-forest-analysis.ipynb *
Feature engineering training set, finding optimal hyperparameters, and performing the ablation study on a random forest model. The most predictive feature is verified using three separate methods.

### 3-survey-results.ipynb
Visualizing the survey results from our national panel of 1000 adults.

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
├── output
│   ├── figures
│   ├── tables
│   └── datasets
│       ├── amazon_private_label.csv.xz
│       ├── products.csv.xz
│       ├── searches.csv.xz
│       ├── pairwise_training_set.csv.gz
│       └── training_set.csv.gz
└── input
    ├── combined_queries_with_source.csv
    ├── best_sellers
    ├── generic_search_terms
    ├── search-private-label
    ├── search-selenium
    ├── search-selenium-our-brands-filter_
    ├── selenium-products
    ├── seller_central
    └── spotcheck
 ```

`data/output/` contains tables, figures, and datasets used in our methodolgy.

`data/output/datasets/amazon_private_label.csv.xz` is our dataset of Amazon brands, exclusives, and proprietary electronics (N=137,428 products). We use each product's unique ID (called an ASIN) to identify Amazon's own products in our methodology.

`data/output/datasets/searches.csv.xz` parsed search result pages from top and generic searchs (N=187,534 product positions). You can filter this by `search_term` for each of these subsets from `data/input/combined_queries_with_source.csv`.

`data/output/datasets/products.csv.xz` parsed product pages from the searches above (N=157,405 product pages). 

`data/output/training_set.csv.gz` metadata used to train and evaluate random forests. Additionally feature engineering is conducted in `notebooks/2-random-forest-analysis.ipynb`, which produces `pairwise_training_set.csv.gz`.

Every file in `data/input` except `combined_queries_with_source.csv` is stored in Google Drive.

## Download Data
You can find the raw inputs in `data/input` in `s3://investigation-amazon-brands`.

If you trust us, you can download the HTML and JSON files in `data/input` using this script:
`sh data/download_input_data.sh`

**Note this is not necessary to run notebooks and see full results.**
 
### data/input/search-selenium/ (12 GB uncompressed)
First page of search results collected in January 2021. Download the HTML files `search-selenium.tar.xz` (238 MB compressed). 

### data/input/selenium-products/ (220 GB uncompressed)
Product pages collected in February 2021. Download the HTML files `selenium-products.tar.xz` (9 GB compressed) here.
 
### data/input/search-selenium-our-brands-filter_/ (35 GB uncompressed)
Search results filtered by "our brands". Contains every page of search results. Download `search-selenium-our-brands-filter_.tar.xz` (403 MB compressed)

### data/input/search-private-label/ (25 GB uncompressed)
API responses for search results filtered down to products Amazon identifies as "our brands". Contains paginated API results. Download the JSON files `search-private-label.tar.xz` (402 MB uncompressed)

### data/input/seller_central/ (105 MB)
Seller central data for Q4 2020. `All_Q4_2020.csv.xz` (105 MB compressioned).

### data/input/best_sellers/ (4 GB)
Amazon's best sellers under the category "Amazon Devices & Accessories". Download the HTML files `best_sellers.tar.xz` (60MB compressed).

### data/input/spotcheck/ (4 GB)
A sub-sample of product pages for spotchecking buy box changes. Download the HTML files `spotcheck.tar.xz` (159 MB compressed).
