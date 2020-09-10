# Google Maps Businesses Scraper
Built with Python running Selenium, this app allows you to scrape places info from the google maps search results

# CLI Arguments
* `--query`
  * First part of the query you want to execute, excluding any locations, zip codes, etc. For example "Commerical property managers near"
* `--places`
  * This is the second part of the query. Comma separated places,zip codes, cities, etc. For example "Washington,Miami,Chicago"
* `--pages`
  * Number of pages to scrape for each search. This defaults to 1. If the defined number of pages exceed the number of pages actually in the results, the program will notice that and won't throw an error
* `--skip-duplicate-addresses`
  * Flag that if included in the command, will tell the app to not scrape the results which have the addresses that is already in the file
* `--scrape-website`
  * Flag that if included in the command, will tell the app to scrape website URLs too. This is optional and defaults fo false because the process is greatly slower with this flag on

# Examples
The example command you can run with this app is:
```
python script.py --query="Commercial property managers near" --places="Washington,Miami,Chicago"
```

This will generate three search queries:
1. Commercial property managers near Washington
2. Commercial property managers near Miami
3. Commercial property managers near Chicago

The above command will scrape all **Commercial property managers** that are **near Washington, Miami and Chicago**.

## Scraping the website too
The app allows you to scrape the website urls for each company. This is disabled by default as it slows down the process.
You can enable this by including a flag `--scrape-website` in the command like so:
```
python script.py --query="Commercial property managers near" --places="Washington,Miami,Chicago" --scrape-website
```

This will add "Website" column to the excel output file.

# Requirements
As this app is made with Python and Selenium, it is required to install [Python](https://www.python.org/downloads/) and also it requires the Chrome driver, which you can download from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure to select your browser version and put the downloaded executable in the PATH variable in your system.
