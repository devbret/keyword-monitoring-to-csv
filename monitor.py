import time
import schedule
from scraper import crawl_site 
from alert_writer import write_alerts_to_csv
from config import WEBSITES, KEYWORDS

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

