import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from aiohttp import web
from common.logger import Logger
from ai.embeddings_to_recommendation_json import extract_recommendation
from web.json_data_to_html import html_to_file
from common.paths import Paths

async def handle(request):
    recommendation_count = extract_recommendation(threshold=.85)
    Logger.log(f"found: {recommendation_count} recommendation(s)")

    html_to_file()
    
    with open(Paths.ALL_HTML, 'r') as file:
        html_content = file.read()

    return web.Response(text=html_content, content_type='text/html')

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(
        [
            web.get('/', handle)
        ]
    )
    web.run_app(app)