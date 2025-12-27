import os
import json
from requests_html import HTMLSession
from common.paths import DataPath
from common.logger import Logger
from common.data import Data, write_data
from fetch.target_date import MeetupQueryDate, QueryDate

def create_query_json(endCursor, start_date):
    json_string = '''
{
  "operationName": "recommendedEventsWithSeries",
  "variables": {
    "first": 20,
    "lat": 40.75,
    "lon": -73.98999786376953,
    "startDateRange": "2025-12-27T09:28:53-05:00[US/Eastern]",
    "numberOfEventsForSeries": 5,
    "seriesStartDate": "2025-12-27",
    "sortField": "RELEVANCE",
    "doConsolidateEvents": true,
    "doPromotePaypalEvents": false,
    "indexAlias": "{\\"filterOutWrongLanguage\\": \\"true\\",\\"modelVersion\\": \\"split_offline_online\\"}",
    "dataConfiguration": "{\\"isSimplifiedSearchEnabled\\": true, \\"include_events_from_user_chapters\\": true}",
    "after": "MTI="
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "cf6348a7edb376af58158519e78130eb8beced0aaaed60ab379e82f25fd52eea"
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
    
    results = response_json['data']['result']
    hasNextPage = results['pageInfo']['hasNextPage']
    nextCursor = results['pageInfo']['endCursor']
    formatted_json = to_formatted_json(results['edges'])
    
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

def fetch(query_date: QueryDate) -> int:
  data_path: DataPath = DataPath(query_date.day())
  target_day: MeetupQueryDate = query_date.meetup()

  data_dir = os.path.join(data_path.dir(), "meetup")
  data_file = os.path.join(data_dir, 'data.json')
  
  edges_json = get_all_results(target_day)    
  text_result = create_delimted_text_from_json(edges_json)

  os.makedirs(data_dir, exist_ok=True)
  write_data(data_file, edges_json)
  write_text_to_file(data_dir, text_result)

  event_count = len(edges_json)

  Logger.log(f"meetup fetched: {event_count} results")

  return event_count

if __name__ == "__main__":
    fetch(QueryDate.Today)
    