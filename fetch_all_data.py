from fetch.eventbrite.get_data import fetch as fetch_eventbrite
from fetch.collect import collect_all_data

if __name__ == "__main__":
    fetch_amount = fetch_eventbrite()
    print(f"fetched: {len(fetch_amount)} results")

    joined_amount = collect_all_data()
    print(f"total data records: {joined_amount}")
