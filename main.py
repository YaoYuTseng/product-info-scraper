from pathlib import Path

import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from constants import *
from helper import create_word_cloud
from logging_setup import LOGGER
from models.Product import Product
from models.ProductWordCount import ProductWordCount
from Scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    switch_products: dict[str, list[Product]] = {}
    product_word_counts: list[ProductWordCount] = []

    # robots.txt: https://www.netgear.com/robots.txt
    # Navigate to NETGEAR switch product root page and get product categories and their hrefs
    scraper.navigate_to(SWITCH_HREF)
    cateogries = scraper.locate_multiple(CATEGORIES_XPATH)
    category_hrefs = {
        a.text.replace("Shop ", ""): a.get_attribute("href") for a in cateogries
    }
    LOGGER.info(
        f"NETGEAR switch categories include: {[k for k in category_hrefs.keys()]}"
    )

    # Navigate to each of the category page
    for category, href in category_hrefs.items():
        scraper.navigate_to(href)
        try:
            if category == "AV over IP Switches":
                products = scraper.locate_multiple(AVOIP_PRODUCTS_XPATH)
            else:
                products = scraper.locate_multiple(OTHER_PRODUCTS_XPATH)
        except TimeoutException:
            LOGGER.warning(
                f"(Category: {category}) Product hrefs not found. See {href}"
            )
            continue

        # Navigate to each product in said category and store it info in Product object
        product_refs = {a.text: a.get_attribute("href") for a in products}
        switch_products[category] = []
        for product, href in product_refs.items():
            scraper.navigate_to(href)

            try:
                p_info = Product()
                p_info.category = category
                p_info.model = scraper.locate_one(MODEL_XPATH).text
                p_info.title = scraper.locate_one(TITLE_XPATH).text
                p_info.highlight = scraper.locate_one(HIGHLIGHT_XPATH).text

                desc_block = scraper.locate_one(DESC_BLOCK_XPATH)
                description = desc_block.find_elements(By.XPATH, ".//p | .//li")
                p_info.description = ".".join([t.text for t in description])

            except TimeoutException:
                LOGGER.warning(f"(Product: {product}) Info incomplete. See {href}")
                continue

            if p_info in switch_products[category]:
                LOGGER.warning(f"(Product: {product}) Duplicate records. See {href}")
                continue

            switch_products[category].append(p_info)

    # Concatenate all product into a new 'all' category
    all_products = [p for c in switch_products for p in switch_products[c]]
    switch_products["all"] = all_products

    # Get word count for descriptive info (highlight & description)
    for category, p_lst in switch_products.items():
        h_texts = [p.highlight for p in p_lst]
        h_count = ProductWordCount(category, "highlight", h_texts)
        h_count.count_words()

        d_texts = [p.description for p in p_lst]
        d_count = ProductWordCount(category, "description", d_texts)
        d_count.count_words()

        product_word_counts.append(h_count)
        product_word_counts.append(d_count)

    # Output product overview
    to_df_view = [vars(p) for p in all_products]
    df_view = pd.DataFrame(to_df_view)
    df_view.to_csv(Path(OUTPUT_DIR, "product_view.csv"), index=False)

    # Output product word counts
    to_df_count = [
        {k: v for k, v in vars(c).items() if k in ["category", "count_for", "count"]}
        for c in product_word_counts
    ]
    df_count = pd.DataFrame(to_df_count)
    df_count.to_csv(Path(OUTPUT_DIR, "product_word_count.csv"), index=False)

    # Output word clouds
    create_word_cloud("Highlights_Wordcloud", h_count.count)
    create_word_cloud("Descriptions_Wordcloud", d_count.count)

    scraper.close()
