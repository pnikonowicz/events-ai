import os
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from common.paths import Paths

def load_json(json_data_file):
    with open(json_data_file, 'r') as file:
        return json.load(file)

def load_api_key(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def get_embeddings_from_json_data(model_name, api_key, json_data):
    embedding_api = GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key = api_key
    )

    embeddings = embedding_api.embed_documents(json_data)
    return embeddings

def extract_text_from_json_data(json_data):
    text_data = []
    for x in json_data:
        text_data.append(x['title'])
    return text_data

def write_embeddings(output_file, embeddings):
    with open(output_file, "w") as json_file:
        json.dump(embeddings, json_file, indent=4)

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"filename {filename} not found, nothing to delete")

def data_to_embeddings():
    json_data_file = os.path.join(Paths.DATA_DIR, 'unique.json')
    secrets_dir = os.path.join(Paths.PROJECT_DIR, "secrets")
    api_key_file = os.path.join(secrets_dir, "google-api-key")
    embeddings_file = os.path.join(Paths.DATA_DIR, "data.embeddings.json")

    remove_file(embeddings_file)

    if not os.path.exists(api_key_file):
        print(f"!!!WARNING!!! \n{api_key_file} does not exist. add an api key to this file to enable recommondations.")
        return 0

    json_data = load_json(json_data_file)
    api_key = load_api_key(api_key_file)

    google_ai_model = "models/text-embedding-004"
    text_data = extract_text_from_json_data(json_data)
    embeddings = get_embeddings_from_json_data(google_ai_model, api_key, text_data)
    
    write_embeddings(embeddings_file, embeddings)

    return len(embeddings)
