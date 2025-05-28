import json
from common.data import Data
from common.data import to_json_string

def test_json_serializer():
    data = [
        Data(
            title = "event",
            similar_events = [
                    Data(
                    title="similar_event"
                )
            ],
        )
    ]
    
    json_string = to_json_string(data)
    print(json_string)
    assert json_string == '''[
  {
    "image": null,
    "link": null,
    "title": "event",
    "time": null,
    "location": null,
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