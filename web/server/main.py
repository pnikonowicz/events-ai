import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from aiohttp import web
from common.logger import Logger
from web.json_data_to_html import json_to_html
from fetch.eventbrite.get_data import fetch as fetch_eventbrite
from fetch.meetup.get_data import fetch as fetch_meetup
from fetch.collect import collect_all_data
from fetch.unique import unique
from ai.json_data_to_embeddings import data_to_embeddings
from ai.query_data_to_embedding import query_to_embeddings_from_file
from ai.embeddings_to_recommendation_json import extract_recommendation
from ai.embeddings_to_recommendation_json import read_embeddings
from ai.embeddings_to_recommendation_json import get_previous_events
from common.paths import Paths
from fetch.target_date import QueryDate
from common.logger import Logger

def setup(query_date):
    if os.path.exists(Paths.DATA_DIR):
        Logger.log("data already exists. setup not needed")
        return

    fetch_amount = fetch_eventbrite(query_date.eventbrite())
    Logger.log(f"eventbrite fetched: {fetch_amount} results")

    fetch_amount = fetch_meetup(query_date.meetup())
    Logger.log(f"meetup fetched: {fetch_amount} results")

    joined_amount = collect_all_data()
    Logger.log(f"total data records: {joined_amount}")

    dups_removed_amount = unique(.60)
    Logger.log(f"found {dups_removed_amount} duplicates")

    embeddings_count = data_to_embeddings()
    Logger.log(f"created {embeddings_count} data embeddings")

    query_embeddings_count = query_to_embeddings_from_file()
    Logger.log(f"created {query_embeddings_count} query embeddings")

Logger.log("global setup")
setup(QueryDate.Today)

original_query_data = get_previous_events(Paths.PREVIOUS_EVENTS)
query_embeddings = read_embeddings(Paths.QUERY_EMBEDDINGS)

async def handle(request):
    recommendation_json, recommendation_count = extract_recommendation(original_query_data, query_embeddings, threshold=.85)
    Logger.log(f"found: {recommendation_count} recommendation(s)")

    recommendation_html = json_to_html(recommendation_json)
    
    return web.Response(text=recommendation_html, content_type='text/html')

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(
        [
            web.get('/', handle)
        ]
    )
    web.run_app(app)