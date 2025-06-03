import os
import json

from common.paths import Paths
from common.logger import Logger
from common.data import query_data_to_embedding_filename
from .embedding_service import EmbeddingService
from .embedding_cache import EmbeddingCache

def get_query_text_contents(root_folder):
    query_text_contents = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames: 
            full_file_path = os.path.join(dirpath, filename)

            with open(full_file_path, 'r') as file: 
                query_text_contents.append(file.read().strip())
    
    return query_text_contents

def write_embeddings(embedding_dir, embeddings, query_texts):
    for query_idx in range(0, len(query_texts)):
        query_text = query_texts[query_idx]
        embedding = embeddings[query_idx]
        output_file = query_data_to_embedding_filename(query_text)
        
        with open(os.path.join(embedding_dir, output_file), "w") as json_file:
            json.dump(embedding, json_file, indent=4)



def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        Logger.log(f"filename {filename} not found, nothing to delete")

def query_to_embeddings(embedding_cache: EmbeddingCache, embedding_service: EmbeddingService, query_texts):
    embeddings = [None] * len(query_texts) # fixed length array
    query_texts_that_need_embeddings = []
    query_texts_original_idx = []

    for idx, query in enumerate(query_texts):
        query = query_texts[idx]
        if embedding_cache.contains(query):
            embeddings[idx] = embedding_cache.get(query)
        else:
            query_texts_that_need_embeddings.append(query)
            query_texts_original_idx.append(idx)

    if len(query_texts_that_need_embeddings) > 0:
        new_embeddings = embedding_service.fetch(query_texts_that_need_embeddings) # from get_embeddings_from
        
        for query_text, new_embedding, original_query_idx in zip(query_texts_that_need_embeddings, new_embeddings, query_texts_original_idx):
            embedding_cache.set(
                query_text,
                new_embedding
            )
            embeddings[original_query_idx] = new_embedding
    
    return embeddings

def query_to_embeddings_from_file():
    query_texts = get_query_text_contents(Paths.PREVIOUS_EVENTS)
    embeddings = query_to_embeddings(EmbeddingCache(), EmbeddingService(), query_texts)

    return embeddings