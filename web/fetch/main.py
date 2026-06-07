import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from common.logger import Logger
from fetch.eventbrite.get_data import fetch as fetch_eventbrite
from fetch.meetup.get_data import fetch as fetch_meetup
from fetch.collect import collect_all_data
from fetch.unique import unique
from ai.json_data_to_embeddings import data_to_embeddings
from fetch.target_date import QueryDate
from common.logger import Logger
from common.paths import clear_directory, DataPath, Paths
from common.fetch_amounts import write_total_eventbrite_amount_to_file, write_total_meetup_amount_to_file
import datetime


def embed_all_event_data(query_date: QueryDate):
    Logger.log(f"embed_all_event_data from: {query_date.day()}")

    data_path = DataPath(query_date.day())

    Logger.log(f"collecting data from: {data_path.dir()}")
    joined_amount = collect_all_data(data_path)

    Logger.log(f"total data records: {joined_amount}")
    dups_removed_amount = unique(data_path, .60)
    Logger.log(f"found {dups_removed_amount} duplicates")

    embeddings_count = data_to_embeddings(data_path)
    Logger.log(f"created {embeddings_count} data embeddings")

if __name__ == '__main__':
    total_eventbrite_amount = 0
    total_meetup_amount = 0

    tmp_local_directory = Paths.TEMP_LOCAL_DIR
    
    total_eventbrite_amount += fetch_eventbrite(QueryDate.Today)
    Logger.log(f"eventbrite fetched: {total_eventbrite_amount} results")

    total_meetup_amount += fetch_meetup(QueryDate.Today)
    Logger.log(f"meetup fetched: {total_meetup_amount} results")

    embed_all_event_data(QueryDate.Today)

    total_eventbrite_amount += fetch_eventbrite(QueryDate.Tomorrow)
    total_meetup_amount += fetch_meetup(QueryDate.Tomorrow)
    embed_all_event_data(QueryDate.Tomorrow)
    
    today = datetime.datetime.today().weekday()  # Monday is 0, Sunday is 6
    # Only fetch Friday's data if today is not Thursday (3) OR Friday (4)
    if today == 4 or today == 3:
        Logger.log("Today is Thursday or Friday, skipping Friday's data fetch.")
    else:
        total_eventbrite_amount += fetch_eventbrite(QueryDate.Friday)
        total_meetup_amount += fetch_meetup(QueryDate.Friday)
        embed_all_event_data(QueryDate.Friday)
    if total_eventbrite_amount == 0:
        Logger.error("fetch returned zero results for eventbrite")
    else:
        Logger.log(f"total eventbrite amount: {total_eventbrite_amount}")
        write_total_eventbrite_amount_to_file(tmp_local_directory, Paths.FETCH_AMOUNTS, total_eventbrite_amount)
    
    if total_meetup_amount == 0:
        Logger.error("fetch returned zero results for meetup")
    else:
        Logger.log(f"total meetup amount: {total_meetup_amount}")
        write_total_meetup_amount_to_file(tmp_local_directory, Paths.FETCH_AMOUNTS, total_meetup_amount)


    if total_eventbrite_amount == 0 or total_meetup_amount == 0:
        Logger.error(
            f"fetch returned zero results: eventbrite={total_eventbrite_amount}, meetup={total_meetup_amount}"
        )
        sys.exit(1)
