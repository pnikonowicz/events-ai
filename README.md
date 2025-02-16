### goal
answers the question "are there any events going on that i might be interested in?"

there are a lot of data sites, and scrolling through all of them is time consuming.
this is a recomendation engine for events that are personalized to your preferences.

simply enter in some information about previous events you've been to, select which
data sources to pull from, and see if any recemondations come up. 

### problem
data sites have some cool events in their listings. 
but too often are the results littered with duplicates. 
and these duplicates are on other data sources as well

also, there are a lot of data sites our there, but we only
care about certain things

### solution
this project aims to allow for the dedupping of results
and creating a unique result to make events easier to 
browse through by leveraging TF-IDF vectorization.

It does this with a nearest neighbors search to group
simliar results, and then grabs the first item in the group

# running
right now everything is in modules / seperate files. so you'll need to:

1. `python get_data_[eventbrite|meetup].py`
2. `python eventbrite_to_json.py # if grabbing eventbrite data`
3. `python unique.py # to remove the duplicates`
4. `json_to_html.py # to view the results (TODO)`
then open `results.html` in your browser and see the results
