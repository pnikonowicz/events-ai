import json
import os
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from common.paths import DataPath
from common.logger import Logger
from common.data import Data, read_data, query_data_to_embedding_filename

def read_embeddings(file_name):
    with open(file_name) as file:
        return json.load(file)

def read_query_embeddings(query_embedding_dir, original_query_data):
    embeddings = []

    for query_data_idx in range(0, len(original_query_data)):
        query_text = original_query_data[query_data_idx]
        embedding_file_name = query_data_to_embedding_filename(query_text)

        with open(os.path.join(query_embedding_dir, embedding_file_name)) as file:
            embeddings.append(json.load(file))

    return embeddings
    
def normalize_embeddings(embeddings):
    normalized = normalize(embeddings, "l2")
    return normalized

def log(message):
    Logger.log(message)

def grab_similar_items(similarity_matrix, threshold):
    """
    Find the most similar items from a similarity matrix, one per row, above a threshold.
    
    Args:
        similarity_matrix (np.ndarray): 2D array of similarity scores
        threshold (float): Minimum similarity score for a recommendation
    
    Returns:
        tuple: (list of matches, count of recommendations above threshold)
    """

    sorted_indicies = np.argsort(similarity_matrix, axis=1, stable=True)[:, ::-1]

    # Track current position in sorted indices for each row
    current_indexes = [0] * len(sorted_indicies)
    
    visited = set()
    result = []
    recommendation_count = 0

    while len(visited) < similarity_matrix.shape[1]:
        best_similarity_value = 0
        best_similarity_idx = 0
        best_query_idx = 0
        already_visited = False

        for current_idx in range(len(current_indexes)):
            sorted_indicies_idx = current_indexes[current_idx]
            similarity_idx = sorted_indicies[current_idx][sorted_indicies_idx]
            similarity_value = similarity_matrix[current_idx][similarity_idx]

            if similarity_idx in visited:
                current_indexes[current_idx] += 1
                already_visited = True
                break
            elif similarity_value > best_similarity_value:
                best_similarity_value = similarity_value
                best_query_idx = int(similarity_idx)
                best_similarity_idx = current_idx
        
        if already_visited:
            continue
        
        current_indexes[best_similarity_idx] += 1
        visited.add(best_query_idx)

        if best_similarity_value >= threshold:
            recommendation_count += 1
            result.append(
                {"query_index":  best_similarity_idx, "data_index": best_query_idx}
            )
        else:
            result.append(
                {"query_index":  None, "data_index": best_query_idx}
            )

    return result, recommendation_count

def join_recommendation_indexes_with_original_data(recomendation_indexes, original_query_data_json, original_data_json):
    recemondation_json = []
    for recomendation_index in recomendation_indexes:
        original_data = original_data_json[recomendation_index['data_index']]

        original_query_data = None
        if recomendation_index['query_index'] != None:
            original_query_data = original_query_data_json[recomendation_index['query_index']]
        
        recemondation = Data(
            image = original_data.image,
            link = original_data.link,
            title = original_data.title,
            location = original_data.location,
            time = original_data.time,
            recommendation_source = original_query_data,
            similar_events = original_data.similar_events,
        )
        recemondation_json.append(recemondation)
    return recemondation_json

def get_previous_events(root_folder):
    query_text_contents = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames: 
            full_file_path = os.path.join(dirpath, filename)

            with open(full_file_path, 'r') as file: 
                query_text_contents.append(file.read().strip())
    
    return query_text_contents

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        Logger.log(f"filename {filename} not found, nothing to delete")

def extract_recommendation(data_path: DataPath, original_query_data, query_embeddings, threshold):
    json_data_file = os.path.join(data_path.dir(), 'unique.json')
    original_data = read_data(json_data_file) # data used to create the data embeddings
    data_embeddings_path = os.path.join(data_path.dir(), 'data.embeddings.json')

    if len(query_embeddings) == 0:
        Logger.warn("no query embeddings found")
        return original_data, 0
    
    if not os.path.exists(data_embeddings_path):
        Logger.warn("no data embeddings found")
        return original_data, 0
    
    data_embeddings = read_embeddings(data_embeddings_path)
    if len(data_embeddings) == 0:
        Logger.warn("no data embeddings found")
        return original_data, 0
    
    normalized_data_embeddings = normalize_embeddings(data_embeddings)
    normalized_query_embeddings = normalize_embeddings(query_embeddings)

    similarity_matrix = cosine_similarity(normalized_query_embeddings, normalized_data_embeddings)
    recomendation_indexes, recomendation_count = grab_similar_items(similarity_matrix, threshold)

    recommendation_json = join_recommendation_indexes_with_original_data(recomendation_indexes, original_query_data, original_data)

    return recommendation_json, recomendation_count
