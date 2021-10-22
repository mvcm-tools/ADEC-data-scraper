# ADEC-data-scraper
python script that scrapes data from the ADEC webpage:

https://dec.alaska.gov/air/air-monitoring/alaska-air-quality-real-time-data

Must have a webdriver for Google Chrome or Mozilla Firefox to run this script. 

- Download geckodriver for Firefox here: https://github.com/mozilla/geckodriver/releases
- Download chromedriver for Chrome here: https://sites.google.com/chromium.org/driver/


Usage:

./ncore-hourly-dualbrowser.py "site name" output_filepath browser driver_filepath

site name = "NCore", "Hurst Road", or "A St." (keep "" so multi-word site names are not used as sys inputs
output_filepath = location to send output
browser = firefox or chrome (keep lowercase)
driver_filepath = location of the webdriver







