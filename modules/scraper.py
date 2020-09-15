from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from modules.helpers import *
from modules.settings import SETTINGS
from modules.colors import fore

import time
import xlsxwriter

def scrape(args):
    if args.pages is not None:
        SETTINGS["PAGE_DEPTH"] = args.pages
    SETTINGS["BASE_QUERY"] = args.query
    SETTINGS["PLACES"] = args.places.split(',')

    # Created driver and wait
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 15)

    # Set main box class name
    BOX_CLASS = "section-result-content"

    # Initialize workbook / worksheet
    workbook = xlsxwriter.Workbook('ScrapedData_GoogleMaps.xlsx')
    worksheet = workbook.add_worksheet()

    # Headers and data
    data = {
        "name": "",
        "phone": "",
        "address": "",
        "website": ""
    }
    headers = generate_headers(args, data)
    print_table_headers(worksheet, headers)

    # Start from second row in xlsx, as first one is reserved for headers
    row = 1

    # Remember scraped addresses to skip duplicates
    addresses_scraped = {}

    start_time = time.time()

    for place in SETTINGS["PLACES"]:
        # Go to the index page
        driver.get(SETTINGS["MAPS_INDEX"])

        # Build the query string
        query = "{0} {1}".format(SETTINGS["BASE_QUERY"], place)
        print(f"{fore.GREEN}Moving on to {place}{fore.RESET}")

        # Fill in the input and press enter to search
        q_input = driver.find_element_by_name("q")
        q_input.send_keys(query, Keys.ENTER)
        
        # Wait for the results page to load. If no results load in 10 seconds, continue to next place
        try:
            w = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, BOX_CLASS))
            )
        except:
            continue

        # Loop through pages and results
        for _ in range(0, SETTINGS["PAGE_DEPTH"]):
            # Get all the results boxes
            boxes = driver.find_elements_by_class_name(BOX_CLASS)

            # Loop through all boxes and get the info from it and store into an excel
            for box in boxes:
                # Just get the values, add only after we determine this is not a duplicate (or duplicates should not be skiped)
                name = box.find_element_by_class_name("section-result-title").find_element_by_xpath(".//span[1]").text

                address = box.find_element_by_class_name("section-result-location").text

                scraped = address in addresses_scraped

                if scraped and args.skip_duplicate_addresses:
                    print(f"{fore.WARNING}Skipping {name} as duplicate by address{fore.RESET}")
                else:
                    # Initiate the list and add to it only now
                    data["name"] = name
                    data["address"] = address

                    phone = box.find_element_by_class_name("section-result-phone-number").find_element_by_xpath(".//span[1]").text

                    data["phone"] = phone

                    if scraped:
                        addresses_scraped[address] += 1
                        print(f"{fore.WARNING}Currently scraping on{fore.RESET}: {name}, for the {addresses_scraped[address]}. time")
                    else:
                        addresses_scraped[address] = 1
                        print(f"{fore.GREEN}Currently scraping on{fore.RESET}: {name}")
                         
                    # Only if user wants to get the URL to, get it
                    if args.scrape_website:
                        url = box.find_element_by_class_name("section-result-action-icon-container").find_element_by_xpath("./..").get_attribute("href")
                        website = get_website_url(url)
                        data["website"] = website
                    
                    write_data_row(worksheet, data, row)
                    row += 1

            # Go to next page                                
            next_page_link = driver.find_element_by_class_name("n7lv7yjyC35__button-next-icon")
            try:
                next_page_link.click()
            except WebDriverException:
                print(f"{fore.WARNING}No more pages for this search. Advancing to next one.{fore.RESET}")
                break

            # Wait for the next page to load
            time.sleep(5)
        print("-------------------")

    workbook.close()
    driver.close()

    end_time = time.time()
    print(f"{fore.GREEN}Done. Time it took was {end_time-start_time}s{fore.RESET}")