set -o errexit

curl https://markup-public-data.s3.amazonaws.com/amazon-brands/spotcheck.tar.xz -o data/input/;tar -xf data/input/spotcheck.tar.xz -C data/input/spotcheck/
curl https://markup-public-data.s3.amazonaws.com/amazon-brands/selenium-products.tar.xz -o data/input/;tar -xf data/input/selenium-products.tar.xz -C data/input/selenium-products/
curl https://markup-public-data.s3.amazonaws.com/amazon-brands/searches-selenium.tar.xz -o data/input/;tar -xf data/input/searches-selenium.tar.xz -C data/input/searches-selenium/
curl https://markup-public-data.s3.amazonaws.com/amazon-brands/search-selenium-our-brands-filter_.tar.xz -o data/input/;tar -xf data/input/search-selenium-our-brands-filter_.tar.xz -C data/input/search-selenium-our-brands-filter_
curl https://markup-public-data.s3.amazonaws.com/amazon-brands/best_sellers.tar.xz -o data/input/;tar -xf data/input/best_sellers.tar.xz -C data/input/best_sellers/
curl https://markup-public-data.s3.amazonaws.com/amazon-brands/All_Q4_2020.csv.xz -o data/input/;tar -xf data/input/All_Q4_2020.csv.xz -C data/input/seller_central/
curl https://markup-public-data.s3.amazonaws.com/amazon-brands/search-private-label.tar.xz -o data/input/;tar -xf data/input/search-private-label.tar.xz -C data/input/search-private-label