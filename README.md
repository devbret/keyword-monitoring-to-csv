# Regular Keyword Monitoring With CSV Reporting

Continuously crawls specified websites to detect targeted keywords, logs matching URLs and terms to timestamped CSV files and automatically repeats the monitoring process every 60 minutes.

## Overview

The application recursively crawls each site starting from its homepage, fetches page content using `requests`, parses HTML with `BeautifulSoup` and searches for specific keywords. If any keywords are found on a page, the script records the page URL and matched terms.

All detected alerts are written to a timestamped CSV file inside a `csv-files` directory, including the URL, keywords found and a timestamp. The script runs immediately on startup and then uses the `schedule` library to automatically repeat the monitoring process every 60 minutes in a continuous loop.

## Set Up Instructions

Below are the required software programs and instructions for installing and using this application.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps For Use

1. Install the above programs

2. Open a terminal

3. Clone this repository using `git` by running the following command: `git clone git@github.com:devbret/keyword-monitoring-to-csv.git`

4. Navigate to the repo's directory by running: `cd keyword-monitoring-to-csv`

5. Create a virtual environment with this command: `python3 -m venv venv`

6. Activate your virtual environment using: `source venv/bin/activate`

7. Install the needed dependencies for running the script: `pip install -r requirements.txt`

8. Add monitored keywords to line 10 of the `app.py` file

9. Add monitored domains to line 11 of the `app.py` file

10. Run the program using this command: `python3 app.py`

11. To exit the program, press the `CTRL` and `C` keys on your keyboard at the same time

12. To exit the virtual environment, type this command in the terminal: `deactivate`

13. Any resulting CSV files will be output to the `csv-files` directory

## Other Considerations

This project repo is intended to demonstrate an ability to do the following:

- Continuously crawl specified websites to detect and log keywords for automated monitoring

- Generate timestamped CSV reports of detected keyword matches

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
