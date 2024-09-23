from pathlib import Path

OUTPUT_DIR = Path("output")

SWITCH_HREF = "https://www.netgear.com/business/wired/switches/"

# XPATHs for product navigation
CATEGORIES_XPATH = "//a[@class='btn cta']"
AVOIP_PRODUCTS_XPATH = "//div[@class='atc_desc_padding']/a"
OTHER_PRODUCTS_XPATH = "//p[@class='eyebrow-small']/a"

# XPATH for acquiring product details
MODEL_XPATH = "//li[@class='breadcrumb-item active']//span[@itemprop='name']"
TITLE_XPATH = "//div[@class='title-block']//h2"
HIGHLIGHT_XPATH = "//div[@class='title-block']//h1"
DESC_BLOCK_XPATH = "//div[@class='title-block product-desc-block']"
