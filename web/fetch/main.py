import os
import sys
import argparse
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


def dates_to_fetch(current_date=None, requested_day=None):
    if requested_day:
        Logger.log(f"Fetching events for requested date: {requested_day}")
        return [QueryDate.requested_dates[requested_day]]

    dates = [QueryDate.Today, QueryDate.Tomorrow]
    current_date = current_date or datetime.datetime.today()

    # Monday is 0, Sunday is 6.
    if current_date.weekday() in (3, 4):
        Logger.log("Today is Thursday or Friday, skipping Friday's data fetch.")
    else:
        dates.append(QueryDate.Friday)

    return dates


def parse_arguments(arguments=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        choices=QueryDate.requested_dates,
        help="fetch events for only this relative date",
    )
    return parser.parse_args(arguments)


def main(requested_day=None):
    Logger.log(f"clearing data: {Paths.DATA_DIR}")
    clear_result = clear_directory(Paths.DATA_DIR)
    
    if clear_result: 
        Logger.log("data cleared")
    else:
        Logger.error("data not cleared")
        exit(1)

    total_eventbrite_amount = 0
    total_meetup_amount = 0

    for query_date in dates_to_fetch(requested_day=requested_day):
        total_eventbrite_amount += fetch_eventbrite(
            DataPath(query_date.day()), query_date.eventbrite()
        )
        total_meetup_amount += fetch_meetup(query_date)
        embed_all_event_data(query_date)

    Logger.log(f"eventbrite fetched: {total_eventbrite_amount} results")
    Logger.log(f"meetup fetched: {total_meetup_amount} results")

    write_fetch_amounts_to_file(Paths.FETCH_AMOUNTS, total_eventbrite_amount, total_meetup_amount)

    if total_eventbrite_amount == 0 or total_meetup_amount == 0:
        Logger.error(
            f"fetch returned zero results: eventbrite={total_eventbrite_amount}, meetup={total_meetup_amount}"
        )
        sys.exit(1)


if __name__ == '__main__':
    main(parse_arguments().date)
