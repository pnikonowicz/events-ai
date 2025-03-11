from fetch.eventbrite.get_data import fetch as fetch_eventbrite
from fetch.meetup.get_data import fetch as fetch_meetup
from fetch.collect import collect_all_data
from fetch.unique import unique
from ai.json_data_to_embeddings import data_to_embeddings
from ai.query_data_to_embedding import query_to_embeddings
from ai.embeddings_to_recommendation_json import extract_recommendation
from web.json_data_to_html import to_html
import os
from shutil import rmtree
from common.paths import Paths
from fetch.target_date import QueryDate

def remove_dir(dir):
    if os.path.exists(dir):
        rmtree(dir)
    else:
        print("dir not found, nothing to delete")

if __name__ == "__main__":
    data_dir = os.path.join(Paths.PROJECT_DIR, "data")
    remove_dir(data_dir)

    query_date = QueryDate.Today
    fetch_amount = fetch_eventbrite(query_date.eventbrite())
    print(f"eventbrite fetched: {fetch_amount} results")

    fetch_amount = fetch_meetup(query_date.meetup())
    print(f"meetup fetched: {fetch_amount} results")

    joined_amount = collect_all_data()
    print(f"total data records: {joined_amount}")

    dups_removed_amount = unique(.60)
    print(f"found {dups_removed_amount} duplicates")

    embeddings_count = data_to_embeddings()
    print(f"created {embeddings_count} data embeddings")

    query_embeddings_count = query_to_embeddings()
    print(f"created {query_embeddings_count} query embeddings")

    recommendation_count = extract_recommendation(threshold=.85)
    print(f"found: {recommendation_count} recommendation(s)")

    output_html_location = to_html()
    print(f"see results at: {output_html_location}")

