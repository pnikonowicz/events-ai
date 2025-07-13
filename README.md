## Recommendation Engine for Unique Events  

![screenshot](https://github.com/pnikonowicz/events-ai/blob/main/docs/events-screenshot.jpg)

### Overview  
This recommendation engine helps discover unique events from multiple data sources, personalized to your preferences based on past events you've attended.  

Currently hosted at: [https://storage.cloud.google.com/events-ai-public/query_entry.html](https://storage.cloud.google.com/events-ai-public/query_entry.html)

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

# To run locally (from inside the dev container see: https://code.visualstudio.com/docs/devcontainers/containers)
1. Prerequistes: you need folders: 
```
	mkdir -p secrets
```
1. add google ai api key to `secrets/google-api-key`
1. first fetch events with: `python web/fetch/main.py`
2. run web server with: `python web/server/main.py`

#### Previous Events
These are events that you've been to in the past. 

#### Custom weights
You may want some items grouped up more aggressively. Or you may want some items grouped up less aggressively. For that, you can use custom weights. Create the following file: `weights/weights.json`
and add something similar to the following:
```
    {
        "comedy": 10, # add a value greater than 10 to increase the odds of it being grouped together
        "networking": .5 # add a value less than 1 to decrease the odds of it being grouped together
    }
```

###  Running the tests
run `pytest` from the project root (`/workspaces/events-ai` in the dev container)

### Running the mcp server (currently disabled due to other dev work. contributions welcome!)
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

### Deployment steps to prod

The containers will be uploaded to dockerhub at https://hub.docker.com/repository/docker/pnikonowicz/events-ai/ via a github action. 
Afterwards, gcp cloudrun destination images will need to be updated to point to the new container. 

# common issues
### GRPC Illegal header value

This is probably a copy and paste issue from windows to WSL. to verify:

see if a `0a` (new line) char exists
```
xxd secrets/google-api-key
```

and if you see the char:
```
 truncate -s -1 secrets/google-api-key
```
