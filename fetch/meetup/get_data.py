import os
import json
from requests_html import HTMLSession
from common.paths import DataPath
from common.logger import Logger
from common.data import Data, write_data

def create_query_json(endCursor, start_date):
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
      "sha256Hash": "41c4ab255edd3c793ee394cfaeec3f4e823eab251620360e4705032be0f949a1"
    }
  }
}
'''
    
    json_data = json.loads(json_string)

    json_data["variables"]["after"] = endCursor
    json_data["variables"]["seriesStartDate"] = start_date
    json_data["variables"]["startDateRange"] = f"{start_date}T00:00:00-05:00"
    json_data["variables"]["endDateRange"] = f"{start_date}T23:59:00-05:00"

    return json_data

def grab_results(json, session=HTMLSession()):
    url = "https://www.meetup.com/gql2"
    headers = {"Content-Type": "application/json"}

    response = session.post(url, json=json, headers=headers)
    response.raise_for_status()
    
    response_json = response.json()
    
    return response_json

def to_formatted_json(edges):
    formatted_json = []
    for edge in edges:
        node = edge['node']

        if node['featuredEventPhoto']:
          image = node['featuredEventPhoto']['highResUrl']
        else:
          image = None

        link = node['eventUrl']
        title = node['title']
        formatted_json.append(
           Data(
              image = image,
              link = link,
              title = title,
          )
        )
    return formatted_json

def get_all_results(target_date, session=HTMLSession()):
  hasNextPage = True
  nextCursor = ""
  json_results = []

  while hasNextPage and nextCursor != None:
    query_json = create_query_json(nextCursor, target_date)
    response_json = grab_results(query_json, session)
    
    if 'data' not in response_json or response_json['data'] is None:
      Logger.log("could not retrieve data: 'data' key missing or None")
      Logger.log(str(response_json))
      return []
    
    hasNextPage = response_json['data']['result']['pageInfo']['hasNextPage']
    nextCursor = response_json['data']['result']['pageInfo']['endCursor']
    formatted_json = to_formatted_json(response_json['data']['result']['edges'])
    
    json_results.extend(formatted_json)

    Logger.log(f"hasNextPage: {hasNextPage} nextCursor: {nextCursor}")

  return json_results

def create_delimted_text_from_json(edges):
    separator = "\n" + "-" * 30 + "\n"

    text_result = ''
    for edge in edges:
        item = edge.title
        text_result += f"{item}{separator}"
    
    return text_result

def write_json_to_file(data_dir, json_data): 
    os.makedirs(data_dir, exist_ok=True)

    text_file = os.path.join(data_dir, 'data.json')
    with open(text_file, "w") as file:
        json.dump(json_data, file, indent=4)

def write_text_to_file(data_dir, text_results):
    os.makedirs(data_dir, exist_ok=True)

    text_file = os.path.join(data_dir, 'text_delimited.txt')
    with open(text_file, "w") as file:
        file.write(text_results)

def fetch(data_path: DataPath, target_date):
  data_dir = os.path.join(data_path.dir(), "meetup")
  data_file = os.path.join(data_dir, 'data.json')

  edges_json = get_all_results(target_date)    
  text_result = create_delimted_text_from_json(edges_json)

  os.makedirs(data_dir, exist_ok=True)
  write_data(data_file, edges_json)
  write_text_to_file(data_dir, text_result)

  return len(edges_json)

if __name__ == "__main__":
    fetch()
    