import os
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from common.paths import Paths

def get_query_text_contents(root_folder):
    query_text_contents = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames: 
            full_file_path = os.path.join(dirpath, filename)

            with open(full_file_path, 'r') as file: 
                query_text_contents.append(file.read().strip())
    
    return query_text_contents

def get_embeddings_from(model_name, api_key, data):
    embedding_api = GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key = api_key
    )

    embeddings = embedding_api.embed_documents(data)
    return embeddings

def write_embeddings(output_file, embeddings):
    with open(output_file, "w") as json_file:
        json.dump(embeddings, json_file, indent=4)

def load_api_key(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"filename {filename} not found, nothing to delete")

def query_to_embeddings():
    data_dir = os.path.join(Paths.PROJECT_DIR, 'data')
    previous_events_dir = os.path.join(data_dir, 'previous_events')
    secrets_dir = os.path.join(Paths.PROJECT_DIR, "secrets")
    api_key_file = os.path.join(secrets_dir, "google-api-key")
    query_embeddings_file = os.path.join(data_dir, 'query.embeddings.json')

    remove_file(query_embeddings_file)

    if not os.path.exists(api_key_file):
        print(f"""!!!WARNING!!! \n{previous_events_dir} does not exist. add previous events to this location, one for each event. example:
    previous_events
        - fun_event.event
        - fun_event_2.event

    the filenames are not important.
              """)
        return 0
    
    query_texts = get_query_text_contents(previous_events_dir)
    api_key = load_api_key(api_key_file)
    google_ai_model = "models/text-embedding-004"

    embeddings = get_embeddings_from(google_ai_model, api_key, query_texts)

    write_embeddings(query_embeddings_file, embeddings)

    return len(embeddings)