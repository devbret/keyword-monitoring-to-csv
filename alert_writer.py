import csv
from datetime import datetime

def write_alerts_to_csv(alerts):
    filename = f"keyword_alerts_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Keywords Found', 'Timestamp'])
        for alert in alerts:
            writer.writerow([alert['url'], ', '.join(alert['keywords']), datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    print(f"Alerts written to {filename}")

