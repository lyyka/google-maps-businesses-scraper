import requests

def generate_headers(args, example_dict):
    headers = example_dict.keys()
    if not args.scrape_website:
        headers.remove("website")
    
    return [header.capitalize() for header in headers]

def print_table_headers(worksheet, headers):
    col = 0
    for header in headers:
        worksheet.write(0, col, header)
        col += 1

def write_data_row(worksheet, data, row):
    col = 0
    for key in data:
        worksheet.write(row, col, data[key])
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