from fetch.eventbrite.get_data import get_number_of_pages_from_html

def test_get_number_of_pages():
    raw_html = """
    <html><body><script>
        window.__SERVER_DATA__ = {
            "search_data": {
                "events": {
                    "pagination": {
                        "page_count": 8
                    }
                }
            }
        };
    </script></body></html>
"""
    actual_page_number = get_number_of_pages_from_html(raw_html)

    assert actual_page_number == 8
