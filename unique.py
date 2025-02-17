from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import json

def get_json_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def group_similar(json_array, threshold):
    # Vectorize the chunks using TF-IDF
    str_array = [(s.get('title') or "") + "\n" + (s.get('description') or "") for s in json_array]
    vectorizer = TfidfVectorizer().fit_transform(str_array)
    vectors = vectorizer.toarray()

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

def write_json_to_file(output_file, grouped_json):
    text = json.dumps(grouped_json, indent=4)
    with open(output_file, "w") as file:
        file.write(text)

def grab_first_in_group(grouped_json):
    unique_flatten = []
    for group in grouped_json:
        unique_flatten.append(group[0])
    return unique_flatten

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')

    data_json_file = os.path.join(data_dir, 'eventbrite', "data.json")
    data_json = get_json_data_from_file(data_json_file)

    grouped_json = group_similar(data_json, .60)
    unique_json = grab_first_in_group(grouped_json)
    
    json_output_file = os.path.join(data_dir, 'result.json')
    write_json_to_file(json_output_file, unique_json)
    # write_json_to_file(json_output_file, grouped_json)
    