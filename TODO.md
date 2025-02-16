# find out how many pages are available in eventbrite results and conditionally use that for data retrieval

# format the json into something presentable

# RAG
* import langchain
* decide on model and grab api key (laod into secrets)
* create an embedding
* load embedding into in memory database (langchain provides this)
* generate results from the context of "is there anything going on this day"
