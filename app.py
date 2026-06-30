import os
import re
import csv
import time
import logging
from datetime import datetime
from urllib.parse import urlparse, urljoin, urldefrag

import requests
import schedule
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def get_list_env(name):
    raw = os.getenv(name, "")
    items = (item.strip().strip("\"'") for item in raw.split(","))
    return [item for item in items if item]


KEYWORDS = get_list_env("KEYWORDS")
WEBSITES = get_list_env("WEBSITES")
INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", "60"))
MAX_LINKS = int(os.getenv("MAX_LINKS", "100"))

RUN_LOG = "csv-files/monitoring_runs.csv"

os.makedirs("csv-files", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("monitoring.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

KEYWORD_PATTERNS = {
    kw: re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE) for kw in KEYWORDS
}


def is_internal(url, base):
    return urlparse(url).netloc == urlparse(base).netloc


def fetch_website_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


def search_keywords(content):
    return [kw for kw, pattern in KEYWORD_PATTERNS.items() if pattern.search(content)]


def is_pdf_link(url):
    return url.lower().endswith(".pdf")


def crawl_site(start_url, max_links=MAX_LINKS):
    visited = set()
    site_alerts = []

    def crawl(url):
        if len(visited) >= max_links:
            return
        if url in visited:
            return
        visited.add(url)
        logger.info(f"Crawling: {url}")

        content = fetch_website_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            found_keywords = search_keywords(soup.get_text())
            if found_keywords:
                site_alerts.append(
                    {
                        "url": url,
                        "keywords": found_keywords,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

            for link in soup.find_all("a", href=True):
                href, _ = urldefrag(urljoin(url, link.get("href")))
                if (
                    is_internal(href, start_url)
                    and href not in visited
                    and not is_pdf_link(href)
                ):
                    crawl(href)

    crawl(start_url)
    return site_alerts, len(visited)


def write_alerts_to_csv(alerts):
    filename = f"csv-files/keyword_alerts_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Keywords Found", "Timestamp"])
        for alert in alerts:
            writer.writerow(
                [alert["url"], ", ".join(alert["keywords"]), alert["timestamp"]]
            )
    logger.info(f"Alerts written to {filename}")


def record_run(pages_crawled, alerts_found):
    new_file = not os.path.exists(RUN_LOG)
    with open(RUN_LOG, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["Timestamp", "Sites", "Pages Crawled", "Alerts Found"])
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                len(WEBSITES),
                pages_crawled,
                alerts_found,
            ]
        )


def run_monitoring():
    logger.info("Running keyword alert monitoring...")
    all_alerts = []
    total_pages = 0
    for url in WEBSITES:
        logger.info(f"Starting crawl on: {url}")
        alerts, pages = crawl_site(url)
        all_alerts.extend(alerts)
        total_pages += pages
    if all_alerts:
        write_alerts_to_csv(all_alerts)
    else:
        logger.info("No alerts found.")
    record_run(total_pages, len(all_alerts))


def schedule_monitoring():
    schedule.every(INTERVAL_MINUTES).minutes.do(run_monitoring)
    logger.info(f"Monitoring scheduled to run every {INTERVAL_MINUTES} minutes.")


if __name__ == "__main__":
    if not WEBSITES:
        logger.error(
            "No WEBSITES configured. Add them to your .env file (see .env.template)."
        )
        raise SystemExit(1)
    if not KEYWORDS:
        logger.error(
            "No KEYWORDS configured. Add them to your .env file (see .env.template)."
        )
        raise SystemExit(1)

    logger.info("Initial run of the monitoring system.")
    run_monitoring()
    schedule_monitoring()
    while True:
        schedule.run_pending()
        time.sleep(1)
