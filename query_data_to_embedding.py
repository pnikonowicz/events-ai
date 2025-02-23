import os
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings

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

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    previous_events_dir = os.path.join(current_dir, 'previous_events')

    query_texts = get_query_text_contents(previous_events_dir)

    secrets_dir = os.path.join(current_dir, "secrets")
    api_key_file = os.path.join(secrets_dir, "google-api-key")
    api_key = load_api_key(api_key_file)
    google_ai_model = "models/text-embedding-004"

    embeddings = get_embeddings_from(google_ai_model, api_key, query_texts)

    query_embeddings_file = os.path.join(data_dir, 'query.embeddings.json')
    write_embeddings(query_embeddings_file, embeddings)