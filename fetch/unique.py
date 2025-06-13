from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
import numpy as np
from common.paths import Paths, DataPath
from common.logger import Logger
from common.data import Data, write_data

def get_json_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def get_discriminitive_weights_from_file(file_path):
    if not os.path.exists(file_path):
        Logger.warn("no weights found")
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def group_similar(json_array, weights, threshold):
    # Vectorize the chunks using TF-IDF
    str_array = [(s.get('title') or "") + "\n" + (s.get('description') or "") for s in json_array]
    vectorizer = TfidfVectorizer()
    vector_matrix = vectorizer.fit_transform(str_array)
    feature_names = vectorizer.get_feature_names_out()
    vectors = vector_matrix.toarray()

    # apply weights
    for word, weight in weights.items():
        if word in feature_names:
            idx = np.where(feature_names == word)[0][0]
            vectors[:, idx] *= weight

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(vectors)

    groups = []
    visited = set()

    for i in range(len(json_array)):
        if i in visited:
            continue
        group = [json_array[i]]
        visited.add(i)
        for j in range(i + 1, len(json_array)):
            if cosine_sim[i][j] >= threshold:
                group.append(json_array[j])
                visited.add(j)
        groups.append(group)

    return groups

def grab_first_in_group(grouped_json):
    unique_flatten = []
    dups_removed = 0
    for group in grouped_json:
        first_group = group[0]
        json_with_similiar_events= Data(
            image = first_group["image"],
            link = first_group["link"],
            title = first_group["title"],
            time = first_group["time"],
            location = first_group["location"],
            similar_events = group[1:],
        )
        unique_flatten.append(json_with_similiar_events)
        dups_removed += len(group) - 1 if len(group) > 0 else 0
    return unique_flatten, dups_removed

def unique(data_path: DataPath, threshold):
    data_json_file = os.path.join(data_path.data_dir(), "joined.json")
    data_json = get_json_data_from_file(data_json_file)

    weights_file = os.path.join(Paths.PROJECT_DIR, "weights", "weights.json")
    weights_json = get_discriminitive_weights_from_file(weights_file)

    grouped_json = group_similar(data_json, weights_json, threshold)
    unique_json, dups_removed = grab_first_in_group(grouped_json)

    json_output_file = os.path.join(data_path.data_dir(), 'unique.json')
    write_data(json_output_file, unique_json)
    # write_json_to_file(json_output_file, grouped_json)

    return dups_removed
    