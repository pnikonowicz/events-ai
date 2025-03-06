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
import datetime

def remove_dir(dir):
    if os.path.exists(dir):
        rmtree(dir)
    else:
        print("dir not found, nothing to delete")

if __name__ == "__main__":
    data_dir = os.path.join(Paths.PROJECT_DIR, "data")
    remove_dir(data_dir)

    target_day = "tomorrow"
    # target_day = "today"
    fetch_amount = fetch_eventbrite(target_day)
    print(f"fetched: {fetch_amount} results")

    # target_date = datetime.today().strftime("%Y-%m-%d")
    target_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    fetch_amount = fetch_meetup(target_date)
    
    joined_amount = collect_all_data()
    print(f"total data records: {joined_amount}")

    dups_removed_amount = unique()
    print(f"found {dups_removed_amount} duplicates")

    embeddings_count = data_to_embeddings()
    print(f"created {embeddings_count} data embeddings")

    query_embeddings_count = query_to_embeddings()
    print(f"created {query_embeddings_count} query embeddings")

    recommendation_count = extract_recommendation(threshold=.85)
    print(f"found: {recommendation_count} recommendation(s)")

    output_html_location = to_html()
    print(f"see results at: {output_html_location}")

