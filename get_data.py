import os
from requests_html import HTMLSession

def grab_results_via_url(page_number):
    session = HTMLSession()
    search_term = f"ny--new-york/events--tomorrow/?page={page_number}"
    url = f"https://www.eventbrite.com/d/online/{search_term}/"

    response = session.get(url)

    """
        grabs the search results but ignores the first div. the first div contains
        mobile information and would therefore result in a duplicate result
    """
    event_list_items = response.html.find('div[data-testid="search-event"] > div:nth-child(2)') 

    text_result = ''
    html_result = ''
    separator = "\n" + "-" * 30 + "\n"

    for item in event_list_items:
        text_result += f"{item.text}{separator}"
        html_result += f"{item.html}{separator}"

    text_result += ''

    return html_result, text_result

def load_oauth_token(current_dir):
    token_path = "secrets/oauth.token"
    file_path = os.path.join(current_dir, token_path)

    with open(file_path, "r") as file:
        return file.read().strip()  

def write_to_file(data_dir, text_results, html_results): 
    os.makedirs(data_dir, exist_ok=True)

    text_file = os.path.join(data_dir, 'text_delimited.txt')
    with open(text_file, "w") as file:
        file.write(text_results)

    html_file = os.path.join(data_dir, 'html_delimited.txt')
    with open(html_file, "w") as file:
        file.write(html_results)     

if __name__ == "__main__":
    # token = load_oauth_token(current_dir)

    html_results = ''
    text_results = ''
    # for page_number in range(60):
    for page_number in range(1):
        html_result, text_result = grab_results_via_url(page_number)
        html_results += html_result
        text_results += text_result
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    
    write_to_file(data_dir, text_results, html_results)
