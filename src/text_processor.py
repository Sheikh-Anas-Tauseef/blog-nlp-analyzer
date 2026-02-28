import re
from typing import List, Dict
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer


# Download required NLTK resources (safe if already installed)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)


class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    # -------------------------------------------------
    # BASIC CLEANING
    # -------------------------------------------------
    def clean_text(self, text: str) -> str:
        text = re.sub(r"[^A-Za-z\s]", "", text)
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def tokenize(self, text: str) -> List[str]:
        words = text.split()
        words = [
            self.lemmatizer.lemmatize(w)
            for w in words
            if w not in self.stop_words and len(w) > 3
        ]
        return words

    def preprocess(self, text: str) -> List[str]:
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        return tokens

    # -------------------------------------------------
    # KEYWORD EXTRACTION (TF-IDF)
    # -------------------------------------------------
    def extract_keywords(self, documents: List[str], top_n: int = 10) -> Dict[int, List[str]]:
        """
        Returns top keywords for each document using TF-IDF.
        Output format:
        {
            0: ['keyword1', 'keyword2', ...],
            1: [...],
            ...
        }
        """

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=1000
        )

        tfidf_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()

        keywords = {}

        for doc_index in range(tfidf_matrix.shape[0]):
            scores = tfidf_matrix[doc_index].toarray().flatten()
            top_indices = scores.argsort()[-top_n:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            keywords[doc_index] = top_words

        return keywords

    # -------------------------------------------------
    # GLOBAL WORD FREQUENCY (for trend analysis)
    # -------------------------------------------------
    def global_word_frequency(self, token_lists: List[List[str]]) -> Counter:
        all_words = []
        for tokens in token_lists:
            all_words.extend(tokens)
        return Counter(all_words)

    # -------------------------------------------------
    # MOTIVE CLASSIFICATION (Rule-Based)
    # -------------------------------------------------
    def classify_motive(self, text: str) -> str:
        text = text.lower()

        promotional_keywords = ["buy", "register", "sign up", "offer", "free trial", "discount"]
        research_keywords = ["study", "research", "paper", "experiment", "analysis", "dataset"]
        educational_keywords = ["tutorial", "guide", "how to", "learn", "introduction", "basics"]

        if any(word in text for word in promotional_keywords):
            return "Promotional"

        elif any(word in text for word in research_keywords):
            return "Research-Oriented"

        elif any(word in text for word in educational_keywords):
            return "Educational"

        else:
            return "Informational"