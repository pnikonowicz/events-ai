
import datetime
from fetch import target_date

def test_meetupquerydate_tomorrow():
    # Set a fixed date for reproducibility
    fixed_now = datetime.datetime(2025, 7, 18)  # Friday
    expected_tomorrow = "2025-07-19"
    result = target_date.MeetupQueryDate.Tomorrow(date_time_now=fixed_now)
    assert result == expected_tomorrow

def test_meetupquerydate_friday():
    # Set a fixed date for reproducibility
    fixed_now = datetime.datetime(2025, 7, 18)  # Friday
    # Should return the same day if today is Friday
    expected_friday = "2025-07-18"
    result = target_date.MeetupQueryDate.Friday(date_time_now=fixed_now)
    assert result == expected_friday

    # Test for a Thursday
    thursday = datetime.datetime(2025, 7, 17)  # Thursday
    expected_friday = "2025-07-18"
    result = target_date.MeetupQueryDate.Friday(date_time_now=thursday)
    assert result == expected_friday

    # Test for a Saturday (should return next Friday)
    saturday = datetime.datetime(2025, 7, 19)  # Saturday
    expected_friday = "2025-07-25"
    result = target_date.MeetupQueryDate.Friday(date_time_now=saturday)
    assert result == expected_friday

def test_eventbritequerydate_friday():
    # Set a fixed date for reproducibility
    fixed_now = datetime.datetime(2025, 7, 18)  # Friday
    expected_friday = "2025-07-18"
    url = target_date.FridayEventbriteQueryDate(fixed_now).create(2)
    assert expected_friday in url

    # Test for a Thursday
    thursday = datetime.datetime(2025, 7, 17)  # Thursday
    expected_friday = "2025-07-18"
    url = target_date.FridayEventbriteQueryDate(thursday).create(2)
    assert expected_friday in url

    # Test for a Saturday (should return next Friday)
    saturday = datetime.datetime(2025, 7, 19)  # Saturday
    expected_friday = "2025-07-25"
    url = target_date.FridayEventbriteQueryDate(saturday).create(2)
    assert expected_friday in url

def test_querydate_day_directories_use_short_date_format():
    fixed_now = datetime.datetime(2025, 7, 18)  # Friday

    assert target_date.QueryDate.Today.day(fixed_now) == "25-07-18"
    assert target_date.QueryDate.Tomorrow.day(fixed_now) == "25-07-19"
    assert target_date.QueryDate.Friday.day(fixed_now) == "25-07-18"

def test_querydate_friday_day_directory_uses_next_friday():
    saturday = datetime.datetime(2025, 7, 19)

    assert target_date.QueryDate.Friday.day(saturday) == "25-07-25"
