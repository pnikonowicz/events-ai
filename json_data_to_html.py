import json
import os

def json_to_html(items):
    html_content = """
    <html>
    <head>
        <title>JSON to HTML</title>
        <style>
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; display: flex; align-items: center; }
            img { width: 100px; height: auto; margin-right: 20px; }
            a { text-decoration: none; color: #333; font-size: 18px; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <ul>
        <!-- insert list conent -->
    """

    for item in items:
        html_content += f"""
            <li>
                <img src="{item['image']}" alt="Thumbnail">
                <a href="{item['link']}">{item['title']}</a>
            </li>
        """

    html_content += """
        </ul>
    </body>
    </html>
    """

    return html_content

def write_html_to_file(output_file, html_content):
    with open(output_file, 'w') as f:
        f.write(html_content)

def read_json_file(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    json_data_file = os.path.join(data_dir, 'result.json')

    json_data = read_json_file(json_data_file)
    result_html_content = json_to_html(json_data)

    html_file = os.path.join(data_dir, "out.html")
    write_html_to_file(html_file, result_html_content)
