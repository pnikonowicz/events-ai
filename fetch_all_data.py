from fetch.eventbrite.get_data import fetch as fetch_eventbrite
import os
import json
from common.paths import Paths

def collect_json_data(root_folder, target_filename="data.json"):
    aggregated_data = []

    for dirpath, _, filenames in os.walk(root_folder):
        if target_filename in filenames:
            file_path = os.path.join(dirpath, target_filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for d in data:
                    aggregated_data.append(d)

    return aggregated_data

def write_aggregated_json(output_path, data):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def collect_all_data():
    data_dir = os.path.join(Paths.PROJECT_DIR, 'data')

    aggregate_json = collect_json_data(data_dir)
    output_file_name = os.path.join(data_dir, "joined.json")
    write_aggregated_json(output_file_name, aggregate_json)

    return len(aggregate_json)

if __name__ == "__main__":
    fetch_amount = fetch_eventbrite()
    print(f"fetched: {len(fetch_amount)} results")

    joined_amount = collect_all_data()
    print(f"total data records: {joined_amount}")
