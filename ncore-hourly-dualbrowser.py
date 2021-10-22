# Usage:

# ./ncore-hourly-dualbrowser.py "site name" output_filepath browser driver_filepath

# site name = "NCore", "Hurst Road", or "A St." (keep "" so multi-word site names are not used as sys inputs
# output_filepath = location to send output
# browser = firefox or chrome (keep lowercase)
# driver_filepath = location of the webdriver

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
import glob
import time
import datetime
from datetime import timedelta
import sys

# set site
site_name = str(sys.argv[1])
# set file path
filepath = str(sys.argv[2]) # keep this without a trailing slash
# URL of DEC webpage
url = "https://dec.alaska.gov/air/air-monitoring/alaska-air-quality-real-time-data"
# designate browser
browser = str(sys.argv[3])
# set path to either firefox or chrome driver
path_to_driver = str(sys.argv[4])

def get_dec_data(site):
# set options for webdriver to operate as headless display
    if browser == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=path_to_driver,firefox_options=opts)
    elif browser == "chrome":
        opts = Options()
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        driver = Chrome(path_to_driver,options=opts)
    else:
        print("browser options are either 'chrome' or 'firefox'")
        exit(1)

    # open browser to URL
    driver.get(url) 

    print("connected to url, waiting for map to load")
    print("...")
    print(" ")
    time.sleep(15)

# ids of the iframe html elements
    ifids = ["avFrame","ctl00_MainContent_SiteDisplayPopupPanel1_uxSiteDataPopupControl_CIF-1"]

# id of the timestamp in the data table
    timestamp_id = "ctl00_MainContent_SiteAqiDisplayPanel1_SiteTimestamp"

# switch to first iframe
    driver.switch_to.frame(ifids[0])

    print('switched to first iframe')
    print("...")
    print(" ")
    time.sleep(5)

# select site from dropdown to open popup iframe of site
    sitelist = driver.find_element_by_id("SiteList")
    select_object = Select(sitelist)
    
    select_object.select_by_visible_text(site)

    print('selecting '+site+' from Site List dropdown')
    print("...")
    print(" ")
    time.sleep(15)

# switch to second iframe of site popup
    driver.switch_to.frame(ifids[1])
    
    print('switched to second iframe')
    print("...")
    print(" ")
    time.sleep(5)

# get values from table in the second iframe
# start with data timestamp
    table_ts = driver.find_element_by_id("ctl00_MainContent_SiteAqiDisplayPanel1_SiteTimestamp").text

# add leading zero to hour if missing
    table_ts_fix = []

    if len(table_ts) == 21:
        print('adding zero to hour')
        table_ts_fix = table_ts[0:11] + "0" + table_ts[11:18]

# format timestamp
    table_ts_fix = pd.to_datetime(table_ts_fix, format="%m/%d/%Y %I:%M %p")

# scrape all column labels from table
    labels = []

    for row in driver.find_elements_by_css_selector("td.siteDisplayLabel"):
        labels.append(row.text)

# scrape data for each column
    samples = []

    for row in driver.find_elements_by_css_selector("td.siteDisplayValue"):
        samples.append(row.text)

# scrape the units for each column
    units = []

    for row in driver.find_elements_by_css_selector("td.siteDisplayUnit"):
        units.append(row.text)

# add datetime to data line
    samples = [str(table_ts_fix)] + samples

# add missing column names
    col_names = ['datetime'] + labels[0:3] + ['PM25'] + labels[10:] 

# add missing units
    units = ['AK','DEG','DEG',''] + units

# merge column names and units
    col_names_wunit = []

# format column headers
    for xi in range(0,len(col_names)):
        col = str(col_names[xi])+" "+str(units[xi])
        col = col.replace(":","")
        col = col.replace(" ","_")
        col = col.replace("/","_")
        col = col.replace(",","")
        col_names_wunit.append(col)

# pull list of adec logfiles
    files = []

    for name in glob.glob(filepath+'/adec-'+site+'-log-*.txt'):
        files.append(name)

# if no log files are present, create new file starting with column headers
# if logfiles are present, find the latest logfile and merge data onto it
    if len(files) == 0:
        outfilename = datetime.datetime.now().strftime('adec-'+site+'-log-%Y%m%dT%H%M%S.txt')
        outfile = open(os.path.join(filepath, outfilename), 'w')
        outfile.write('\t'.join(col_names_wunit)+'\n')
        outfile.write('\t'.join(samples)+'\n')
        print('wrote data to file: '+outfilename)
    else:
        outfilename = files[len(files)-1]
        outfile = open(os.path.join(filepath, outfilename), 'a')
        outfile.write('\t'.join(samples)+'\n')
        print('wrote data to file: '+outfilename)

# close browser
    driver.close()



get_dec_data(site_name)
