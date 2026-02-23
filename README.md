# Regular Keyword Monitoring With CSV Reporting

Continuously crawls specified websites to detect targeted keywords, logs matching URLs and terms to timestamped CSV files and automatically repeats the monitoring process every 60 minutes.

## Overview

The application recursively crawls each site starting from its homepage, fetches page content using `requests`, parses HTML with `BeautifulSoup` and searches for specific keywords. If any keywords are found on a page, the script records the page URL and matched terms.

All detected alerts are written to a timestamped CSV file inside a `csv-files` directory, including the URL, keywords found and a timestamp. The script runs immediately on startup and then uses the `schedule` library to automatically repeat the monitoring process every 60 minutes in a continuous loop.
