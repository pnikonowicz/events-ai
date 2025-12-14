from bs4 import BeautifulSoup
import os
import json
from requests_html import HTML
from common.logger import Logger
from common.data import Data, write_data
import re

def read_file(file_path):
    text = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            text += line
    return text

def json_text_to_data(json_texts : list[str]) -> list[Data]: 
    data = []
    for i in range(0, len(json_texts)):
        json_text = json_texts[i]
        json_result = json.loads(json_text)
        search_data = json_result.get('search_data', {})
        events = search_data.get('events', {})
        results = events.get('results', [])
        if len(results) == 0:
            Logger.warn(f"=== no results found in json for page: ({i+1})")
            continue

        for result in results:
            new_data = Data(
                image = result.get('image', {}).get('url', "about:blank"),
                link = result.get('url', 'UNKNOWN_URL'),
                title = result.get('summary', 'UNKNOWN_TITLE'),
                time = result.get('start_time', 'UNKNOWN_START_TIME'),
                location = result.get('primary_venue', {}).get('name', 'UNKNOWN_VENUE')
            )
            data.append(new_data)
    
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


def get_json_results(raw_htmls):
    json_results = []
    
    for i in range(0, len(raw_htmls)):
        raw_html = raw_htmls[i]
        match = re.search(r'__SERVER_DATA__\s*=\s*({.*?});', raw_html, re.DOTALL)
        if match:
            server_data_json_text = match.group(1)
            json_results.append(server_data_json_text)
        else:
            Logger.error(f"couldn't find __SERVER_DATA__ in html page {i+1}")

    return json_results

def get_raw_htmls(raw_data_dir):
    raw_htmls = []
    for dirpath, _, filenames in os.walk(raw_data_dir):
         for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r') as file:
                data = file.read()
                raw_htmls.append(data)
    return raw_htmls

def to_json(data_dir, raw_htmls):
    json_results = get_json_results(raw_htmls)
    Logger.log(f"got json for: {len(json_results)} pages")
    
    json_data = json_text_to_data(json_results)
    Logger.log(f"extracted {len(json_data)} events to json data objects")

    json_data_file = os.path.join(data_dir, 'data.json')
    write_data(json_data_file, json_data)

    Logger.log(f"translated {len(json_data)} events to json")

    return len(json_data)
