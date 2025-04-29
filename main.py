from fetch.eventbrite.get_data import fetch as fetch_eventbrite
from fetch.meetup.get_data import fetch as fetch_meetup
from fetch.collect import collect_all_data
from fetch.unique import unique
from ai.json_data_to_embeddings import data_to_embeddings
from ai.query_data_to_embedding import query_to_embeddings_from_file
from ai.embeddings_to_recommendation_json import extract_recommendation_from_file
from web.json_data_to_html import html_to_file
import os
from shutil import rmtree
from common.paths import Paths
from fetch.target_date import QueryDate
from common.logger import Logger

from common.paths import remove_dir

if __name__ == "__main__":
    query_date = QueryDate.Today

    remove_dir(Paths.DATA_DIR)

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

    recommendation_count = extract_recommendation_from_file(threshold=.85)
    Logger.log(f"found: {recommendation_count} recommendation(s)")

    output_html_location = html_to_file()
    Logger.log(f"see results at: {output_html_location}")

