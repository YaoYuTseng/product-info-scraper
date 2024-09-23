from pathlib import Path

import nltk

from logging_setup import LOGGER


def nltk_setup() -> None:
    # Create nltk_data directory if not existed
    NLTK_DATA = Path("nltk_data")
    if not NLTK_DATA.exists():
        NLTK_DATA.mkdir()
        LOGGER.info("Create nltk data folder")
    if not str(NLTK_DATA) in nltk.data.path:
        nltk.data.path.append(str(NLTK_DATA))
        LOGGER.info("Add nltk data folder path")

    # Download necessary files if not existed
    if not Path(NLTK_DATA, "tokenizers", "punkt_tab").exists():
        nltk.download("punkt_tab", download_dir=NLTK_DATA)
        LOGGER.info("Download nltk punkt_tab")
    if not Path(NLTK_DATA, "corpora", "stopwords").exists():
        nltk.download("stopwords", download_dir=NLTK_DATA)
        LOGGER.info("Download nltk stopwords")


nltk_setup()
