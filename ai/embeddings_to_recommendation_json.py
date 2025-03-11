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

def grab_similar_items(similarity_matrix, threshold):
    ranked_similarities = np.argsort(similarity_matrix, axis=1, stable=True)[:, ::-1]

    merge_lookups = []
    for _ in range(len(ranked_similarities)):
        merge_lookups.append(0)
    
    visited = set()
    result = []
    recommendation_count = 0

    while len(visited) < len(ranked_similarities[0]):
        max_similarity_value = 0
        max_merge_lookup_index = 0
        max_similarity_index = 0
        value_already_in_set = False

        for merge_lookup in range(len(merge_lookups)):
            ranked_column_index = merge_lookups[merge_lookup]
            similarity_index = ranked_similarities[merge_lookup][ranked_column_index]
            similarity_value = similarity_matrix[merge_lookup][similarity_index]

            if similarity_index in visited:
                merge_lookups[merge_lookup] += 1
                value_already_in_set = True
                break
            elif similarity_value > max_similarity_value:
                max_similarity_value = similarity_value
                max_similarity_index = int(similarity_index)
                max_merge_lookup_index = merge_lookup
        
        if value_already_in_set:
            continue
        
        merge_lookups[max_merge_lookup_index] += 1
        visited.add(max_similarity_index)

        if max_similarity_value >= threshold:
            recommendation_count += 1
            result.append(
                {"query_index":  max_merge_lookup_index, "data_index": max_similarity_index}
            )
        else:
            result.append(
                {"query_index":  None, "data_index": max_similarity_index}
            )

    return result, recommendation_count

def load_json(json_data_file):
    with open(json_data_file, 'r') as file:
        return json.load(file)
    
def join_recommendation_indexes_with_original_data(recomendation_indexes, original_query_data_json, original_data_json):
    recemondation_json = []
    for recomendation_index in recomendation_indexes:
        original_data = original_data_json[recomendation_index['data_index']]

        original_query_data = None
        if recomendation_index['query_index'] != None:
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

    if len(data_embeddings) == 0:
        print("WARN: no data embeddings found")
        return 0

    if len(query_embeddings) == 0:
        print("WARN: no query embeddings found")
        return 0

    normalized_data_embeddings = normalize_embeddings(data_embeddings)
    normalized_query_embeddings = normalize_embeddings(query_embeddings)

    similarity_matrix = cosine_similarity(normalized_query_embeddings, normalized_data_embeddings)
    recomendation_indexes, recomendation_count = grab_similar_items(similarity_matrix, threshold)

    json_data_file = os.path.join(data_dir, 'unique.json')
    previous_events_dir = os.path.join(Paths.PROJECT_DIR, 'previous_events')
    original_data = load_json(json_data_file) # data used to create the data embeddings
    original_query_data = get_query_text_contents(previous_events_dir)
    
    recommendation_json = join_recommendation_indexes_with_original_data(recomendation_indexes, original_query_data, original_data)

    write_to_file(recommendation_json_filename, recommendation_json)

    return recomendation_count

