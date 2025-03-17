# Apply stemming or lemitization to vectors

# Fix weights folder doesn’t exist

# Use CAG not RAG for recommendations

# adhere meetup data to schema; do not put in description (for now)

# don't normalize. it is unecessary for cosine 

# add time and location to result

# handle multiple days for data gathering
* eventbrite

# allow zero recommendations to still render results

# logs
* move all print statements to log
* determine log levels

# lits results
* add time to list output
* show what data source is responsible for the result


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

# a front end that allows for entering all needed info

# out of scope
### ranking results
it would be interesting to allow for certain past events to be ranked by how much they enjoyed the event. using attenuation, we can adjust the previous event to better affect future recemondations 

