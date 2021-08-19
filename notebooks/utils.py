import pandas as pd

def value_counts(df: pd.DataFrame, 
                 col: str, 
                 *args, **kwargs) -> pd.DataFrame:
    """
    For a DataFrame (`df`): display normalized (percentage) 
    `value_counts(normalize=True)` and regular counts 
    `value_counts()` for a given `col`.
    """
    count = df[col].value_counts(*args, **kwargs).to_frame(name='count')
    perc = df[col].value_counts(normalize=True, *args,**kwargs) \
                  .to_frame(name='percentage')
    
    return pd.concat([count, perc], axis=1)


def calculate_table(df, amazon_asin):
    
    df_s = df[df.is_sponsored == True]
    df_ns = df[df.is_sponsored == False]
    
    n_samples = df.search_term.nunique()
    n_products = df.asin.nunique()    
    
    df_amazon = df_ns[df_ns.asin.isin(amazon_asin)]
    df_amazon_not_featured = df_amazon[df_amazon.is_featured_brand == False]

    df_non_amazon = df_ns[(~df_ns.asin.isin(amazon_asin))]
    df_non_amazon_non_sold_ = df_ns[(~df_ns.asin.isin(amazon_asin)) & 
                                   (df_ns.is_sold_by_amazon == False) &
                                   (df_ns.is_fresh == False)]
    df_non_amazon_sold_by_amazon_ = df_ns[
        (~df_ns.asin.isin(amazon_asin)) & 
        (df_ns.is_sold_by_amazon == True)
    ]
    
    df_amazon_brand_ = df_ns[df_ns.asin.isin(amazon_asin)]
    df_non_amazon_brand_ = df_ns[~df_ns.asin.isin(df_amazon.asin)]

    df_amazon_sold_ = df_ns[df_ns.is_sold_by_amazon == True]
    df_not_amazon_sold_ = df_ns[df_ns.is_sold_by_amazon != True]

    df_prime_ =  df_ns[df_ns.is_shipped_by_amazon_TRUE == True]
    df_prime_no_amazon =  df_prime_[~df_prime_.asin.isin(amazon_asin)]

    df_non_amazon_ = df_ns[
        (~df_ns.asin.isin(amazon_asin))
      & (df_ns.is_sold_by_amazon == False)
      & (df_ns.is_shipped_by_amazon == False)
      & (df_ns.is_prime == False) 
      & (df_ns.is_fresh == False)
    ]

    res = pd.DataFrame([
         {
            'Category': 'Wholly Non-Amazon',
            'Perc Products': df_non_amazon_[
                ~df_non_amazon_.is_sold_by_amazon.isnull()
            ].asin.nunique() / n_products* 100,
            'Perc #1 spot': df_non_amazon_[df_non_amazon_.product_order == 1].search_term.nunique() / n_samples* 100,
             'Perc first row': df_non_amazon_[df_non_amazon_.product_order <= 3].search_term.nunique() / n_samples* 100,
        },
        {
            'Category': 'Amazon',
            'Perc Products': df_amazon_brand_.asin.nunique() / n_products * 100,
            'Perc #1 spot': df_amazon_brand_[df_amazon_brand_.product_order == 1].search_term.nunique() / n_samples * 100,
            'Perc first row': df_amazon_brand_[df_amazon_brand_.product_order <= 3].search_term.nunique() / n_samples * 100,
            
        },

        {
            'Category': 'Non-Amazon',
            'Perc Products': df_non_amazon_brand_.asin.nunique() / n_products* 100,
            'Perc #1 spot': df_non_amazon_brand_[df_non_amazon_brand_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_non_amazon_brand_[df_non_amazon_brand_.product_order <= 3].search_term.nunique() / n_samples* 100,
            
        },
        {
            'Category': 'Non-Amazon Brand and Not Amazon Sold',
            'Perc Products': df_non_amazon_non_sold_.asin.nunique() / n_products* 100,
            'Perc #1 spot': df_non_amazon_non_sold_[df_non_amazon_non_sold_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_non_amazon_non_sold_[df_non_amazon_non_sold_.product_order <= 3].search_term.nunique() / n_samples* 100,
            
        },
         {
            'Category': 'Amazon product not featured',
            'Perc Products': df_amazon_not_featured.asin.nunique() / n_products * 100,
            'Perc #1 spot': df_amazon_not_featured[df_amazon_not_featured.product_order == 1].search_term.nunique() / n_samples * 100,
            'Perc first row': df_amazon_not_featured[df_amazon_not_featured.product_order <= 3].search_term.nunique() / n_samples * 100,
        },

         {
            'Category': 'Sponsored',
            'Perc Products': (df_s.asin.nunique() / n_products) * 100,
            'Perc #1 spot': df_s[df_s.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_s[df_s.product_order <= 3].search_term.nunique() / n_samples* 100,
        },

        {
            'Category': 'Amazon sold',
            'Perc Products': df_amazon_sold_.asin.nunique() / n_products * 100,
            'Perc #1 spot': df_amazon_sold_[df_amazon_sold_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_amazon_sold_[df_amazon_sold_.product_order <= 3].search_term.nunique() / n_samples* 100,
           
        },
        {
            'Category': 'Amazon sold non-Amazon',
            'Perc Products':  df_non_amazon_sold_by_amazon_.asin.nunique() / n_products * 100,
            'Perc #1 spot':  df_non_amazon_sold_by_amazon_[ df_non_amazon_sold_by_amazon_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row':  df_non_amazon_sold_by_amazon_[ df_non_amazon_sold_by_amazon_.product_order <= 3].search_term.nunique() / n_samples* 100,
           
        },

         {
            'Category': 'Non-Amazon sold',
            'Perc Products': df_not_amazon_sold_.asin.nunique() / n_products * 100,
            'Perc #1 spot': df_not_amazon_sold_[df_not_amazon_sold_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_not_amazon_sold_[df_not_amazon_sold_.product_order <= 3].search_term.nunique() / n_samples* 100,
             
        },

        {
            'Category': 'Amazon Shipped',
            'Perc Products': df_prime_.asin.nunique() / n_products * 100,
            'Perc #1 spot': df_prime_[df_prime_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_prime_[df_prime_.product_order <= 3].search_term.nunique() / n_samples* 100,

        },
        
        {
            'Category': 'Amazon Shipped non-Amazon',
            'Perc Products': df_prime_no_amazon.asin.nunique() / n_products * 100,
            'Perc #1 spot': df_prime_no_amazon[df_prime_no_amazon.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_prime_no_amazon[df_prime_no_amazon.product_order <= 3].search_term.nunique() / n_samples* 100,
        }

    ])
                                    
    return res

def calculate_table_not_unique(df, amazon_asin):
    
    df_s = df[df.is_sponsored == True]
    df_ns = df[df.is_sponsored == False]
    
    n_samples = df.search_term.nunique()
    n_products = len(df)
    
    df_amazon = df_ns[df_ns.asin.isin(amazon_asin)]
    df_amazon_not_featured = df_amazon[df_amazon.is_featured_brand == False]

    df_non_amazon = df_ns[(~df_ns.asin.isin(amazon_asin))]
    df_non_amazon_non_sold_ = df_ns[(~df_ns.asin.isin(amazon_asin)) & 
                                   (df_ns.is_sold_by_amazon == False) &
                                   (df_ns.is_fresh == False)]
    df_non_amazon_sold_by_amazon_ = df_ns[
        (~df_ns.asin.isin(amazon_asin)) & 
        (df_ns.is_sold_by_amazon == True)
    ]
    
    df_amazon_brand_ = df_ns[df_ns.asin.isin(amazon_asin)]
    df_non_amazon_brand_ = df_ns[~df_ns.asin.isin(df_amazon.asin)]

    df_amazon_sold_ = df_ns[df_ns.is_sold_by_amazon == True]
    df_not_amazon_sold_ = df_ns[df_ns.is_sold_by_amazon != True]

    df_prime_ =  df_ns[df_ns.is_shipped_by_amazon_TRUE == True]
    df_prime_no_amazon =  df_prime_[~df_prime_.asin.isin(amazon_asin)]

    df_non_amazon_ = df_ns[
        (~df_ns.asin.isin(amazon_asin))
      & (df_ns.is_sold_by_amazon == False)
      & (df_ns.is_shipped_by_amazon == False)
      & (df_ns.is_prime == False) 
      & (df_ns.is_fresh == False)
    ]

    res = pd.DataFrame([
         {
            'Category': 'Wholly Non-Amazon',
            'Perc Products': len(df_non_amazon_[
                ~df_non_amazon_.is_sold_by_amazon.isnull()
            ]) / n_products * 100,
            'Perc #1 spot': df_non_amazon_[df_non_amazon_.product_order == 1].search_term.nunique() / n_samples* 100,
             'Perc first row': df_non_amazon_[df_non_amazon_.product_order <= 3].search_term.nunique() / n_samples* 100,
        },
        {
            'Category': 'Amazon',
            'Perc Products': len(df_amazon_brand_) / n_products * 100,
            'Perc #1 spot': df_amazon_brand_[df_amazon_brand_.product_order == 1].search_term.nunique() / n_samples * 100,
            'Perc first row': df_amazon_brand_[df_amazon_brand_.product_order <= 3].search_term.nunique() / n_samples * 100,
            
        },

        {
            'Category': 'Non-Amazon',
            'Perc Products': len(df_non_amazon_brand_) / n_products* 100,
            'Perc #1 spot': df_non_amazon_brand_[df_non_amazon_brand_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_non_amazon_brand_[df_non_amazon_brand_.product_order <= 3].search_term.nunique() / n_samples* 100,
            
        },
        {
            'Category': 'Non-Amazon Brand and Not Amazon Sold',
            'Perc Products': len(df_non_amazon_non_sold_) / n_products* 100,
            'Perc #1 spot': df_non_amazon_non_sold_[df_non_amazon_non_sold_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_non_amazon_non_sold_[df_non_amazon_non_sold_.product_order <= 3].search_term.nunique() / n_samples* 100,
            
        },
         {
            'Category': 'Amazon product not featured',
            'Perc Products': len(df_amazon_not_featured) / n_products * 100,
            'Perc #1 spot': df_amazon_not_featured[df_amazon_not_featured.product_order == 1].search_term.nunique() / n_samples * 100,
            'Perc first row': df_amazon_not_featured[df_amazon_not_featured.product_order <= 3].search_term.nunique() / n_samples * 100,
        },

         {
            'Category': 'Sponsored',
            'Perc Products': len(df_s) / n_products * 100,
            'Perc #1 spot': df_s[df_s.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_s[df_s.product_order <= 3].search_term.nunique() / n_samples* 100,
        },

        {
            'Category': 'Amazon sold',
            'Perc Products': len(df_amazon_sold_) / n_products * 100,
            'Perc #1 spot': df_amazon_sold_[df_amazon_sold_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_amazon_sold_[df_amazon_sold_.product_order <= 3].search_term.nunique() / n_samples* 100,
           
        },
        {
            'Category': 'Amazon sold non-Amazon',
            'Perc Products':  len(df_non_amazon_sold_by_amazon_) / n_products * 100,
            'Perc #1 spot':  df_non_amazon_sold_by_amazon_[ df_non_amazon_sold_by_amazon_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row':  df_non_amazon_sold_by_amazon_[ df_non_amazon_sold_by_amazon_.product_order <= 3].search_term.nunique() / n_samples* 100,
           
        },

         {
            'Category': 'Non-Amazon sold',
            'Perc Products': len(df_not_amazon_sold_) / n_products * 100,
            'Perc #1 spot': df_not_amazon_sold_[df_not_amazon_sold_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_not_amazon_sold_[df_not_amazon_sold_.product_order <= 3].search_term.nunique() / n_samples* 100,
             
        },

        {
            'Category': 'Amazon Shipped',
            'Perc Products': len(df_prime_) / n_products * 100,
            'Perc #1 spot': df_prime_[df_prime_.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_prime_[df_prime_.product_order <= 3].search_term.nunique() / n_samples* 100,

        },
        
        {
            'Category': 'Amazon Shipped non-Amazon',
            'Perc Products': len(df_prime_no_amazon) / n_products * 100,
            'Perc #1 spot': df_prime_no_amazon[df_prime_no_amazon.product_order == 1].search_term.nunique() / n_samples* 100,
            'Perc first row': df_prime_no_amazon[df_prime_no_amazon.product_order <= 3].search_term.nunique() / n_samples* 100,
        }

    ])
                                    
    return res