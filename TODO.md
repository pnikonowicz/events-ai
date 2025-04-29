# Apply stemming or lemitization to vectors

# multi tennant

## extract_recommendation reads query embeddings as argument
* cache the query embedding so that we do not exceed our token limits

## deploy to cloud run
* github action to gcp registry: https://docs.github.com/en/actions/use-cases-and-examples/deploying/deploying-to-google-kubernetes-engine
 
## extract_recommendation should not write to file
* verify image hosts site
* create endpoint that refreshes data

# handle multiple days for data gathering
* eventbrite

# list results
* add time to list output
* show what data source is responsible for the result

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

