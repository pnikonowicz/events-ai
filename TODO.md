# bug: get_data_eventbrite is adding html close tags for each page, which is causing future parsing to stop prematurely 

# data: join the eventbrite and meeetup data

# RAG
* load embedding into in memory database (langchain provides this)
* generate query embedding
* generate results from the context of "is there anything going on this day"

# web service docker container that hosts everything

# a front end that allows for entering all needed info