# data: add tests for each layer

# adhere meetup data to schema; do not put in description (for now)

# don't normalize. it is unecessary for cosine 

# add time and location to result

# fetch
* meetup tomorrow date range incorrect

# handle multiple days for data gathering
* eventbrite

# make api_key optional
* add api key info to README

# logs
* move all print statements to log
* determine log levels

# sort
* add time
* add id
* sort or filter by time
* also sort by recommended index

# refactor common areas
* write to file
* write json to file
* load_api_key
* retrieve embeddings
* ai model name
* common dir names
* log
* get_query_text_contents
* paths
* json schema to common location

# get data in parallel
speed the fetch process up

# render source
show what data source is responsible for the result that is rendered

# web service docker container that hosts everything

# a front end that allows for entering all needed info

# out of scope
### ranking results
it would be interesting to allow for certain past events to be ranked by how much they enjoyed the event. using attenuation, we can adjust the previous event to better affect future recemondations 

