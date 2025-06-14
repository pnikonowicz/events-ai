import os
import json
from common.paths import DataPath

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

def collect_all_data(data_path: DataPath):
    aggregate_json = collect_json_data(data_path.dir())
    output_file_name = os.path.join(data_path.dir(), "joined.json")
    write_aggregated_json(output_file_name, aggregate_json)

    return len(aggregate_json)