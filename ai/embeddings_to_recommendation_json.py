import json
import os
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from common.paths import Paths

def read_embeddings(file_name):
    with open(file_name) as file:
        return json.load(file)
    
def normalize_embeddings(embeddings):
    normalized = normalize(embeddings, "l2")
    return normalized

def log(message):
    print(message)

def grab_similar_items(normalized_data_embeddings, normalized_query_embeddings, threshold, k=5):
    similarity_matrix = cosine_similarity(normalized_query_embeddings, normalized_data_embeddings)
    ranked_similarites_with_poor_results = np.argsort(similarity_matrix, axis=1, stable=True)

    indexes = []
    for query_row_with_poor_results_index in range(len(ranked_similarites_with_poor_results)):
        log(f"==== checking query index: {query_row_with_poor_results_index}")
        query_row_with_poor_results = ranked_similarites_with_poor_results[query_row_with_poor_results_index]

        for data_col_with_poor_results_index in range(len(query_row_with_poor_results)):
            reversed_data_col_with_poor_results_index = (len(query_row_with_poor_results) - 1) - data_col_with_poor_results_index
            log(f"checking data index: {reversed_data_col_with_poor_results_index}")

            similarity_column_index = ranked_similarites_with_poor_results[query_row_with_poor_results_index][reversed_data_col_with_poor_results_index]
            similarity_score = similarity_matrix[query_row_with_poor_results_index, similarity_column_index]

            if similarity_score >= threshold:
                log(f"good score: {similarity_score} at index: {similarity_column_index}")
                indexes.append({
                    "query_index": query_row_with_poor_results_index, 
                    "data_index":  int(similarity_column_index),
                })
            else:
                log(f"bad score: {similarity_score}")
                break

    return indexes

def load_json(json_data_file):
    with open(json_data_file, 'r') as file:
        return json.load(file)
    
def join_recommendation_indexes_with_original_data(recomendation_indexes, original_query_data_json, original_data_json):
    recemondation_json = []
    for recomendation_index in recomendation_indexes:
        original_data = original_data_json[recomendation_index['data_index']]
        original_query_data = original_query_data_json[recomendation_index['query_index']]
        recemondation = {
            "image": original_data['image'],
            "link": original_data['link'],
            "title": original_data['title'],
            "recemondation_source": original_query_data,
        }
        recemondation_json.append(recemondation)
    return recemondation_json

def get_query_text_contents(root_folder):
    query_text_contents = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames: 
            full_file_path = os.path.join(dirpath, filename)

            with open(full_file_path, 'r') as file: 
                query_text_contents.append(file.read().strip())
    
    return query_text_contents

def write_to_file(output_file, json_data):
    with open(output_file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"filename {filename} not found, nothing to delete")

def extract_recommendation(threshold):
    data_dir = os.path.join(Paths.PROJECT_DIR, 'data')

    data_embeddings_path = os.path.join(data_dir, 'data.embeddings.json')
    query_emeddings_path = os.path.join(data_dir, 'query.embeddings.json')
    recommendation_json_filename = os.path.join(data_dir, "recemondations.json")

    remove_file(recommendation_json_filename)

    if not os.path.exists(data_embeddings_path):
        print("log: no data embeddings found")
        return 0
    
    if not os.path.exists(query_emeddings_path):
        print("log: no query embeddings found")
        return 0

    data_embeddings = read_embeddings(data_embeddings_path)
    query_embeddings = read_embeddings(query_emeddings_path)

    normalized_data_embeddings = normalize_embeddings(data_embeddings)
    normalized_query_embeddings = normalize_embeddings(query_embeddings)

    recomendation_indexes = grab_similar_items(normalized_data_embeddings, normalized_query_embeddings, threshold)

    log(recomendation_indexes)

    json_data_file = os.path.join(data_dir, 'unique.json')
    previous_events_dir = os.path.join(Paths.PROJECT_DIR, 'previous_events')
    original_data = load_json(json_data_file) # data used to create the data embeddings
    original_query_data = get_query_text_contents(previous_events_dir)
    
    recommendation_json = join_recommendation_indexes_with_original_data(recomendation_indexes, original_query_data, original_data)

    write_to_file(recommendation_json_filename, recommendation_json)

    return len(recommendation_json)

