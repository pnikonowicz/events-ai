
# full stack

## additinal data sites
* luma: https://lu.ma/nyc

## allow events to be saved
this way the user does not need to re-enter events all the time

## show preview counts on query page
when the query page is loaded, contain counters that show how many events 
are shown on the site, group the events by source type, eventbrite, meetup, etc..

## list times
* add time to list output

## handle multiple days for data gathering
currently just shows today. would be nice to have tomorrow or weekend as well

## show site summary at top
* meetup results and eventbrite results sum so that we know that meetup results are included


# Dev ops

## allow query.html to point to local env
currently the query.html page has a static link to the prod site. 
making this variable depending on environment will make development easier

## add robots.txt
for non-user agents
https://events-ai-server-152896986419.us-central1.run.app/robots.txt


## clenaup unused repositories on dockerhub
the fetch and server repositories should no longer be being used. 
verify this and remove if true

## fix persisted query for meetup
the query id is wrong (again)

## auto push docker changes
* when one of the prod docker files change, upload to dockerhub

## add healthcheck endpoint
* for gcs to determine that servcie is up and running

## restrict gcs servcie account to public bucket
* currrently has access to all buckets. only allow access to public bucket
* should probably be `projects/_/buckets/events-ai-public` but remember it takes time to propagate
* more infor here: https://cloud.google.com/iam/docs/conditions-resource-attributes#resource-name

# SRE

## alert on fetch errors
if a fetch fails, notify

  

========================

# Bugs

## fix 404 img bug

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

# out of scope
### ranking results
it would be interesting to allow for certain past events to be ranked by how much they enjoyed the event. using attenuation, we can adjust the previous event to better affect future recemondations 

### Apply stemming or lemitization to vectors

