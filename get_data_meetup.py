import os
import json
from requests_html import HTMLSession

def create_query_json(endCursor):
    json_string = '''
{
  "operationName": "recommendedEventsWithSeries",
  "variables": {
    "first": 20,
    "lat": "40.75",
    "lon": "-73.98999786376953",
    "startDateRange": "2025-02-04T00:00:00-05:00",
    "endDateRange": "2025-02-04T23:59:00-05:00",
    "eventType": "PHYSICAL",
    "numberOfEventsForSeries": 1,
    "seriesStartDate": "2025-01-30",
    "sortField": "RELEVANCE",
    "doConsolidateEvents": true,
    "after": "MTAw"
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "d3b3542df9c417007a7e6083b931d2ed67073f4d74891c3f14da403164e56469"
    }
  }
}
'''
    
    json_data = json.loads(json_string)

    json_data["variables"]["after"] = endCursor

    return json_data

def grab_results(json):
    session = HTMLSession()
    url = "https://www.meetup.com/gql2"
    headers = {"Content-Type": "application/json"}

    response = session.post(url, json=json, headers=headers)

    return response

if __name__ == "__main__":
    json = create_query_json("")
    response = grab_results(json)

    print(response.status_code)
    print(response.text)