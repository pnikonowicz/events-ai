import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from common.logger import Logger
from fetch.eventbrite.get_data import fetch as fetch_eventbrite
from fetch.meetup.get_data import fetch as fetch_meetup
from fetch.collect import collect_all_data
from fetch.unique import unique
from ai.json_data_to_embeddings import data_to_embeddings
from common.paths import Paths
from fetch.target_date import QueryDate
from common.logger import Logger
from common.paths import clear_directory

def fetch_all_event_data(query_date):
    Logger.log("clearing data")
    clear_result = clear_directory(Paths.DATA_DIR)
    
    if clear_result: 
        Logger.log("data cleared")
    else:
        Logger.error("data not cleared")
        exit(1)


    fetch_amount = fetch_eventbrite(query_date.eventbrite())
    Logger.log(f"eventbrite fetched: {fetch_amount} pages")

    fetch_amount = fetch_meetup(query_date.meetup())
    Logger.log(f"meetup fetched: {fetch_amount} results")

    joined_amount = collect_all_data()
    Logger.log(f"total data records: {joined_amount}")

    dups_removed_amount = unique(.60)
    Logger.log(f"found {dups_removed_amount} duplicates")

    embeddings_count = data_to_embeddings()
    Logger.log(f"created {embeddings_count} data embeddings")

if __name__ == '__main__':
    Logger.log("global setup")
    fetch_all_event_data(QueryDate.Today)