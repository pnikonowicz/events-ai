from bs4 import BeautifulSoup
import os

def read_file(file_path):
    text = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            text += line
    return text


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    unique_html_file = os.path.join(data_dir, 'unique.html')
    html = read_file(unique_html_file)

    print(html)
