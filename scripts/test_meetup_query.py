import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import fetch.meetup.get_data as meetup
from fetch.target_date import QueryDate

query_json = meetup.create_query_json("", QueryDate.Today.meetup())
response_json = meetup.grab_results(query_json)

print(response_json)