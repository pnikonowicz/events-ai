import os
from requests_html import HTMLSession

def grab_results_via_url():
    session = HTMLSession()
    search_term = "ny--new-york/events--tomorrow/?page=1"
    url = f"https://www.eventbrite.com/d/online/{search_term}/"

    response = session.get(url)
    event_list_items = response.html.find('.search-results-panel-content__events section li')

    # Iterate through and print each item
    for item in event_list_items:
        print(item.text)
        print("-" * 30)

def load_oauth_token(current_dir):
    token_path = "secrets/oauth.token"
    file_path = os.path.join(current_dir, token_path)

    with open(file_path, "r") as file:
        return file.read().strip()        

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # token = load_oauth_token(current_dir)

    grab_results_via_url()
