from fetch.eventbrite.to_json import json_text_to_data

def test_json_to_data():
    json_text_a=""" 
{"search_data": {"events": {"results": [{"primary_venue": {"name": "location_1"}, "start_time": "time_1", "summary": "title_1", "image": {"url": "image_url_1"}, "url": "link_url_1"}, {"image": {"url": "image_url_2"}, "url": "link_url_2"} ]}}}
"""
    json_text_b=""" 
{"search_data": {"events": {"results": [{"url": "link_url_3"} ]}}}
"""
    
    result = json_text_to_data([json_text_a, json_text_b])

    assert len(result) == 3

    assert result[0].image == "image_url_1"
    assert result[0].link == "link_url_1"
    assert result[0].title == "title_1"
    assert result[0].time == "time_1"
    assert result[0].location == "location_1"

    assert result[1].image == "image_url_2"
    assert result[1].link == "link_url_2"
    assert result[1].title == "UNKNOWN_TITLE"
    assert result[1].time == "UNKNOWN_START_TIME"
    assert result[1].location == "UNKNOWN_VENUE"

    assert result[2].image == "about:blank"
    assert result[2].link == "link_url_3"
    assert result[2].title == "UNKNOWN_TITLE"
    assert result[2].time == "UNKNOWN_START_TIME"
    assert result[2].location == "UNKNOWN_VENUE"