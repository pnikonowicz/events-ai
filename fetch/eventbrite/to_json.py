from bs4 import BeautifulSoup
import os
import json
from requests_html import HTML

def read_file(file_path):
    text = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            text += line
    return text

def write_to_file(output_file, json_data):
    with open(output_file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def html_to_json(html_text): 
    soup = BeautifulSoup(html_text, 'html.parser')

    data = []
    for div in soup.find('html').find_all('div', recursive=False):
        img = div.find('img', src=True)
        div_data = {
            "image": img['src'] if img else None, # images are optional
            "link": div.find('a', href=True)['href'],
            "title": div.find('h3').get_text(strip=True)
        }
        data.append(div_data)
    
    return data

def extract_html_results_from_html_page(raw_html):
    """
        grabs the search results but ignores the first div. the first div contains
        mobile information and would therefore result in a duplicate result
    """
    response_html = HTML(html=raw_html)
    event_list_items = response_html.find('div[data-testid="search-event"] > div:nth-child(2)') 

    number_of_results = 0
    text_result = ''
    html_result = ''
    separator = "\n" + "-" * 30 + "\n"

    for item in event_list_items:
        text_result += f"{item.text}{separator}"
        html_result += f"{item.html}\n\n"
        number_of_results += 1

    return html_result, text_result, number_of_results


def fetch_all_results(raw_htmls):
    total_number_of_results_fetched = 0
    html_results = "<html>\n\n"
    text_results = ""
    
    for raw_html in raw_htmls:
        html_result, text_result, number_fetched = extract_html_results_from_html_page(raw_html)
        html_results += html_result
        text_results += text_result
        total_number_of_results_fetched += number_fetched

    html_results += "\n\n</html>"

    return total_number_of_results_fetched, html_results, text_results

def get_raw_htmls(raw_data_dir):
    raw_htmls = []
    for dirpath, _, filenames in os.walk(raw_data_dir):
         for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r') as file:
                data = file.read()
                raw_htmls.append(data)
    return raw_htmls

def to_json(Paths, raw_data_dir):
    data_dir = os.path.join(Paths.PROJECT_DIR, 'data', 'eventbrite')
    html_file = os.path.join(data_dir, 'data.html')

    raw_htmls = get_raw_htmls(raw_data_dir)

    total_number_of_results_fetched, html_results, text_results = fetch_all_results(raw_htmls)
    print(text_results)
    print(f"fetched: {total_number_of_results_fetched} results")
    
    json_data = html_to_json(html_results)

    json_data_file = os.path.join(data_dir, 'data.json')
    write_to_file(json_data_file, json_data)

    print(f"translated {len(json_data)} events to json")
