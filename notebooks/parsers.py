import re
import json

from lxml import html, etree
import pandas as pd

def is_sold_by_amazon(row, col='sold_by'):
    amazon_sellers = ['zappos', 'whole foods', 'amazon']
    if row[col] == None:
        return None
    to_check = str(row[col]).lower()
    if any(seller in to_check for seller in amazon_sellers):
        return True
    elif row['product_by_amazon']:
        return True
    else:
        return False
    
def is_shipped_by_amazon(row, col='shipped_by'):
    amazon_sellers = ['zappos', 'whole foods', 'amazon']
    if row[col] == None:
        return None
    to_check = str(row[col]).lower()
    if any(seller in to_check for seller in amazon_sellers):
        return True
    elif row['product_by_amazon']:
        return True
    else:
        return False

def clean_text(text):
    """
    If text exists, this cleans it up a bit.
    """
    if not text:
        return ""
    text = text.encode("ascii", "ignore").decode("utf-8").strip().replace("\n", " ")
    text = re.sub(r"\s{2,}", " ", text)
    return text

def clean_text_list(text_list, remove_empty=True):
    text_list = (clean_text(t) for t in text_list)
    if remove_empty:
        text_list = filter(None, text_list)
    return list(text_list)


def clean_text_list_to_str(text_list, join_with=" "):
    text = clean_text_list(text_list)
    text = join_with.join(text)
    return text or None


def parse_product_listing(product, fn, search_term, product_order, 
                          product_type="regular_placement"):
    """
    Does the thing
    """
    asin = product.xpath("string(@data-asin)")
    product_name = clean_text_list_to_str(product.xpath('.//h2//text()'))
    url = product.xpath('string(.//h2//a//@href)')
    is_prime = product.xpath('boolean(.//i[@aria-label="Amazon Prime"])')
    is_amazon_fresh = product.xpath('boolean(.//img[@alt="Amazon Fresh" or @alt="Whole Foods Market"])')
    is_sponsored = product.xpath('boolean(.//span[contains(text(), "Sponsored")])')
    is_featured_brand = product.xpath('boolean(.//span[contains(text(), "Featured from our brands")])')
    brand = clean_text_list_to_str(product.xpath('.//h5//text()'))
    is_amazons_choice = product.xpath(
        """boolean(.//span[@aria-label="Amazon's Choice"])"""
    )
    is_best_seller = product.xpath(
        'boolean(.//span[contains(@aria-labelledby, "best-seller-label")])'
    )
    stars = clean_text_list_to_str(
        product.xpath('.//span[contains(@aria-label, "out of 5 stars")]//@aria-label')
    )
    price = clean_text_list_to_str(
        product.xpath('.//span[@class="a-offscreen"]//text()')
    )
    price_std = clean_text_list_to_str(
        product.xpath('.//span[class="a-size-base a-color-secondary"]//text()')
    )
    if stars:
        stars = stars.replace(' out of 5 stars', '')
    reviews = clean_text_list_to_str(product.xpath('.//a[contains(@href, "#customerReviews")]//text()'))
    if reviews:
        reviews = reviews.replace(',', '')
    row = {
        "asin": asin,
        "product_name": product_name,
        "stars": stars,
        "reviews": reviews,
        "brand": brand,
        "product_url": url,
        "is_prime": is_prime,
        "is_fresh": is_amazon_fresh,
        "is_sponsored": is_sponsored,
        "is_featured_brand": is_featured_brand,
        "is_amazons_choice": is_amazons_choice,
        "is_best_seller": is_best_seller,
        "product_order": product_order,
        "search_term": search_term,
        "product_type": product_type,
        "price": price,
        "price_std": price_std,
        "filename": fn
    }
    
    return row

def process_search_result(fn, year='2021'):
    """Takes in a file parses it into a dictionary"""
    
    search_term = fn.split(year)[0].strip('/').split('/')[-1]    
    dom = html.fromstring(open(fn).read())
    products = dom.xpath('.//div[string-length(@data-asin) > 0]')
    data_out = []
    product_order = 1
    for product in products:
        if product.xpath('boolean(@data-component-type="s-search-result")'):
            row = parse_product_listing(product, fn, search_term, product_order, 
                                        product_type="regular_placement")
            data_out.append(row)
            product_order += 1
        elif product.xpath('boolean(ancestor::span[contains(@data-cel-widget, "MAIN-FEATURED_ASINS_LIST")]//span[contains(text(), "Amazon’s private and select exclusive brands")])'):
            row = parse_product_listing(product, fn, search_term, product_order, 
                                        product_type="featured_brands_carousel")
            data_out.append(row)
        elif product.xpath('boolean(ancestor::span[contains(@data-cel-widget, "MAIN-FEATURED_ASINS_LIST")]//span[contains(text(), "Sponsored")])'):
            row = parse_product_listing(product, fn, search_term, product_order, 
                                        product_type="misc_sponsored_carousel")
            row['is_sponsored'] = True
            data_out.append(row)

        elif product.xpath('boolean(ancestor::span[contains(@data-cel-widget, "MAIN-FEATURED_ASINS_LIST")])'):
            row = parse_product_listing(product, fn, search_term, product_order, 
                                        product_type="misc_carousel")
            data_out.append(row)

        elif product.xpath('boolean(ancestor::span[contains(@data-cel-widget, "MAIN-SHOPPING_ADVISER")])'):
            row = parse_product_listing(product, fn, search_term, product_order, 
                                        product_type="editorial_recs_carousel")
            data_out.append(row)
            
        elif product.xpath('boolean(ancestor::div[@data-aid])'):
            row = parse_product_listing(product, fn, search_term, -1, 
                                        product_type="sponsored_banner")
            row['is_sponsored'] = True
            data_out.append(row)
        else:
            row = parse_product_listing(product, fn, search_term, product_order, 
                                        product_type="regular_placement__missed")
            row['is_sponsored'] = True
            data_out.append(row)
            
    return data_out


def get_dispatch(data):
    """
    Returns the dispatch type. 
    This will help determine how to parse the record
    """
    return data[1]

def get_dispatch_canonical(data):
    """Gets the canonicle URL for certain searches."""
    for record in data:
        record_type = get_dispatch(record)
        if record_type == 'data-title-and-meta':
            return record[-1].get('canonical')
        
def process_our_brands_api(fn, year='2021'):
    """Takes in a file from s3 and parses it into a dictionary"""
    search_term = fn.split(year)[0].strip('/').split('/')[-1]
    stream = json.loads(open(fn).read())
    
    data_out = []
    for record in stream.strip('\n&&&\n').split('&&&'):
        try:
            record = json.loads(record)
        except ValueError:
            continue
        title = get_dispatch(record)
        if 'data-main-slot:search-result' in title:
            # read the HTML into LXML dom tree
            product_source_code = record[-1]['html']
            product_dom = html.fromstring(product_source_code)
            
            # parse out fields
            asin = product_dom.xpath("string(@data-asin)")
            product_name = clean_text_list_to_str(product_dom.xpath('.//h2//text()'))
            url = product_dom.xpath('string(.//h2//a//@href)')
            product_order = product_dom.xpath('string(@data-index)')

            row = {
                "asin": asin,
                "product_name": product_name,
                "product_url": url,
                "product_order": product_order,
                "fn": fn,
                "search_term": search_term
            }
            
            data_out.append(row)
    return data_out

def process_our_brands_filter(fn, year='2021'):
    data_out = []
    dom = html.fromstring(open(fn).read())
    search_term = fn.split(year)[0].strip('/').split('/')[-1]    

    # check these un-filtered searches.
    
    if not dom.xpath(
        'boolean(.//span[contains(text(), "Our Brands")])'
    ):
#         print("not our filtered")
        return []
    
    # need to pop off "all-departments stuff"
    all_dept_xpath = [
        './/span[@data-cel-widget="MAIN-TOP_BANNER_MESSAGE-1" and .//span[contains(text(), "No results")]]/../..',
        './/div[@data-asin="" and .//span[text() = "All Departments"]]',
         './/div[@data-asin="" and .//span[text() = "Showing results from All Departments"]]/..'
    ]
    
    for xpath in all_dept_xpath:
        for all_departments in dom.xpath(xpath):
            all_departments.getparent().remove(all_departments)
    
   
    products = dom.xpath(
        './/div[@data-component-type="s-search-result"]'
    )
    product_order = 1
    for product in products:
        asin = product.xpath("string(@data-asin)")
        product_name = clean_text_list_to_str(product.xpath('.//h2//text()'))
        url = product.xpath('string(.//h2//a//@href)')
        row = {
            "asin": asin,
            "product_name": product_name,
            "product_url": url,
            "product_order": product_order,
            "fn": fn,
            "search_term": search_term
        }
        data_out.append(row)
        product_order += 1
    return data_out

def process_best_sellers(fn):
    """"""
    data_out = []
    dom = html.document_fromstring(open(fn).read())
    category = dom.xpath('string(.//span[@class="category"])')
    path = ' > '.join(clean_text_list(dom.xpath('.//div[@id="zg-left-col"]//text()')))
    for tile in dom.xpath('.//li[@role="gridcell"]'):
        link = tile.xpath('string(.//a[@href]/@href)')
        asin = link.split('/dp/')[-1].split('/')[0]
        rank = tile.xpath('string(.//span[@class="zg-badge-text"]/text())')
        title = tile.xpath('string(.//img[@alt]/@alt)')
        record = {
            'product_url': link,
            'asin': asin,
            'rank': rank,
            'product_name': title,
            'category': category,
            'path': path,
            'fn': fn
        }
        data_out.append(record)
    return data_out

def parse_product_page(fn):
    """"""
    dom = html.fromstring(open(fn).read())
      
    if dom.xpath('boolean(.//div[@id="merchant-info" and '
                 'contains(text(), "Ships from and sold by Amazon") or'
                 'contains(text(), "Ships from and sold by ACI Gift Cards LLC, an Amazon company.")])'):
        sold_by = "Amazon.com"
        shipped_by= "Amazon.com"
    elif dom.xpath('boolean(.//div[@data-feature-name="audiblebuyboxv2"])'):
            sold_by = 'Amazon AUDIBLE'
            shipped_by = 'Amazon AUDIBLE'
    else:
        if dom.xpath('boolean(.//div[@data-client-id="primeAcquisition"])'):
            shipped_by = 'Amazon.com'
        else:
            shipped_by = clean_text_list_to_str(dom.xpath(
                '(.//span[@id="tabular-buybox-truncate-0"]//'
                'span[contains(@class, "a-truncate")]//text())[1]'))
            if not shipped_by:
                shipped_by = clean_text_list_to_str(dom.xpath(
                    '(.//div[@data-feature-name="freshShipsFromSoldBy"]'
                    '//span[@class="a-size-small a-color-base"]//text())[1]'))
        sold_by = clean_text_list_to_str(dom.xpath(
            '(.//span[@id="tabular-buybox-truncate-1"]'
            '//span[contains(@class, "a-truncate")]//text())[1]'))
        if not sold_by:
            sold_by = clean_text_list_to_str(dom.xpath(
                    '(.//div[@data-feature-name="freshShipsFromSoldBy"]'
                    '//span[@class="a-size-small a-color-base"]//text())[2]'))
        if not sold_by:
            if dom.xpath('boolean(.//div[@id="merchant-info" and '
                         'a[@id="SSOFpopoverLink" and '
                         'contains(text(), "Fulfilled by Amazon")]])'):
                sold_by = clean_text_list_to_str(dom.xpath(
                    './/a[@id="sellerProfileTriggerId"]//text()'))
                shipped_by = "Amazon.com"

            elif dom.xpath('boolean(.//div[@id="merchant-info" and '
                           'contains(text(), "Ships from and sold by")])'):
                sold_by = clean_text_list_to_str(
                    dom.xpath('.//a[@id="sellerProfileTriggerId"]//text()'))
                shipped_by = sold_by
            elif dom.xpath('boolean(.//td[@class="a-span1 a-color-secondary '
                           'a-text-left a-align-top kindlePriceLabel a-nowrap"])'):
                sold_by = 'Amazon KINDLE'
                shipped_by = 'Amazon KINDLE'
            elif dom.xpath('.//div[@data-cel-widget="bylineInfo" and .//span[contains(text(), "Kindle Edition")]]'):
                sold_by = 'Amazon KINDLE'
                shipped_by = 'Amazon KINDLE'
            else: # used products
                sold_by = clean_text_list_to_str(dom.xpath(
                    './/a[@id="sellerProfileTriggerId"]//text()'))

        
    no_buybox_winner = dom.xpath(
        'boolean(.//a[contains(@title,"See All Buying Options")])'
    )
    suggestions = clean_text_list(dom.xpath(
        './/*[@data-asin and not(@data-closed-captions)]//@data-asin'
    ))
    third_party = dom.xpath(
        'boolean(.//span[@data-action="show-all-offers-display"])'
    )
    by_amazon = dom.xpath(
        'boolean(.//a[@id="gc-brand-name-link" and contains(text(), "Amazon")])'
    )
    s_and_s = dom.xpath(
        'boolean(.//span[@class="a-size-small a-color-secondary" and '
        'contains(text(), "Ships from and sold by Amazon.com")])'
    )
    carousel = dom.xpath(
        'boolean(.//div[@data-a-carousel-options and '
        './/h2[contains(text(), "from our brands") or '
        'contains(text(), "Amazon Device")]]//@data-a-carousel-options)'
    )
    ads = []
    for ad in dom.xpath(
        './/*[@data-ad-details]'
    ):
        ads.append(etree.tostring(ad))
        
    
    if s_and_s:
        sold_by = 'Amazon.com'
        shipped_by = 'Amazon.com'
    
    is_out_of_stock = dom.xpath(
        'boolean(.//div[@id="outOfStock" or @id="almOutOfStockBuyBox_feature_div"])'
    )
    
    is_page_gone = dom.xpath(
        'boolean(.//a[@href="/dogsofamazon"])'
    )
    title = clean_text_list_to_str(dom.xpath(
        './/span[@id="productTitle"]//text()')
    )
        
    records = {
        'fn': fn,
        'title': title,
        'shipped_by': shipped_by,
        'sold_by': sold_by,
        'has_third_party_sellers': third_party,
        'product_by_amazon': by_amazon,
        'our_brands_carousel': carousel,
        'ads': ads,
        'no_buybox_winner': no_buybox_winner,
        'is_out_of_stock': is_out_of_stock,
        'is_page_gone': is_page_gone,
        'suggestions': suggestions
    }
    
    return records