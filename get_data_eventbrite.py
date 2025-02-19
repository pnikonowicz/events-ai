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

    number_of_results = 0
    text_result = ''
    html_result = ''
    separator = "\n" + "-" * 30 + "\n"

    for item in event_list_items:
        text_result += f"{item.text}{separator}"
        html_result += f"{item.html}\n\n"
        number_of_results += 1

    return html_result, text_result, number_of_results

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
    session = HTMLSession()
    response = session.get(url)

    page_numbers = response.html.find('footer', first=True).text

    if(page_numbers.startswith("1 of")):
        number_str = page_numbers[len("1 of"):].strip()
        if(number_str.isdigit()):
            return int(number_str)
        

    print(f"ERROR: coudn't parse the string: {page_numbers}")
    exit(1)

def fetch_all_results(target_day, number_of_pages):
    total_number_of_results_fetched = 0
    html_results = "<html>\n\n"
    text_results = ""
    
    for page_number in range(1, number_of_pages):
        url = create_search_url(target_day, page_number)
        print(f"fetching results for: {url}")
        html_result, text_result, number_fetched = fetch_results(url)
        html_results += html_result
        text_results += text_result
        total_number_of_results_fetched += number_fetched

    html_results += "\n\n</html>"

    return total_number_of_results_fetched, html_results, text_results

if __name__ == "__main__":
    target_day = "tomorrow"

    number_of_pages = get_number_of_pages(create_search_url(target_day, 1))
    total_number_of_results_fetched, html_results, text_results = fetch_all_results(
        target_day, number_of_pages
    )
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data", "eventbrite")
    
    write_to_file(data_dir, text_results, html_results)

    print(f"fetched: {total_number_of_results_fetched} results")

