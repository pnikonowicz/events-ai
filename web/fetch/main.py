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
from common.paths import DataPath, Paths
from common.fetch_amounts import publish_working_data, write_total_eventbrite_amount_to_file, write_total_meetup_amount_to_file
import datetime


def embed_all_event_data(data_path: DataPath):
    Logger.log(f"embed_all_event_data from: {data_path.day}")
    Logger.log(f"collecting data from: {data_path.dir()}")
    joined_amount = collect_all_data(data_path)

    Logger.log(f"total data records: {joined_amount}")
    dups_removed_amount = unique(data_path, .60)
    Logger.log(f"found {dups_removed_amount} duplicates")

    embeddings_count = data_to_embeddings(data_path)
    Logger.log(f"created {embeddings_count} data embeddings")

def publish(eventbrite_amount, meetup_amount, data_path):
    if eventbrite_amount == 0:
        Logger.error("fetch returned zero results for eventbrite")
    else:
        Logger.log(f"eventbrite amount: {eventbrite_amount}")
        publish_working_data("eventbrite", data_path, Paths.DATA_DIR)

    if meetup_amount == 0:
        Logger.error("fetch returned zero results for meetup")
    else:
        Logger.log(f"meetup amount: {meetup_amount}")
        publish_working_data("meetup", data_path, Paths.DATA_DIR)
    

if __name__ == '__main__':
    today_data_path = DataPath(QueryDate.Today.day(), Paths.TEMP_LOCAL_DIR)
    total_eventbrite_amount = 0
    total_meetup_amount = 0
    
    today_eventbrite_amount = fetch_eventbrite(QueryDate.Today, today_data_path)
    today_meetup_amount = fetch_meetup(QueryDate.Today, today_data_path)

    embed_all_event_data(today_data_path)
    publish(today_eventbrite_amount, today_meetup_amount, today_data_path)

    tomorrow_data_path = DataPath(QueryDate.Tomorrow.day(), Paths.TEMP_LOCAL_DIR)
    tomorrow_eventbrite_amount = fetch_eventbrite(QueryDate.Tomorrow, tomorrow_data_path)
    tomorrow_meetup_amount = fetch_meetup(QueryDate.Tomorrow, tomorrow_data_path)
    
    embed_all_event_data(tomorrow_data_path)
    publish(tomorrow_eventbrite_amount, tomorrow_meetup_amount, tomorrow_data_path)
    
    total_eventbrite_amount = today_eventbrite_amount + tomorrow_eventbrite_amount
    total_meetup_amount = today_meetup_amount + tomorrow_meetup_amount

    today = datetime.datetime.today().weekday()  # Monday is 0, Sunday is 6
    # Only fetch Friday's data if today is not Thursday (3) OR Friday (4)
    if today == 4 or today == 3:
        Logger.log("Today is Thursday or Friday, skipping Friday's data fetch.")
    else:
        friday_data_path = DataPath(QueryDate.Friday.day(), Paths.TEMP_LOCAL_DIR)
        friday_eventbrite_amount = fetch_eventbrite(QueryDate.Friday, friday_data_path)
        friday_meetup_amount = fetch_meetup(QueryDate.Friday, friday_data_path)
        embed_all_event_data(friday_data_path)
        publish(friday_eventbrite_amount, friday_meetup_amount, friday_data_path)
        total_eventbrite_amount += friday_eventbrite_amount
        total_meetup_amount += friday_meetup_amount

    if total_eventbrite_amount == 0:
        Logger.error("fetch returned zero results for eventbrite")
    else:
        Logger.log(f"total eventbrite amount: {total_eventbrite_amount}")
        write_total_eventbrite_amount_to_file(Paths.FETCH_AMOUNTS, total_eventbrite_amount)
    
    if total_meetup_amount == 0:
        Logger.error("fetch returned zero results for meetup")
    else:
        Logger.log(f"total meetup amount: {total_meetup_amount}")
        write_total_meetup_amount_to_file(Paths.FETCH_AMOUNTS, total_meetup_amount)

    if total_eventbrite_amount == 0 or total_meetup_amount == 0:
        Logger.error(
            f"fetch returned zero results: eventbrite={total_eventbrite_amount}, meetup={total_meetup_amount}"
        )
        sys.exit(1)
