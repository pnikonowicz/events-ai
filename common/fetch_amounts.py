import json
import os

def write_fetch_amounts_to_file(fetch_amount_file, eventbrite_fetch_amount, meetup_fetch_amount):
    fetch_dict = {
        "eventbrite": eventbrite_fetch_amount,
        "meetup": meetup_fetch_amount
    }

    with open(fetch_amount_file, "w") as json_file:
        json.dump(fetch_dict, json_file, indent=4) 

def write_total_eventbrite_amount_to_file(fetch_amount_file, total_eventbrite_amount):
    # read the eventbrite that is already in the file, if any
    # update this value if non zero, otherwise keep the existing value
    # write this new value back to the file

    fetch_amounts = {
        "eventbrite": 0,
        "meetup": 0
    }
    fetch_amounts = read_fetch_amounts_from_file(fetch_amount_file)

    if total_eventbrite_amount != 0:
        fetch_amounts["eventbrite"] = total_eventbrite_amount

    with open(fetch_amount_file, "w") as json_file:
        json.dump(fetch_amounts, json_file, indent=4)

def write_total_meetup_amount_to_file(fetch_amount_file, total_meetup_amount):
    # read the meetup that is already in the file, if any
    # update this value if non zero, otherwise keep the existing value
    # write this new value back to the file

    fetch_amounts = {
        "eventbrite": 0,
        "meetup": 0
    }
    fetch_amounts = read_fetch_amounts_from_file(fetch_amount_file)

    if total_meetup_amount != 0:
        fetch_amounts["meetup"] = total_meetup_amount

    with open(fetch_amount_file, "w") as json_file:
        json.dump(fetch_amounts, json_file, indent=4)

def publish_working_data(source_name, source_dir, destination_dir):
    None

def read_fetch_amounts_from_file(fetch_amount_file):
    with open(fetch_amount_file, "r") as json_file:
        return json.load(json_file) 

if __name__ == '__main__': # test driver for function
    write_fetch_amounts_to_file('deleteme.json', 123, 456)
    amounts = read_fetch_amounts_from_file("deleteme.json")

    print(f"amounts: {amounts}")
