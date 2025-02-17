import os
from requests_html import HTMLSession

def fetch_results(url):
    session = HTMLSession()
    response = session.get(url)

    """
        grabs the search results but ignores the first div. the first div contains
        mobile information and would therefore result in a duplicate result
    """
    event_list_items = response.html.find('div[data-testid="search-event"] > div:nth-child(2)') 

    text_result = ''
    html_result = '<html>\n\n'
    separator = "\n" + "-" * 30 + "\n"

    for item in event_list_items:
        text_result += f"{item.text}{separator}"
        html_result += f"{item.html}\n\n"

    text_result += ''
    html_result += '</html>'

    return html_result, text_result

def write_to_file(data_dir, text_results, html_results): 
    os.makedirs(data_dir, exist_ok=True)

    text_file = os.path.join(data_dir, 'text_delimited.txt')
    with open(text_file, "w") as file:
        file.write(text_results)

    html_file = os.path.join(data_dir, 'data.html')
    with open(html_file, "w") as file:
        file.write(html_results)     

def create_search_url(day, page_number):
    day = "tomorrow"
    return f"https://www.eventbrite.com/d/ny--new-york/events--{day}/events-{day}/?page={page_number}"

def get_number_of_pages(url):
    return 1

if __name__ == "__main__":
    html_results = ''
    text_results = ''

    target_day = "tomorrow"

    number_of_pages = get_number_of_pages(create_search_url(target_day, 1))
    
    # for page_number in range(60):
    for page_number in range(1):
        url = create_search_url(target_day, page_number)
        html_result, text_result = fetch_results(url)
        html_results += html_result
        text_results += text_result
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data", "eventbrite")
    
    write_to_file(data_dir, text_results, html_results)
