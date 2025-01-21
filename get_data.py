import os
from requests_html import HTMLSession

def grab_results_via_url(page_number):
    session = HTMLSession()
    search_term = f"ny--new-york/events--tomorrow/?page={page_number}"
    url = f"https://www.eventbrite.com/d/online/{search_term}/"

    response = session.get(url)
    event_list_items = response.html.find('.search-results-panel-content__events section li')

    results = ''
    for item in event_list_items:
        results += '\n'
        results += "-" * 30
        results += '\n'
        results += item.text

    results += ''

    return results

def load_oauth_token(current_dir):
    token_path = "secrets/oauth.token"
    file_path = os.path.join(current_dir, token_path)

    with open(file_path, "r") as file:
        return file.read().strip()        

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # token = load_oauth_token(current_dir)

    results = ''
    for page_number in range(60):
    # for page_number in range(1):
        results += grab_results_via_url(page_number)
    
    print(results)
