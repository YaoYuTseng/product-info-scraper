from pathlib import Path

import matplotlib.pyplot as plt
from wordcloud import WordCloud

from constants import OUTPUT_DIR


# Function to create and save a word cloud
def create_word_cloud(title: str, word_count: tuple[str, int], dir: Path = OUTPUT_DIR):
    word_count_dict = {k: v for k, v in word_count}
    wordcloud = WordCloud(width=1200, height=600, background_color="white")
    wordcloud = wordcloud.generate_from_frequencies(word_count_dict)

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title, fontsize=24, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(Path(dir, f"{title}.png"))
    plt.close()
