import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import schedule
import csv
from datetime import datetime
import os

KEYWORDS = ["data breach", "cyber attack", "ransomware", "zero-day", "APT"]
WEBSITES = [
    "https://www.exampleone.com/",
    "https://www.exampletwo.com/",
    "https://www.examplethree.com/",
]

os.makedirs('csv-files', exist_ok=True)

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

def is_pdf_link(url):
    return url.lower().endswith('.pdf')

def crawl_site(start_url, keywords, max_links=100):
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
                if is_internal(href, start_url) and href not in visited and not is_pdf_link(href):
                    crawl(href)

    crawl(start_url)
    return site_alerts

def write_alerts_to_csv(alerts):
    filename = f"csv-files/keyword_alerts_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Keywords Found', 'Timestamp'])
        for alert in alerts:
            writer.writerow([alert['url'], ', '.join(alert['keywords']), datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    print(f"Alerts written to {filename}")

def run_monitoring():
    print("Running Keyword Alert Monitoring...")
    all_alerts = []
    for url in WEBSITES:
        print(f"Starting crawl on: {url}")
        alerts = crawl_site(url, KEYWORDS)
        all_alerts.extend(alerts)
    if all_alerts:
        write_alerts_to_csv(all_alerts)
    else:
        print("No alerts found.")

def schedule_monitoring():
    schedule.every(60).minutes.do(run_monitoring)
    print("Monitoring scheduled to run every 60 minutes.")

if __name__ == "__main__":
    print("Initial run of the monitoring system.")
    run_monitoring()
    schedule_monitoring()
    while True:
        schedule.run_pending()
        time.sleep(1)
