set -o errexit

curl https://investigation-amazon-brands.s3.us-east-2.amazonaws.com/spotcheck.tar.xz -o data/input/;tar -xf data/input/spotcheck.tar.xz -C data/input/spotcheck/
curl https://investigation-amazon-brands.s3.us-east-2.amazonaws.com/selenium-products.tar.xz -o data/input/;tar -xf data/input/selenium-products.tar.xz -C data/input/selenium-products/
curl https://investigation-amazon-brands.s3.us-east-2.amazonaws.com/searches-selenium.tar.xz -o data/input/;tar -xf data/input/searches-selenium.tar.xz -C data/input/searches-selenium/
curl https://investigation-amazon-brands.s3.us-east-2.amazonaws.com/search-selenium-our-brands-filter_.tar.xz -o data/input/;tar -xf data/input/search-selenium-our-brands-filter_.tar.xz -C data/input/search-selenium-our-brands-filter_
curl https://investigation-amazon-brands.s3.us-east-2.amazonaws.com/best_sellers.tar.xz -o data/input/;tar -xf data/input/best_sellers.tar.xz -C data/input/best_sellers/
curl https://investigation-amazon-brands.s3.us-east-2.amazonaws.com/All_Q4_2020.csv.xz -o data/input/;tar -xf data/input/All_Q4_2020.csv.xz -C data/input/seller_central/