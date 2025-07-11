import json

def write_fetch_amounts_to_file(fetch_amount_file, eventbrite_fetch_amount, meetup_fetch_amount):
    fetch_dict = {
        "eventbrite": eventbrite_fetch_amount,
        "meetup": meetup_fetch_amount
    }

    with open(fetch_amount_file, "w") as json_file:
        json.dump(fetch_dict, json_file, indent=4) 

def read_fetch_amounts_from_file(fetch_amount_file):
    with open(fetch_amount_file, "r") as json_file:
        return json.load(json_file) 

if __name__ == '__main__': # test driver for function
    write_fetch_amounts_to_file('deleteme.json', 123, 456)
    amounts = read_fetch_amounts_from_file("deleteme.json")

    print(f"amounts: {amounts}")