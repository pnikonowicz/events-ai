import os

def get_query_embeddings(root_folder):
    embeddings = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames: 
            embeddings.append(f"{filename}\n")
    
    return embeddings

def write_embeddings_to_file(output_file, embeddings):
    with open(output_file, 'w') as f:
        for embedding in embeddings:
            f.write(embedding)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    previous_events_dir = os.path.join(current_dir, 'previous_events')

    embeddings = get_query_embeddings(previous_events_dir)

    query_embeddings_file = os.path.join(data_dir, 'query.embeddings')
    write_embeddings_to_file(query_embeddings_file, embeddings)