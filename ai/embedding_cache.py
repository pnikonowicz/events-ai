from common.data import query_data_to_embedding_filename
from common.paths import Paths
import os
import json

class EmbeddingCache:
    def contains(self, query):
        file_name = query_data_to_embedding_filename(query)
        file_path = os.path.join(Paths.QUERY_EMBEDDINGS_DIR, file_name)
        
        return os.path.exists(file_path)
    
    def get(self, query):
        file_name = query_data_to_embedding_filename(query)
        file_path = os.path.join(Paths.QUERY_EMBEDDINGS_DIR, file_name)
        
        with open(file_path, 'r') as f:
            embedding = json.load(f)
        return embedding

    def set(self, query, embedding):
        file_name = query_data_to_embedding_filename(query)
        file_path = os.path.join(Paths.QUERY_EMBEDDINGS_DIR, file_name)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w") as json_file:
            json.dump(embedding, json_file, indent=4)