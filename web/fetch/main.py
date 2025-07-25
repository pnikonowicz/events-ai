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
from common.fetch_amounts import write_fetch_amounts_to_file
import datetime


def fetch_all_event_data(query_date: QueryDate):
    data_path = DataPath(query_date.day())

    eventbrite_fetch_amount = fetch_eventbrite(data_path, query_date.eventbrite())
    Logger.log(f"eventbrite fetched: {eventbrite_fetch_amount} results")

    meetup_fetch_amount = fetch_meetup(data_path, query_date.meetup())
    Logger.log(f"meetup fetched: {meetup_fetch_amount} results")

    joined_amount = collect_all_data(data_path)
    Logger.log(f"total data records: {joined_amount}")

    dups_removed_amount = unique(data_path, .60)
    Logger.log(f"found {dups_removed_amount} duplicates")

    embeddings_count = data_to_embeddings(data_path)
    Logger.log(f"created {embeddings_count} data embeddings")

    return eventbrite_fetch_amount, meetup_fetch_amount

if __name__ == '__main__':
    Logger.log(f"clearing data: {Paths.DATA_DIR}")
    clear_result = clear_directory(Paths.DATA_DIR)
    
    if clear_result: 
        Logger.log("data cleared")
    else:
        Logger.error("data not cleared")
        exit(1)

    today_eventbrite_amount, today_meetup_amount = fetch_all_event_data(QueryDate.Today)
    tomorrow_eventbrite_amount, tomorrow_meetup_amount = fetch_all_event_data(QueryDate.Tomorrow)

    today = datetime.datetime.today().weekday()  # Monday is 0, Sunday is 6

    # Only fetch Friday's data if today is not Thursday (3) OR Friday (4)
    if today == 4 or today == 3:
        friday_eventbrite_amount = 0
        friday_meetup_amount = 0
        Logger.log("Today is Thursday or Friday, skipping Friday's data fetch.")
    else:
        friday_eventbrite_amount, friday_meetup_amount = fetch_all_event_data(QueryDate.Friday)

    total_eventbrite_amount = today_eventbrite_amount + tomorrow_eventbrite_amount + friday_eventbrite_amount
    total_meetup_amount = today_meetup_amount + tomorrow_meetup_amount + friday_meetup_amount

    write_fetch_amounts_to_file(Paths.FETCH_AMOUNTS, total_eventbrite_amount, total_meetup_amount)
