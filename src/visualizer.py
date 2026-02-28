import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud


class Visualizer:

    # -------------------------------------------------
    # SENTIMENT BAR CHART
    # -------------------------------------------------
    def plot_sentiment_distribution(self, sentiment_counts: dict, blog_title: str):
        labels = list(sentiment_counts.keys())
        values = list(sentiment_counts.values())

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_xlabel("Sentiment Category")
        ax.set_ylabel("Number of Comments")
        ax.set_title(f"Sentiment Distribution - {blog_title}")
        plt.xticks(rotation=0)
        plt.tight_layout()
        return fig

    # -------------------------------------------------
    # POPULARITY VS POSITIVE SENTIMENT
    # -------------------------------------------------
    def plot_popularity_vs_sentiment(self, popularity_list: list, positive_percentages: list):
        fig, ax = plt.subplots()
        ax.scatter(popularity_list, positive_percentages)
        ax.set_xlabel("Popularity Score (Likes + Shares)")
        ax.set_ylabel("Positive Sentiment (%)")
        ax.set_title("Popularity vs Positive Sentiment")
        plt.tight_layout()
        return fig

    # -------------------------------------------------
    # TOP WORD FREQUENCY BAR CHART
    # -------------------------------------------------
    def plot_top_words(self, word_counter: Counter, top_n: int = 10):
        most_common = word_counter.most_common(top_n)
        words = [item[0] for item in most_common]
        counts = [item[1] for item in most_common]

        fig, ax = plt.subplots()
        ax.bar(words, counts)
        ax.set_xlabel("Words")
        ax.set_ylabel("Frequency")
        ax.set_title("Top Word Frequencies")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    # -------------------------------------------------
    # WORD CLOUD
    # -------------------------------------------------
    def plot_wordcloud(self, word_counter: Counter):
        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(word_counter)

        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        ax.set_title("Word Cloud of Blog Content")
        plt.tight_layout()
        return fig