import os

def get_query_text_contents(root_folder):
    query_text_contents = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames: 
            full_file_path = os.path.join(dirpath, filename)

            with open(full_file_path, 'r') as file: 
                query_text_contents.append(file.read().strip())
    
    return query_text_contents

def get_embeddings_from(model_name, api_key, query_text_contents):
    return query_text_contents

def write_embeddings_to_file(output_file, embeddings):
    with open(output_file, 'w') as f:
        for embedding in embeddings:
            f.write(f"{embedding}\n")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    previous_events_dir = os.path.join(current_dir, 'previous_events')

    query_texts = get_query_text_contents(previous_events_dir)
    embeddings = get_embeddings_from('', '', query_texts)

    query_embeddings_file = os.path.join(data_dir, 'query.embeddings')
    write_embeddings_to_file(query_embeddings_file, query_texts)