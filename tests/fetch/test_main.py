import datetime
import pytest

from fetch.target_date import QueryDate
from web.fetch.main import dates_to_fetch, parse_arguments


def test_dates_to_fetch_includes_friday_on_non_thursday_or_friday():
    requested_dates = dates_to_fetch(datetime.datetime(2025, 7, 19))  # Saturday

    assert requested_dates == [
        QueryDate.Today,
        QueryDate.Tomorrow,
        QueryDate.Friday,
    ]


def test_dates_to_fetch_skips_friday_on_thursday_and_friday():
    thursday_dates = dates_to_fetch(datetime.datetime(2025, 7, 17))
    friday_dates = dates_to_fetch(datetime.datetime(2025, 7, 18))

    assert thursday_dates == [QueryDate.Today, QueryDate.Tomorrow]
    assert friday_dates == [QueryDate.Today, QueryDate.Tomorrow]


@pytest.mark.parametrize(
    ("requested_day", "expected_date"),
    [
        ("today", QueryDate.Today),
        ("tomorrow", QueryDate.Tomorrow),
        ("friday", QueryDate.Friday),
    ],
)
def test_dates_to_fetch_returns_only_the_requested_date(
    requested_day, expected_date
):
    dates = dates_to_fetch(requested_day=requested_day)

    assert dates == [expected_date]


def test_parse_arguments_accepts_requested_date():
    arguments = parse_arguments(["--date", "tomorrow"])

    assert arguments.date == "tomorrow"
