# Apply stemming or lemitization to vectors

# multi tennant

## add healthcheck endpoint

## only use one container
* parameterize the start CMD so that only one container is used for fetch and server
* rotate google secret api key
* delete all unused keys

## put default previous events into blob storage
* this will fix issues when containers have different copies of these files

## extract_recommendation reads query embeddings as argument
* cache the query embedding so that we do not exceed our token limits

## auto push docker changes
* when one of the prod docker files change, upload to dockerhub

# handle multiple days for data gathering
* eventbrite

# show site summary at top
* meetup results and eventbrite results sum so that we know that meetup results are included
  
# list results
* add time to list output
* show what data source is responsible for the result

# add robots.txt

for non-user agents
https://events-ai-server-152896986419.us-central1.run.app/robots.txt


# fix 404 img bug

GET404 143 B 33 ms Firefox 138 https://events-ai-server-152896986419.us-central1.run.app/None

I think it's coming from when an image has no url to grab

# refactor common areas
* write to file
* write json to file
* load_api_key
* retrieve embeddings
* ai model name
* common dir names
* get_query_text_contents
* paths
* json schema to common location

# additinal data sites
* luma: https://lu.ma/nyc

# a front end that allows for entering all needed info

# out of scope
### ranking results
it would be interesting to allow for certain past events to be ranked by how much they enjoyed the event. using attenuation, we can adjust the previous event to better affect future recemondations 

