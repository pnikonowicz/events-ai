from unittest.mock import MagicMock, patch
from fetch.meetup.get_data import grab_results

def test_get_all_results_extracts_graphql_and_formats_to_json_schema():
    with patch("requests_html.HTMLSession") as MockSession:
        json_response = {"data": {"meetups": ["Mocked Meetup 1", "Mocked Meetup 2"]}}
        mock_post_response = MagicMock()
        MockSession.post.return_value = mock_post_response
        mock_post_response.raise_for_status.return_value = None
        mock_post_response.json.return_value = json_response
        
        result = grab_results({"query": "mocked query"}, MockSession)

        assert result == json_response