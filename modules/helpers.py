import requests

def generate_headers(args):
    headers = ["Company name", "Phone number", "Address"]
    if args.scrape_website:
        headers.append("Website")
    return headers

def print_table_headers(worksheet, headers):
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