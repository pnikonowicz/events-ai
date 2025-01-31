# eventbrite-unique

### problem
eventbrite has some cool events in their listings. 
but too often are the results littered with duplicates. 


### solution
this project aims to allow for the dedupping of results
and creating a unique result to make events easier to 
browse through. 

It does this through the use of TD-IDF vectoriztion. 

# running
right now everything is in modules / seperate files. so you'll need to:

1. `python get_data.py`
2. `python unique.py`
3. `python clean_html.py`

then open `without_inline_styles.html` in your browser and see the results
