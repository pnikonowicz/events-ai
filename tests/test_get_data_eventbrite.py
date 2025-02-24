from get_data_eventbrite import get_number_of_pages_from_html

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
