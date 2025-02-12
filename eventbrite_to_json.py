from bs4 import BeautifulSoup
import os

def read_file(file_path):
    text = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            text += line
    return text

def remove_inline_styles(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup.find_all():
        if tag.has_attr("style"):
            del tag["style"]

    return str(soup)

def write_to_file(output_file, text):
    with open(output_file, "w") as file:
        file.write(text)
        
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    unique_html_file = os.path.join(data_dir, 'unique.html')
    
    html_text = read_file(unique_html_file)
    html_without_styles = remove_inline_styles(html_text);

    output_file_name = os.path.join(data_dir, 'without_inline_styles.html')
    write_to_file(output_file_name, html_without_styles)
