from dataclasses import dataclass, field, asdict
from typing import List
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

    def to_dict(self):
        """Convert the dataclass to a JSON-serializable dictionary."""
        data = asdict(self)
        # Ensure similar_events is recursively converted
        data['similar_events'] = [event.to_dict() for event in self.similar_events]
        return data

def from_data_dict(dict):
    return Data(
        image=dict['image'],
        link=dict['link'],
        title=dict['title'],
        time=dict['time'],
        location=dict['location'],
        similar_events=dict['similar_events'],
        recommendation_source=dict['recommendation_source']
    )

class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Data):
            return obj.to_dict()
        return super().default(obj)

def write_data(output_file, data_objects):
    data = [asdict(d) for d in data_objects]
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=4)

def read_data(json_data_file):
    with open(json_data_file, 'r') as file:
        return from_json_string(file.read())
    
def query_data_to_embedding_filename(query_text):
    return sha256(query_text.encode('ascii')).hexdigest()

def to_json_string(data): 
    return json.dumps(data, cls=DataEncoder, indent=2)

def from_json_string(data):
    return json.loads(data, object_hook = from_data_dict)