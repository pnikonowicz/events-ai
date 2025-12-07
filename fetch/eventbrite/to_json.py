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

def html_to_json(json_results): 
    data = []
    for json_result in json_results:
        result = json_result.get('search_data', {})
        events = result.get('events', {}).get('events', [])
        results = events.get('results', [])
        for result in results:
            new_data = Data(
                image = results.get('image', {}).get('url', "about:blank"),
                link = results.get('url', 'UNKNOWN_URL'),
                title = result.get('summary', 'UNKNOWN_TITLE'),
                time = results.get('start_time', 'UNKNOWN_START_TIME'),
                location = result.get('primary_venue', {}).get('get', 'UNKNOWN_VENUE')
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


def fetch_all_results(raw_htmls):
    json_results = []
    
    for raw_html in raw_htmls:
        match = re.search(r'__SERVER_DATA__\s*=\s*({.*?});', raw_html, re.DOTALL)
        if match:
            server_data_json = json.loads(match.group(1))
            json_results.append(server_data_json)

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
    json_results = fetch_all_results(raw_htmls)
    Logger.log(f"fetched: {len(json_results)} results")
    
    json_data = html_to_json(json_results)
    Logger.log(f"extracted {len(json_data)} events to json data objects")

    json_data_file = os.path.join(data_dir, 'data.json')
    write_data(json_data_file, json_data)

    Logger.log(f"translated {len(json_data)} events to json")

    return len(json_data)


#### ===============================================================

def _extract_json_from_script(script_text, var_name):
    # match var assignment like: window.__REACT_QUERY_STATE__ = {...}; or window.__SERVER_DATA__ = {...}
    pattern = re.compile(rf"{re.escape(var_name)}\s*=\s*(\{{.*\}})\s*;?", re.S)
    m = pattern.search(script_text)
    if not m:
        return None
    return m.group(1)

def get_eventbrite_page_count_from_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    # Prefer REACT_QUERY_STATE (contains "queries" -> state -> data -> events -> pagination)
    candidate_vars = ["window.__REACT_QUERY_STATE__", "window.__SERVER_DATA__"]

    for script in soup.find_all("script"):
        script_text = script.string or script.get_text() or ""
        for var in candidate_vars:
            json_text = _extract_json_from_script(script_text, var)
            if not json_text:
                continue
            try:
                obj = json.loads(json_text)
            except json.JSONDecodeError:
                # If JSON is not strict JSON, consider json5:
                try:
                    import json5  # pip install json5
                    obj = json5.loads(json_text)
                except Exception:
                    # give up on this script and try others
                    continue

            # Try common paths where pagination may live
            # Path 1: react query state: queries[0].state.data.data.events.pagination.page_count
            try:
                queries = obj.get("queries") or []
                if queries:
                    q0 = queries[0]
                    page_count = (
                        q0.get("state", {})
                          .get("data", {})
                          .get("data", {})
                          .get("events", {})
                          .get("pagination", {})
                          .get("page_count")
                    )
                    if isinstance(page_count, int):
                        return page_count
            except Exception:
                pass

            # Path 2: server data: search_data -> events -> pagination.page_count
            try:
                page_count = (
                    obj.get("search_data", {})
                       .get("events", {})
                       .get("pagination", {})
                       .get("page_count")
                )
                if isinstance(page_count, int):
                    return page_count
            except Exception:
                pass

    # Fallback: parse the footer text "1 of N" (existing method)
    footer = soup.find("footer")
    if footer and footer.get_text():
        txt = footer.get_text(strip=True)
        if txt.startswith("1 of"):
            num = txt[len("1 of"):].strip()
            if num.isdigit():
                return int(num)

    # If nothing found, return None
    return None
