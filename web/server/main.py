import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from aiohttp import web, ClientSession
from multidict import MultiDict
from common.logger import Logger
from web.json_data_to_html import json_to_html
from ai.embeddings_to_recommendation_json import extract_recommendation
from ai.query_data_to_embedding import query_to_embeddings, query_to_embeddings_from_file
from ai.embeddings_to_recommendation_json import get_previous_events
from common.paths import Paths
from common.logger import Logger
from common.data import to_json_string
from ai.embedding_service import EmbeddingService
from ai.embedding_cache import EmbeddingCache
import random


original_query_data = get_previous_events(Paths.PREVIOUS_EVENTS)

async def redirect_to_handle(request):
    scheme = request.scheme
    if 'localhost' not in request.host:
        scheme = 'https' # assume prod

    url = f"{scheme}://{request.host}/recommendations"
    
    original_query_form_data = MultiDict()
    for query in original_query_data:
        original_query_form_data.add(f"{random.randint(1, 10000000)}", query)

    async with ClientSession() as session:
        async with session.post(url, data=original_query_form_data, allow_redirects=False) as response:
            if response.status == 200:
                text = await response.text()
                return web.Response(text = text, content_type='text/html')
            else:
                text = await response.text()
                return web.Response(text = f"Request failed with status: {response.status}: {text}", content_type='text/html')

async def handle(request):
    original_query_form_data = await request.post() # should be json array of strings
    original_query_data = [f"{value}" for key, value in original_query_form_data.items()]
    Logger.log(f"data: {original_query_data}")

    if not isinstance(original_query_data, list):
        return web.Response(
            text = f"Payload {original_query_data} must be a JSON array of strings. got: {type(original_query_data).__name__}",
            content_type='text/html',
            status=400
        )
    
    query_embeddings = query_to_embeddings(EmbeddingCache(), EmbeddingService(), original_query_data)

    recommendation_json, recommendation_count = extract_recommendation(original_query_data, query_embeddings, threshold=.85)
    Logger.log(f"found: {recommendation_count} recommendation(s)")

    recommendation_html = json_to_html(recommendation_json)

    return web.Response(text=recommendation_html, content_type='text/html')

query_embeddings = query_to_embeddings_from_file()

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
            web.get('/', redirect_to_handle),
            web.post('/recommendations', handle),
            web.get('/json', handleJSON)
        ]
    )
    web.run_app(app)
