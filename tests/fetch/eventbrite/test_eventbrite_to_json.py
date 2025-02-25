from fetch.eventbrite.to_json import extract_html_results_from_html_page


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
