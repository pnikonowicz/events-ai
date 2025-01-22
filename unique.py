from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import DBSCAN
import numpy as np
import os

def get_data_chunks(file_path, delimiter):
    chunks = []
    chunk = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if delimiter in line:
                chunks.append(chunk)
                chunk = ''
            else:
                chunk += line
    
    chunks.append(chunk)
    
    return chunks

def perform_unique(chunks, threshold):
    print(chunks)
    print(len(chunks))
    print(chunks[5])
    return ''

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = f"{current_dir}/data/data.txt"

    chunks = get_data_chunks(data_file, '------------------------------')
    unique = perform_unique(chunks, .90)