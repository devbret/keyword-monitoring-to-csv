import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from config import KEYWORDS

def is_internal(url, base):
    return urlparse(url).netloc == urlparse(base).netloc

def fetch_website_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def search_keywords(content, keywords):
    found_keywords = [kw for kw in keywords if kw.lower() in content.lower()]
    return found_keywords

def crawl_site(start_url, keywords, max_links=2):
    visited = set()
    site_alerts = []

    def crawl(url):
        if len(visited) >= max_links:
            return
        if url in visited:
            return
        visited.add(url)
        print(f"Crawling: {url}")

        content = fetch_website_content(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            found_keywords = search_keywords(soup.get_text(), keywords)
            if found_keywords:
                site_alerts.append({"url": url, "keywords": found_keywords})

            for link in soup.find_all('a', href=True):
                href = urljoin(url, link.get('href'))
                if is_internal(href, start_url) and href not in visited:
                    crawl(href)

    crawl(start_url)
    return site_alerts

def scrape_and_search(websites, keywords):
    all_alerts = []
    for url in websites:
        print(f"Starting crawl on: {url}")
        alerts = crawl_site(url, keywords)
        all_alerts.extend(alerts)
    return all_alerts

