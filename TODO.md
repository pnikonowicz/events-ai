# Apply stemming or lemitization to vectors

# multi tennant

## add request previous event argument
* the server currently does not accept any arguemnts. allow a json [] for previous events to be sent down and processed on demand

## create previous events front end
* allow for a user to enter in their previous events

# Dev ops

## auto push docker changes
* when one of the prod docker files change, upload to dockerhub

## make deploying static assets automatic
* when static assets (web/static) changes, automatically update the blob in our public bucket

## add healthcheck endpoint
* for gcs to determine that servcie is up and running

# SRE

## alert on fetch errors
if a fetch fails, notify

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

