import string
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from logging_setup import LOGGER


@dataclass
class ProductWordCount:
    category: str
    count_for: str
    texts: list[str]
    count: Optional[list[tuple]] = None
    _num_of_count: int = 20

    @staticmethod
    def tokenize_texts(texts: list[str]) -> list[str]:
        try:
            blob = " ".join(texts).lower()
            tokens = word_tokenize(blob)
            return tokens
        except Exception as e:
            LOGGER.error(e)
            return []

    @staticmethod
    def filter_meaningless(tokens: list[str]) -> list[str]:
        try:
            ignore_words = set(stopwords.words("english"))
            punct = set(string.punctuation)
            filtered = [
                t
                for t in tokens
                if t.lower() not in ignore_words  # Not stopword
                and t not in punct  # Not punctuation
                and not (t.isdigit() and len(t) == 1)  # Not single digit
            ]
            return filtered
        except Exception as e:
            LOGGER.error(e)
            return []

    def count_words(self) -> None:
        tokens = self.tokenize_texts(self.texts)
        tokens = self.filter_meaningless(tokens)
        try:
            word_count = Counter(tokens)
            self.count = word_count.most_common(self._num_of_count)
        except Exception as e:
            LOGGER.critical("Fail to count words")
            LOGGER.error(e)
