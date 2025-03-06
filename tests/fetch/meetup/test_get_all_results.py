from unittest.mock import MagicMock, patch
from fetch.meetup.get_data import get_all_results
from datetime import datetime

def test_get_all_results_extracts_graphql_and_formats_to_json_schema():
    json_response = {
        "data": {
            "result": { 
                "pageInfo": { 
                    "hasNextPage": False,
                    "endCursor": "end_cursor",
                }, 
                "edges": {

                }
            }
        }
    }
    target_date = datetime.today().strftime("%Y-%m-%d")
    
    with patch("requests_html.HTMLSession") as MockSession:
        mock_post_response = MagicMock()
        MockSession.post.return_value = mock_post_response
        mock_post_response.raise_for_status.return_value = None
        mock_post_response.json.return_value = json_response
        
        result = get_all_results(target_date, MockSession)

        assert result == []