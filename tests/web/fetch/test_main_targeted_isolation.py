import pytest

from common.paths import Paths
from fetch.target_date import QueryDate
from web.fetch import main as fetch_main


DERIVED_WORKFLOW_FUNCTIONS = (
    "collect_all_data",
    "unique",
    "data_to_embeddings",
    "publish_working_data",
    "write_total_eventbrite_amount_to_file",
    "write_total_meetup_amount_to_file",
    "embed_all_event_data",
    "publish",
)


def fail_if_called(name):
    def _fail(*args, **kwargs):
        raise AssertionError(f"{name} should not be called in targeted mode")

    return _fail


@pytest.fixture
def block_derived_workflows(monkeypatch):
    for function_name in DERIVED_WORKFLOW_FUNCTIONS:
        monkeypatch.setattr(
            fetch_main,
            function_name,
            fail_if_called(function_name),
        )


def test_targeted_eventbrite_today_invokes_only_eventbrite(monkeypatch, block_derived_workflows):
    calls = []

    def fake_eventbrite(query_date, data_path):
        calls.append(("eventbrite", query_date, data_path.day, data_path.base_dir))
        return 7

    monkeypatch.setattr(fetch_main, "fetch_eventbrite", fake_eventbrite)
    monkeypatch.setattr(fetch_main, "fetch_meetup", fail_if_called("fetch_meetup"))

    assert fetch_main.main(["eventbrite", "today"]) == 0

    assert calls == [
        ("eventbrite", QueryDate.Today, "today", Paths.TEMP_LOCAL_DIR),
    ]


def test_targeted_meetup_friday_invokes_only_meetup(monkeypatch, block_derived_workflows):
    calls = []

    def fake_meetup(query_date, data_path):
        calls.append(("meetup", query_date, data_path.day, data_path.base_dir))
        return 3

    monkeypatch.setattr(fetch_main, "fetch_eventbrite", fail_if_called("fetch_eventbrite"))
    monkeypatch.setattr(fetch_main, "fetch_meetup", fake_meetup)

    assert fetch_main.main(["meetup", "friday"]) == 0

    assert calls == [
        ("meetup", QueryDate.Friday, "friday", Paths.TEMP_LOCAL_DIR),
    ]


def test_zero_result_targeted_mode_returns_nonzero_without_derived_calls(
    monkeypatch, block_derived_workflows
):
    calls = []

    def fake_meetup(query_date, data_path):
        calls.append(("meetup", query_date, data_path.day, data_path.base_dir))
        return 0

    monkeypatch.setattr(fetch_main, "fetch_eventbrite", fail_if_called("fetch_eventbrite"))
    monkeypatch.setattr(fetch_main, "fetch_meetup", fake_meetup)

    assert fetch_main.main(["meetup", "tomorrow"]) == 1

    assert calls == [
        ("meetup", QueryDate.Tomorrow, "tomorrow", Paths.TEMP_LOCAL_DIR),
    ]
