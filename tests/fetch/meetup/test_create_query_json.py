from fetch.target_date import MeetupQueryDate
from fetch.meetup.get_data import create_query_json
from datetime import datetime

time_seed = datetime(2025, 2, 4, 15, 25, 20)
def test_query_json_with_cursor():
    cursor = "graph_ql_next_cursor"
    result = create_query_json(cursor, MeetupQueryDate.Today(time_seed))
    
    assert result["variables"]["after"] == cursor

def test_query_json_with_today():
    result = create_query_json("", MeetupQueryDate.Today(time_seed))
    
    assert result["variables"]["endDateRange"] == "2025-02-04T23:59:00-05:00"
    assert result["variables"]["startDateRange"] == "2025-02-04T00:00:00-05:00"
    assert result["variables"]["seriesStartDate"] == "2025-02-04"

def test_query_json_with_tomorrow():
    result = create_query_json("", MeetupQueryDate.Tomorrow(time_seed))
    
    assert result["variables"]["endDateRange"] == "2025-02-05T23:59:00-05:00"
    assert result["variables"]["startDateRange"] == "2025-02-05T00:00:00-05:00"
    assert result["variables"]["seriesStartDate"] == "2025-02-05"