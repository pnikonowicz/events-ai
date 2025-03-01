import json
import os
from common.paths import Paths
import pathlib

def json_to_html(items):
    html_content = """
    <html>
    <head>
        <title>JSON to HTML</title>
        <style>
            body { background-color: #000; color: #fff; font-family: Arial, sans-serif; }
            ul { list-style-type: none; padding: 0; }
            li { 
                margin: 1em 0; 
                align-items: center; 
                background: linear-gradient(135deg, #1e3c72, #2a5298); /* Deep blue gradient */
                padding: 2em;
                border-radius: 5em;
                box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
                transition: transform 0.2s ease-in-out;
                transform-origin: left; /* Make the scale pivot from the left side */
                display: flex;
            }
            li div {
                display: flex;
                flex-direction: column;
            }
            li:hover { 
                transform: scale(1, 1.1); /* Scale up, moving more to the right */
                box-shadow: 2px 2px 15px rgba(255, 255, 255, 0.4);
            }
            img { 
                width: 100px; 
                height: auto; 
                margin-right: 20px;
                border-radius: 5px;
                object-fit: cover;
            }
            a { text-decoration: none; color: #fff; font-size: 18px; font-weight: bold; }
            a:hover { text-decoration: underline; color: #ffcc00; }
            span {
                    display: flex;
                    flex-direction: column;
            }
            .similiar_events {
                margin-left: 1em;
                padding: 1em;                
            }
        </style>

    </head>
    <body>
        <ul>
        <!-- insert list content -->
    """

    for item in items:
        similiar_events_json = item.get('similar_events', [])
        similiar_events_titles = "\n".join("<span>" + event['title'] + "</span>" for event in similiar_events_json)
        html_similiar_events = f"""
            <div class="similiar_events">
                {similiar_events_titles}
            </div>
        """
        html_content += f"""
            <li>
                <img src="{item['image']}" alt="Thumbnail">
                <div>
                    <span>because you liked: {item.get('recemondation_source') or "N/A"}<span>
                    <a href="{item['link']}" target="about:blank">{item['title']}</a>
                    <div>there are also {len(similiar_events_json)} similiar events
                        {html_similiar_events}
                    </div>
                </div>
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

def log(text, level="DEBUG"):
    print(f"{level}: {text}")

def get_recemondation_html_content(recemondation_json_file):
    if os.path.isfile(recemondation_json_file):
        recemondation_json_data = read_json_file(recemondation_json_file)
        recemondation_html_content = json_to_html(recemondation_json_data)
        return recemondation_html_content
    else:
        log("no recemondation data file found at {recemondation_json_file}, skipping", "WARN")
        return ""
    

def to_html():
    data_dir = os.path.join(Paths.PROJECT_DIR, 'data')
    json_data_file = os.path.join(data_dir, 'unique.json')
    
    recemondation_json_file = os.path.join(data_dir, 'recemondations.json')
    recemondation_html_content = get_recemondation_html_content(recemondation_json_file)

    all_json_data = read_json_file(json_data_file)
    result_html_content = json_to_html(all_json_data)

    html_file = os.path.join(data_dir, "all.html")
    write_html_to_file(html_file, recemondation_html_content + result_html_content)

    return pathlib.Path(os.path.abspath(html_file)).as_uri()
