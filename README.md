# Regular Keyword Monitoring With CSV Reporting

Continuously crawl specified websites to detect targeted keywords, log matching URLs and terms to timestamped CSV files and automatically repeat the monitoring process at a configurable interval.

## Application Overview

Recursively crawls each site starting from its homepage, following internal links while skipping PDFs, then fetches page content using `requests` and parses the HTML with `BeautifulSoup`. The visible page text is searched for chosen keywords. When a keyword is found on a page, the script records the page URL and the matched terms.

Detected alerts are written to a timestamped CSV file inside the `csv-files` directory, capturing the URL, keywords found and the time each match was detected. Every run is also recorded and activity is logged, so there is a trail even when nothing matches.

The Python script runs once immediately on startup and then uses the `schedule` library to repeat the monitoring process at a configurable interval in a continuous loop. Keywords, websites and other settings are read from a `.env` file.

## Basic Setup Instructions

Below are the required software programs and instructions for installing and using this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps For Use

1. Install the above programs

2. Open a terminal

3. Clone this repository: `git clone git@github.com:devbret/keyword-monitoring-to-csv.git`

4. Navigate to the repo's directory: `cd keyword-monitoring-to-csv`

5. Create a virtual environment: `python3 -m venv venv`

6. Activate your virtual environment: `source venv/bin/activate`

7. Install the needed dependencies: `pip install -r requirements.txt`

8. Create your configuration file from the template: `cp .env.template .env`

9. Open `.env` and set values for `KEYWORDS` and `WEBSITES`

10. Run the program: `python3 app.py`

11. When finished, stop the program: `CTRL + C`

12. Exit the virtual environment: `deactivate`

## Other Considerations

Below you will find information not covered in the installation and use sections above. Including the abilities this repo is intended to demonstrate. As well as an overview of the license this code is made available with. And a way to contact the maintainer with questions, suggestions and collaboration opportunities.

### Abilities Demonstrated

This project repo is intended to demonstrate an ability to do the following:

- Monitor a list of websites for specific keywords

- Crawl internal links on each website, skip PDFs and search the visible page text for keywords

- When keywords are found, record the matching URL, detected keywords and timestamp in a CSV file

- Run once immediately, then continue running automatically every 60 minutes to check the websites again

### License Information

This repository is distributed under the MIT License. You are free to use, copy, modify, merge, publish, distribute, sublicense and sell copies of this software, including as part of proprietary or commercial work. The single condition is the copyright and permission notices contained in the LICENSE file must be included with any copy or substantial portion of the software that you redistribute. The software is provided "as is", without warranty of any kind, and the copyright holder is not liable for any claim or damages arising from its use.

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
