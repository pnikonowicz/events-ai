from fetch.eventbrite.get_data import fetch as fetch_eventbrite

if __name__ == "__main__":
    amount = fetch_eventbrite()
    print(f"fetched: {len(amount)} results")
