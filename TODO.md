# data: add tests for each layer

# adhere meetup data to schema; do not put in description (for now)

# refactor common areas
* write to file
* write json to file
* load_api_key
* retrieve embeddings
* ai model name
* common dir names

# RAG
* G - create query prompt engineering context
* G - generate results from the context of "is there anything going on this day"
* A - take the indexes and create html that says ("because you liked <recomendation query>" and then provide the html for recemondation)

# ranking results
it would be interesting to allow for certain past events to be ranked by how much they enjoyed the event. using attenuation, we can adjust the previous event to better affect future recemondations 

# web service docker container that hosts everything

# a front end that allows for entering all needed info
