# data: add tests for each layer

# adhere meetup data to schema; do not put in description (for now)

# remove raw folder when grabbing data to avoid stale results

# don't normalize. it is unecessary for cosine 

# handle multiple days for data gathering
* eventbrite

# logs
* move all print statements to log
* determine log levels

# keep track of groups. 
when groups are created in unique.py, keep the group data so that
they can eventually be displayed in the final html via a collapsable form. this way, 
we can continue to see what events were grouped together in case there are any issues
with this

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

# RAG
* G - create query prompt engineering context
* G - generate results from the context of "is there anything going on this day"
* A - take the indexes and create html that says ("because you liked <recomendation query>" and then provide the html for recemondation)

# ranking results
it would be interesting to allow for certain past events to be ranked by how much they enjoyed the event. using attenuation, we can adjust the previous event to better affect future recemondations 

# web service docker container that hosts everything

# a front end that allows for entering all needed info

