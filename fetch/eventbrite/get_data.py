import os
from shutil import rmtree
from requests_html import HTMLSession
from requests_html import HTML
from .to_json import to_json
from common.paths import Paths

def fetch_result(page_number, target_day):
    url = create_search_url(target_day, page_number)
    session = HTMLSession()
    response = session.get(url)
    
    return response.text


def fetch_results(url):
    session = HTMLSession()
    response = session.get(url)    

    return response.text

def write_raw_data_to_file(data_dir, page_number, raw_html):
    os.makedirs(data_dir, exist_ok=True)

    text_file = os.path.join(data_dir, f"{page_number}.html")
    with open(text_file, "w") as file:
        file.write(raw_html)

def write_to_file(data_dir, text_results, html_results): 
    os.makedirs(data_dir, exist_ok=True)

    text_file = os.path.join(data_dir, 'text_delimited.txt')
    with open(text_file, "w") as file:
        file.write(text_results)

    html_file = os.path.join(data_dir, 'data.html')
    with open(html_file, "w") as file:
        file.write(html_results)     

def create_search_url(day, page_number):
    return f"https://www.eventbrite.com/d/ny--new-york/events--{day}/?page={page_number}"

def get_number_of_pages_from_html(raw_html):
    response_html = HTML(html=raw_html)
    page_numbers = response_html.find('footer', first=True).text

    if(page_numbers.startswith("1 of")):
        number_str = page_numbers[len("1 of"):].strip()
        if(number_str.isdigit()):
            return int(number_str)
        

    print(f"ERROR: coudn't parse the string: {page_numbers}")
    exit(1)

def get_number_of_pages(url):
    session = HTMLSession()
    response = session.get(url)
    response_html = response.html

    return get_number_of_pages_from_html(response_html)

def fetch_all_raw_html(target_day, number_of_pages):
    raw_htmls = []

    print(f"fetching {number_of_pages} results")
    for page_number in range(1, number_of_pages):
        url = create_search_url(target_day, page_number)
        print(f"fetching results for: {url}")
        raw_html = fetch_results(url)
        raw_htmls.append(raw_html)

    return raw_htmls

def remove_dir(dir):
    if os.path.exists(dir):
        rmtree(dir)
    else:
        print("dir not found, nothing to delete")

def fetch():
    # target_day = "tomorrow"
    target_day = "today"
    data_dir = os.path.join(Paths.PROJECT_DIR, "data", "eventbrite")
    raw_data_dir = os.path.join(data_dir)
    
    raw_htmls = fetch_from_eventbrite(target_day, raw_data_dir)
    
    to_json(Paths, raw_data_dir)

    return len(raw_htmls)

def fetch_from_eventbrite(target_day, raw_data_dir):
    first_result_html = fetch_result(1, target_day)

    remove_dir(raw_data_dir)
    write_raw_data_to_file(raw_data_dir, 1, first_result_html)

    number_of_pages = get_number_of_pages_from_html(first_result_html)

    raw_htmls = fetch_all_raw_html(target_day, number_of_pages)
    for i in range(1, len(raw_htmls)):
        raw_html = raw_htmls[i]
        write_raw_data_to_file(raw_data_dir, i, raw_html)
    return raw_htmls
