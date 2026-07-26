import os
import json
from langchain_openai import OpenAIEmbeddings
from common.paths import Paths, DataPath
from common.logger import Logger
from common.models import OPENAI_EMBEDDING_MODEL

def load_json(json_data_file):
    with open(json_data_file, 'r') as file:
        return json.load(file)

def load_api_key(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def get_embeddings_from_text_data(model_name, api_key, text_data: list[str]) -> list:
    embedding_api = OpenAIEmbeddings(
        model=model_name,
        api_key=api_key.strip(),
    )

    embeddings = embedding_api.embed_documents(texts=text_data)
    return embeddings

def extract_text_from_json_data(json_data) -> list[str]:
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
        Logger.log(f"filename {filename} not found, nothing to delete")

def data_to_embeddings(data_path: DataPath):
    json_data_file = os.path.join(data_path.dir(), 'unique.json')
    secrets_dir = os.path.join(Paths.PROJECT_DIR, "secrets")
    api_key_file = os.path.join(secrets_dir, "api-key")
    embeddings_file = os.path.join(data_path.dir(), "data.embeddings.json")

    remove_file(embeddings_file)

    if not os.path.exists(api_key_file):
        Logger.warn(f"{api_key_file} does not exist. add an api key to this file to enable recommondations.")
        return 0

    if(json_data_file is None or not os.path.exists(json_data_file)):
        Logger.warn(f"{json_data_file} does not exist. no data to create embeddings from.")
        return 0
    
    json_data = load_json(json_data_file)
    api_key = load_api_key(api_key_file)

    openai_model = OPENAI_EMBEDDING_MODEL
    text_data = extract_text_from_json_data(json_data)
    embeddings = get_embeddings_from_text_data(openai_model, api_key, text_data)
    
    write_embeddings(embeddings_file, embeddings)

    return len(embeddings)
