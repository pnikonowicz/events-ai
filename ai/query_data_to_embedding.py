import os
import json

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from common.paths import Paths
from common.logger import Logger
from common.paths import remove_dir
from common.paths import make_dir
from common.data import query_data_to_embedding_filename

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

def write_embeddings(embedding_dir, embeddings, query_texts):
    for query_idx in range(0, len(query_texts)):
        query_text = query_texts[query_idx]
        embedding = embeddings[query_idx]
        output_file = query_data_to_embedding_filename(query_text)
        
        with open(os.path.join(embedding_dir, output_file), "w") as json_file:
            json.dump(embedding, json_file, indent=4)

def load_api_key(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        Logger.log(f"filename {filename} not found, nothing to delete")

def query_to_embeddings(query_texts):
    secrets_dir = os.path.join(Paths.PROJECT_DIR, "secrets")
    api_key_file = os.path.join(secrets_dir, "google-api-key")
    api_key = load_api_key(api_key_file)
    google_ai_model = "models/text-embedding-004"

    embeddings = get_embeddings_from(google_ai_model, api_key, query_texts)

    return embeddings

def query_to_embeddings_from_file():
    previous_events_dir = os.path.join(Paths.PROJECT_DIR, 'previous_events')

    remove_dir(Paths.QUERY_EMBEDDINGS_DIR)

    if not os.path.exists(previous_events_dir):
        Logger.warn(f"""{previous_events_dir} does not exist. add previous events to this location, one for each event. example:
    previous_events
        - fun_event.event
        - fun_event_2.event

    the filenames are not important.
              """)
        return 0
    
    query_texts = get_query_text_contents(previous_events_dir)
    embeddings = query_to_embeddings(query_texts)

    make_dir(Paths.QUERY_EMBEDDINGS_DIR)
    write_embeddings(Paths.QUERY_EMBEDDINGS_DIR, embeddings, query_texts)

    return len(embeddings)