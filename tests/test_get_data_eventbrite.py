from get_data_eventbrite import get_number_of_pages_from_html
from get_data_eventbrite import extract_html_results_from_html_page

def test_get_number_of_pages():
    raw_html = """
<html>
    <body>
        <footer>1 of 8</footer>
    </body>
</html>
"""
    actual_page_number = get_number_of_pages_from_html(raw_html)

    assert actual_page_number == 8

def test_extract_html_results_from_html_page():
    raw_html = """
<html>
    <body>
        <div>NOT SEARCH EVENT DIV</div>
        <div data-testid="search-event">
            <div>BAD DIV 1</div>
            <div>GOOD DIV 1</div>
        </div>
        <div data-testid="search-event">
            <div>BAD DIV 2</div>
            <div>GOOD DIV 2</div>
        </div>
    </body>
</html>
"""
    html_result, text_result, number_of_results = extract_html_results_from_html_page(raw_html)

    assert number_of_results == 2

    for result in [html_result, text_result]:
        assert "GOOD DIV 1" in result
        assert "GOOD DIV 2" in result
        assert "BAD DIV 1" not in result
        assert "BAD DIV 2" not in result
