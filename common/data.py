from dataclasses import dataclass, field
from typing import List
from dataclasses import asdict
from hashlib import sha256

import json

@dataclass
class Data:
    image: str = field(default=None)
    link: str = field(default=None)
    title: str = field(default=None)
    time: str = field(default=None)
    location: str = field(default=None)
    similar_events: List['Data'] = field(default_factory=list)
    recommendation_source: str = field(default=None)

def write_data(output_file, data_objects):
    data = [asdict(d) for d in data_objects]
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=4)

def read_data(json_data_file):
    with open(json_data_file, 'r') as file:
        data_list = json.load(file)
        return [Data(**item) for item in data_list]
    
def query_data_to_embedding_filename(query_text):
    return sha256(query_text.encode('ascii')).hexdigest()