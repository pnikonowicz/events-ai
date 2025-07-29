
# full stack

## additinal data sites
* luma: https://lu.ma/nyc
* luma api: https://api.lu.ma/discover/get-paginated-events (uses a cursor)

## list times
* add time to meetup events

## handle multiple days for data gathering
add saturday

## dynamically generate previous events
use supported data sites to grab previous events that the user
has attended so that they will not have to enter in this information manually

# Dev ops

## allow query.html to point to local env
currently the query.html page has a static link to the prod site. 
making this variable depending on environment will make development easier

## add robots.txt
for non-user agents
https://events-ai-server-152896986419.us-central1.run.app/robots.txt

## cleanup unused repositories on dockerhub
the fetch and server repositories should no longer be being used. 
verify this and remove if true

## fix persisted query for meetup
the persisted query graphql sha changes often. 
allow this query sha to update dynamically

## add healthcheck endpoint
* for gcs to determine that servcie is up and running

## restrict gcs servcie account to public bucket
* currrently has access to all buckets. only allow access to public bucket
* should probably be `projects/_/buckets/events-ai-public` but remember it takes time to propagate
* more infor here: https://cloud.google.com/iam/docs/conditions-resource-attributes#resource-name

# SRE

## alert on fetch errors
if a fetch fails, notify

## set billing threshold
if billing goes over threshold, deativate service to prevent overuse


  

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

