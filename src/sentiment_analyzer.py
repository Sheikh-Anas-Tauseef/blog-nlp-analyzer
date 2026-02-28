import random
from typing import List, Dict
from collections import Counter
import numpy as np

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon (safe if already exists)
nltk.download("vader_lexicon", quiet=True)


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    # -------------------------------------------------
    # COMMENT GENERATION (Balanced Sentiments)
    # -------------------------------------------------
    def generate_comments(self, blog_title: str, num_comments: int = 20) -> List[str]:
        positive_templates = [
            f"I really enjoyed reading about {blog_title}.",
            f"This article on {blog_title} was very insightful.",
            f"Great explanation of {blog_title}, well written!",
            f"Excellent post about {blog_title}, learned a lot."
        ]

        neutral_templates = [
            f"This blog discusses {blog_title}.",
            f"The article covers several points about {blog_title}.",
            f"It provides information regarding {blog_title}.",
            f"An overview of {blog_title} is presented here."
        ]

        negative_templates = [
            f"I disagree with some arguments in {blog_title}.",
            f"This article on {blog_title} lacks depth.",
            f"Not fully convinced by this discussion on {blog_title}.",
            f"The explanation of {blog_title} could be clearer."
        ]

        comments = []

        for _ in range(num_comments):
            sentiment_type = random.choices(
                ["positive", "neutral", "negative"],
                weights=[0.5, 0.3, 0.2],  # realistic distribution
                k=1
            )[0]

            if sentiment_type == "positive":
                comments.append(random.choice(positive_templates))
            elif sentiment_type == "neutral":
                comments.append(random.choice(neutral_templates))
            else:
                comments.append(random.choice(negative_templates))

        return comments

    # -------------------------------------------------
    # SENTIMENT CLASSIFICATION
    # -------------------------------------------------
    def analyze_comments(self, comments: List[str]) -> Dict[str, int]:
        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}

        for comment in comments:
            score = self.analyzer.polarity_scores(comment)["compound"]

            if score >= 0.05:
                sentiment_counts["Positive"] += 1
            elif score <= -0.05:
                sentiment_counts["Negative"] += 1
            else:
                sentiment_counts["Neutral"] += 1

        return sentiment_counts

    # -------------------------------------------------
    # POPULARITY SIMULATION
    # -------------------------------------------------
    def simulate_popularity(self) -> Dict[str, int]:
        likes = random.randint(50, 500)
        shares = random.randint(10, 200)
        popularity_score = likes + shares

        return {
            "likes": likes,
            "shares": shares,
            "popularity_score": popularity_score
        }

    # -------------------------------------------------
    # SENTIMENT PERCENTAGES
    # -------------------------------------------------
    def sentiment_percentages(self, sentiment_counts: Dict[str, int]) -> Dict[str, float]:
        total = sum(sentiment_counts.values())
        if total == 0:
            return {k: 0 for k in sentiment_counts}

        return {
            k: round((v / total) * 100, 2)
            for k, v in sentiment_counts.items()
        }

    # -------------------------------------------------
    # CORRELATION ANALYSIS
    # -------------------------------------------------
    def compute_correlation(self, popularity_list: List[int], positive_percentages: List[float]) -> float:
        if len(popularity_list) < 2:
            return 0.0

        correlation_matrix = np.corrcoef(popularity_list, positive_percentages)
        return round(float(correlation_matrix[0, 1]), 3)