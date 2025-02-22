import os
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings

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

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    json_data_file = os.path.join(data_dir, 'unique.json')
    json_data = load_json(json_data_file)

    secrets_dir = os.path.join(current_dir, "secrets")
    api_key_file = os.path.join(secrets_dir, "google-api-key")
    api_key = load_api_key(api_key_file)

    google_ai_model = "models/text-embedding-004"
    text_data = extract_text_from_json_data(json_data)
    embeddings = get_embeddings_from_json_data(google_ai_model, api_key, text_data)
    
    embeddings_file = os.path.join(data_dir, "data.embeddings.json")
    write_embeddings(embeddings_file, embeddings)

    print(f"embeddings count: {len(embeddings)}")
    print(f"text_data count: {len(text_data)}")