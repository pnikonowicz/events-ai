import json
from common.data import Data
from common.data import to_json_string, from_data_dict

expected_json_string = '''[
  {
    "image": "image",
    "link": "link",
    "title": "event",
    "time": "time",
    "location": "location",
    "similar_events": [
      {
        "image": null,
        "link": null,
        "title": "similar_event",
        "time": null,
        "location": null,
        "similar_events": [],
        "recommendation_source": null
      }
    ],
    "recommendation_source": null
  }
]'''

expected_data_object = [
  Data(
      image="image",
      link="link",
      title="event",
      time="time",
      location="location",
      similar_events = [
          Data(
            title="similar_event",
          )
      ],
  )
]

def from_json_file(data):
    return json.loads(data, object_hook = from_data_dict)
    
def test_json_serializer():
    json_string = to_json_string(expected_data_object)
    
    assert expected_json_string == json_string

def test_json_deserializer():
    data_object = from_json_file(expected_json_string)

    assert data_object == expected_data_object

def test_round_trip():
    assert to_json_string(from_json_file(expected_json_string)) == expected_json_string