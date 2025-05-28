import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from aiohttp import web
from common.logger import Logger
from web.json_data_to_html import json_to_html
from ai.embeddings_to_recommendation_json import extract_recommendation
from ai.query_data_to_embedding import query_to_embeddings_from_file
from ai.embeddings_to_recommendation_json import get_previous_events
from common.paths import Paths
from common.logger import Logger
from common.data import to_json_string


original_query_data = get_previous_events(Paths.PREVIOUS_EVENTS)
query_embeddings = query_to_embeddings_from_file()


async def handle(request):
    recommendation_json, recommendation_count = extract_recommendation(original_query_data, query_embeddings, threshold=.85)
    Logger.log(f"found: {recommendation_count} recommendation(s)")

    recommendation_html = json_to_html(recommendation_json)

    return web.Response(text=recommendation_html, content_type='text/html')


async def handleJSON(request):
    recommendation_list, recommendation_count = extract_recommendation(
        original_query_data, query_embeddings, threshold=.85)
    Logger.log(f"found: {recommendation_count} recommendation(s)")

    recommendation_json = to_json_string(recommendation_list)

    return web.json_response(recommendation_json)

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(
        [
            web.get('/', handle),
            web.get('/json', handleJSON)
        ]
    )
    web.run_app(app)
