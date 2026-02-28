import streamlit as st
import os
from collections import Counter
from dotenv import load_dotenv

from blog_fetcher import BlogFetcher
from text_processor import TextProcessor
from sentiment_analyzer import SentimentAnalyzer
from visualizer import Visualizer

# Load environment variables from .env file
load_dotenv()


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Blog Sentiment Intelligence", layout="wide")

st.title("Web Blog Sentiment & Engagement Analysis System")
st.markdown("Analyze blog themes, sentiment, and engagement patterns.")


# -------------------------------
# USER INPUT
# -------------------------------
keyword = st.text_input("Enter Keyword (e.g., machine learning)")
limit = st.slider("Number of Blogs", min_value=3, max_value=10, value=5)

analyze_button = st.button("Analyze Blogs")


# -------------------------------
# MAIN LOGIC
# -------------------------------
if analyze_button and keyword:

    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        st.error("Please set SERPAPI_KEY as an environment variable.")
        st.stop()

    fetcher = BlogFetcher(api_key)
    processor = TextProcessor()
    sentiment = SentimentAnalyzer()
    viz = Visualizer()

    with st.spinner("Fetching blogs..."):
        blogs = fetcher.fetch_multiple(keyword, limit)

    if not blogs:
        st.warning("No blogs found.")
        st.stop()

    blog_results = []
    all_popularity = []
    all_positive_percent = []
    global_tokens = []

    st.subheader("Blog Analysis Summary")

    for blog in blogs:

        tokens = processor.preprocess(blog.main_text)
        global_tokens.extend(tokens)

        motive = processor.classify_motive(blog.main_text)

        comments = sentiment.generate_comments(blog.title, 25)
        sentiment_counts = sentiment.analyze_comments(comments)
        sentiment_percent = sentiment.sentiment_percentages(sentiment_counts)

        popularity_data = sentiment.simulate_popularity()

        all_popularity.append(popularity_data["popularity_score"])
        all_positive_percent.append(sentiment_percent["Positive"])

        blog_results.append({
            "Title": blog.title,
            "Source": blog.source,
            "Author": blog.author,
            "Date": blog.date,
            "Motive": motive,
            "Popularity": popularity_data["popularity_score"],
            "Positive %": sentiment_percent["Positive"],
            "Neutral %": sentiment_percent["Neutral"],
            "Negative %": sentiment_percent["Negative"]
        })

    st.dataframe(blog_results, use_container_width=True)

    correlation = sentiment.compute_correlation(all_popularity, all_positive_percent)

    st.markdown(f"### Correlation between Popularity and Positive Sentiment: `{correlation}`")

    # -------------------------------
    # VISUALIZATIONS
    # -------------------------------

    st.subheader("Sentiment Distribution (First Blog Example)")
    fig1 = viz.plot_sentiment_distribution(sentiment_counts, blogs[0].title)
    st.pyplot(fig1)

    st.subheader("Popularity vs Positive Sentiment")
    fig2 = viz.plot_popularity_vs_sentiment(all_popularity, all_positive_percent)
    st.pyplot(fig2)

    word_counter = Counter(global_tokens)

    st.subheader("Top Word Frequencies")
    fig3 = viz.plot_top_words(word_counter, 10)
    st.pyplot(fig3)

    st.subheader("Word Cloud")
    fig4 = viz.plot_wordcloud(word_counter)
    st.pyplot(fig4)