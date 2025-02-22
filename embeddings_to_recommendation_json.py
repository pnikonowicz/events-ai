import json
import os
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def read_embeddings(file_name):
    with open(file_name) as file:
        return json.load(file)
    
def normalize_embeddings(embeddings):
    normalized = normalize(embeddings, "l2")
    return normalized

def log(message):
    print(message)

def grab_similar_items(normalized_data_embeddings, normalized_query_embeddings, threshold=.9, k=5):
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

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')

    data_embeddings_path = os.path.join(data_dir, 'data.embeddings.json')
    query_emeddings_path = os.path.join(data_dir, 'query.embeddings.json')

    data_embeddings = read_embeddings(data_embeddings_path)
    query_embeddings = read_embeddings(query_emeddings_path)

    normalized_data_embeddings = normalize_embeddings(data_embeddings)
    normalized_query_embeddings = normalize_embeddings(query_embeddings)

    recomendation_indexes = grab_similar_items(normalized_data_embeddings, normalized_query_embeddings)

    print(recomendation_indexes)

