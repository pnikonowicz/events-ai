## Recommendation Engine for Unique Events  

![screenshot](https://github.com/pnikonowicz/events-ai/blob/main/docs/events-screenshot.jpg)

### Overview  
This recommendation engine helps discover unique events from multiple data sources, personalized to your preferences based on past events you've attended.  

### Goal  
**Question:** *Are there any events happening that I might be interested in?*  
- Enter details about past events you've attended.  
- Select data sources to pull from.  
- Get personalized recommendations and a de-duplicated event list.  

There is MCP integration:
![screenshot](https://github.com/pnikonowicz/events-ai/blob/main/docs/claude_mcp.png)

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
To process and view events with similar events grouped:  
1. execute `main.py`

#### If you want recommendations
1. add previous events to a `previous_events` folder relative to the projct dir
2. add google api key to `secrets/google-api-key`

#### Custom weights
You may want some items grouped up more aggressively. Or you may want some items grouped up less aggressively. For that, you can use custom weights. Create the following file: `weights/weights.json`
and add something similar to the following:
```
    {
        "comedy": 10, # add a value greater than 10 to increase the odds of it being grouped together
        "networking": .5 # add a value less than 1 to decrease the odds of it being grouped together
    }
```

### Running Project with React Frontend
1. ./scripts/run-react-frontend.sh

###  Running the tests
run `pytest` from the project root (`/workspaces/events-ai` in the dev container)

### Running the mcp server
You'll first need to build the dev container at `.devcontainer/Dockerfile`

#### WSL and Claude Desktop
replace the docker image to be the image from `.devcontainer/Dockerfile` add the following config:
```
{
	"mcpServers": {
		"events-ai": {
			"command": "wsl.exe",
			"args": [
				"docker", "run", "-v", "/root/workspace/events-ai:/app", "-i", "vsc-events-ai-5b6c547e5b8561359a378f2d1037c7d8acb17e98ae6c4925f95dc8a9635b2157", 
                "mcp", "run", "/app/mcp/server/server.py"
			]
		}
	}
}
```
