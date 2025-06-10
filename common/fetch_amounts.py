import json

def write_fetch_amounts_to_file(fetch_amount_file, eventbrite_fetch_amount, meetup_fetch_amount):
    fetch_dict = {
        "eventbrite_fetch_amount": eventbrite_fetch_amount,
        "meetup_fetch_amount": meetup_fetch_amount
    }

    with open(fetch_amount_file, "w") as json_file:
        json.dump(fetch_dict, json_file, indent=4) 


if __name__ == '__main__': # test driver for function
    write_fetch_amounts_to_file('deleteme.json', 123, 456)