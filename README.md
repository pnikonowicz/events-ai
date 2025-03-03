## Recommendation Engine for Unique Events  

### Overview  
This recommendation engine helps discover unique events from multiple data sources, personalized to your preferences based on past events you've attended.  

### Goal  
**Question:** *Are there any events happening that I might be interested in?*  
- Enter details about past events you've attended.  
- Select data sources to pull from.  
- Get personalized recommendations and a de-duplicated event list.  

### Problem  
- Event listings often contain duplicate entries across multiple sources.  
- Finding relevant events based on past interests is difficult.  

### Solution  
This project:  
- **Removes duplicates** across multiple data sources.  
- **Ranks personalized recommendations** based on your past events.  
- **Creates a unique event list** to make browsing easier.  

### How It Works  
- **De-duplication**: Uses TF-IDF vectorization and nearest neighbors search to group similar events, selecting the most relevant one.  
- **Recommendations**: Uses an AI model to compare past events with all unique events, recommending those above a similarity threshold.  

### Running the Project  
To process and view events:  
1. execute `main.py`

### Running Project with React Frontend
1. ./scripts/run-react-frontend.sh

###  Running the tests
run `pytest` from the project root (`/workspaces/events-ai` in the dev container)
