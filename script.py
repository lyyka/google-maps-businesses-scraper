from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

import time
import xlsxwriter
import requests

# Index page of google maps where search box is located
MAPS_INDEX = "https://maps.google.com"

# How many pages to look through
PAGE_DEPTH=1

# Near what cities to look
BASE_QUERY = 'commercial property management near'
CITIES = ['West Palm Beach', "Fort Lauderdale"]

def print_table_headers(worksheet):
    headers = ["Company name", "Phone number", "Address", "Website"]
    col = 0
    for header in headers:
        worksheet.write(0, col, header)
        col += 1

def write_data_row(worksheet, data, row):
    col = 0
    for val in data:
        worksheet.write(row, col, val)
        col += 1

def get_website_url(url):
    # Will try to get URLs that are given through google, that;s why we allow redirects
    try:
        if url is not None:
            response = requests.head(url, allow_redirects=True)
            return response.url
        else:
            return ""
    except:
        return ""

def main():
    # Created driver and wait
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    # Set main box class name
    BOX_CLASS = "section-result-content"

    # Initialize workbook / worksheet
    workbook = xlsxwriter.Workbook('ScrapedData_GoogleMaps.xlsx')
    worksheet = workbook.add_worksheet()
    print_table_headers(worksheet)

    # Start from second row in xlsx, as first one is reserved for headers
    row = 1

    for city in CITIES:
        # Go to the index page
        driver.get(MAPS_INDEX)
        
        # Build the query string
        query = "{0} {1}".format(BASE_QUERY, city)

        # Fill in the input and press enter to search
        q_input = driver.find_element_by_name("q")
        q_input.send_keys(query, Keys.ENTER)
        
        # Wait for the results page to load
        #try:
        _ = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, BOX_CLASS))
        )
        for _ in range(0, PAGE_DEPTH):
            # Get all the results boxes
            boxes = driver.find_elements_by_class_name(BOX_CLASS)

            # Loop through all boxes and get the info from it and store into an excel
            for box in boxes:
                name = box.find_element_by_class_name("section-result-title").find_element_by_xpath(".//span[1]").text

                phone = box.find_element_by_class_name("section-result-phone-number").find_element_by_xpath(".//span[1]").text
                
                address = box.find_element_by_class_name("section-result-location").text
                
                url = box.find_element_by_class_name("section-result-action-icon-container").find_element_by_xpath("./..").get_attribute("href")
                website = get_website_url(url)
                
                data = [name, phone, address, website]
                write_data_row(worksheet, data, row)
                row += 1

            # Go to next page                                
            next_page_link = driver.find_element_by_class_name("n7lv7yjyC35__button-next-icon")
            try:
                next_page_link.click()
            except WebDriverException:
                print("No more pages, navigation not clickable")
                break

            # Wait for the next page to load
            time.sleep(5)

    workbook.close()
    driver.close()

main()


