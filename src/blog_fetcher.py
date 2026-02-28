import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.parse import urlparse
from serpapi import GoogleSearch
import re
import time


@dataclass
class BlogPost:
    title: str
    url: str
    author: str
    date: str
    source: str
    raw_html: str
    main_text: str


class BlogFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def search_blogs(self, keyword: str, limit: int = 10):
        """
        Search blog URLs using SerpAPI
        """
        blogs = []
        limit = min(limit, 10)

        for start in range(0, limit, 10):
            params = {
                "engine": "google",
                "q": f"{keyword} blog",
                "api_key": self.api_key,
                "num": 10,
                "start": start
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            organic_results = results.get("organic_results", [])

            for item in organic_results:
                title = item.get("title", "")
                link = item.get("link", "")

                if title and link:
                    blogs.append({"title": title, "url": link})

                if len(blogs) >= limit:
                    break

            time.sleep(1)

            if len(blogs) >= limit:
                break

        return blogs

    def fetch_blog_content(self, blog_info: dict) -> BlogPost:
        """
        Fetch and extract blog content and metadata
        """
        url = blog_info["url"]
        title = blog_info["title"]

        try:
            response = requests.get(url, timeout=10)
            html = response.text
        except Exception:
            return None

        soup = BeautifulSoup(html, "html.parser")

        # Extract author (if available)
        author = self._extract_author(soup)

        # Extract publication date
        date = self._extract_date(soup)

        # Extract main text
        main_text = self._extract_main_text(soup)

        source = urlparse(url).netloc

        return BlogPost(
            title=title,
            url=url,
            author=author,
            date=date,
            source=source,
            raw_html=html,
            main_text=main_text
        )

    def fetch_multiple(self, keyword: str, limit: int = 10):
        """
        Fetch multiple blogs and return structured BlogPost objects
        """
        blog_links = self.search_blogs(keyword, limit)
        blog_posts = []

        for blog in blog_links:
            blog_post = self.fetch_blog_content(blog)
            if blog_post and blog_post.main_text:
                blog_posts.append(blog_post)

        return blog_posts

    def _extract_author(self, soup):
        # Common meta tag patterns
        author_meta = soup.find("meta", attrs={"name": "author"})
        if author_meta:
            return author_meta.get("content", "Unknown")

        author_class = soup.find(attrs={"class": re.compile("author", re.I)})
        if author_class:
            return author_class.get_text(strip=True)

        return "Unknown"

    def _extract_date(self, soup):
        date_meta = soup.find("meta", attrs={"property": "article:published_time"})
        if date_meta:
            return date_meta.get("content", "Unknown")

        time_tag = soup.find("time")
        if time_tag:
            return time_tag.get_text(strip=True)

        return "Unknown"

    def _extract_main_text(self, soup):
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

        # Basic cleaning
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text