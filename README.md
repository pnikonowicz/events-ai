Here’s a clearer and more concise version of your README while maintaining all the key details:  

---

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
1. Fetch data:  
   ```sh
   python get_data_eventbrite.py  # or python get_data_meetup.py
   ```  
2. Convert Eventbrite data (if applicable):  
   ```sh
   python eventbrite_to_json.py
   ```  
3. Merge all data sources:  
   ```sh
   python join_data.py
   ```  
4. Remove duplicates:  
   ```sh
   python unique.py
   ```  
5. (Optional) Generate recommendations (requires AI api key):  
   ```sh
   python json_data_to_embeddings.py
   ```  
6. View results in a browser:  
   ```sh
   python json_data_to_html.py  # outputs to data/all.html