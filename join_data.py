import os
import json

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

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')

    aggregate_json = collect_json_data(data_dir)
    output_file_name = os.path.join(data_dir, "joined.json")
    write_aggregated_json(output_file_name, aggregate_json)

    print(f"wrote {len(aggregate_json)} records to {output_file_name}")



