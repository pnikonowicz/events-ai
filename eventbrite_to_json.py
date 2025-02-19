from bs4 import BeautifulSoup
import os
import json

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

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data', 'eventbrite')
    html_file = os.path.join(data_dir, 'data.html')
    
    html_text = read_file(html_file)
    json_data = html_to_json(html_text)

    json_data_file = os.path.join(data_dir, 'data.json')
    write_to_file(json_data_file, json_data)
